#################################################
# Include libaries
# Import orders
#     - Internal STL 
#         - sys calls first
#         - alpahbetic
#     - External
#################################################
import os
import sys

import dataclasses
import datetime
import inspect
import logging
import multiprocessing as mp
import typing as T

from loguru import logger


#################################################
# Utils
#################################################
def singleton(func):
    """
    A singleton decorator that ensures the decorated function is called only once
    per Python process. Multiprocessing.Lock is used for thread-safety within a process.
    """
    # This lock is local to each process.
    # When a new process is spawned, it gets its own lock and instance variable.
    lock = mp.Lock() 

    def wrapper(*args, **kwargs):
        if wrapper.instance is None:
            with lock:
                if wrapper.instance is None:
                    wrapper.instance = func(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper



#################################################
# Configurations
#################################################
SUPPRESSED_NOISY_LOGS: T.Tuple[str] = (
    "uvicorn", "uvicorn.error", "uvicorn.server",
    "sse_starlette.sse", "h11", "httpx", "watchdog.observers"
)

@dataclasses.dataclass
class _BaseDefaultConfig:
    service_name: str = ""

    level: str = dataclasses.field(
        default="INFO"
    )
    format: str = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.format = "".join((
            self.service_name,
            "|{time:YYYY-MM-DD HH:mm:ss.SSS}|{level}|{file}|line:{line}|{function}|{message}"
        ))

    def to_dict(self) -> dict:
        # service name is not kwarg of the handler settings, needs to be pooped
        dicted_values = self.__dict__.copy()
        dicted_values.pop("service_name")
        return dicted_values

@dataclasses.dataclass
class StdoutConfig(_BaseDefaultConfig):
    sink: T.Any = sys.stdout

@dataclasses.dataclass
class FileOutConfig(_BaseDefaultConfig):
    sink: str = dataclasses.field(
        default="log/app.log"
    )
    rotation: T.Union[int, str, datetime.timedelta, datetime.time] = dataclasses.field(
        default="0:00"
    )
    retention: T.Union[int, str, datetime.timedelta] = dataclasses.field(
        default="30 days"
    )
    # `enqueue = True` is crucial for multiprocessing safety when writing to a shared file
    enqueue: bool = dataclasses.field(
        default=True 
    )

# Cherry picked from https://github.com/Delgan/loguru/issues/977
class InterceptHandler(logging.Handler):
    def __init__(self, level: T.Union[int, str] = 0):
        super().__init__(level)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame:
            filename = frame.f_code.co_filename
            is_logging_module = filename == logging.__file__
            is_frozen_importlib = "importlib" in filename and "_bootstrap" in filename
            if depth > 0 and not (is_logging_module or is_frozen_importlib):
                break
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth, exception=record.exc_info
        ).log(level, record.getMessage())


#################################################
# Main Interface.
# Call this function before use STL logging.
#################################################
@singleton
def set_logger(
    service_name: str = "",
    log_level: str = "INFO",
    enable_uvicorn_access_logs: bool = False,
    stdout_sink: bool = True,
    file_sink: bool = True,
    log_file_path: str = "log/app.log",
    log_file_rotation: T.Union[int, str, datetime.timedelta, datetime.time] = "0:00",
    log_file_retention: T.Union[int, str, datetime.timedelta] = "30 days"
) -> int:
    """
    Configures Loguru to be the central logging system, intercepting
    all standard Python logging messages. This function is designed to be
    called only once per process.

    Args:
        log_level (str): The minimum logging level to display/save (e.g., "INFO", "DEBUG").
        enable_uvicorn_access_logs (bool): Whether to show Uvicorn's HTTP access logs.
                                            Set to False to reduce verbosity.
        stdout_sink (bool): Enable logging to standard output (console).
        file_sink (bool): Enable logging to a file.
        log_file_path (str): Path to the log file.
        log_file_rotation (Union[int, str, datetime.timedelta, datetime.time]): Log file rotation policy.
                                                                                e.g., "500 MB", "1 day", "0:00".
        log_file_retention (Union[int, str, datetime.timedelta]): Log file retention policy.
                                                                  e.g., "10 days", "1 month".

    Returns:
        int: 1 for initialized. (for singleton value for check)
    """

    # Remove default handlers in STL logging and those in loguru for fresh start
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger.remove()


    # Configure the root Python logging to route all messages to Loguru
    # Intercept handler captures logs from ANY library which uses the STL `logging`
    logging.basicConfig(
        handlers=[InterceptHandler(level=0)],
        level=0,
        force=True
    )

    # Suppress propagation and directly handle specific noisy/duplicate loggers
    for logger_name in SUPPRESSED_NOISY_LOGS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.propagate = False
        logging_logger.handlers = [InterceptHandler(level=log_level)]
        logging_logger.setLevel(log_level)

    # Handle Uvicorn's access logs separately, as they are often disabled
    if not enable_uvicorn_access_logs:
        logging.getLogger("uvicorn.access").disabled = True
    else:
        # If enabled, ensure it's also handled by our InterceptHandler and doesn't propagate
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.propagate = False
        uvicorn_access_logger.handlers = [InterceptHandler(level=log_level)]
        uvicorn_access_logger.setLevel(log_level)


    # Configure Loguru's actual sinks (where logs are written/displayed)
    # These are the *final* output destinations and apply the primary log_level filtering.
    handler_options = []

    if stdout_sink:
        stdout_config = StdoutConfig(service_name=service_name, level=log_level).to_dict()
        handler_options.append(stdout_config)
    
    if file_sink:
        # Ensure the parent directory for the log file exists before Loguru tries to write
        log_dir = os.path.dirname(log_file_path)
        if log_dir: # Only create if path implies a directory (e.g., "log/app.log" not just "app.log")
            os.makedirs(log_dir, exist_ok=True)

        # Pass enqueue=True for multiprocessing safety
        file_config = FileOutConfig(
            service_name=service_name,
            level=log_level,
            sink=log_file_path,
            rotation=log_file_rotation,
            retention=log_file_retention,
            enqueue=True # Explicitly set to True for multiprocessing
        ).to_dict()
        handler_options.append(file_config)

    # If no sinks are enabled, add a default null sink to prevent "No handler found" warnings
    if not handler_options:
        handler_options.append({"sink": lambda msg: None, "level": log_level})

    logger.configure(handlers=handler_options)

    # Inform the user that logging is set up
    logger.info("Logging system initialized and configured.")
    if not enable_uvicorn_access_logs:
        logger.info("Uvicorn access logs are disabled.")
    else:
        logger.info("Uvicorn access logs are enabled.")
    
    return 1 # Return a value to indicate initialization success
