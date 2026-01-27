import aiofiles

from os import PathLike
from pathlib import Path
from typing import Generator

from ..Global_Config_Manager import Licenses_Config

class LicenseLoader:
    """
    A class for loading licenses from a file.
    """
    def __init__(self, licenses_config: Licenses_Config) -> None:
        """
        Initialize the class.

        :param path: Path to the file.
        """
        self._base_path = Path(licenses_config.license_dir)
        self._licenses: dict[str, dict[str, Path]] = {}
        self._encoding = licenses_config.license_encoding
        self._self_license_paths: dict[str, str] = licenses_config.self_license_files

    def _scan_dir(self) -> Generator[tuple[Path, str], None, None]:
        """
        Scan a directory for files.

        :return: Generator of paths to files.
        """
        for path in Path(self._base_path).iterdir():
            name = path.name
            licenses_dir = (path / "LICENSES")
            if licenses_dir.exists() and licenses_dir.is_dir():
                yield licenses_dir, name
    
    def scan_licenses(self):
        """
        Scan a directory for licenses.
        """
        for license_path, name in self._scan_dir():
            licenses: dict[str, Path] = {}
            for path in license_path.iterdir():
                licenses[path.name] = path
            self._licenses[name] = licenses
    
    def __contains__(self, requirement_name: str) -> bool:
        """
        Check if a requirement is in the licenses.

        :param requirement_name: Name of the requirement.
        :return: True if the requirement is in the licenses, False otherwise.
        """
        return requirement_name in self._licenses
    
    async def get_requirement_license(self, requirement_name: str) -> dict[str, str]:
        """
        Get a license for a requirement.

        :param requirement_name: Name of the requirement.
        :return: Licenses.
        """
        licenses: dict[str, str] = {}
        for license_name, path in self._licenses[requirement_name].items():
            async with aiofiles.open(path, "r", encoding = self._encoding) as f:
                licenses[license_name] = await f.read()
        return licenses
    
    async def get_self_license(self) -> dict[str, str]:
        licenses: dict[str, str] = {}
        for license_type, path in self._self_license_paths.items():
            async with aiofiles.open(path, "r", encoding = self._encoding) as f:
                licenses[license_type] = await f.read()
        return licenses
    
    def get_requirements_list(self) -> list[str]:
        """
        Get all requirements.

        :return: Requirements.
        """
        return list(self._licenses.keys())