from typing import Optional
from loguru import logger
import sys
import os


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "7 days",
    format_string: Optional[str] = None,
) -> None:
    """
    Configure loguru logging for the slab project.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging to file
        rotation: Log rotation policy (e.g., "10 MB", "1 day")
        retention: Log retention policy (e.g., "7 days", "1 week")
        format_string: Custom format string for log messages
    """
    # Remove default logger
    logger.remove()

    # Default format for console output
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    # Add console handler
    logger.add(
        sys.stderr,
        format=format_string,
        level=level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Add file handler if specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation=rotation,
            retention=retention,
            backtrace=True,
            diagnose=True,
            enqueue=True,  # Thread-safe logging
        )

    logger.info(f"Logging configured with level: {level}")
    if log_file:
        logger.info(f"Log file: {log_file}")


def get_logger(name: str):
    """
    Get a logger instance with the given name.

    Args:
        name: Name for the logger (typically __name__)

    Returns:
        Configured logger instance
    """
    return logger.bind(name=name)
