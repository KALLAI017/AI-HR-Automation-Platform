"""
Test script for video confidence analyzer
Tests the upgraded DeepFace + SpeechBrain implementation
"""

from video_analyzer import analyze_candidate_video
import os
import json
import numpy as np

def test_video_analysis(video_path: str, expected_confidence: str = "unknown"):
    """Test video analysis and display results"""
    
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return None
    
    print(f"\n{'='*60}")
    print(f"📹 Analyzing: {os.path.basename(video_path)}")
    print(f"Expected confidence level: {expected_confidence}")
    print(f"{'='*60}\n")
    
    # Analyze the video
    print("🔍 Starting analysis (this may take 1-2 minutes)...")
    result = analyze_candidate_video(video_path)
    
    # Display results
    print(f"\n✅ Analysis complete!")
    print(f"\n{'='*60}")
    print(f"📊 CONFIDENCE SCORE: {result['confidence_score']}/10")
    print(f"{'='*60}")
    print(f"\n💬 Interpretation:")
    print(f"   {result['interpretation']}")
    
    print(f"\n✨ Strengths:")
    for strength in result.get('strengths', []):
        print(f"   ✓ {strength}")
    
    print(f"\n💡 Areas for Improvement:")
    for improvement in result.get('areas_for_improvement', []):
        print(f"   • {improvement}")
    
    # Detailed metrics
    print(f"\n{'='*60}")
    print(f"📈 DETAILED METRICS")
    print(f"{'='*60}")
    
    visual = result.get('visual_analysis', {})
    if visual and 'error' not in visual:
        print(f"\n👁️  Visual Analysis:")
        print(f"   Face Presence: {visual.get('face_presence', 0):.1f}%")
        print(f"   Emotional Positivity: {visual.get('emotional_positivity', 0):.1f}%")
        print(f"   Eye Contact: {visual.get('eye_contact_rate', 0):.1f}%")
        print(f"   Head Stability: {visual.get('head_stability', 0):.1f}%")
        print(f"   Nervousness Indicators: {visual.get('nervousness_indicators', 0):.1f}")
        
        # DeepFace emotion breakdown
        if 'emotion_breakdown' in visual:
            print(f"\n   🎭 Emotion Breakdown (DeepFace):")
            emotions = visual['emotion_breakdown']
            for emotion, score in emotions.items():
                print(f"      {emotion.capitalize()}: {score:.1f}%")
    
    audio = result.get('audio_analysis', {})
    if audio and 'error' not in audio:
        print(f"\n🔊 Audio Analysis:")
        print(f"   Pitch Stability: {audio.get('pitch_stability', 0):.1f}%")
        print(f"   Energy Consistency: {audio.get('energy_consistency', 0):.1f}%")
        print(f"   Speaking Ratio: {audio.get('speaking_ratio', 0):.1f}%")
        print(f"   Speech Rate: {audio.get('speech_rate', 0):.1f} onsets/min")
        
        if audio.get('speechbrain_used', False):
            print(f"\n   🎙️  Voice Emotion (SpeechBrain):")
            print(f"      Detected: {audio.get('detected_emotion', 'unknown')}")
            print(f"      Confidence: {audio.get('voice_emotion_score', 0):.1f}%")
        else:
            print(f"\n   ℹ️  SpeechBrain emotion detection not available (using acoustic features only)")
    
    print(f"\n{'='*60}\n")
    
    # Save results to JSON
    output_file = video_path.replace('.mp4', '_analysis.json').replace('.avi', '_analysis.json').replace('.mov', '_analysis.json')
    def _to_serializable(o):
        """Recursively convert numpy types to native Python types for JSON dumping."""
        # dict
        if isinstance(o, dict):
            return {k: _to_serializable(v) for k, v in o.items()}
        # list/tuple
        if isinstance(o, (list, tuple)):
            return [_to_serializable(v) for v in o]
        # numpy scalars
        if isinstance(o, (np.floating, np.float32, np.float64)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        # numpy arrays
        if hasattr(o, 'tolist'):
            try:
                return _to_serializable(o.tolist())
            except Exception:
                pass
        # fallback
        return o

    serializable_result = _to_serializable(result)
    with open(output_file, 'w') as f:
        json.dump(serializable_result, f, indent=2)
    print(f"📄 Full results saved to: {output_file}\n")
    
    return result


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   VIDEO CONFIDENCE ANALYZER - ACCURACY TEST               ║
    ║   Using DeepFace + SpeechBrain (Option 1)                 ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Test with sample videos
    test_videos = [
        ("uploads/interview_videos/candidate_confident.mp4", "high confidence"),
        ("uploads/interview_videos/candidate_nervous.mp4", "low confidence"),
    ]
    
    results = {}
    for video_path, expected in test_videos:
        result = test_video_analysis(video_path, expected)
        if result:
            results[video_path] = result['confidence_score']
    
    # Summary
    if results:
        print(f"\n{'='*60}")
        print(f"📊 SUMMARY")
        print(f"{'='*60}")
        for video, score in results.items():
            print(f"{os.path.basename(video)}: {score}/10")
        print(f"{'='*60}\n")
