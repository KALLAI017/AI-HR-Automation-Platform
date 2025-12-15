"""
Quick test to verify the fix for KeyError: 'overall_confidence_score'
"""
from video_analyzer_hybrid import analyze_candidate_video_ai

print("Testing hybrid analyzer with fix...")
print("=" * 60)

video_path = "uploads/interview_videos/candidate_confident.mp4"

try:
    result = analyze_candidate_video_ai(video_path)
    
    print("\n✅ Analysis completed successfully!")
    print(f"Status: {result.get('status')}")
    print(f"Overall Score: {result.get('overall_confidence_score'):.2f}/10")
    print(f"Heuristic Score: {result.get('heuristic_score'):.2f}/10")
    print(f"AI Communication: {result.get('ai_communication_score')}/100")
    
    if result.get('status') == 'error':
        print(f"\n❌ Error: {result.get('error')}")
    
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()
