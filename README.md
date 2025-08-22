Email Classifier AI

Uma aplicação web full-stack moderna para classificação automática de emails usando inteligência artificial. O sistema analisa emails e os classifica como Produtivos ou Improdutivos, fornecendo sugestões de respostas automáticas.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple.svg)


Características Principais

Frontend
- ✨ Interface moderna e responsiva com **Bootstrap 5**
- 🌙 **Dark Mode** com toggle
- 📁 Upload de arquivos **.txt** e **.pdf**
- ✍️ Inserção manual de texto
- 🎯 Validação em tempo real
- ⚡ **Spinner de loading** e animações suaves
- 🏷️ **Badges coloridas** para categorias
- 💬 **Tooltips** explicativos
- 🎨 **Ícones** do Bootstrap Icons
- 📱 **Mobile-first** e totalmente responsivo
- 🔄 Comunicação **AJAX** sem reloads

Backend
- 🐍 **Python 3.8+** com **Flask**
- 📄 Processamento de **PDF** e **TXT**
- 🧠 **NLP** avançado com **spaCy** e **NLTK**
- 🤖 Integração com **OpenAI GPT** para classificação inteligente
- 🔧 Arquitetura modular e extensível
- 📊 **Logs** detalhados
- ⚡ **API RESTful** com validação
- 🛡️ Tratamento robusto de erros

Arquitetura

```
📦 Email Classifier AI
├── 🔧 backend/              # Servidor Flask
│   ├── app.py              # Aplicação principal
│   ├── config.py           # Configurações
│   ├── requirements.txt    # Dependências Python
│   └── utils/              # Utilitários
│       ├── text_processor.py     # Processamento NLP
│       ├── email_classifier.py   # Classificação IA
│       └── __init__.py
├── 🎨 frontend/            # Interface web
│   ├── index.html          # Página principal
│   └── static/
│       ├── css/
│       │   └── style.css   # Estilos customizados
│       └── js/
│           └── app.js      # Lógica frontend
└── 📚 README.md
```

Instalação

### Pré-requisitos
- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd email-classifier-ai
```

### 2. Instale as dependências do backend
```bash
cd backend
pip install -r requirements.txt
```

**Nota**: O arquivo requirements.txt agora inclui a biblioteca `openai` necessária para a integração.

**Se encontrar erro de compatibilidade com OpenAI:**
```bash
pip install --upgrade openai
```

**Se encontrar erro de compilação do spaCy no Windows:**
```bash
pip install --upgrade spacy
python -m spacy download pt_core_news_sm
```

### 3. Instale o modelo do spaCy (opcional, mas recomendado)
```bash
python -m spacy download pt_core_news_sm
```
Configure a API OpenAI
Crie um arquivo `.env` na pasta `backend/`:
```env
# Configurações da aplicação Email Classifier AI
SECRET_KEY=your-secret-key-here-change-in-production

# Configurações da OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Configurações de ambiente
FLASK_CONFIG=development
LOG_LEVEL=INFO
```

**Como obter sua chave API da OpenAI:**
1. Acesse [platform.openai.com](https://platform.openai.com)
2. Faça login ou crie uma conta
3. Vá para "API Keys" no menu
4. Clique em "Create new secret key"
5. Copie a chave e cole no arquivo `.env`

**Modelos disponíveis:**
- `gpt-3.5-turbo`: Mais rápido e econômico (recomendado para início)
- `gpt-4`: Mais preciso, mas mais caro
- `gpt-4-turbo`: Balanceado entre velocidade e precisão

Execução

### Modo Desenvolvimento
```bash
cd backend
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

### Modo Produção (com Gunicorn)
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Como Usar

### 1. **Inserção de Texto Manual**
   - Acesse a aba "Texto Manual"
   - Cole o conteúdo do email
   - Clique em "Analisar Email"

### 2. **Upload de Arquivo**
   - Acesse a aba "Upload de Arquivo"
   - Selecione um arquivo `.txt` ou `.pdf`
   - Ou arraste e solte na área designada
   - Clique em "Analisar Arquivo"

### 3. **Visualizar Resultados**
   - ✅ **Categoria**: Produtivo/Improdutivo
   - 📊 **Confiança**: Percentual de certeza
   - 💬 **Resposta Sugerida**: Texto para resposta automática
   - 📋 **Copiar Resposta**: Botão para copiar para área de transferência

Categorias de Email

| Categoria | Descrição | Exemplos |
|-----------|-----------|----------|
| 🟢 **Produtivo** | Emails relacionados a trabalho, projetos, prazos | Reuniões, propostas, contratos, relatórios |
| 🔴 **Improdutivo** | Emails de spam, promoções, newsletters não solicitados | Propaganda, ofertas, phishing, malware |

API Endpoints

### `POST /api/classify`
Classifica um email e gera resposta automática.

**Parâmetros:**
- `text` (string): Texto do email
- `file` (arquivo): Arquivo .txt ou .pdf

**Resposta:**
```json
{
  "success": true,
  "classification": "Produtivo",
  "confidence": 0.85,
  "suggested_response": "Resposta sugerida...",
  "keywords": ["reunião", "projeto"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### `GET /api/health`
Verifica o status da API.

**Resposta:**
```json
{
  "status": "healthy",
  "services": {
    "text_processor": true,
    "email_classifier": true,
    "spacy_model": true
  },
  "version": "1.0.0"
}
```

Processamento NLP

O sistema utiliza várias técnicas de processamento de linguagem natural:

1. **Limpeza de Texto**: Remove caracteres especiais e normaliza
2. **Tokenização**: Divide o texto em tokens
3. **Remoção de Stopwords**: Remove palavras irrelevantes
4. **Lemmatização**: Reduz palavras à forma canônica
5. **Extração de Palavras-chave**: Identifica termos importantes

Recursos Visuais

- 🎨 **Design Moderno**: Interface limpa e profissional
- 🌙 **Dark Mode**: Alternância entre temas claro e escuro
- ⚡ **Animações**: Transições suaves e feedbacks visuais
- 📱 **Responsivo**: Adapta-se a qualquer tamanho de tela
- 🏷️ **Badges Coloridas**: Indicadores visuais claros
- 💡 **Tooltips**: Explicações contextuais
- 🎯 **Ícones**: Interface rica em elementos visuais

Integração com OpenAI

O sistema utiliza a poderosa API da OpenAI para classificação inteligente de emails. Para ativar:

1. **Obtenha sua chave API** da OpenAI em [platform.openai.com](https://platform.openai.com)
2. **Configure as variáveis de ambiente** no arquivo `.env`
3. **A integração será automática** - o sistema detectará a chave e usará GPT

**Modelos suportados:**
- `gpt-3.5-turbo` (padrão, mais rápido e econômico)
- `gpt-4` (mais preciso, mas mais caro)
- `gpt-4-turbo` (balanceado)

**Fallback**: Quando a API da OpenAI não está configurada, o sistema usa classificação local baseada em palavras-chave.


 Segurança

- ✅ Validação de arquivos (tipo e tamanho)
- ✅ Sanitização de inputs
- ✅ Tratamento de erros robusto
- ✅ CORS configurado
- ✅ Logs de segurança


