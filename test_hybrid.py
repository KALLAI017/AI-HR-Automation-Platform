"""
Quick test runner for hybrid video analyzer
Tests the analyze_candidate_video_ai function on a sample video
"""

from video_analyzer_hybrid import analyze_candidate_video_ai
import os
import json

def test_hybrid_analyzer():
    """Test the hybrid analyzer on available videos"""
    video_dir = "uploads/interview_videos"
    
    if not os.path.exists(video_dir):
        print(f"❌ Video directory not found: {video_dir}")
        return
    
    # Get all videos
    videos = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    if not videos:
        print(f"❌ No videos found in {video_dir}")
        return
    
    print(f"📹 Found {len(videos)} video(s)")
    print("=" * 60)
    
    # Test first video
    test_video = os.path.join(video_dir, videos[0])
    print(f"\n🎬 Testing: {videos[0]}")
    print("-" * 60)
    
    try:
        results = analyze_candidate_video_ai(test_video)
        
        if results['status'] == 'success':
            print("✅ Analysis successful!\n")
            print(f"📊 Overall Confidence: {results['overall_confidence_score']:.2f}/10")
            print(f"🎯 Heuristic Score: {results['heuristic_score']:.2f}/10")
            print(f"🤖 AI Communication: {results['ai_communication_score']}/100")
            print(f"\n💬 AI Feedback:")
            print(f"   {results['ai_feedback']}")
            print(f"\n📝 Transcript ({len(results['transcript'])} chars):")
            print(f"   {results['transcript'][:200]}...")
            
            # Save full results
            output_file = "test_results.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Full results saved to: {output_file}")
            
        else:
            print(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Hybrid Video Analyzer Test")
    print("=" * 60)
    test_hybrid_analyzer()
