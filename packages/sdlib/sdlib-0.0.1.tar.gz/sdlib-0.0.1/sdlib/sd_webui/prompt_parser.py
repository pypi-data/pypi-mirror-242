from .. import hijacker, function_params
from .api_impl import webui_api
from modules import prompt_parser, scripts, script_callbacks, shared
from typing import List, Optional
import torch


sdlib_hijacker_attribute = "__sdlib_hijacker"
prompt_parser_hijacker = hijacker.ModuleHijacker.install_or_get(
    module=prompt_parser,
    hijacker_attribute=sdlib_hijacker_attribute,
    register_uninstall=script_callbacks.on_script_unloaded,
)


negative_schedule: Optional[List[prompt_parser.ScheduledPromptConditioning]] = None


@prompt_parser_hijacker.hijack("get_learned_conditioning")
def get_learned_conditioning(model, prompts, steps, *args, original_function, **kwargs):
    hires_steps, use_old_scheduling, *_ = args if args else (None, True)
    encoder = PromptScheduleEncoder(model, prompts, steps, hires_steps, not prompts.is_negative_prompt, original_function, args, kwargs)
    conds = [encoder.process_prompt(prompt) for prompt in prompts]
    return conds


class PromptScheduleEncoder:
    def __init__(self, model, all_prompts, lowres_steps, hires_steps, is_positive, original_function, original_args, original_kwargs):
        self.model = model if model is not None else shared.sd_model
        self.all_prompts = all_prompts
        self.lowres_steps = lowres_steps
        self.hires_steps = hires_steps
        self.is_positive = is_positive
        self.original_function = original_function
        self.original_args = original_args
        self.original_kwargs = original_kwargs
        self.current_cond_key = None

    def is_hires(self):
        return self.hires_steps is not None

    def process_prompt(self, prompt: str):
        if self.model.is_sdxl:
            all_keys = set(webui_api.get_empty_cond().keys())
            seen_keys = set()
            results = []

            while unprocessed_keys := all_keys - seen_keys:
                self.current_cond_key = next(iter(unprocessed_keys))
                seen_keys.add(self.current_cond_key)
                result = self.call_encode_prompt_schedule(prompt)
                results.append((result, self.current_cond_key))

            self.current_cond_key = None
            return dict_of_lists_to_list_of_dicts({k: v for v, k in results})
        else:
            return self.call_encode_prompt_schedule(prompt)

    def call_encode_prompt_schedule(self, prompt: str):
        global negative_schedule
        empty_cond = webui_api.get_empty_cond(self.model)
        if self.current_cond_key is not None:
            empty_cond = empty_cond[self.current_cond_key]

        params = function_params.EncodePromptScheduleParams(
            prompt=prompt,
            steps=self.hires_steps if self.is_hires() else self.lowres_steps,
            pass_index=int(self.is_hires()),
            is_positive=self.is_positive,
            empty_cond=empty_cond,
            negative_schedule=negative_schedule if self.is_positive else None,
        )

        cond_schedule = encode_prompt(params, prompt_encoder=self)
        if not self.is_positive:
            negative_schedule = cond_schedule
        else:
            negative_schedule = None

        return to_webui_cond_schedule(cond_schedule)


def normalize_conds_wrapper(params: function_params.EncodePromptScheduleParams, prompt_encoder):
    res = yield params
    return res


@webui_api.host_plugin.function(private_params={"prompt_encoder"}, meta_wrapper=normalize_conds_wrapper)
def encode_prompt(params: function_params.EncodePromptScheduleParams, prompt_encoder):
    self = prompt_encoder

    lowres_steps = self.lowres_steps if params.pass_index == 1 else params.steps
    hires_steps = params.steps if params.pass_index == 1 else None
    additional_args = () if not self.original_args else (hires_steps, self.original_args[1])
    prompts = [params.prompt]
    if getattr(prompt_parser, "SdConditioning", None) is not None:
        prompts = prompt_parser.SdConditioning(prompts, copy_from=self.all_prompts)

    cond_schedule = self.original_function(self.model, prompts, lowres_steps, *additional_args, **self.original_kwargs)[0]

    if self.model.is_sdxl:
        return to_sdlib_cond_schedule(cond_schedule, key=self.current_cond_key)

    return to_sdlib_cond_schedule(cond_schedule)


def to_webui_cond_schedule(cond_schedule: torch.Tensor) -> List[prompt_parser.ScheduledPromptConditioning]:
    schedule = []
    for cond_i, cond in enumerate(cond_schedule):
        if schedule and (schedule[-1].cond == cond).all():
            schedule[-1] = prompt_parser.ScheduledPromptConditioning(cond=schedule[-1].cond, end_at_step=cond_i)
        else:
            schedule.append(prompt_parser.ScheduledPromptConditioning(cond=cond, end_at_step=cond_i))

    return schedule


def to_sdlib_cond_schedule(cond_schedules: List[prompt_parser.ScheduledPromptConditioning], key: Optional[str] = None) -> torch.Tensor:
    max_size = max(len(cond_schedule.cond if key is None else cond_schedule.cond[key]) for cond_schedule in cond_schedules)

    res = []
    for scheduled_cond in cond_schedules:
        cond = scheduled_cond.cond
        if key is not None:
            cond = cond[key]

        missing_size = max_size - cond.shape[0]
        if missing_size > 0:
            cond = torch.cat([cond, torch.zeros(missing_size, *cond.shape[1:])])

        res.append(cond)

        while len(res) < scheduled_cond.end_at_step:
            res.append(res[-1])

    return torch.stack(res, dim=0)


def dict_of_lists_to_list_of_dicts(lists: dict):
    keys = lists.keys()
    any_key = next(iter(keys))
    length = len(next(iter(lists.values())))
    result = []
    for i in range(length):
        current_dict = prompt_parser.ScheduledPromptConditioning(
            cond={key: lists[key][i].cond for key in keys},
            end_at_step=lists[any_key][i].end_at_step,
        )
        result.append(current_dict)

    return result
