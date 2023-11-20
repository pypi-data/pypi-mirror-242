from .. import sdlib, function_params
from modules import devices, prompt_parser, scripts, script_callbacks, shared
import torch
import inspect


class WebuiApi(sdlib.Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        script_callbacks.on_model_loaded(self.__init_empty_cond)
        self.__empty_cond = None

    def __del__(self):
        script_callbacks.remove_callbacks_for_function(self.__init_empty_cond)

    def register_plugin(self, name: str):
        plugin = super().register_plugin(name)
        patch_caller_module(name, inspect.stack()[1][0].f_globals)
        return plugin

    def get_empty_cond(self, model=None) -> torch.Tensor:
        self.__init_empty_cond(model)
        return self.__empty_cond

    def __init_empty_cond(self, model):
        if model is None and self.__empty_cond is not None:
            return

        if model is None:
            model = shared.sd_model

        model.to(devices.get_optimal_device())
        cond = model.get_learned_conditioning([''])
        if isinstance(cond, dict):
            cond = {k: v[0] for k, v in cond.items()}
        else:
            cond = cond[0]

        self.__empty_cond = cond


def patch_caller_module(plugin_name, caller_globals):
    capital_name, pascal_name = get_script_cases(plugin_name)
    custom_script_class = type(f"{pascal_name}Script", (WebuiScript,), {
        "title": lambda self: capital_name,
    })
    caller_globals[f"__sdapi_{WebuiScript.__name__}"] = custom_script_class


def get_script_cases(snake_name):
    split_name = [word.capitalize() for word in snake_name.split('_')]
    return ' '.join(split_name), ''.join(split_name)


class WebuiScript(scripts.Script):
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def process(self, *args, **kwargs):
        pass


webui_api = WebuiApi({**vars(function_params)}, __name__)
