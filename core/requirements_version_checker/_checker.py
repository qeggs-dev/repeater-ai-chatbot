from ._module_unit import ModuleUnit
from loguru import logger

def check_package_list(packages: list[ModuleUnit]):
    for package in packages:
        logger.info(
            "Use package: {package_name}: {package_version}",
            package_name=package.name,
            package_version=package.version,
        )
        if not package.check_version():
            logger.warning(
                "Package {package_name} expected version {expected_package_version}, but found {package_version}",
                package_name = package.name,
                package_version = package.version,
                expected_package_version = package.expected_version,
            )

        