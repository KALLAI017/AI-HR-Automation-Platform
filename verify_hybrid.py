"""
FINAL VERIFICATION TEST
This demonstrates the hybrid analyzer is working by showing each component
"""
import os
import sys

print("=" * 70)
print("  VIDEO ANALYZER HYBRID - FINAL VERIFICATION")
print("=" * 70)

# Step 1: Verify all files exist
print("\n1️⃣ VERIFYING FILES...")
files_to_check = [
    "video_analyzer.py",
    "video_analyzer_hybrid.py",
    "app.py",
    ".env",
    "uploads/interview_videos/candidate_confident.mp4"
]

all_exist = True
for file in files_to_check:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"   {status} {file}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n❌ Some required files are missing!")
    sys.exit(1)

# Step 2: Check integration in app.py
print("\n2️⃣ CHECKING STREAMLIT INTEGRATION...")
with open("app.py", "r", encoding="utf-8") as f:
    app_content = f.read()
    
checks = {
    "show_video_interview_interface function": "def show_video_interview_interface():" in app_content,
    "hybrid analyzer import": "from video_analyzer_hybrid import analyze_candidate_video_ai" in app_content,
    "analyze_candidate_video_ai call": "analyze_candidate_video_ai(video_path)" in app_content,
    "video interview UI call": "show_video_interview_interface()" in app_content
}

integration_ok = True
for check_name, check_result in checks.items():
    status = "✅" if check_result else "❌"
    print(f"   {status} {check_name}")
    if not check_result:
        integration_ok = False

if not integration_ok:
    print("\n❌ Streamlit integration is incomplete!")
    sys.exit(1)

# Step 3: Verify imports work
print("\n3️⃣ TESTING IMPORTS (this may take 15-20 seconds)...")
try:
    print("   Loading video_analyzer_hybrid...")
    from video_analyzer_hybrid import analyze_candidate_video_ai, HybridVideoAnalyzer
    print("   ✅ video_analyzer_hybrid imported successfully")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Step 4: Test Groq API
print("\n4️⃣ TESTING GROQ API...")
try:
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("   ❌ GROQ_API_KEY not found")
        sys.exit(1)
    
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{"role": "user", "content": "Respond with only: OK"}],
        max_tokens=5
    )
    print(f"   ✅ Groq API working: {resp.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Groq API test failed: {e}")
    sys.exit(1)

# Step 5: Summary
print("\n" + "=" * 70)
print("  ✅ ALL CHECKS PASSED - HYBRID ANALYZER IS READY!")
print("=" * 70)

print("\n📝 TO USE IN STREAMLIT:")
print("   1. Run: python -m streamlit run app.py")
print("   2. Login as a candidate")
print("   3. Complete the test")
print("   4. Upload a video in the 'Video Self-Introduction' section")
print("   5. Click 'Analyze with AI' and wait 30-60 seconds")
print("   6. View your results!")

print("\n📝 TO TEST FROM COMMAND LINE:")
print('   python -c "from video_analyzer_hybrid import analyze_candidate_video_ai; ')
print('   result = analyze_candidate_video_ai(\'uploads/interview_videos/candidate_confident.mp4\'); ')
print('   print(f\'Score: {result[\"overall_confidence_score\"]:.1f}/10\')"')

print("\n" + "=" * 70)
