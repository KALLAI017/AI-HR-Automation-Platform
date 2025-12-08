# Quick Start Guide - Video Interview Feature

## Installation

1. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

2. **Create Upload Directory**
```powershell
mkdir uploads\interview_videos
```

3. **Run the Application**
```powershell
streamlit run app.py
```

## Testing the Feature

### As a Candidate

1. **Login to Candidate Portal**
   - Click "Apply for Jobs"
   
2. **Apply for a Position**
   - Upload resume
   - Fill application form
   - Submit

3. **Take Technical Test** (if resume accepted)
   - Answer all questions
   - Submit test
   - Need 60%+ to pass

4. **Record Video Interview** (NEW!)
   - You'll be automatically redirected after passing test
   - Record a 1-3 minute self-introduction video
   - Include:
     - Your background
     - Relevant experience
     - Why you want to join
     - Key skills
   - Upload the video (MP4, AVI, MOV, WebM)
   - Submit for analysis

5. **View Results**
   - See your confidence score (0-10)
   - Get strengths and improvement areas
   - Wait for admin decision

### As an Admin

1. **Login to Admin Portal**
   - Username: `admin`
   - Password: `admin123`

2. **View Candidates**
   - Go to "Dashboard" or "Manage Applications"
   - Look for candidates with status: "Interview_Completed"

3. **Review Interview**
   - See confidence score displayed prominently
   - Watch the interview video
   - Review test scores and resume

4. **Make Decision**
   - Click "✅ Hire" to convert to employee
   - Click "❌ Reject" to reject candidate
   - Hired candidates get email with employee credentials

## Example Test Video

For testing, record a short video where you:
- Face the camera clearly
- Speak for 1-2 minutes
- Introduce yourself professionally
- Maintain good eye contact (look at camera)
- Smile and show enthusiasm

### Tips for High Confidence Score:
- ✅ Good lighting on your face
- ✅ Look directly at camera
- ✅ Smile naturally
- ✅ Speak clearly and steadily
- ✅ Minimize head movement
- ✅ Professional background
- ✅ Clear audio

### What Lowers Score:
- ❌ Looking away frequently
- ❌ Shaky/unstable video
- ❌ Poor lighting
- ❌ Nervous expressions
- ❌ Long pauses
- ❌ Unclear audio

## Understanding Confidence Scores

- **9-10**: Exceptional - Very confident presenter
- **7-8**: Good - Confident and professional
- **5-6**: Average - Acceptable performance
- **3-4**: Below Average - Shows nervousness
- **0-2**: Poor - Needs significant improvement

## Workflow Diagram

```
Candidate Journey:
┌──────────────┐
│ Apply for Job│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Resume Review │ (AI-powered)
└──────┬───────┘
       │ (Accepted)
       ▼
┌──────────────┐
│Technical Test│
└──────┬───────┘
       │ (Passed 60%+)
       ▼
┌──────────────┐
│ Video Interview│ ← NEW STEP
└──────┬───────┘
       │ (Submitted)
       ▼
┌──────────────┐
│Admin Review  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Hire/Reject  │
└──────────────┘
```

## API Reference

### VideoConfidenceAnalyzer

```python
from video_analyzer import analyze_candidate_video

# Analyze a video file
result = analyze_candidate_video("path/to/video.mp4")

# Result structure:
{
    'confidence_score': 7.5,  # 0-10
    'interpretation': 'Confident - Good communication...',
    'strengths': ['Good eye contact', 'Clear voice', ...],
    'areas_for_improvement': ['Work on...', ...],
    'visual_analysis': {
        'face_presence': 95.0,
        'emotional_positivity': 65.0,
        'smile_rate': 45.0,
        'eye_contact_rate': 70.0,
        'head_stability': 80.0
    },
    'audio_analysis': {
        'pitch_stability': 75.0,
        'energy_consistency': 70.0,
        'speech_rate': 120.0,
        'speaking_ratio': 85.0
    }
}
```

## Troubleshooting

### Video upload fails
```powershell
# Ensure directory exists
mkdir uploads\interview_videos
```

### Import errors
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Analysis takes too long
- Use shorter videos (1-2 minutes)
- Ensure video quality is not too high (720p recommended)
- Check system resources

### Low score despite good video
- Ensure good lighting
- Face camera directly
- Minimize background noise
- Keep head relatively still

## Support

For issues or questions:
1. Check VIDEO_INTERVIEW_FEATURE.md for detailed documentation
2. Review error messages in terminal
3. Verify all dependencies are installed
4. Check video format and quality

## Demo Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

**Sample Employee Login:**
- Username: `john.doe`
- Password: `password123`

Enjoy the new video interview feature! 🎥✨
