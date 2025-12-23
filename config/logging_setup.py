"""
Centralized logging configuration for the application.
Provides structured logging with JSON formatting for production.
"""

import logging
import logging.config
import json
from pathlib import Path
from config.config import config


def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(config.logging.log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # Basic configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': config.logging.level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': config.logging.level,
                'formatter': 'detailed',
                'filename': config.logging.log_file,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
            },
        },
        'root': {
            'level': config.logging.level,
            'handlers': ['console', 'file']
        },
        'loggers': {
            'uvicorn': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
            },
            'uvicorn.access': {
                'level': 'INFO',
                'handlers': ['file'],
                'propagate': False,
            },
        }
    }
    
    logging.config.dictConfig(logging_config)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.info(
        f"Logging initialized - Level: {config.logging.level}, "
        f"File: {config.logging.log_file}, Environment: {config.app.environment}"
    )


class JSONFormatter(logging.Formatter):
    """JSON logging formatter for structured logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
