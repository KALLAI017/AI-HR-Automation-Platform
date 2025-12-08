# Getting Test Videos for Accuracy Testing

## Current System Status ✅
- **DeepFace**: ✅ Working (7-emotion facial recognition)
- **SpeechBrain**: ⚠️ Fallback mode (using librosa acoustic features)
- **Overall**: Ready to test with hybrid approach

---

## Option 1: Download from YouTube (Recommended)

### Install yt-dlp:
```powershell
python -m pip install yt-dlp
```

### Download Sample Videos:

**Confident Interview Example:**
```powershell
yt-dlp -f "best[height<=720]" -o "uploads/interview_videos/candidate_confident.%(ext)s" "https://www.youtube.com/watch?v=naIkpQ_cIt0"
```
*(Example: Professional interview response - confident tone)*

**Nervous Interview Example:**
```powershell
yt-dlp -f "best[height<=720]" -o "uploads/interview_videos/candidate_nervous.%(ext)s" "https://www.youtube.com/watch?v=9x0q3XXhPUw"
```
*(Example: Nervous interview response - anxious tone)*

### Alternative Search Terms:
- "confident job interview example"
- "nervous interview candidate"
- "mock interview confident"
- "anxious job interview"

---

## Option 2: Use Emotion Recognition Datasets

### RAVDESS Dataset (Recommended for Research)
- **Link**: https://zenodo.org/record/1188976
- **Content**: Professional actors displaying different emotions
- **Advantage**: Pre-labeled emotion categories
- **How to use**:
  1. Download video files from Zenodo
  2. Look for files with emotion codes:
     - `01` = neutral
     - `02` = calm (confident)
     - `03` = happy (confident)
     - `05` = angry
     - `06` = fear (nervous)
     - `07` = disgust
     - `08` = surprised

### CREMA-D Dataset
- **Link**: https://github.com/CheyneyComputerScience/CREMA-D
- **Content**: Emotional speech and facial expressions
- **Advantage**: Multimodal (audio + video)

---

## Option 3: Record Your Own Test Videos

### Simple Test Recording Script:

Create two 30-60 second self-introduction videos:

**Video 1 - Confident:**
- Good posture, sitting upright
- Steady eye contact with camera
- Clear, steady voice
- Smiling, relaxed facial expressions
- Script: "Hello, my name is [name]. I'm excited to introduce myself for this position. I have 5 years of experience in software development..."

**Video 2 - Nervous:**
- Fidgeting, looking away from camera
- Speaking faster or slower than normal
- Minimal smiling, tense expressions
- Script: Same content, but delivered nervously

**Save as:**
- `uploads/interview_videos/candidate_confident.mp4`
- `uploads/interview_videos/candidate_nervous.mp4`

---

## Option 4: Use Online Mock Interview Videos

### Free Resources:
1. **Indeed Career Guide** - Mock interview examples on YouTube
2. **LinkedIn Learning** - Free trial has interview samples
3. **Coursera Interview Prep** - Some courses have sample videos

---

## Testing After Getting Videos

### Run the test script:
```powershell
python test_video_analyzer.py
```

### Expected Output:
- Confident video: **7.5-9.5/10**
- Nervous video: **2.5-4.5/10**

### What You'll See:
```
📊 CONFIDENCE SCORE: 8.3/10

💬 Interpretation: Strong performance with good emotional control

✨ Strengths:
   ✓ Excellent emotional positivity (happy: 65%, neutral: 30%)
   ✓ Stable head movement throughout video
   ✓ Good face visibility and presence

💡 Areas for Improvement:
   • Eye contact could be more consistent

🎭 Emotion Breakdown (DeepFace):
      Happy: 65.2%
      Neutral: 30.1%
      Fear: 2.1%
      Sad: 1.5%
```

---

## Quick Start (Easiest Method)

If you want to start testing **immediately**, here's the simplest approach:

```powershell
# 1. Install video downloader
python -m pip install yt-dlp

# 2. Create directory
New-Item -Path "uploads/interview_videos" -ItemType Directory -Force

# 3. Download one confident example
yt-dlp -f "best[height<=720]" -o "uploads/interview_videos/test_confident.%(ext)s" "https://youtu.be/YOUR_VIDEO_ID"

# 4. Download one nervous example  
yt-dlp -f "best[height<=720]" -o "uploads/interview_videos/test_nervous.%(ext)s" "https://youtu.be/YOUR_VIDEO_ID"

# 5. Run test
python test_video_analyzer.py
```

---

## Need Help Finding Videos?

I can't directly browse YouTube, but you can:
1. Search YouTube for "confident job interview" + "nervous job interview"
2. Copy the video URLs
3. Use yt-dlp commands above with those URLs
4. Or just upload any MP4 files you have to `uploads/interview_videos/`

---

## Troubleshooting

**Issue**: yt-dlp not working
- **Fix**: Update: `python -m pip install -U yt-dlp`

**Issue**: Video format not supported
- **Fix**: Convert to MP4 using FFmpeg: `ffmpeg -i input.avi output.mp4`

**Issue**: Videos too large
- **Fix**: Use `-f "best[height<=480]"` for smaller resolution

---

## What to Look For in Test Results

### Good Accuracy Indicators:
- ✅ Confident video scores **above 7/10**
- ✅ Nervous video scores **below 4/10**
- ✅ Emotion breakdown shows appropriate emotions (happy vs fear/sad)
- ✅ Clear difference (3+ points) between confident and nervous scores

### If Accuracy is Low:
- Try videos with more exaggerated emotions
- Ensure good lighting in videos
- Check that faces are clearly visible
- Videos should be at least 30 seconds long

---

**Ready to test?** Get two videos, place them in `uploads/interview_videos/`, and run `python test_video_analyzer.py`!
