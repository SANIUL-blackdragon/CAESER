import logging

def setup_logging(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger instance.
    Args:
        name (str): Logger name (defaults to module name).
        level (int): Logging level (defaults to INFO).
    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(name)