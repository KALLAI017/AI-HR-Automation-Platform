"""
Video Confidence Analyzer
Analyzes candidate's self-introduction video to measure confidence level
Uses facial expression analysis, voice analysis, and behavioral patterns
"""

import cv2
import numpy as np
import librosa
import tempfile
import os
from typing import Dict, Tuple
from moviepy.editor import VideoFileClip
import warnings
warnings.filterwarnings('ignore')


class VideoConfidenceAnalyzer:
    """
    Analyzes video to assess candidate confidence through multiple signals:
    1. Facial Expression Analysis (smile detection using OpenCV)
    2. Voice Analysis (pitch stability, speech rate, pauses)
    3. Behavioral Patterns (eye contact estimation, head movement)
    """
    
    def __init__(self):
        # Load OpenCV pre-trained smile detector
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
    def analyze_video(self, video_path: str) -> Dict:
        """
        Main method to analyze video and return confidence score
        
        Args:
            video_path: Path to the uploaded video file
            
        Returns:
            Dict with confidence_score (0-10) and detailed analysis
        """
        try:
            # Extract audio from video
            audio_path = self._extract_audio(video_path)
            
            # Analyze visual components
            visual_analysis = self._analyze_visual(video_path)
            
            # Analyze audio components
            audio_analysis = self._analyze_audio(audio_path) if audio_path else {}
            
            # Calculate overall confidence score
            confidence_score = self._calculate_confidence_score(visual_analysis, audio_analysis)
            
            # Clean up temporary audio file
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
            
            return {
                'confidence_score': round(confidence_score, 2),
                'visual_analysis': visual_analysis,
                'audio_analysis': audio_analysis,
                'interpretation': self._interpret_score(confidence_score),
                'strengths': self._identify_strengths(visual_analysis, audio_analysis),
                'areas_for_improvement': self._identify_improvements(visual_analysis, audio_analysis)
            }
            
        except Exception as e:
            print(f"Error analyzing video: {str(e)}")
            return {
                'confidence_score': 5.0,
                'error': str(e),
                'interpretation': 'Unable to fully analyze video'
            }
    
    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video file"""
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                return None
            
            # Save to temporary file
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
            video.close()
            
            return temp_audio.name
        except Exception as e:
            print(f"Error extracting audio: {str(e)}")
            return None
    
    def _analyze_visual(self, video_path: str) -> Dict:
        """Analyze visual components: facial expressions, eye contact, posture"""
        cap = cv2.VideoCapture(video_path)
        
        frame_count = 0
        analyzed_frames = 0
        smile_frames = 0
        face_detected_frames = 0
        stable_head_frames = 0
        
        # Face cascade for basic face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        prev_face_center = None
        eye_contact_frames = 0
        brightness_scores = []
        
        # Sample every 10th frame for efficiency
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Analyze every 10th frame to save processing time
            if frame_count % 10 != 0:
                continue
            
            analyzed_frames += 1
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                face_detected_frames += 1
                x, y, w, h = faces[0]
                face_roi_gray = gray[y:y+h, x:x+w]
                
                # Simple smile detection using cascade
                smiles = self.smile_cascade.detectMultiScale(face_roi_gray, 1.8, 20)
                if len(smiles) > 0:
                    smile_frames += 1
                
                # Measure face brightness (proxy for positive expression)
                avg_brightness = np.mean(face_roi_gray)
                brightness_scores.append(avg_brightness)
                
                # Check eye contact (if eyes are detected in upper half of face)
                eyes = eye_cascade.detectMultiScale(gray[y:y+h//2, x:x+w], 1.1, 3)
                if len(eyes) >= 2:
                    eye_contact_frames += 1
                
                # Track head stability
                current_center = (x + w//2, y + h//2)
                if prev_face_center is not None:
                    movement = np.sqrt((current_center[0] - prev_face_center[0])**2 + 
                                     (current_center[1] - prev_face_center[1])**2)
                    if movement < 20:  # Threshold for stable head
                        stable_head_frames += 1
                prev_face_center = current_center
        
        cap.release()
        
        # Calculate metrics
        if analyzed_frames == 0:
            return {
                'error': 'No frames could be analyzed',
                'face_presence': 0,
                'emotional_positivity': 0,
                'smile_rate': 0,
                'eye_contact_rate': 0,
                'head_stability': 0
            }
        
        # Calculate emotional positivity from brightness and smile rate
        avg_brightness = np.mean(brightness_scores) if brightness_scores else 100
        # Normalize brightness (typical range 50-150)
        brightness_normalized = min(100, max(0, (avg_brightness - 50) / 100 * 100))
        
        smile_rate_pct = (smile_frames / analyzed_frames) * 100
        emotional_positivity = (smile_rate_pct * 0.7 + brightness_normalized * 0.3)
        
        return {
            'face_presence': (face_detected_frames / analyzed_frames) * 100,
            'emotional_positivity': emotional_positivity,
            'smile_rate': smile_rate_pct,
            'eye_contact_rate': (eye_contact_frames / analyzed_frames) * 100,
            'head_stability': (stable_head_frames / max(1, analyzed_frames - 1)) * 100,
            'nervousness_indicators': max(0, 100 - emotional_positivity),  # Inverse of positivity
            'total_frames_analyzed': analyzed_frames
        }
    
    def _analyze_audio(self, audio_path: str) -> Dict:
        """Analyze audio components: pitch stability, speech rate, energy"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=None)
            
            # Extract features
            
            # 1. Pitch stability (using zero crossing rate as proxy)
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            pitch_stability = 100 - (np.std(zcr) * 1000)  # Lower std = more stable
            pitch_stability = max(0, min(100, pitch_stability))
            
            # 2. Speech energy
            rms = librosa.feature.rms(y=y)[0]
            avg_energy = np.mean(rms)
            energy_consistency = 100 - (np.std(rms) / (np.mean(rms) + 0.001) * 50)
            energy_consistency = max(0, min(100, energy_consistency))
            
            # 3. Speech rate (onset detection)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
            speech_rate = len(onsets) / (len(y) / sr) * 60  # onsets per minute
            
            # 4. Silence/pause analysis
            intervals = librosa.effects.split(y, top_db=30)
            if len(intervals) > 0:
                speaking_time = sum([interval[1] - interval[0] for interval in intervals]) / sr
                total_time = len(y) / sr
                speaking_ratio = (speaking_time / total_time) * 100
            else:
                speaking_ratio = 0
            
            # 5. Voice clarity (spectral centroid)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            voice_clarity = min(100, (np.mean(spectral_centroids) / 3000) * 100)
            
            return {
                'pitch_stability': round(pitch_stability, 2),
                'energy_consistency': round(energy_consistency, 2),
                'speech_rate': round(speech_rate, 2),
                'speaking_ratio': round(speaking_ratio, 2),
                'voice_clarity': round(voice_clarity, 2),
                'duration_seconds': round(len(y) / sr, 2)
            }
            
        except Exception as e:
            print(f"Error in audio analysis: {str(e)}")
            return {
                'error': str(e),
                'pitch_stability': 50,
                'energy_consistency': 50,
                'speech_rate': 100,
                'speaking_ratio': 80
            }
    
    def _average_emotions(self, emotion_scores: list) -> Dict:
        """Average emotion scores across all frames"""
    
    def _calculate_confidence_score(self, visual: Dict, audio: Dict) -> float:
        """
        Calculate overall confidence score (0-10) based on weighted factors
        
        Confidence indicators:
        - High: Good eye contact, smiling, stable head, clear voice, consistent energy
        - Low: Avoiding eye contact, nervous expressions, shaky head, unstable pitch
        """
        
        # Visual factors (60% weight)
        visual_score = 0
        if 'error' not in visual:
            # Face presence (must be visible)
            face_weight = min(10, visual.get('face_presence', 0) / 10)
            
            # Emotional positivity (smiling, happy)
            emotion_score = (
                visual.get('emotional_positivity', 0) * 0.4 +
                visual.get('smile_rate', 0) * 0.3 -
                visual.get('nervousness_indicators', 0) * 0.3
            ) / 10
            
            # Eye contact
            eye_score = visual.get('eye_contact_rate', 0) / 10
            
            # Head stability
            stability_score = visual.get('head_stability', 0) / 10
            
            visual_score = (face_weight * 0.2 + emotion_score * 0.35 + 
                          eye_score * 0.25 + stability_score * 0.2) * 6
        else:
            visual_score = 3  # Default moderate score if analysis fails
        
        # Audio factors (40% weight)
        audio_score = 0
        if audio and 'error' not in audio:
            pitch_score = audio.get('pitch_stability', 50) / 10
            energy_score = audio.get('energy_consistency', 50) / 10
            speaking_score = audio.get('speaking_ratio', 80) / 10
            clarity_score = audio.get('voice_clarity', 50) / 10
            
            audio_score = (pitch_score * 0.3 + energy_score * 0.3 + 
                          speaking_score * 0.2 + clarity_score * 0.2) * 4
        else:
            audio_score = 2  # Default moderate score if analysis fails
        
        total_score = visual_score + audio_score
        return max(0, min(10, total_score))
    
    def _interpret_score(self, score: float) -> str:
        """Interpret the confidence score"""
        if score >= 8.5:
            return "Highly Confident - Excellent presentation skills and composure"
        elif score >= 7.0:
            return "Confident - Good communication and comfortable demeanor"
        elif score >= 5.5:
            return "Moderately Confident - Acceptable with room for improvement"
        elif score >= 4.0:
            return "Somewhat Nervous - Shows signs of anxiety but manages"
        else:
            return "Needs Improvement - Significant nervousness detected"
    
    def _identify_strengths(self, visual: Dict, audio: Dict) -> list:
        """Identify candidate's strengths"""
        strengths = []
        
        if 'error' not in visual:
            if visual.get('face_presence', 0) > 80:
                strengths.append("Maintains good camera presence")
            if visual.get('smile_rate', 0) > 40:
                strengths.append("Warm and friendly demeanor")
            if visual.get('eye_contact_rate', 0) > 50:
                strengths.append("Good eye contact")
            if visual.get('head_stability', 0) > 70:
                strengths.append("Composed body language")
        
        if audio and 'error' not in audio:
            if audio.get('pitch_stability', 0) > 70:
                strengths.append("Stable and clear voice")
            if audio.get('energy_consistency', 0) > 70:
                strengths.append("Consistent speaking energy")
            if audio.get('speaking_ratio', 0) > 75:
                strengths.append("Good speaking pace")
        
        if not strengths:
            strengths.append("Completed the interview process")
        
        return strengths
    
    def _identify_improvements(self, visual: Dict, audio: Dict) -> list:
        """Identify areas for improvement"""
        improvements = []
        
        if 'error' not in visual:
            if visual.get('eye_contact_rate', 0) < 30:
                improvements.append("Work on maintaining eye contact")
            if visual.get('smile_rate', 0) < 20:
                improvements.append("Consider showing more positive expressions")
            if visual.get('nervousness_indicators', 0) > 30:
                improvements.append("Practice to reduce nervousness")
        
        if audio and 'error' not in audio:
            if audio.get('pitch_stability', 0) < 50:
                improvements.append("Work on voice stability")
            if audio.get('speaking_ratio', 0) < 60:
                improvements.append("Increase speaking time and reduce long pauses")
        
        if not improvements:
            improvements.append("Continue building confidence through practice")
        
        return improvements


# Utility function for streamlit integration
def analyze_candidate_video(video_file_path: str) -> Dict:
    """
    Convenience function to analyze a candidate's video
    
    Args:
        video_file_path: Path to the video file
        
    Returns:
        Analysis results dictionary
    """
    analyzer = VideoConfidenceAnalyzer()
    return analyzer.analyze_video(video_file_path)
