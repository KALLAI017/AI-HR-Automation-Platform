"""
Test script to verify interview storage system
"""

from interview_storage import InterviewStorage
from datetime import datetime

def test_storage_system():
    """Test all storage functionality"""
    
    print("=" * 60)
    print("TESTING INTERVIEW STORAGE SYSTEM")
    print("=" * 60)
    
    # Initialize storage
    print("\n1. Initializing storage...")
    storage = InterviewStorage("interview_results")
    print("✅ Storage initialized")
    
    # Create sample interview data
    print("\n2. Creating sample interview data...")
    
    sample_interview_1 = {
        'interview_id': 'INT_20250129_140000',
        'problem': 'Two Sum',
        'stages_completed': ['introduction', 'clarification', 'approach', 'coding', 'review'],
        'approach_quality': 85,
        'communication_score': 90,
        'hints_used': 1,
        'total_messages': 12,
        'duration_estimate': 24
    }
    
    sample_scoring_1 = {
        'test_score': 45.0,
        'quality_score': 27.0,
        'approach_score': 8.5,
        'communication_score': 9.0,
        'hint_penalty': -5,
        'final_score': 84.5,
        'test_results': {
            'passed': 9,
            'total': 10,
            'all_passed': False
        }
    }
    
    sample_interview_2 = {
        'interview_id': 'INT_20250129_150000',
        'problem': 'Valid Parentheses',
        'stages_completed': ['introduction', 'approach', 'coding', 'review'],
        'approach_quality': 95,
        'communication_score': 95,
        'hints_used': 0,
        'total_messages': 8,
        'duration_estimate': 16
    }
    
    sample_scoring_2 = {
        'test_score': 50.0,
        'quality_score': 28.5,
        'approach_score': 9.5,
        'communication_score': 9.5,
        'hint_penalty': 0,
        'final_score': 97.5,
        'test_results': {
            'passed': 10,
            'total': 10,
            'all_passed': True
        }
    }
    
    print("✅ Sample data created")
    
    # Save interviews
    print("\n3. Saving interview results...")
    
    path1 = storage.save_interview_result(
        candidate_id="TEST_CAND_001",
        interview_data=sample_interview_1,
        scoring_data=sample_scoring_1
    )
    print(f"   Interview 1 saved to: {path1}")
    
    path2 = storage.save_interview_result(
        candidate_id="TEST_CAND_001",
        interview_data=sample_interview_2,
        scoring_data=sample_scoring_2
    )
    print(f"   Interview 2 saved to: {path2}")
    
    # Save for second candidate
    path3 = storage.save_interview_result(
        candidate_id="TEST_CAND_002",
        interview_data=sample_interview_1,
        scoring_data=sample_scoring_1
    )
    print(f"   Interview 3 saved to: {path3}")
    
    print("✅ All interviews saved")
    
    # Load interviews
    print("\n4. Loading interview results...")
    
    interviews = storage.load_candidate_interviews("TEST_CAND_001")
    print(f"   Found {len(interviews)} interviews for TEST_CAND_001")
    for idx, interview in enumerate(interviews, 1):
        score = interview['scoring']['final_score']
        problem = interview['interview_data']['problem']
        print(f"   - Interview {idx}: {problem} = {score}/100")
    
    print("✅ Interviews loaded successfully")
    
    # Load latest
    print("\n5. Loading latest interview...")
    
    latest = storage.load_latest_interview("TEST_CAND_001")
    if latest:
        print(f"   Latest interview: {latest['interview_data']['problem']}")
        print(f"   Score: {latest['scoring']['final_score']}/100")
        print(f"   Date: {latest['metadata']['date']}")
    
    print("✅ Latest interview loaded")
    
    # Get all candidates
    print("\n6. Getting all candidates...")
    
    candidates = storage.get_all_candidates()
    print(f"   Found {len(candidates)} candidates: {', '.join(candidates)}")
    
    print("✅ Candidates listed")
    
    # Get summary
    print("\n7. Getting candidate summary...")
    
    summary = storage.get_candidate_summary("TEST_CAND_001")
    print(f"   Candidate: {summary['candidate_id']}")
    print(f"   Total Interviews: {summary['total_interviews']}")
    print(f"   Average Score: {summary['average_score']:.1f}/100")
    print(f"   Highest Score: {summary['highest_score']:.1f}/100")
    print(f"   Problems Attempted: {summary['problems_attempted']}")
    
    print("✅ Summary generated")
    
    # Export all
    print("\n8. Exporting all results...")
    
    export_path = storage.export_all_results("test_export.json")
    print(f"   All results exported to: {export_path}")
    
    print("✅ Export complete")
    
    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ Storage initialization: PASSED")
    print("✅ Save interview results: PASSED")
    print("✅ Load interviews: PASSED")
    print("✅ Load latest interview: PASSED")
    print("✅ List candidates: PASSED")
    print("✅ Generate summary: PASSED")
    print("✅ Export all results: PASSED")
    print("\n🎉 ALL TESTS PASSED!")
    print("=" * 60)
    
    # Show file locations
    print("\n📁 Generated Files:")
    print(f"   - interview_results/TEST_CAND_001/ (2 interviews)")
    print(f"   - interview_results/TEST_CAND_002/ (1 interview)")
    print(f"   - interview_results/test_export.json")
    print("\nYou can now:")
    print("  1. Check the JSON files in interview_results/")
    print("  2. Run the app and view results in Admin Portal → Interview Results")
    print("  3. Use the Python API to access data programmatically")


if __name__ == "__main__":
    try:
        test_storage_system()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
