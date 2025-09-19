"""Setup script for the Tech Search Engine."""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created. Please edit it with your API keys.")
        return True
    elif not env_file.exists():
        print("❌ No env.example file found!")
        return False
    else:
        print("✅ .env file already exists.")
        return True

def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        "streamlit",
        "httpx", 
        "pydantic",
        "pydantic-settings",
        "sqlmodel",
        "youtube_transcript_api",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "python-dotenv":
                __import__("dotenv")
            elif package == "youtube-transcript-api":
                __import__("youtube_transcript_api")
            elif package == "pydantic-settings":
                __import__("pydantic_settings")
            else:
                __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed.")
        return True

def check_api_keys():
    """Check if API keys are configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    issues = []
    
    if not tavily_key or tavily_key.startswith("your_"):
        issues.append("TAVILY_API_KEY not configured")
    
    if not groq_key or groq_key.startswith("your_"):
        issues.append("GROQ_API_KEY not configured")
    
    if issues:
        print("⚠️  API Key Issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nEdit your .env file with valid API keys.")
        return False
    else:
        print("✅ API keys are configured.")
        return True

def main():
    """Main setup function."""
    print("🔍 Tech Search Engine Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check API keys
    api_keys_ok = check_api_keys()
    
    print("\n" + "=" * 40)
    if api_keys_ok:
        print("🎉 Setup complete! Run: streamlit run app.py")
    else:
        print("⚠️  Setup partially complete. Configure API keys in .env file.")
        print("   Then run: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main()
