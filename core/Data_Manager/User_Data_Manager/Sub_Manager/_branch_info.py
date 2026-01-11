from pydantic import BaseModel
from TextProcessors import format_carry_duration
from ....Global_Config_Manager import ConfigManager

SIZE_UNITS = [
    ("Bytes", "B", 1024),
    ("Kibibyte", "KiB", 1024),
    ("Mebibyte", "MiB", 1024),
    ("Gibibyte", "GiB", 1024),
    ("Tebibyte", "TiB", 1024),
    ("Pebibyte", "PiB", 1024),
    ("Exbibyte", "EiB", 1024),
]

FINAL_SIZE_UNIT = ("Yobibyte", "YiB")


class BranchInfo(BaseModel):
    """Branch Info"""
    branch_id: str = ""
    size: int = 0
    modified_time: int = 0
    
    @property
    def readable_size(self) -> str:
        return format_carry_duration(
            self.size,
            SIZE_UNITS,
            final_level = FINAL_SIZE_UNIT,
            use_abbreviation = ConfigManager.get_configs().user_data.file_size_use_abbreviation
        )