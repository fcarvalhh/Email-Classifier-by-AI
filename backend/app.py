"""
Aplicação Flask para classificação e resposta automática de emails.
Backend da aplicação web full-stack.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

# Importar utilitários personalizados
from utils.text_processor import TextProcessor
from utils.email_classifier import EmailClassifier
from config import config

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Factory function para criar a aplicação Flask."""
    app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
    
    # Configurar aplicação
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Habilitar CORS
    CORS(app)
    
    # Criar pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicializar processadores
    app.text_processor = TextProcessor()
    app.email_classifier = EmailClassifier(
        openai_api_key=app.config.get('OPENAI_API_KEY'),
        openai_model=app.config.get('OPENAI_MODEL')
    )
    
    return app

# Criar instância da aplicação
app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')

@app.route('/api/classify', methods=['POST'])
def classify_email():
    """Endpoint para classificação de emails."""
    try:
        text_content = ""
        
        # Verificar se há arquivo no upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                try:
                    # Extrair texto baseado na extensão
                    if filename.lower().endswith('.pdf'):
                        text_content = app.text_processor.extract_text_from_pdf(file_path)
                    elif filename.lower().endswith('.txt'):
                        text_content = app.text_processor.extract_text_from_txt(file_path)
                    
                    # Remover arquivo após processamento
                    os.remove(file_path)
                    
                except Exception as e:
                    # Remover arquivo em caso de erro
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    raise e
        
        # Verificar se há texto manual
        elif 'text' in request.form:
            text_content = request.form['text']
        
        # Verificar se há conteúdo JSON
        elif request.is_json:
            data = request.get_json()
            text_content = data.get('text', '')
        
        if not text_content.strip():
            return jsonify({
                'error': 'Nenhum conteúdo de texto foi fornecido.',
                'success': False
            }), 400
        
        # Pré-processar texto
        processed_text = app.text_processor.preprocess_text(text_content)
        
        # Classificar com IA
        classification_result = app.email_classifier.classify_email(processed_text)
        
        # Extrair palavras-chave
        keywords = app.text_processor.extract_keywords(processed_text, max_keywords=5)
        
        # Preparar resposta
        response_data = {
            'success': True,
            'original_text': text_content[:500] + '...' if len(text_content) > 500 else text_content,
            'processed_text': processed_text[:300] + '...' if len(processed_text) > 300 else processed_text,
            'classification': classification_result['category'],
            'confidence': classification_result['confidence'],
            'suggested_response': classification_result['suggested_response'],
            'keywords': keywords,
            'metadata': classification_result.get('metadata', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Email classificado como: {classification_result['category']} (confiança: {classification_result['confidence']})")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return jsonify({
            'error': f'Erro no processamento: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de health check."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'text_processor': app.text_processor is not None,
            'email_classifier': app.email_classifier is not None,
            'spacy_model': app.text_processor.nlp is not None if app.text_processor else False
        },
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Configuração para produção (Render) e desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_CONFIG', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
