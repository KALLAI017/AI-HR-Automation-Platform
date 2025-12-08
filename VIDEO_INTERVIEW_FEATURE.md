# Video Interview Confidence Assessment Feature

## Overview

This feature adds an AI-powered video interview assessment step after candidates pass the technical assessment test. The system analyzes the candidate's self-introduction video to measure confidence levels and presentation skills using advanced computer vision and audio processing techniques.

## Feature Flow

1. **Candidate applies** for a position
2. **Resume screening** by LLM
3. **Technical assessment** test (if accepted)
4. **✨ NEW: Video Interview** (if test passed)
5. **Admin reviews** confidence score
6. **Final decision** and hiring

## Technology Stack

### Video Analysis
- **OpenCV (cv2)**: Computer vision for facial detection and analysis
- **FER (Facial Emotion Recognition)**: Deep learning-based emotion detection
- **Haar Cascades**: Face and eye detection

### Audio Analysis
- **librosa**: Audio feature extraction and analysis
- **moviepy**: Video to audio extraction
- **pydub**: Audio processing

### Metrics Analyzed

#### Visual Components (60% weight)
1. **Face Presence** (20%): Maintains camera visibility
2. **Emotional Positivity** (35%): Smile rate, happiness detection
3. **Eye Contact** (25%): Eye detection in upper face region
4. **Head Stability** (20%): Composure and minimal head movement

#### Audio Components (40% weight)
1. **Pitch Stability** (30%): Voice consistency
2. **Energy Consistency** (30%): Speaking energy levels
3. **Speaking Ratio** (20%): Time speaking vs. pauses
4. **Voice Clarity** (20%): Spectral quality of voice

## Confidence Score Interpretation

| Score Range | Interpretation | Meaning |
|-------------|----------------|---------|
| 8.5 - 10.0 | Highly Confident | Excellent presentation skills and composure |
| 7.0 - 8.4 | Confident | Good communication and comfortable demeanor |
| 5.5 - 6.9 | Moderately Confident | Acceptable with room for improvement |
| 4.0 - 5.4 | Somewhat Nervous | Shows signs of anxiety but manages |
| 0.0 - 3.9 | Needs Improvement | Significant nervousness detected |

## Files Modified/Created

### New Files
- **`video_analyzer.py`**: Core video analysis module with confidence assessment logic

### Modified Files
- **`requirements.txt`**: Added video/audio processing libraries
- **`hr_agent.py`**: Updated Candidate model with interview fields
- **`app.py`**: Added interview interface and admin dashboard updates

## Database Changes

### Candidate Model Updates
```python
@dataclass
class Candidate:
    # ... existing fields ...
    interview_video_path: Optional[str] = None  # Path to uploaded video
    confidence_score: Optional[float] = None    # Score 0-10
    interview_completed: bool = False           # Interview status
    status: str  # Added new statuses: "Interview_Pending", "Interview_Completed"
```

### New Database Methods
- `update_candidate_interview_status(candidate_id, video_path, confidence_score)`
- `mark_candidate_for_interview(candidate_id)`

## User Interfaces

### Candidate Portal - Interview Page
- Upload video interface (MP4, AVI, MOV, WebM)
- Video preview before submission
- Real-time analysis with progress indication
- Detailed feedback with:
  - Confidence score (0-10)
  - Interpretation message
  - Strengths identified
  - Areas for improvement
  - Detailed metrics (expandable)

### Admin Dashboard Enhancements
- **Dashboard**: Shows interview completion status
- **Manage Applications**: 
  - Displays confidence scores with visual gauge
  - Embedded video player for review
  - Hire/Reject buttons for interview-completed candidates
  - Status tracking through entire pipeline

## Usage Instructions

### For Candidates
1. Complete your job application
2. Pass the resume screening
3. Take and pass the technical assessment (60%+ required)
4. **Record a 1-3 minute self-introduction video**:
   - Introduce yourself and background
   - Describe relevant experience
   - Explain why you want to join the company
   - Highlight key skills and strengths
5. Upload your video and submit
6. View your confidence assessment
7. Wait for admin's final decision

### For Admins
1. Navigate to Admin Portal
2. View **Dashboard** or **Manage Applications**
3. Check candidates with "Interview_Completed" status
4. Review:
   - Confidence score (out of 10)
   - Interview video
   - Test scores
   - Application details
5. Make final hiring decision:
   - **Hire**: Converts to employee with credentials
   - **Reject**: Updates status and notifies candidate

## Installation

### Install Required Packages
```bash
pip install -r requirements.txt
```

### Required Dependencies
```
opencv-python==4.8.1.78
librosa==0.10.1
moviepy==1.0.3
transformers==4.36.2
torch==2.1.2
fer==22.5.1
pydub==0.25.1
```

## Directory Structure
```
HR_Agent/
├── app.py                      # Main Streamlit app (updated)
├── hr_agent.py                 # Core HR logic (updated)
├── video_analyzer.py           # NEW: Video analysis module
├── requirements.txt            # Updated dependencies
└── uploads/
    └── interview_videos/       # Stored candidate videos
```

## Technical Details

### Video Analysis Pipeline

1. **Video Upload**: Streamlit file uploader
2. **Audio Extraction**: moviepy separates audio track
3. **Frame Analysis**: 
   - Sample every 10th frame for efficiency
   - Detect faces using Haar Cascades
   - Analyze emotions with FER (MTCNN)
   - Track eye contact and head stability
4. **Audio Analysis**:
   - Extract pitch, energy, speech rate
   - Analyze speaking vs. silence ratio
   - Measure voice clarity
5. **Score Calculation**: Weighted combination of metrics
6. **Results Generation**: Detailed report with insights

### Performance Optimizations
- Frame sampling (every 10th frame) for faster processing
- Temporary file cleanup after analysis
- Progress indicators for user feedback
- Error handling with fallback scores

## Best Practices

### For Optimal Video Quality
- **Lighting**: Face should be well-lit
- **Background**: Plain, non-distracting
- **Camera**: Eye-level, stable position
- **Audio**: Clear, minimal background noise
- **Duration**: 1-3 minutes (comprehensive but concise)
- **Content**: Professional, enthusiastic, relevant

### For Admins
- Review both test scores AND confidence scores
- Watch the actual video for context
- Consider confidence score as one factor, not sole criteria
- Scores 6.5+ generally indicate good presentation skills
- Lower scores don't always mean reject - consider other factors

## Future Enhancements

Potential improvements for future versions:
- Real-time video recording within the app
- Multi-language support for speech analysis
- Body language analysis
- Automated question-answer format
- AI-generated interview questions
- Comparative analytics across candidates
- Video compression for storage optimization

## Troubleshooting

### Common Issues

**Issue**: Video analysis fails
- **Solution**: Check video format (MP4 recommended)
- Ensure video has both video and audio tracks
- Verify file size < 100MB

**Issue**: Low confidence score despite good presentation
- **Check**: Video quality (lighting, clarity)
- Ensure face is clearly visible
- Verify audio is clear

**Issue**: Import errors
- **Solution**: Run `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

## Security Considerations

- Videos stored locally in `uploads/interview_videos/`
- Unique filenames using candidate_id
- No external API calls for video processing
- All analysis done locally
- Consider adding file size limits
- Implement virus scanning for uploads
- Add video retention policies

## Conclusion

This feature provides an objective, AI-powered assessment of candidate confidence and presentation skills, helping admins make better hiring decisions. The system uses state-of-the-art computer vision and audio processing to analyze multiple confidence indicators, providing both quantitative scores and qualitative insights.
