#!/usr/bin/env python3
"""
Simple test to prove LLM calls are/aren't working
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_single_agent():
    """Test a single agent with raw output"""
    
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    
    print("🧪 TESTING SINGLE AGENT LLM CALL")
    print("=" * 40)
    
    # Simple test
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=200)
    
    system_msg = SystemMessage(content="""You are Dr. Marcus Chen, Chief of Energy Department in Mailopolis.
You are technical and data-driven, passionate about carbon neutrality goals.

Respond in this EXACT format:
Decision: [SUPPORT/OPPOSE/NEUTRAL]
Reasoning: [Your 1-2 sentence reasoning in character]
Confidence: [Number from 1-10]""")
    
    human_msg = HumanMessage(content="""Should we support a Green Building Retrofit Program that provides incentives for solar panels and energy-efficient systems?""")
    
    print("📤 Sending to OpenAI...")
    response = await llm.ainvoke([system_msg, human_msg])
    
    print(f"📥 RAW LLM Response:")
    print(f"'{response.content}'")
    print()
    
    # Test parsing
    response_text = response.content
    lines = response_text.split('\n')
    
    decision = "UNKNOWN"
    reasoning = "No reasoning found"
    confidence = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith("Decision:"):
            decision = line.replace("Decision:", "").strip()
        elif line.startswith("Reasoning:"):
            reasoning = line.replace("Reasoning:", "").strip()
        elif line.startswith("Confidence:"):
            conf_str = line.replace("Confidence:", "").strip()
            try:
                confidence = int(conf_str) * 10
            except:
                confidence = 50
    
    print(f"✅ PARSED RESULTS:")
    print(f"  Decision: {decision}")
    print(f"  Reasoning: {reasoning}")
    print(f"  Confidence: {confidence}%")

if __name__ == "__main__":
    asyncio.run(test_single_agent())