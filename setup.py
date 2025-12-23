"""
Setup script for initializing the Aloysius Chatbot project.
Handles environment validation, dependencies, and data preparation.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def check_env_file():
    """Check if .env file exists and is properly configured"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("⚠️  .env file not found")
        if env_example.exists():
            print("   Creating .env from .env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("   ✅ Created .env (update with your API key)")
        else:
            print("   ❌ .env.example not found")
    
    # Check if GEMINI_API_KEY is configured
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_google_gemini_api_key_here" in content or "GEMINI_API_KEY=" not in content:
            print("⚠️  GEMINI_API_KEY not configured in .env")
            print("   Please update .env with your Google Gemini API key")
            return False
    
    print("✅ .env file configured")
    return True


def check_directories():
    """Create necessary directories"""
    directories = [
        "data/raw_markdown",
        "data/processed_chunks",
        "data/vector_db",
        "logs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure verified")


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def verify_imports():
    """Verify critical imports"""
    print("\n🔍 Verifying imports...")
    critical_imports = [
        ("fastapi", "FastAPI"),
        ("google.generativeai", "google-generativeai"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "sentence-transformers"),
    ]
    
    for module, name in critical_imports:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} not installed")
            return False
    
    return True


def main():
    """Run all setup checks"""
    print("\n" + "="*60)
    print("  Aloysius Chatbot - Setup & Initialization")
    print("="*60 + "\n")
    
    # Run checks
    check_python_version()
    print()
    
    env_configured = check_env_file()
    print()
    
    check_directories()
    print()
    
    # Ask to install dependencies
    response = input("📦 Install/upgrade dependencies? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    print()
    
    # Verify imports
    if verify_imports():
        print()
        print("="*60)
        if env_configured:
            print("✅ Setup complete! You're ready to go.")
            print()
            print("Next steps:")
            print("  1. Start the API server:")
            print("     python -m phase7_api.main")
            print()
            print("  2. Open API docs:")
            print("     http://localhost:8000/docs")
        else:
            print("⚠️  Setup complete, but .env configuration needed")
            print()
            print("Next steps:")
            print("  1. Edit .env and add your GEMINI_API_KEY")
            print("  2. Run setup again to verify")
        print("="*60)
    else:
        print("\n❌ Setup incomplete - fix import errors and try again")
        sys.exit(1)


if __name__ == "__main__":
    main()
