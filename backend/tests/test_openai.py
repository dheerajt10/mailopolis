#!/usr/bin/env python3
"""
Simple test of OpenAI API integration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import openai
    
    print("OpenAI package imported successfully")
    print(f"Version: {openai.__version__}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"API key found: {api_key[:10]}...")
        
        # Try to create client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully!")
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from Mailopolis!'"}
            ],
            max_tokens=50
        )
        
        print(f"✅ API call successful: {response.choices[0].message.content}")
        
    else:
        print("❌ No API key found in environment")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()