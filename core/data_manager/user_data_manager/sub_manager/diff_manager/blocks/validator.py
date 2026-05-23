from .head_jump import HeadJumpModel
from .end_jump import EndJumpModel
from .diff_model import DiffModel
from .snapshot import SnapShotModel
from typing import Union
from pydantic import BaseModel, Field

DATA_BLOCKS = Union[DiffModel, SnapShotModel]
INSTRUCTION_BLOCKS = Union[HeadJumpModel, EndJumpModel]
ALL_BLOCKS = Union[INSTRUCTION_BLOCKS, DATA_BLOCKS]


class Validator(BaseModel):
    block: ALL_BLOCKS = Field(...)
    