"""
Utilitários para processamento de texto e NLP.
"""

import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader
import pdfplumber

# Importação opcional do spaCy
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    spacy = None
    SPACY_AVAILABLE = False

logger = logging.getLogger(__name__)

class TextProcessor:
    """Classe para processamento de texto."""
    
    def __init__(self):
        """Inicializa o processador de texto."""
        self.nlp = self._load_spacy_model()
        self.stop_words = self._load_stopwords()
        self._ensure_nltk_data()
    
    def _load_spacy_model(self):
        """Carrega o modelo do spaCy."""
        if not SPACY_AVAILABLE:
            logger.info("spaCy não disponível. Funcionalidade de lemmatização desabilitada.")
            return None
            
        try:
            return spacy.load("pt_core_news_sm")
        except OSError:
            logger.warning("Modelo pt_core_news_sm não encontrado. Funcionalidade de lemmatização desabilitada.")
            return None
    
    def _load_stopwords(self):
        """Carrega stopwords em português."""
        try:
            return set(stopwords.words('portuguese'))
        except LookupError:
            logger.warning("Stopwords em português não encontradas.")
            return set()
    
    def _ensure_nltk_data(self):
        """Garante que os dados necessários do NLTK estão disponíveis."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    
    def extract_text_from_pdf(self, file_path):
        """Extrai texto de arquivo PDF."""
        try:
            text = ""
            
            # Tentar com pdfplumber primeiro (melhor para layout complexo)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Se pdfplumber não funcionou, tentar PyPDF2
            if not text.strip():
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
            raise
    
    def extract_text_from_txt(self, file_path):
        """Extrai texto de arquivo TXT."""
        try:
            # Tentar UTF-8 primeiro
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Fallback para latin-1
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logger.error(f"Erro ao ler arquivo TXT: {str(e)}")
                raise
    
    def clean_text(self, text):
        """Limpa o texto removendo caracteres especiais e normalizando."""
        # Remover caracteres especiais mantendo acentos
        text = re.sub(r'[^\w\sáàâãéèêíìîóòôõúùûç]', ' ', text, flags=re.IGNORECASE)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text)
        
        # Remover quebras de linha e tabs
        text = re.sub(r'[\r\n\t]+', ' ', text)
        
        return text.strip().lower()
    
    def remove_stopwords(self, text):
        """Remove stopwords do texto."""
        try:
            words = word_tokenize(text, language='portuguese')
            filtered_words = [
                word for word in words 
                if word not in self.stop_words and len(word) > 2
            ]
            return ' '.join(filtered_words)
        except Exception as e:
            logger.error(f"Erro na remoção de stopwords: {str(e)}")
            return text
    
    def lemmatize_text(self, text):
        """Realiza lemmatização do texto usando spaCy."""
        if not self.nlp:
            return text
        
        try:
            doc = self.nlp(text)
            lemmatized_words = [
                token.lemma_ for token in doc 
                if not token.is_stop and not token.is_punct and not token.is_space
            ]
            return ' '.join(lemmatized_words)
        except Exception as e:
            logger.error(f"Erro na lemmatização: {str(e)}")
            return text
    
    def preprocess_text(self, text):
        """Pipeline completo de pré-processamento de texto."""
        try:
            # 1. Limpeza básica
            cleaned_text = self.clean_text(text)
            
            # 2. Remoção de stopwords
            no_stopwords = self.remove_stopwords(cleaned_text)
            
            # 3. Lemmatização
            lemmatized = self.lemmatize_text(no_stopwords)
            
            return lemmatized
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento: {str(e)}")
            return text.lower()
    
    def extract_keywords(self, text, max_keywords=10):
        """Extrai palavras-chave mais relevantes do texto."""
        try:
            if not self.nlp:
                # Fallback simples sem spaCy
                words = text.split()
                word_freq = {}
                for word in words:
                    if len(word) > 3:
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
                return [word for word, freq in sorted_words[:max_keywords]]
            
            doc = self.nlp(text)
            
            # Extrair entidades nomeadas e tokens importantes
            keywords = []
            
            # Adicionar entidades nomeadas
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT']:
                    keywords.append(ent.text.lower())
            
            # Adicionar substantivos e adjetivos importantes
            for token in doc:
                if (token.pos_ in ['NOUN', 'ADJ'] and 
                    not token.is_stop and 
                    not token.is_punct and 
                    len(token.text) > 3):
                    keywords.append(token.lemma_.lower())
            
            # Remover duplicatas e retornar as mais frequentes
            keyword_freq = {}
            for keyword in keywords:
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
            
            sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
            return [keyword for keyword, freq in sorted_keywords[:max_keywords]]
            
        except Exception as e:
            logger.error(f"Erro na extração de palavras-chave: {str(e)}")
            return []
