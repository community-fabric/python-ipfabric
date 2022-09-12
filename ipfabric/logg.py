from logging import config
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from typing_extensions import Literal


class LoggingConfig(BaseModel):
    """Using pydantic as it is a standard across this library"""

    version: Literal[1] = 1
    """useful versioning for logger"""

    disable_existing_loggers: bool = False
    """disable non-root loggers"""

    filters: Optional[Dict[str, Dict[str, Any]]] = None
    """A dict in which each key is a filter id and each value is a dict 
    describing how to configure the corresponding Filter instance."""

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
    """
    A dict in which each key is a handler id and each value is a dict describing 
    how to configure the corresponding Handler instance.
    
    Example File Handlers:
    {
        "fileHandler": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "json_formatter",
                "filename": "python-ipfabric.log",
        },
        "rotatingFileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json_formatter",
            "maxBytes": 5000000,
            "backupCount": 3,
            "filename": "python-ipfabric.log",
        },
    }
    """

    loggers: Union[Dict[str, Dict[str, Any]], None] = None
    """
    A dict in which each key is a logger name and each value is a dict describing 
    how to configure the corresponding Logger instance.
    
    Example:
    {
        "python-ipfabric": {
            "level": "INFO",
            "handlers": ["rotatingFileHandler"],
        },
    }
    """

    root: Dict[str, Union[Dict[str, Any], List[Any], str]] = {"handlers": ["console"], "level": "INFO"}
    """This will be the configuration for the root logger. Processing of the configuration will be as for any logger,
    except that the propagate setting will not be applicable. 
    Logs will always print to stdout unless this Root logger is changed."""

    def configure(self) -> None:
        """Configured logger with the given configuration."""
        config.dictConfig(self.dict(exclude_none=True))
