import sys
from loguru import logger
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    logs_dir / "etl_{time}.log",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)

def get_logger():
    """Get configured logger instance."""
    return logger 