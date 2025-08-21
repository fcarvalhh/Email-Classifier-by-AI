"""
Classificador de emails usando IA (OpenAI GPT).
"""

import logging
import json
import random
from typing import Dict, Any

# Importação da biblioteca OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class EmailClassifier:
    """Classificador de emails usando IA."""
    
    def __init__(self, openai_api_key=None, openai_model='gpt-3.5-turbo'):
        """Inicializa o classificador."""
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        
        # Inicializar cliente OpenAI se disponível
        self.openai_client = None
        if OPENAI_AVAILABLE and openai_api_key:
            try:
                # Inicialização simples e compatível
                self.openai_client = OpenAI(api_key=openai_api_key)
                logger.info("Cliente OpenAI inicializado com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao inicializar cliente OpenAI: {str(e)}")
                logger.info("Usando classificação local como fallback.")
                self.openai_client = None
        elif not OPENAI_AVAILABLE:
            logger.warning("Biblioteca OpenAI não está instalada. Usando classificação local.")
        elif not openai_api_key:
            logger.warning("Chave API da OpenAI não fornecida. Usando classificação local.")
        
        # Palavras-chave para classificação de fallback
        self.productive_keywords = [
            'reunião', 'projeto', 'prazo', 'entrega', 'cliente', 'proposta', 
            'contrato', 'orçamento', 'cronograma', 'deadline', 'apresentação',
            'relatório', 'análise', 'desenvolvimento', 'implementação', 'teste',
            'aprovação', 'revisão', 'feedback', 'documentação', 'especificação',
            'requisito', 'funcionalidade', 'bug', 'correção', 'melhoria'
        ]
        
        self.unproductive_keywords = [
            'spam', 'promoção', 'desconto', 'oferta', 'grátis', 'clique aqui',
            'ganhe', 'prêmio', 'sorteio', 'loteria', 'compre agora', 'liquidação',
            'newsletter', 'marketing', 'propaganda', 'anúncio', 'publicidade',
            'vírus', 'malware', 'phishing', 'golpe', 'fraude'
        ]
        
        # Templates de resposta
        self.productive_responses = [
            "Obrigado pelo seu email. Analisarei as informações e retornarei em breve com uma resposta detalhada.",
            "Recebi sua mensagem e estou revisando os detalhes. Entrarei em contato nas próximas horas.",
            "Agradeço o contato. Vou verificar as informações mencionadas e responder o mais breve possível.",
            "Email recebido com sucesso. Estou analisando sua solicitação e responderei em breve.",
            "Obrigado por entrar em contato. Vou revisar os pontos mencionados e dar um retorno adequado.",
            "Mensagem recebida. Analisarei o conteúdo e responderei com as informações solicitadas."
        ]
        
        self.unproductive_responses = [
            "Este email foi identificado como não prioritário e será arquivado automaticamente.",
            "Mensagem classificada como promocional. Movida para a pasta de spam.",
            "Email identificado como propaganda. Não requer resposta.",
            "Conteúdo classificado como não relevante para análise manual."
        ]
    
    def classify_with_openai(self, text: str) -> Dict[str, Any]:
        """
        Classifica email usando a API da OpenAI GPT.
        """
        try:
            if not self.openai_client:
                logger.warning("Cliente OpenAI não configurado. Usando classificação local.")
                return self._classify_local(text)
            
            # Prompt otimizado para classificação de emails
            system_prompt = """Você é um especialista em classificação de emails. Analise o conteúdo do email e classifique-o como:

PRODUTIVO: Emails relacionados a trabalho, projetos, negócios, reuniões, contratos, propostas, prazos, clientes, desenvolvimento, feedback profissional, relatórios, análises técnicas, documentação oficial.

IMPRODUTIVO: Emails de spam, promoções comerciais, newsletters não solicitados, propaganda, ofertas comerciais, sorteios, phishing, malware, conteúdo irrelevante para o trabalho.

Responda APENAS com um JSON no formato:
{
  "category": "Produtivo" ou "Improdutivo",
  "confidence": número entre 0.0 e 1.0,
  "reasoning": "breve explicação da classificação"
}"""

            user_prompt = f"Classifique este email:\n\n{text[:2000]}" 
            
            # Fazer requisição para a API OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.1  # Baixa temperatura para maior consistência
            )
            
            # Extrair resposta
            content = response.choices[0].message.content.strip()
            
            # Tentar fazer parse do JSON
            try:
                result = json.loads(content)
                
                # Validar campos obrigatórios
                category = result.get("category", "Incerto")
                confidence = float(result.get("confidence", 0.5))
                reasoning = result.get("reasoning", "")
                
                # Normalizar categoria
                if category.lower() in ['produtivo', 'productive']:
                    category = "Produtivo"
                elif category.lower() in ['improdutivo', 'unproductive']:
                    category = "Improdutivo"
                else:
                    category = "Incerto"
                
                # Garantir que a confiança está no range correto
                confidence = max(0.0, min(1.0, confidence))
                
                return {
                    "category": category,
                    "confidence": confidence,
                    "method": "openai_gpt",
                    "reasoning": reasoning
                }
                
            except json.JSONDecodeError:
                logger.error(f"Erro ao fazer parse da resposta OpenAI: {content}")
                # Fallback: tentar extrair categoria da resposta de texto
                content_lower = content.lower()
                if "produtivo" in content_lower:
                    return {
                        "category": "Produtivo",
                        "confidence": 0.7,
                        "method": "openai_text_fallback"
                    }
                elif "improdutivo" in content_lower:
                    return {
                        "category": "Improdutivo",
                        "confidence": 0.7,
                        "method": "openai_text_fallback"
                    }
                else:
                    return self._classify_local(text)
                
        except Exception as e:
            logger.error(f"Erro na classificação com OpenAI: {str(e)}")
            return self._classify_local(text)
    
    def _classify_local(self, text: str) -> Dict[str, Any]:
        """Classificação local usando palavras-chave (fallback)."""
        try:
            text_lower = text.lower()
            
            # Contar ocorrências de palavras-chave
            productive_score = sum(
                1 for keyword in self.productive_keywords 
                if keyword in text_lower
            )
            
            unproductive_score = sum(
                1 for keyword in self.unproductive_keywords 
                if keyword in text_lower
            )
            
            # Análise adicional baseada em padrões
            # Emails com muitos links ou palavras em maiúscula são suspeitos
            links_count = text.count('http') + text.count('www.')
            caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
            
            if links_count > 3:
                unproductive_score += 2
            
            if caps_ratio > 0.3:
                unproductive_score += 1
            
            # Emails muito curtos ou muito longos podem ser suspeitos
            word_count = len(text.split())
            if word_count < 10 or word_count > 1000:
                unproductive_score += 1
            
            # Determinar categoria
            if productive_score > unproductive_score:
                category = "Produtivo"
                confidence = min(0.85, 0.6 + (productive_score * 0.05))
            elif unproductive_score > productive_score:
                category = "Improdutivo"
                confidence = min(0.85, 0.6 + (unproductive_score * 0.05))
            else:
                # Critério de desempate baseado no comprimento e estrutura
                if 50 <= word_count <= 500:
                    category = "Produtivo"
                    confidence = 0.6
                else:
                    category = "Improdutivo"
                    confidence = 0.6
            
            return {
                "category": category,
                "confidence": confidence,
                "method": "local_keywords",
                "productive_score": productive_score,
                "unproductive_score": unproductive_score
            }
            
        except Exception as e:
            logger.error(f"Erro na classificação local: {str(e)}")
            return {
                "category": "Incerto",
                "confidence": 0.5,
                "method": "error_fallback"
            }
    
    def generate_response(self, category: str, original_text: str = "") -> str:
        """Gera resposta automática baseada na categoria."""
        try:
            if category.lower() == "produtivo":
                # Selecionar resposta baseada no hash do texto para consistência
                response_index = abs(hash(original_text)) % len(self.productive_responses)
                return self.productive_responses[response_index]
            elif category.lower() == "improdutivo":
                response_index = abs(hash(original_text)) % len(self.unproductive_responses)
                return self.unproductive_responses[response_index]
            else:
                return "Email recebido. Será analisado manualmente devido à classificação incerta."
                
        except Exception as e:
            logger.error(f"Erro na geração de resposta: {str(e)}")
            return "Email recebido e será processado adequadamente."
    
    def classify_email(self, text: str) -> Dict[str, Any]:
        """Pipeline completo de classificação de email."""
        try:
            # Classificar usando IA
            classification = self.classify_with_openai(text)
            
            # Gerar resposta
            response = self.generate_response(
                classification["category"], 
                text
            )
            
            return {
                "category": classification["category"],
                "confidence": round(classification["confidence"], 2),
                "suggested_response": response,
                "method": classification.get("method", "unknown"),
                "metadata": {
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "productive_score": classification.get("productive_score", 0),
                    "unproductive_score": classification.get("unproductive_score", 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro no pipeline de classificação: {str(e)}")
            return {
                "category": "Erro",
                "confidence": 0.0,
                "suggested_response": "Não foi possível classificar este email devido a um erro interno.",
                "method": "error",
                "metadata": {"error": str(e)}
            }
