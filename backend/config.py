"""
Configurações da aplicação.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base da aplicação."""
    
    # Configurações do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações de upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    # Configurações da API OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')  # Modelo padrão
    
    # Configurações de NLP
    SPACY_MODEL = 'pt_core_news_sm'
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação."""
        pass

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False

class TestingConfig(Config):
    """Configurações para ambiente de testes."""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
