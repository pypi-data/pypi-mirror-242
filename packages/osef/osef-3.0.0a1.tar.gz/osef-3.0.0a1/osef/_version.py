"""OSEF library version."""
# Standard imports
import importlib.metadata
from osef._logger import osef_logger

try:
    __version__ = importlib.metadata.version("osef")
except importlib.metadata.PackageNotFoundError as exp:
    osef_logger.warning(
        f"{str(exp)} \nThis is normal if you are using OSEF as a git submodule/python subpackage."
    )
    __version__ = ""
