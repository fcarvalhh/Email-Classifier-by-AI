#!/usr/bin/env python3
"""
Script para executar a aplicação Email Classifier AI.
Facilita a inicialização e configuração da aplicação.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Exibe o banner da aplicação."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        📧 EMAIL CLASSIFIER AI 📧                        ║
    ║                                                          ║
    ║        Classificação Inteligente de Emails               ║
    ║        Powered by Flask + Bootstrap 5 + AI              ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} detectado")

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    backend_path = Path(__file__).parent / "backend"
    is_windows = platform.system().lower() == "windows"
    
    print("📦 Verificando dependências...")
    
    # Verificar dependências essenciais
    essential_missing = []
    optional_missing = []
    
    try:
        import flask
        import flask_cors
        print("✅ Flask e Flask-CORS instalados")
    except ImportError:
        essential_missing.append("Flask/Flask-CORS")
    
    try:
        import nltk
        print("✅ NLTK instalado")
    except ImportError:
        if is_windows:
            optional_missing.append("NLTK (opcional no Windows)")
        else:
            essential_missing.append("NLTK")
            
    try:
        import spacy
        print("✅ spaCy instalado")
        
        # Verificar modelo português
        try:
            nlp = spacy.load("pt_core_news_sm")
            print("✅ Modelo pt_core_news_sm carregado")
        except OSError:
            print("⚠️  Modelo pt_core_news_sm não encontrado")
            print("   Execute: python -m spacy download pt_core_news_sm")
    except ImportError:
        if is_windows:
            optional_missing.append("spaCy (opcional no Windows)")
            print("⚠️  spaCy não instalado (funcionalidade avançada indisponível)")
        else:
            essential_missing.append("spaCy")
    
    # Verificar outras dependências essenciais
    try:
        import PyPDF2
        print("✅ PyPDF2 instalado")
    except ImportError:
        essential_missing.append("PyPDF2")
    
    # Resultado da verificação
    if essential_missing:
        print(f"❌ Dependências essenciais faltando: {', '.join(essential_missing)}")
        return False
    
    if optional_missing:
        print(f"⚠️  Dependências opcionais faltando: {', '.join(optional_missing)}")
        print("💡 A aplicação funcionará com funcionalidade básica")
    
    return True

def install_dependencies():
    """Instala as dependências necessárias."""
    backend_path = Path(__file__).parent / "backend"
    
    # Detectar sistema operacional e escolher arquivo de requirements apropriado
    is_windows = platform.system().lower() == "windows"
    
    if is_windows:
        requirements_file = backend_path / "requirements_windows.txt"
        print("🪟 Sistema Windows detectado - usando requirements otimizados")
    else:
        requirements_file = backend_path / "requirements.txt"
        print("🐧 Sistema Unix/Linux detectado")
    
    if not requirements_file.exists():
        print(f"❌ Arquivo {requirements_file.name} não encontrado!")
        return False
    
    print("📦 Instalando dependências...")
    
    try:
        # Estratégia específica para Windows
        if is_windows:
            print("🔧 Usando estratégia otimizada para Windows...")
            # Atualizar pip primeiro
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True)
            
            # Instalar com flags específicas para Windows
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--only-binary=all",  # Força uso de wheels pré-compilados
                "--upgrade",
                "-r", str(requirements_file)
            ], check=True, cwd=backend_path)
        else:
            # Instalação padrão para Unix/Linux
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=backend_path)
        
        print("✅ Dependências instaladas com sucesso!")
        
        # Tentar instalar modelo do spaCy
        try:
            print("📥 Baixando modelo pt_core_news_sm...")
            subprocess.run([
                sys.executable, "-m", "spacy", "download", "pt_core_news_sm"
            ], check=True)
            print("✅ Modelo spaCy instalado!")
        except subprocess.CalledProcessError:
            print("⚠️  Erro ao instalar modelo spaCy (não crítico)")
            if is_windows:
                print("💡 No Windows, o modelo spaCy é opcional para funcionalidade básica")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        
        # Fallback para Windows
        if is_windows:
            print("🔄 Tentando instalação alternativa para Windows...")
            return install_dependencies_fallback()
        
        return False

def install_dependencies_fallback():
    """Instalação alternativa para Windows com dependências mínimas."""
    print("🔄 Iniciando instalação alternativa...")
    
    # Lista de dependências essenciais que devem funcionar em qualquer Windows
    essential_packages = [
        "Flask==2.3.3",
        "Flask-CORS==4.0.0", 
        "PyPDF2==3.0.1",
        "pdfplumber==0.9.0",
        "requests==2.31.0",
        "Werkzeug==2.3.7",
        "python-dotenv==1.0.0"
    ]
    
    try:
        for package in essential_packages:
            print(f"📦 Instalando {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True)
        
        # Tentar instalar NLTK separadamente
        try:
            print("📦 Instalando NLTK...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "nltk==3.8.1"
            ], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  NLTK pode ser instalado manualmente depois")
        
        print("✅ Instalação mínima concluída!")
        print("⚠️  spaCy foi omitido devido a problemas de compilação")
        print("💡 A aplicação funcionará com funcionalidade básica")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha na instalação alternativa: {e}")
        print("💡 Tente instalar manualmente: pip install Flask Flask-CORS PyPDF2")
        return False

def setup_nltk_data():
    """Configura dados necessários do NLTK."""
    try:
        import nltk
        print("📥 Configurando dados NLTK...")
        
        # Download silencioso dos dados necessários
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
            
        print("✅ Dados NLTK configurados!")
        return True
        
    except Exception as e:
        print(f"⚠️  Erro ao configurar NLTK: {e}")
        return False

def create_uploads_folder():
    """Cria a pasta de uploads se não existir."""
    backend_path = Path(__file__).parent / "backend"
    uploads_path = backend_path / "uploads"
    
    uploads_path.mkdir(exist_ok=True)
    print("✅ Pasta de uploads criada")

def run_application(mode="development"):
    """Executa a aplicação."""
    backend_path = Path(__file__).parent / "backend"
    
    print(f"🚀 Iniciando aplicação em modo {mode}...")
    print("🌐 Aplicação será executada em: http://localhost:5000")
    print("💡 Pressione Ctrl+C para parar")
    print("-" * 60)
    
    try:
        if mode == "production":
            # Executar com Gunicorn se disponível
            try:
                subprocess.run([
                    "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"
                ], check=True, cwd=backend_path)
            except FileNotFoundError:
                print("⚠️  Gunicorn não encontrado, usando modo desenvolvimento")
                subprocess.run([sys.executable, "app.py"], cwd=backend_path)
        else:
            # Modo desenvolvimento
            subprocess.run([sys.executable, "app.py"], cwd=backend_path)
            
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")

def show_help():
    """Exibe informações de ajuda."""
    is_windows = platform.system().lower() == "windows"
    
    help_text = f"""
📖 Como usar o Email Classifier AI:

Comandos:
    python run.py                 - Executa em modo desenvolvimento
    python run.py --install      - Instala dependências
    python run.py --production   - Executa em modo produção
    python run.py --help         - Mostra esta ajuda

Primeiro uso:
    1. python run.py --install   (instala dependências)
    2. python run.py             (executa aplicação)

{"🪟 WINDOWS: O script detecta automaticamente o Windows e usa instalação otimizada" if is_windows else "🐧 LINUX/MAC: Instalação padrão com todas as funcionalidades"}

Recursos:
    ✨ Interface web moderna com Bootstrap 5
    🌙 Dark mode toggle
    📁 Upload de arquivos .txt e .pdf  
    🤖 Classificação automática com IA
    💬 Sugestões de resposta automática
    📱 Design responsivo
    
Problemas no Windows:
    • Se o spaCy falhar, a instalação continuará sem ele
    • Funcionalidade básica mantida mesmo sem spaCy
    • Para spaCy completo: instale Visual C++ Build Tools
    
Acesse: http://localhost:5000 após iniciar
    """
    print(help_text)

def main():
    """Função principal."""
    print_banner()
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
            return
        elif arg in ['--install', '-i', 'install']:
            print("🔧 Iniciando instalação...")
            check_python_version()
            if install_dependencies():
                setup_nltk_data()
                create_uploads_folder()
                print("\n✅ Instalação concluída!")
                print("💡 Execute 'python run.py' para iniciar a aplicação")
            else:
                print("❌ Falha na instalação")
            return
        elif arg in ['--production', '-p', 'prod']:
            mode = "production"
        else:
            print(f"❌ Argumento desconhecido: {arg}")
            print("💡 Use 'python run.py --help' para ver opções")
            return
    else:
        mode = "development"
    
    # Verificações iniciais
    check_python_version()
    
    if not check_dependencies():
        print("\n❌ Dependências não instaladas!")
        print("💡 Execute: python run.py --install")
        return
    
    # Configurações adicionais
    setup_nltk_data()
    create_uploads_folder()
    
    # Executar aplicação
    run_application(mode)

if __name__ == "__main__":
    main()
