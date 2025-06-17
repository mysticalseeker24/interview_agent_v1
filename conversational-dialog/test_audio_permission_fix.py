#!/usr/bin/env python3
"""
Test script to verify the audio permission fix
"""

import os
import time
from dotenv import load_dotenv
from interviewer import Interviewer

def test_audio_permission_fix():
    """Test that the audio permission issue is resolved"""
    print("🔧 Testing audio permission fix...")
    
    try:
        # Load environment
        load_dotenv()
        
        # Create a simple test persona
        test_persona = "You are a friendly test interviewer. Keep responses very brief."
        
        # Initialize interviewer
        interviewer = Interviewer(test_persona)
        
        # Test text-to-speech multiple times to check for permission issues
        test_messages = [
            "Hello, this is a test.",
            "Testing audio file handling.",
            "Final test message."
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"   Testing TTS {i}/3: '{message[:30]}...'")
            try:
                interviewer.text_to_speech(message)
                print(f"   ✅ TTS test {i} completed successfully")
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print(f"   ❌ TTS test {i} failed: {e}")
                return False
        
        # Test cleanup
        interviewer._cleanup_temp_files()
        print("   ✅ Cleanup completed successfully")
        
        print("✅ Audio permission fix test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Audio permission test failed: {e}")
        return False

def main():
    """Run the audio permission test"""
    print("🚀 Audio Permission Fix Test")
    print("=" * 40)
    
    success = test_audio_permission_fix()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Audio permission fix is working!")
        print("\n💡 Improvements made:")
        print("   - Unique timestamped audio files prevent conflicts")
        print("   - Proper pygame music unloading releases file handles")
        print("   - Enhanced cleanup handles all temporary audio files")
        print("   - Better error handling for audio operations")
    else:
        print("⚠️  Audio permission test failed. Check error messages above.")
    
    return success

if __name__ == "__main__":
    main()
