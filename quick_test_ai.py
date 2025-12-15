"""
Quick hybrid analyzer test - minimal version
Tests only the AI components (Whisper + LLM) without deep learning models
"""
import os
from dotenv import load_dotenv
load_dotenv()

print("🚀 Quick Hybrid Analyzer Test (AI components only)")
print("=" * 60)

# Test imports
print("\n1. Testing Groq imports...")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    print("   ✅ Groq client initialized")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test LLM
print("\n2. Testing LLM (chat completion)...")
try:
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{"role": "user", "content": "Say 'Working' only"}],
        max_tokens=5
    )
    print(f"   ✅ LLM response: {resp.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test moviepy
print("\n3. Testing MoviePy for audio extraction...")
try:
    from moviepy.editor import VideoFileClip
    print("   ✅ MoviePy imported")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test video file exists
print("\n4. Checking test video...")
video_path = "uploads/interview_videos/candidate_confident.mp4"
if os.path.exists(video_path):
    print(f"   ✅ Video found: {video_path}")
    
    # Try audio extraction
    print("\n5. Testing audio extraction...")
    try:
        video = VideoFileClip(video_path)
        audio_path = "temp_test_audio.wav"
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        
        if os.path.exists(audio_path):
            size = os.path.getsize(audio_path)
            print(f"   ✅ Audio extracted: {size} bytes")
            
            # Test Whisper transcription
            print("\n6. Testing Whisper transcription...")
            try:
                with open(audio_path, "rb") as file:
                    transcription = client.audio.transcriptions.create(
                        file=(audio_path, file.read()),
                        model="whisper-large-v3-turbo",
                        response_format="json",
                        language="en"
                    )
                transcript = transcription.text
                print(f"   ✅ Transcript ({len(transcript)} chars): {transcript[:100]}...")
                
                # Clean up
                os.remove(audio_path)
                
            except Exception as e:
                print(f"   ❌ Whisper failed: {e}")
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                exit(1)
        else:
            print("   ❌ Audio file not created")
            exit(1)
            
    except Exception as e:
        print(f"   ❌ Audio extraction failed: {e}")
        exit(1)
else:
    print(f"   ❌ Video not found: {video_path}")
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL AI COMPONENTS WORKING!")
print("=" * 60)
print("\nThe issue is likely in the Streamlit integration or the")
print("heuristic analyzer (OpenCV/DeepFace) taking too long to load.")
