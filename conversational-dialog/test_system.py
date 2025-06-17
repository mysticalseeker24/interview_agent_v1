#!/usr/bin/env python3
"""
Test script for InterviewPilot.AI system
Tests core functionality without requiring audio input
"""

import os
import sys
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

def test_environment():
    """Test that environment variables are loaded correctly"""
    print("🔧 Testing environment setup...")
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not found")
        return False
        
    print("✅ Environment variables loaded successfully")
    return True

def test_imports():
    """Test that all required modules can be imported"""
    print("\n📦 Testing imports...")
    try:
        import anthropic
        import openai
        import pyaudio
        import pygame
        import PyPDF2
        import pandas
        import numpy
        from audioToText import AudioRecorder, transcribe_audio
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_claude_4_api():
    """Test Claude 4 API connectivity"""
    print("\n🤖 Testing Claude 4 API...")
    try:
        load_dotenv()
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Test Claude 4 Sonnet
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=100,
            temperature=0,
            messages=[{
                'role': 'user', 
                'content': 'You are an AI interviewer. Ask me one professional interview question.'
            }]
        )
        
        print("✅ Claude 4 Sonnet API working")
        print(f"   Sample response: {response.content[0].text[:100]}...")
        
        # Test Claude 4 Opus
        response = client.messages.create(
            model='claude-opus-4-20250514',
            max_tokens=50,
            temperature=0,
            messages=[{
                'role': 'user', 
                'content': 'Generate a brief interviewer persona description.'
            }]
        )
        
        print("✅ Claude 4 Opus API working")
        print(f"   Sample response: {response.content[0].text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Claude 4 API error: {e}")
        return False

def test_openai_api():
    """Test OpenAI API connectivity"""
    print("\n🎵 Testing OpenAI API...")
    try:
        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Test TTS
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Testing InterviewPilot AI system"
        )
        
        # Save test audio file
        with open("test_audio.mp3", "wb") as f:
            f.write(response.content)
            
        print("✅ OpenAI TTS API working")
        
        # Clean up test file
        if os.path.exists("test_audio.mp3"):
            os.remove("test_audio.mp3")
            
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_interviewer_class():
    """Test the Interviewer class initialization"""
    print("\n👔 Testing Interviewer class...")
    try:
        # Read a sample persona
        with open('ethan-the-strategic-planner-product-manager-watershed-response-guidelines.txt', 'r') as file:
            persona = file.read()
        
        from interviewer import Interviewer
        interviewer = Interviewer(persona)
        
        # Test text-to-text functionality
        response = interviewer.text_to_text("Hello, I'm ready for the interview.")
        print("✅ Interviewer class working")
        print(f"   Sample response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Interviewer class error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 InterviewPilot.AI System Test")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_claude_4_api,
        test_openai_api,
        test_interviewer_class
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! InterviewPilot.AI is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
