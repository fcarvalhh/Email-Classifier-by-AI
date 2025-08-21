"""
Arquivo de exemplo de configuração.
Copie este arquivo para config_local.py e ajuste as configurações conforme necessário.
"""

import os

class Config:
    """Configurações base da aplicação."""
    
    # Configurações do Flask
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # Configurações de upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    # Configurações da API OpenAI
    # Substitua pela sua chave API real da OpenAI
    OPENAI_API_KEY = 'your-openai-api-key'
    OPENAI_MODEL = 'gpt-3.5-turbo'  # ou gpt-4 se preferir
    
    # Configurações de NLP
    SPACY_MODEL = 'pt_core_news_sm'
    
    # Configurações de logging
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False
    # Em produção, use variáveis de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')

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
