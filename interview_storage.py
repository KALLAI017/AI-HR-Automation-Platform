"""
Interview Results Storage System
Handles saving and loading interview scores to/from JSON files
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class InterviewStorage:
    """Manage JSON storage of interview results"""
    
    def __init__(self, base_dir: str = "interview_results"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def save_interview_result(self, 
                             candidate_id: str,
                             interview_data: Dict,
                             scoring_data: Optional[Dict] = None) -> str:
        """
        Save interview results to JSON file
        
        Args:
            candidate_id: Unique candidate identifier
            interview_data: Data from get_final_report() or similar
            scoring_data: Additional scoring details (test_score, quality_score, etc.)
        
        Returns:
            Path to saved JSON file
        """
        # Create candidate directory
        candidate_dir = self.base_dir / candidate_id
        candidate_dir.mkdir(exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"interview_{timestamp}.json"
        filepath = candidate_dir / filename
        
        # Prepare complete interview record
        interview_record = {
            'metadata': {
                'candidate_id': candidate_id,
                'timestamp': timestamp,
                'date': datetime.now().isoformat(),
            },
            'interview_data': interview_data,
            'scoring': scoring_data or {}
        }
        
        # Save to JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(interview_record, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Interview results saved: {filepath}")
        return str(filepath)
    
    def load_candidate_interviews(self, candidate_id: str) -> List[Dict]:
        """
        Load all interview results for a candidate
        
        Args:
            candidate_id: Candidate identifier
        
        Returns:
            List of interview records (sorted by date, newest first)
        """
        candidate_dir = self.base_dir / candidate_id
        
        if not candidate_dir.exists():
            return []
        
        interviews = []
        for json_file in candidate_dir.glob("interview_*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['_filepath'] = str(json_file)
                    interviews.append(data)
            except Exception as e:
                print(f"⚠️ Error loading {json_file}: {e}")
        
        # Sort by timestamp (newest first)
        interviews.sort(key=lambda x: x['metadata']['timestamp'], reverse=True)
        
        return interviews
    
    def load_latest_interview(self, candidate_id: str) -> Optional[Dict]:
        """
        Load the most recent interview for a candidate
        
        Args:
            candidate_id: Candidate identifier
        
        Returns:
            Latest interview record or None
        """
        interviews = self.load_candidate_interviews(candidate_id)
        return interviews[0] if interviews else None
    
    def get_all_candidates(self) -> List[str]:
        """
        Get list of all candidate IDs with saved interviews
        
        Returns:
            List of candidate IDs
        """
        candidates = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and list(item.glob("interview_*.json")):
                candidates.append(item.name)
        
        return sorted(candidates)
    
    def get_candidate_summary(self, candidate_id: str) -> Dict:
        """
        Get summary statistics for a candidate
        
        Args:
            candidate_id: Candidate identifier
        
        Returns:
            Summary with total interviews, average score, etc.
        """
        interviews = self.load_candidate_interviews(candidate_id)
        
        if not interviews:
            return {
                'candidate_id': candidate_id,
                'total_interviews': 0,
                'average_score': 0,
                'highest_score': 0,
                'latest_interview': None
            }
        
        # Extract scores
        scores = []
        for interview in interviews:
            scoring = interview.get('scoring', {})
            final_score = scoring.get('final_score', 0)
            if final_score:
                scores.append(final_score)
        
        return {
            'candidate_id': candidate_id,
            'total_interviews': len(interviews),
            'average_score': sum(scores) / len(scores) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'latest_interview': interviews[0]['metadata']['date'] if interviews else None,
            'problems_attempted': len(set(
                i['interview_data'].get('problem', 'Unknown') 
                for i in interviews
            ))
        }
    
    def export_all_results(self, output_file: str = "all_interviews.json") -> str:
        """
        Export all interview results to a single JSON file
        
        Args:
            output_file: Output filename
        
        Returns:
            Path to exported file
        """
        all_data = {}
        
        for candidate_id in self.get_all_candidates():
            all_data[candidate_id] = self.load_candidate_interviews(candidate_id)
        
        output_path = self.base_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ All results exported to: {output_path}")
        return str(output_path)


# Example usage
if __name__ == "__main__":
    # Create storage instance
    storage = InterviewStorage()
    
    # Example: Save interview result
    sample_data = {
        'interview_id': 'INT_20250101_120000',
        'problem': 'Two Sum',
        'stages_completed': ['introduction', 'clarification', 'approach', 'coding', 'review'],
        'approach_quality': 85,
        'communication_score': 90,
        'hints_used': 1,
        'total_messages': 12,
        'duration_estimate': 24
    }
    
    sample_scoring = {
        'test_score': 45,  # out of 50
        'quality_score': 27,  # out of 30
        'approach_score': 8.5,  # out of 10
        'communication_score': 9,  # out of 10
        'hint_penalty': -5,
        'final_score': 84.5
    }
    
    # Save
    filepath = storage.save_interview_result(
        candidate_id="CAND_001",
        interview_data=sample_data,
        scoring_data=sample_scoring
    )
    print(f"Saved to: {filepath}")
    
    # Load latest
    latest = storage.load_latest_interview("CAND_001")
    print(f"\nLatest interview: {latest}")
    
    # Get summary
    summary = storage.get_candidate_summary("CAND_001")
    print(f"\nCandidate summary: {summary}")
