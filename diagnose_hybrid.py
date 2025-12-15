"""
Diagnostic script to test video analyzer hybrid components
"""
import os
import sys

print("=" * 60)
print("🔍 HYBRID ANALYZER DIAGNOSTIC TEST")
print("=" * 60)

# Test 1: Check imports
print("\n1️⃣ Testing imports...")
try:
    from video_analyzer import analyze_candidate_video
    print("   ✅ video_analyzer imported")
except Exception as e:
    print(f"   ❌ video_analyzer import failed: {e}")
    sys.exit(1)

try:
    from video_analyzer_hybrid import analyze_candidate_video_ai, HybridVideoAnalyzer
    print("   ✅ video_analyzer_hybrid imported")
except Exception as e:
    print(f"   ❌ video_analyzer_hybrid import failed: {e}")
    sys.exit(1)

try:
    from groq import Groq
    print("   ✅ groq SDK imported")
except Exception as e:
    print(f"   ❌ groq SDK import failed: {e}")
    sys.exit(1)

try:
    from moviepy.editor import VideoFileClip
    print("   ✅ moviepy imported")
except Exception as e:
    print(f"   ❌ moviepy import failed: {e}")
    sys.exit(1)

# Test 2: Check API key
print("\n2️⃣ Testing API key...")
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
if api_key:
    print(f"   ✅ GROQ_API_KEY found (length: {len(api_key)})")
else:
    print("   ❌ GROQ_API_KEY not found in environment")
    sys.exit(1)

# Test 3: Check video files
print("\n3️⃣ Testing video files...")
video_dir = "uploads/interview_videos"
if os.path.exists(video_dir):
    videos = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
    print(f"   ✅ Video directory exists with {len(videos)} video(s)")
    for v in videos:
        print(f"      - {v}")
else:
    print(f"   ⚠️ Video directory not found: {video_dir}")

# Test 4: Test heuristic analyzer (quick)
print("\n4️⃣ Testing heuristic analyzer...")
if videos:
    test_video = os.path.join(video_dir, videos[0])
    print(f"   Testing with: {videos[0]}")
    try:
        result = analyze_candidate_video(test_video)
        score = result.get('overall_confidence_score', 0)
        print(f"   ✅ Heuristic analysis works (score: {score:.2f}/10)")
    except Exception as e:
        print(f"   ❌ Heuristic analysis failed: {e}")
        import traceback
        traceback.print_exc()

# Test 5: Test Groq API
print("\n5️⃣ Testing Groq API...")
try:
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{"role": "user", "content": "Say 'OK' only"}],
        max_tokens=5
    )
    print(f"   ✅ Groq API works: {resp.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Groq API failed: {e}")
    sys.exit(1)

# Test 6: Test hybrid analyzer initialization
print("\n6️⃣ Testing hybrid analyzer initialization...")
try:
    analyzer = HybridVideoAnalyzer()
    print("   ✅ HybridVideoAnalyzer initialized")
except Exception as e:
    print(f"   ❌ HybridVideoAnalyzer init failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL DIAGNOSTIC TESTS PASSED!")
print("=" * 60)
print("\nThe hybrid analyzer should be working.")
print("If it's not working in Streamlit, check:")
print("1. Streamlit is loading the correct .env file")
print("2. Video upload is saving files correctly")
print("3. Check Streamlit logs for specific errors")
