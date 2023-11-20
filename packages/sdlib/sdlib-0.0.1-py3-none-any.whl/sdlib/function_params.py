import dataclasses
from torch import Tensor
from typing import Optional


@dataclasses.dataclass
class EncodePromptScheduleParams:
    prompt: str
    steps: int
    pass_index: int
    is_positive: bool
    empty_cond: Tensor
    negative_schedule: Optional[Tensor]


@dataclasses.dataclass
class CustomImg2ImgTabParams:
    tab_index: int
