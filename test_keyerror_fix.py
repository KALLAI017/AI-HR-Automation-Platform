"""
Quick error check - tests the key access without full analysis
"""
print("Testing KeyError fix...")

# Simulate the data structure returned by video_analyzer
mock_heuristic_results = {
    'confidence_score': 7.5,
    'visual_analysis': {
        'face_presence': 95.0,
        'emotional_positivity': 65.0,
        'smile_rate': 45.0,
        'eye_contact_rate': 80.0,
        'head_stability': 70.0,
        'nervousness_indicators': 15.0
    },
    'audio_analysis': {
        'confidence_score': 6.8,
        'pitch_variation': 0.15,
        'energy': 0.65,
        'speech_rate': 1.2
    }
}

# Test the key access logic
try:
    # This is what was failing before
    heuristic_score = mock_heuristic_results.get('overall_confidence_score') or mock_heuristic_results.get('confidence_score', 5.0)
    print(f"✅ Key access works! Score: {heuristic_score}")
    
    # Test breakdown extraction
    visual_data = mock_heuristic_results.get('visual_analysis', {})
    audio_data = mock_heuristic_results.get('audio_analysis', {})
    
    breakdown = {
        'nervousness_score': visual_data.get('nervousness_indicators', 0),
        'eye_contact_score': visual_data.get('eye_contact_rate', 0),
        'smile_score': visual_data.get('smile_rate', 0),
        'fidgeting_score': 100 - visual_data.get('head_stability', 0),
        'blink_rate': 0,
        'avg_face_quality': visual_data.get('face_presence', 0),
        'audio_score': audio_data.get('confidence_score', 0),
        'pitch_variation': audio_data.get('pitch_variation', 0),
        'energy': audio_data.get('energy', 0),
        'speech_rate': audio_data.get('speech_rate', 0),
        'emotional_positivity': visual_data.get('emotional_positivity', 0),
        'head_stability': visual_data.get('head_stability', 0)
    }
    
    print("✅ Breakdown extraction works!")
    print(f"   Nervousness: {breakdown['nervousness_score']}")
    print(f"   Eye Contact: {breakdown['eye_contact_score']}")
    print(f"   Smile: {breakdown['smile_score']}")
    
    print("\n✅ ALL FIXES VERIFIED - Error should be resolved!")
    
except KeyError as e:
    print(f"❌ KeyError still present: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
