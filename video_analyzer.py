"""
Video Confidence Analyzer - UPGRADED with DeepFace + SpeechBrain
Analyzes candidate's self-introduction video to measure confidence level
Uses state-of-the-art deep learning models for emotion recognition
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

# Deep learning models for emotion recognition
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️ DeepFace not available - using fallback emotion detection")

try:
    # Suppress torchaudio backend warnings
    import os
    os.environ.setdefault('TORCHAUDIO_USE_BACKEND', 'soundfile')
    
    import torchaudio
    from speechbrain.pretrained import EncoderClassifier
    SPEECHBRAIN_AVAILABLE = True
except (ImportError, AttributeError) as e:
    SPEECHBRAIN_AVAILABLE = False
    print(f"⚠️ SpeechBrain not available - using fallback audio analysis: {e}")


class VideoConfidenceAnalyzer:
    """
    Analyzes video to assess candidate confidence through multiple signals:
    1. Facial Expression Analysis (DeepFace emotion recognition)
    2. Voice Emotion Recognition (SpeechBrain SER model)
    3. Behavioral Patterns (eye contact estimation, head movement)
    """
    
    def __init__(self):
        # Load OpenCV cascades for face/eye detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Load SpeechBrain emotion recognition model (lazy loading)
        self.emotion_classifier = None
        if SPEECHBRAIN_AVAILABLE:
            try:
                print("📦 Loading SpeechBrain emotion recognition model...")
                self.emotion_classifier = EncoderClassifier.from_hparams(
                    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
                    savedir="pretrained_models/emotion_recognition"
                )
                print("✅ SpeechBrain model loaded successfully")
            except Exception as e:
                print(f"⚠️ Could not load SpeechBrain model: {e}")
                self.emotion_classifier = None
        
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
        """Analyze visual components using DeepFace for emotion + behavioral patterns"""
        cap = cv2.VideoCapture(video_path)
        
        frame_count = 0
        analyzed_frames = 0
        face_detected_frames = 0
        stable_head_frames = 0
        
        prev_face_center = None
        eye_contact_frames = 0
        
        # Emotion scores from DeepFace
        emotion_data = {
            'happy': [],
            'neutral': [],
            'sad': [],
            'angry': [],
            'fear': [],
            'surprise': [],
            'disgust': []
        }
        
        # Sample every 15th frame for efficiency (DeepFace is slower)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Analyze every 15th frame to save processing time
            if frame_count % 15 != 0:
                continue
            
            analyzed_frames += 1
            
            # Convert to RGB for DeepFace
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            try:
                # Use DeepFace for emotion analysis
                if DEEPFACE_AVAILABLE:
                    analysis = DeepFace.analyze(
                        frame_rgb, 
                        actions=['emotion'],
                        enforce_detection=False,
                        detector_backend='opencv'
                    )
                    
                    # Handle both single face and multiple faces
                    if isinstance(analysis, list):
                        analysis = analysis[0]
                    
                    if 'emotion' in analysis:
                        emotions = analysis['emotion']
                        for emotion, score in emotions.items():
                            if emotion in emotion_data:
                                emotion_data[emotion].append(score)
                        face_detected_frames += 1
                    
                    # Get face region for eye detection
                    if 'region' in analysis:
                        region = analysis['region']
                        x, y, w, h = region['x'], region['y'], region['w'], region['h']
                        
                        # Check eye contact (if eyes are detected in upper half of face)
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        eyes = self.eye_cascade.detectMultiScale(
                            gray[y:y+h//2, x:x+w], 1.1, 3
                        )
                        if len(eyes) >= 2:
                            eye_contact_frames += 1
                        
                        # Track head stability
                        current_center = (x + w//2, y + h//2)
                        if prev_face_center is not None:
                            movement = np.sqrt((current_center[0] - prev_face_center[0])**2 + 
                                             (current_center[1] - prev_face_center[1])**2)
                            if movement < 25:  # Threshold for stable head
                                stable_head_frames += 1
                        prev_face_center = current_center
                
                else:
                    # Fallback to simple face detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                    if len(faces) > 0:
                        face_detected_frames += 1
                        x, y, w, h = faces[0]
                        eyes = self.eye_cascade.detectMultiScale(gray[y:y+h//2, x:x+w], 1.1, 3)
                        if len(eyes) >= 2:
                            eye_contact_frames += 1
                        
                        current_center = (x + w//2, y + h//2)
                        if prev_face_center is not None:
                            movement = np.sqrt((current_center[0] - prev_face_center[0])**2 + 
                                             (current_center[1] - prev_face_center[1])**2)
                            if movement < 25:
                                stable_head_frames += 1
                        prev_face_center = current_center
                        
            except Exception as e:
                # Skip frames with detection errors
                pass
        
        cap.release()
        
        # Calculate metrics
        if analyzed_frames == 0:
            return {
                'error': 'No frames could be analyzed',
                'face_presence': 0,
                'emotional_positivity': 0,
                'smile_rate': 0,
                'eye_contact_rate': 0,
                'head_stability': 0,
                'nervousness_indicators': 50
            }
        
        # Calculate emotion-based metrics
        avg_happy = np.mean(emotion_data['happy']) if emotion_data['happy'] else 0
        avg_neutral = np.mean(emotion_data['neutral']) if emotion_data['neutral'] else 0
        avg_sad = np.mean(emotion_data['sad']) if emotion_data['sad'] else 0
        avg_fear = np.mean(emotion_data['fear']) if emotion_data['fear'] else 0
        avg_angry = np.mean(emotion_data['angry']) if emotion_data['angry'] else 0
        
        # Emotional positivity: happy emotions indicate confidence
        emotional_positivity = avg_happy + (avg_neutral * 0.3)
        
        # Nervousness indicators: fear, sad, angry
        nervousness_indicators = avg_fear + avg_sad + avg_angry
        
        return {
            'face_presence': (face_detected_frames / analyzed_frames) * 100,
            'emotional_positivity': emotional_positivity,
            'smile_rate': avg_happy,  # Happy emotion as proxy for smile
            'eye_contact_rate': (eye_contact_frames / max(1, analyzed_frames)) * 100,
            'head_stability': (stable_head_frames / max(1, analyzed_frames - 1)) * 100,
            'nervousness_indicators': nervousness_indicators,
            'total_frames_analyzed': analyzed_frames,
            'emotion_breakdown': {
                'happy': avg_happy,
                'neutral': avg_neutral,
                'sad': avg_sad,
                'fear': avg_fear,
                'angry': avg_angry
            }
        }
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
        """Analyze audio using SpeechBrain emotion recognition + librosa features"""
        try:
            # SpeechBrain emotion recognition
            voice_emotion_score = 50  # Default neutral
            emotion_label = "neutral"
            
            if SPEECHBRAIN_AVAILABLE and self.emotion_classifier is not None:
                try:
                    # Load audio for SpeechBrain
                    signal, sr = torchaudio.load(audio_path)
                    
                    # SpeechBrain expects 16kHz
                    if sr != 16000:
                        resampler = torchaudio.transforms.Resample(sr, 16000)
                        signal = resampler(signal)
                    
                    # Get emotion prediction
                    prediction = self.emotion_classifier.classify_batch(signal)
                    
                    # Extract emotion (IEMOCAP labels: neutral, happy, sad, angry, fear)
                    emotion_label = prediction[1][0]  # Get predicted label
                    
                    # Map emotion to confidence score
                    emotion_confidence_map = {
                        'hap': 85,  # Happy = high confidence
                        'neu': 60,  # Neutral = moderate confidence
                        'sad': 30,  # Sad = low confidence
                        'ang': 25,  # Angry = low confidence (defensive)
                        'fea': 15,  # Fear = very low confidence
                    }
                    voice_emotion_score = emotion_confidence_map.get(emotion_label[:3], 50)
                    
                except Exception as e:
                    print(f"SpeechBrain emotion detection failed: {e}")
            
            # Librosa acoustic features (unchanged - still useful)
            y, sr = librosa.load(audio_path, sr=None)
            
            # 1. Pitch stability
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            pitch_stability = 100 - (np.std(zcr) * 1000)
            pitch_stability = max(0, min(100, pitch_stability))
            
            # 2. Speech energy
            rms = librosa.feature.rms(y=y)[0]
            energy_consistency = 100 - (np.std(rms) / (np.mean(rms) + 0.001) * 50)
            energy_consistency = max(0, min(100, energy_consistency))
            
            # 3. Speech rate
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
            speech_rate = len(onsets) / (len(y) / sr) * 60
            
            # 4. Speaking ratio
            intervals = librosa.effects.split(y, top_db=30)
            if len(intervals) > 0:
                speaking_time = sum([interval[1] - interval[0] for interval in intervals]) / sr
                speaking_ratio = (speaking_time / (len(y) / sr)) * 100
            else:
                speaking_ratio = 0
            
            # 5. Voice clarity
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            voice_clarity = min(100, (np.mean(spectral_centroids) / 3000) * 100)
            
            return {
                'pitch_stability': round(pitch_stability, 2),
                'energy_consistency': round(energy_consistency, 2),
                'speech_rate': round(speech_rate, 2),
                'speaking_ratio': round(speaking_ratio, 2),
                'voice_clarity': round(voice_clarity, 2),
                'voice_emotion_score': round(voice_emotion_score, 2),
                'detected_emotion': emotion_label,
                'duration_seconds': round(len(y) / sr, 2),
                'speechbrain_used': SPEECHBRAIN_AVAILABLE and self.emotion_classifier is not None
            }
            
        except Exception as e:
            print(f"Error in audio analysis: {str(e)}")
            return {
                'error': str(e),
                'pitch_stability': 50,
                'energy_consistency': 50,
                'speech_rate': 100,
                'speaking_ratio': 80,
                'voice_emotion_score': 50,
                'detected_emotion': 'unknown'
            }
    
    def _average_emotions(self, emotion_scores: list) -> Dict:
        """Average emotion scores across all frames"""
    
    def _calculate_confidence_score(self, visual: Dict, audio: Dict) -> float:
        """
        Calculate overall confidence score (0-10) based on weighted factors
        
        Confidence indicators:
        - High: Good eye contact, happy emotions, stable head, clear voice, positive voice emotion
        - Low: Avoiding eye contact, nervous/sad/fearful expressions, shaky head, unstable pitch
        """
        
        # Visual factors (60% weight) - Now using DeepFace emotions
        visual_score = 0
        if 'error' not in visual:
            # Face presence (must be visible)
            face_weight = min(10, visual.get('face_presence', 0) / 10)
            
            # Emotional positivity from DeepFace (happy emotions = confidence)
            emotion_score = (
                visual.get('emotional_positivity', 0) / 10 -
                visual.get('nervousness_indicators', 0) / 50  # Penalize nervousness
            )
            emotion_score = max(0, min(10, emotion_score))
            
            # Eye contact
            eye_score = visual.get('eye_contact_rate', 0) / 10
            
            # Head stability
            stability_score = visual.get('head_stability', 0) / 10
            
            visual_score = (face_weight * 0.15 + emotion_score * 0.45 + 
                          eye_score * 0.25 + stability_score * 0.15) * 0.6
        else:
            visual_score = 3  # Default moderate score if analysis fails
        
        # Audio factors (40% weight) - Now includes SpeechBrain emotion
        audio_score = 0
        if audio and 'error' not in audio:
            # If SpeechBrain was used, weight voice emotion heavily
            if audio.get('speechbrain_used', False):
                voice_emotion = audio.get('voice_emotion_score', 50) / 10
                pitch_score = audio.get('pitch_stability', 50) / 10
                energy_score = audio.get('energy_consistency', 50) / 10
                speaking_score = audio.get('speaking_ratio', 80) / 10
                
                audio_score = (voice_emotion * 0.5 + pitch_score * 0.2 + 
                              energy_score * 0.2 + speaking_score * 0.1) * 0.4
            else:
                # Fallback to acoustic features only
                pitch_score = audio.get('pitch_stability', 50) / 10
                energy_score = audio.get('energy_consistency', 50) / 10
                speaking_score = audio.get('speaking_ratio', 80) / 10
                clarity_score = audio.get('voice_clarity', 50) / 10
                
                audio_score = (pitch_score * 0.3 + energy_score * 0.3 + 
                              speaking_score * 0.2 + clarity_score * 0.2) * 0.4
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
