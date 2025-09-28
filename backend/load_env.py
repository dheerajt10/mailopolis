"""
Environment configuration loader for Mailopolis
Loads environment variables from .env file and provides configuration helpers
"""

import os
from pathlib import Path
from typing import Optional


def load_environment_variables():
    """
    Load environment variables from .env file in the backend directory.
    This function looks for a .env file and loads the variables into os.environ.
    """
    # Look for .env file in the backend directory
    backend_dir = Path(__file__).parent
    env_file = backend_dir / '.env'
    
    if env_file.exists():
        print(f"📁 Loading environment variables from: {env_file}")
        
        with open(env_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE format
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Set the environment variable
                    os.environ[key] = value
                    print(f"✅ Loaded {key}")
                else:
                    print(f"⚠️  Warning: Invalid format on line {line_num}: {line}")
    else:
        print(f"📂 No .env file found at: {env_file}")
        print("💡 Create a .env file with your API keys:")
        print("   OPENAI_API_KEY=your_openai_key_here")
        print("   ANTHROPIC_API_KEY=your_anthropic_key_here")


def get_api_key(provider: str) -> Optional[str]:
    """
    Get API key for a specific provider.
    
    Args:
        provider: Either 'openai', 'anthropic', or 'google'
        
    Returns:
        API key if found, None otherwise
    """
    if provider.lower() == 'openai':
        return os.getenv('OPENAI_API_KEY')
    elif provider.lower() == 'anthropic':
        return os.getenv('ANTHROPIC_API_KEY')
    elif provider.lower() == 'google':
        return os.getenv('GOOGLE_API_KEY')
    else:
        raise ValueError(f"Unknown provider: {provider}")


def check_api_configuration() -> dict:
    """
    Check which API providers are configured.
    
    Returns:
        Dict with provider availability status
    """
    config = {
        'openai': bool(get_api_key('openai')),
        'anthropic': bool(get_api_key('anthropic')),
        'google': bool(get_api_key('google')),
        'any_available': False
    }
    
    config['any_available'] = config['openai'] or config['anthropic'] or config['google']
    
    return config


def print_api_status():
    """Print the current API configuration status"""
    config = check_api_configuration()
    
    print("🔑 API Configuration Status:")
    print(f"   OpenAI: {'✅ Configured' if config['openai'] else '❌ Not configured'}")
    print(f"   Google Gemini: {'✅ Configured' if config['google'] else '❌ Not configured'}")
    print(f"   Anthropic: {'✅ Configured' if config['anthropic'] else '❌ Not configured'}")
    
    if not config['any_available']:
        print("⚠️  No API keys configured - will use mock responses")
        print("💡 Set OPENAI_API_KEY, GOOGLE_API_KEY, or ANTHROPIC_API_KEY environment variables")
    else:
        print("🚀 Ready for LLM-powered agent interactions!")


def create_sample_env_file():
    """Create a sample .env file with placeholder values"""
    backend_dir = Path(__file__).parent
    env_file = backend_dir / '.env.example'
    
    sample_content = """# Mailopolis Environment Configuration
# Copy this file to .env and fill in your actual API keys

# OpenAI API Key (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic API Key (for Claude models) 
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Set preferred provider (openai, google, or anthropic)
PREFERRED_LLM_PROVIDER=openai

# Optional: Enable debug logging
DEBUG=false

# Optional: Set temperature for LLM responses (0.0 to 1.0)
LLM_TEMPERATURE=0.7
"""
    
    with open(env_file, 'w') as f:
        f.write(sample_content)
    
    print(f"📝 Created sample environment file: {env_file}")
    print("📋 Copy it to .env and add your actual API keys")


if __name__ == "__main__":
    """Run this script to check your environment configuration"""
    print("🏛️  Mailopolis Environment Configuration")
    print("=" * 50)
    
    # Load environment variables
    load_environment_variables()
    
    # Check and print status
    print_api_status()
    
    # Create sample file if no .env exists
    backend_dir = Path(__file__).parent
    if not (backend_dir / '.env').exists():
        print("\n" + "=" * 50)
        create_sample_env_file()