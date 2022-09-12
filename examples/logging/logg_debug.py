from logging import config
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from typing_extensions import Literal


class LoggingConfig(BaseModel):
    """Using pydantic as it is a standard across this library"""

    version: Literal[1] = 1

    disable_existing_loggers: bool = False

    filters: Optional[Dict[str, Dict[str, Any]]] = None

    formatters: Dict[str, Dict[str, Any]] = {
        "standard": {"format": "%(levelname)s - %(asctime)s - %(name)s - %(module)s - %(message)s"}
    }

    handlers: Dict[str, Dict[str, Any]] = {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        }
    }

    loggers: Union[Dict[str, Dict[str, Any]], None] = {
        "python-ipfabric": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    }

    root: Dict[str, Union[Dict[str, Any], List[Any], str]] = {"handlers": ["console"], "level": "INFO"}

    def configure(self) -> None:
        """Configured logger with the given configuration."""
        config.dictConfig(self.dict(exclude_none=True))
