#!/usr/bin/env python3
"""
Debug LangChain OpenAI integration
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_langchain_openai():
    """Test if LangChain can actually call OpenAI"""
    
    print("🔍 DEBUGGING LANGCHAIN OPENAI INTEGRATION")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API Key found: {api_key[:10]}...")
    else:
        print("❌ No OpenAI API Key found")
        return
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        print("✅ LangChain imports successful")
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=100
        )
        
        print("✅ ChatOpenAI initialized")
        
        # Test simple message
        messages = [HumanMessage(content="Say hello in exactly 5 words.")]
        
        print("📤 Sending test message to OpenAI...")
        response = await llm.ainvoke(messages)
        
        print(f"📥 OpenAI Response: '{response.content}'")
        print(f"📊 Response Type: {type(response)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"🐛 Exception Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    asyncio.run(test_langchain_openai())