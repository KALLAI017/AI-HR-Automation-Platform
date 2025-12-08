# 🎥 Video Interview Confidence Assessment

## Overview

An AI-powered video interview assessment system that analyzes candidate confidence levels after they pass the technical assessment test. The system uses advanced computer vision and audio processing to evaluate presentation skills and confidence.

## 🌟 Key Features

- **Multi-Modal Analysis**: Combines facial expression, eye contact, voice stability, and speech patterns
- **Real-time Processing**: Instant video analysis with detailed feedback
- **Confidence Scoring**: 0-10 scale with interpretation
- **Admin Dashboard**: Review videos and scores before making hiring decisions
- **Open Source Models**: Uses FER, OpenCV, librosa (no paid API calls)
- **Comprehensive Feedback**: Strengths and areas for improvement

## 🚀 Quick Start

### 1. Installation

```powershell
# Run the installation script
.\install_video_feature.ps1

# OR manually:
pip install -r requirements.txt
mkdir uploads\interview_videos
```

### 2. Run the Application

```powershell
streamlit run app.py
```

### 3. Test the Feature

**As Candidate:**
1. Apply for a job
2. Pass the technical test (60%+)
3. Upload a 1-3 minute self-introduction video
4. View your confidence score

**As Admin:**
1. Login (admin/admin123)
2. Navigate to Dashboard or Manage Applications
3. Review candidates with "Interview_Completed" status
4. Watch videos and see confidence scores
5. Hire or reject

## 📊 What Gets Analyzed

### Visual Metrics (60%)
- ✅ Face presence and visibility
- ✅ Emotional positivity (smiling, happiness)
- ✅ Eye contact estimation
- ✅ Head stability and composure

### Audio Metrics (40%)
- ✅ Voice pitch stability
- ✅ Speaking energy consistency
- ✅ Speech rate and pauses
- ✅ Voice clarity

## 📈 Confidence Score Interpretation

| Score | Interpretation |
|-------|----------------|
| 8.5-10.0 | Highly Confident - Excellent presentation skills |
| 7.0-8.4 | Confident - Good communication |
| 5.5-6.9 | Moderately Confident - Acceptable |
| 4.0-5.4 | Somewhat Nervous - Shows anxiety |
| 0.0-3.9 | Needs Improvement - Significant nervousness |

## 💡 Tips for Candidates

### Do's ✅
- Look directly at the camera (simulates eye contact)
- Smile naturally and show enthusiasm
- Speak clearly and at a steady pace
- Maintain good posture
- Use good lighting on your face
- Keep head relatively stable
- Practice your introduction beforehand

### Don'ts ❌
- Don't look away from camera frequently
- Avoid excessive head movement
- Don't speak too fast or too slow
- Avoid long awkward pauses
- Don't record in poor lighting
- Avoid distracting backgrounds
- Don't mumble or speak too softly

## 🛠️ Technical Stack

- **Computer Vision**: OpenCV, Haar Cascades
- **Emotion Detection**: FER (Facial Emotion Recognition)
- **Audio Processing**: librosa, pydub
- **Video Processing**: moviepy
- **Web Framework**: Streamlit
- **Machine Learning**: PyTorch (for FER)

## 📁 File Structure

```
HR_Agent/
├── app.py                          # Main application (enhanced)
├── hr_agent.py                     # Core logic (enhanced)
├── video_analyzer.py               # NEW: Video analysis engine
├── requirements.txt                # Updated dependencies
├── install_video_feature.ps1       # Installation script
├── VIDEO_INTERVIEW_FEATURE.md      # Detailed documentation
├── VIDEO_INTERVIEW_QUICKSTART.md   # Quick start guide
├── IMPLEMENTATION_COMPLETE.md      # Implementation summary
└── uploads/
    └── interview_videos/           # Stored videos
```

## 🔧 How It Works

```
1. Candidate uploads video
   ↓
2. Extract audio from video (moviepy)
   ↓
3. Analyze frames (OpenCV + FER)
   - Detect faces
   - Recognize emotions
   - Track eye contact
   - Measure head stability
   ↓
4. Analyze audio (librosa)
   - Pitch stability
   - Energy consistency
   - Speech rate
   - Voice clarity
   ↓
5. Calculate confidence score
   - Visual: 60% weight
   - Audio: 40% weight
   ↓
6. Generate detailed report
   - Score + interpretation
   - Strengths
   - Improvements
   ↓
7. Admin reviews and decides
```

## 📋 Workflow Integration

```
Job Application
    ↓
Resume Screening (AI)
    ↓
Technical Test (60% to pass)
    ↓
🎥 VIDEO INTERVIEW (NEW!)
    ↓
Admin Review
    ↓
Hire/Reject Decision
```

## 🎯 Use Cases

1. **Remote Hiring**: Assess candidates without in-person interviews
2. **Preliminary Screening**: Filter candidates before final interviews
3. **Skill Assessment**: Evaluate presentation and communication skills
4. **Fair Evaluation**: Objective, AI-based confidence metrics
5. **Efficiency**: Automated analysis saves time

## ⚙️ Configuration

The system uses pre-configured weights for scoring:
- Face Presence: 20% of visual score
- Emotional Positivity: 35% of visual score
- Eye Contact: 25% of visual score
- Head Stability: 20% of visual score

You can adjust these in `video_analyzer.py` if needed.

## 🔐 Privacy & Security

- Videos stored locally (not uploaded to cloud)
- Unique filenames prevent conflicts
- Temporary files cleaned after analysis
- No external API calls for video processing
- All analysis done on your server

## 📚 Documentation

- **VIDEO_INTERVIEW_FEATURE.md**: Complete technical documentation
- **VIDEO_INTERVIEW_QUICKSTART.md**: Quick start and testing guide
- **IMPLEMENTATION_COMPLETE.md**: Implementation details

## 🐛 Troubleshooting

### Video Analysis Fails
- Check video format (MP4 recommended)
- Ensure video has both video and audio
- Verify face is clearly visible
- Check file size (< 100MB recommended)

### Import Errors
```powershell
pip install --upgrade -r requirements.txt
```

### Low Confidence Score
- Improve lighting on face
- Look directly at camera
- Reduce background noise
- Keep head stable
- Smile and show enthusiasm

## 🚀 Future Enhancements

- [ ] In-app video recording
- [ ] Multi-language support
- [ ] Body language analysis
- [ ] Automated interview questions
- [ ] Real-time feedback during recording
- [ ] Comparative analytics
- [ ] Video compression

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review error messages in terminal
3. Verify dependencies are installed
4. Check video format and quality

## 📄 License

This feature is part of the HR Agent system and follows the same license.

## 🙏 Acknowledgments

Built using:
- OpenCV for computer vision
- FER for emotion recognition
- librosa for audio analysis
- Streamlit for the web interface

---

**Status**: ✅ Production Ready
**Version**: 1.0
**Last Updated**: December 2025

Enjoy automating your interview process with AI! 🎉
