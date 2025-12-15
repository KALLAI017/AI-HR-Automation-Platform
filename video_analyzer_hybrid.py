"""
Hybrid Video Analyzer - Combines Heuristic Analysis with Groq AI
Uses visual/audio heuristics from video_analyzer.py + Groq Whisper/LLM for transcript analysis
"""

import os
from typing import Dict
from video_analyzer import analyze_candidate_video
from moviepy.editor import VideoFileClip
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()


class HybridVideoAnalyzer:
    """
    Combines heuristic video analysis with AI-powered transcript analysis
    - Visual/Audio: OpenCV + librosa heuristics (60% weight)
    - Communication: Groq Whisper transcription + LLM analysis (40% weight)
    """
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video to temporary WAV file"""
        try:
            video = VideoFileClip(video_path)
            audio_path = video_path.replace('.mp4', '_temp_audio.wav').replace('.avi', '_temp_audio.wav').replace('.mov', '_temp_audio.wav')
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            return audio_path
        except Exception as e:
            print(f"Audio extraction error: {e}")
            return None
    
    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Groq Whisper"""
        try:
            with open(audio_path, "rb") as file:
                transcription = self.groq_client.audio.transcriptions.create(
                    file=(audio_path, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            return transcription.text
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    def _analyze_transcript(self, transcript: str) -> Dict:
        """Analyze transcript with Groq LLM for communication assessment"""
        if not transcript or len(transcript.strip()) < 20:
            return {
                'communication_score': 0,
                'feedback': 'Transcript too short or empty for analysis'
            }
        
        prompt = f"""Analyze this job interview self-introduction transcript and provide:
1. Communication score (0-100) based on clarity, professionalism, structure, and articulation
2. Brief feedback (2-3 sentences) on strengths and areas for improvement

Transcript:
"{transcript}"

Respond in JSON format:
{{
  "communication_score": <score 0-100>,
  "feedback": "<brief feedback>"
}}"""

        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR interviewer analyzing communication skills. Be concise and constructive."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=300
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                # Remove markdown code blocks if present
                if response_text.startswith('```'):
                    response_text = response_text.split('```')[1]
                    if response_text.startswith('json'):
                        response_text = response_text[4:]
                
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError:
                # Fallback: extract score and feedback manually
                score = 50  # default
                feedback = response_text
                
                # Try to find score in text
                import re
                score_match = re.search(r'"communication_score":\s*(\d+)', response_text)
                if score_match:
                    score = int(score_match.group(1))
                
                return {
                    'communication_score': score,
                    'feedback': feedback[:200]
                }
                
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return {
                'communication_score': 0,
                'feedback': f'AI analysis failed: {str(e)}'
            }
    
    def analyze(self, video_path: str) -> Dict:
        """
        Perform hybrid analysis combining heuristics + AI
        Returns comprehensive results with both scores
        """
        try:
            # 1. Run heuristic analysis (visual + audio behavioral analysis)
            print("🔍 Running visual and audio analysis...")
            heuristic_results = analyze_candidate_video(video_path)
            # Handle both 'confidence_score' and 'overall_confidence_score' keys
            heuristic_score = heuristic_results.get('overall_confidence_score') or heuristic_results.get('confidence_score', 5.0)
            print(f"✅ Heuristic analysis complete (score: {heuristic_score:.1f}/10)")
            
            # 2. Extract and transcribe audio
            audio_path = self._extract_audio(video_path)
            transcript = ""
            ai_results = {'communication_score': 0, 'feedback': 'Transcription failed'}
            
            if audio_path:
                print("🎤 Transcribing audio with Whisper AI...")
                transcript = self._transcribe_audio(audio_path)
                
                # 3. Analyze transcript with AI
                if transcript:
                    print("🤖 Analyzing communication with LLM...")
                    ai_results = self._analyze_transcript(transcript)
                    print(f"✅ AI analysis complete (score: {ai_results['communication_score']}/100)")
                
                # Clean up temp audio
                try:
                    os.remove(audio_path)
                except:
                    pass
            
            # 4. Combine scores (60% heuristic + 40% AI communication)
            # Normalize AI score from 0-100 to 0-10
            ai_score_normalized = ai_results['communication_score'] / 10.0
            
            final_score = (heuristic_score * 0.6) + (ai_score_normalized * 0.4)
            print(f"🎯 Final score: {final_score:.1f}/10")
            
            # 5. Compile comprehensive results
            # Extract breakdown from visual and audio analysis
            visual_data = heuristic_results.get('visual_analysis', {})
            audio_data = heuristic_results.get('audio_analysis', {})
            
            breakdown = {
                'nervousness_score': visual_data.get('nervousness_indicators', 0),
                'eye_contact_score': visual_data.get('eye_contact_rate', 0),
                'smile_score': visual_data.get('smile_rate', 0),
                'fidgeting_score': 100 - visual_data.get('head_stability', 0),
                'blink_rate': 0,  # Not available in this version
                'avg_face_quality': visual_data.get('face_presence', 0),
                'audio_score': audio_data.get('confidence_score', 0),
                'pitch_variation': audio_data.get('pitch_variation', 0),
                'energy': audio_data.get('energy', 0),
                'speech_rate': audio_data.get('speech_rate', 0),
                'emotional_positivity': visual_data.get('emotional_positivity', 0),
                'head_stability': visual_data.get('head_stability', 0)
            }
            
            return {
                'status': 'success',
                'overall_confidence_score': final_score,
                'heuristic_score': heuristic_score,
                'ai_communication_score': ai_results['communication_score'],
                'ai_feedback': ai_results['feedback'],
                'transcript': transcript,
                'breakdown': breakdown,
                'video_path': video_path
            }
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'error',
                'error': str(e),
                'overall_confidence_score': 0
            }


def analyze_candidate_video_ai(video_path: str) -> Dict:
    """
    Convenience function for hybrid video analysis
    Combines heuristic behavioral analysis with AI transcript assessment
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dict with comprehensive analysis results
    """
    try:
        analyzer = HybridVideoAnalyzer()
        results = analyzer.analyze(video_path)
        return results
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'overall_confidence_score': 0
        }
