# 🚀 Deploy no Render - Email Classifier AI

## ✨ Por que Render?

- ✅ **Funcionalidade completa** (spaCy, NLTK, uploads)
- ✅ **Plano gratuito** disponível (com limitações)
- ✅ **Deploy automático** via GitHub
- ✅ **Zero configuração** - detecta Python automaticamente
- ✅ **SSL grátis** incluído
- ✅ **Logs em tempo real**

## 🛠️ Passo a Passo para Deploy

### 1. Preparar o Repositório

Sua aplicação já está pronta! Apenas certifique-se de que tem:
- ✅ `backend/requirements.txt` com todas as dependências
- ✅ `backend/app.py` como arquivo principal
- ✅ Estrutura frontend em `frontend/`

### 2. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em **"Get Started"**
3. Faça login com GitHub (recomendado)

### 3. Deploy da Aplicação

#### Opção A: Deploy Direto (Recomendado)

1. No dashboard do Render, clique **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:

```yaml
Name: email-classifier-ai
Runtime: Python 3
Build Command: cd backend && pip install -r requirements.txt && python -m spacy download pt_core_news_sm
Start Command: cd backend && python app.py
```

#### Opção B: Via Git (Se não usar GitHub)

```bash
# Adicionar Render como remote
git remote add render https://git.render.com/srv-XXXXX.git

# Push para deploy
git push render main
```

### 4. Configurar Variáveis de Ambiente

No painel do Render, vá em **Environment** e adicione:

```
OPENAI_API_KEY=sk-sua-chave-openai-aqui
SECRET_KEY=sua-chave-secreta-super-segura
FLASK_CONFIG=production
PORT=10000
```

### 5. Configurações Avançadas

```yaml
# Configurações recomendadas
Runtime: Python 3.11
Health Check Path: /api/health
Build Command: cd backend && pip install -r requirements.txt && python -m spacy download pt_core_news_sm
Start Command: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

## 📦 Otimizações para Render

Sua aplicação já está otimizada, mas algumas dicas:

### 1. Gunicorn para Produção

O Render roda melhor com Gunicorn (já incluído no requirements.txt):

```bash
# O comando ideal para produção
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### 2. Health Check

Seu endpoint `/api/health` já está configurado - perfeito para o Render!

### 3. Uploads

Para uploads em produção, considere usar:
- **Cloudinary** (imagens/PDFs)
- **AWS S3** (arquivos grandes)
- **Render Disks** (persistent storage)

## 💰 Planos do Render

| Plano | Preço | Recursos |
|-------|-------|----------|
| **Free** | $0 | 512MB RAM, suspende após 15min inativo |
| **Starter** | $7/mês | 512MB RAM, sempre ativo |
| **Standard** | $25/mês | 2GB RAM, auto-scaling |

## 🚨 Limitações do Plano Gratuito

- ⏰ **Suspende** após 15 minutos de inatividade
- 🐌 **Pode ser lento** no primeiro acesso (cold start)
- 💾 **512MB RAM** (suficiente para a aplicação)
- 📊 **750 horas/mês** de uso

## 🔧 Troubleshooting

### Erro de Build

Se o build falhar, tente:

```bash
# Build command alternativo
pip install --no-cache-dir -r requirements.txt && python -m spacy download pt_core_news_sm
```

### Timeout no spaCy

```bash
# Build com timeout maior
pip install -r requirements.txt --timeout 1000 && python -m spacy download pt_core_news_sm
```

### Erro de Memória

Para o plano gratuito, otimize:

```python
# No config.py, ajustar para produção
class ProductionConfig(Config):
    DEBUG = False
    # Reduzir workers se necessário
    WORKERS = 2
```

## 🌐 Configurar Domínio Personalizado

1. No dashboard do Render
2. Vá em **Settings → Custom Domains**
3. Adicione seu domínio
4. Configure DNS (CNAME para seu-app.onrender.com)

## 📊 Monitoramento

O Render oferece:
- 📈 **Métricas** de CPU/RAM em tempo real
- 📋 **Logs** detalhados
- 🔔 **Alertas** por email
- 🚀 **Auto-deploy** em push para main

## 🚀 Exemplo de Deploy Completo

```yaml
# render.yaml (opcional, para configuração como código)
services:
  - type: web
    name: email-classifier-ai
    runtime: python3
    buildCommand: cd backend && pip install -r requirements.txt && python -m spacy download pt_core_news_sm
    startCommand: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
    healthCheckPath: /api/health
    envVars:
      - key: FLASK_CONFIG
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
```

## 🎯 Próximos Passos Após Deploy

1. ✅ Testar todas as funcionalidades
2. ✅ Configurar monitoramento
3. ✅ Adicionar domínio personalizado
4. ✅ Configurar backup de dados
5. ✅ Otimizar performance se necessário

## 📞 Suporte

- 📚 [Documentação Render](https://render.com/docs)
- 💬 [Community Forum](https://community.render.com)
- 📧 [Support Email](mailto:support@render.com)

---

**🎉 Sua aplicação Email Classifier AI estará rodando com funcionalidade completa no Render!**

**URL do deploy:** `https://email-classifier-ai.onrender.com`
