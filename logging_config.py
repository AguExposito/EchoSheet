import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                'logs/echosheet.log',
                maxBytes=1024*1024,  # 1MB
                backupCount=5,
                encoding='utf-8'
            )
        ]
    )
    
    # Set specific loggers
    loggers = [
        'app',
        'utils.autofill',
        'utils.chat_engine', 
        'utils.recommender',
        'utils.spell_manager',
        'utils.equipment_packs'
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
    
    # Suppress some noisy loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return logging.getLogger('app')

def get_logger(name):
    """Get a logger with the specified name"""
    return logging.getLogger(name) 