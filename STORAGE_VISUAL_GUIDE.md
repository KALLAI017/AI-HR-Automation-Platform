# Interview Score Storage - Visual Overview

## 🗂️ Storage Location Map

```
Your Project Directory
│
├── 📁 interview_results/          ← ALL INTERVIEW DATA HERE
│   │
│   ├── 📁 CAND_001/               ← Candidate 1's folder
│   │   ├── 📄 interview_20250129_143022.json   ← Interview #1
│   │   ├── 📄 interview_20250129_150315.json   ← Interview #2
│   │   └── 📄 interview_20250129_162450.json   ← Interview #3
│   │
│   ├── 📁 CAND_002/               ← Candidate 2's folder
│   │   ├── 📄 interview_20250129_141200.json   ← Interview #1
│   │   └── 📄 interview_20250129_155530.json   ← Interview #2
│   │
│   ├── 📁 CAND_003/               ← Candidate 3's folder
│   │   └── 📄 interview_20250129_160000.json   ← Interview #1
│   │
│   └── 📄 all_interviews.json     ← Full export (if created)
│
├── app.py
├── interview_storage.py           ← Storage management code
├── results_viewer_ui.py           ← UI to view results
└── ... (other files)
```

---

## 📊 Score Flow Diagram

### Chat Mode Interview

```
┌─────────────────────────────────────────────────────────────┐
│  CANDIDATE STARTS CHAT INTERVIEW                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Chat: Problem Introduction                               │
│  ├─ "Let's solve Two Sum..."                                │
│  └─ Stores in: conversation_history[]                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Chat: Clarification Questions                            │
│  ├─ "Can you explain the input format?"                     │
│  ├─ "What's the expected time complexity?"                  │
│  └─ Stores in: conversation_history[]                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Chat: Approach Discussion                                │
│  ├─ Candidate explains approach                             │
│  ├─ AI evaluates: 0-100 score                               │
│  └─ Stores in: approach_quality                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Coding Phase: Write Solution                                │
│  ├─ Candidate writes code in editor                         │
│  ├─ Can request hints (max 3)                               │
│  └─ Stores in: hints_used, conversation_history[]           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Click "✅ Submit" Button                                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AUTOMATIC PROCESSING                                        │
│  ├─ Run all test cases                                      │
│  │   └─ Calculate: test_score = (passed/total) * 50        │
│  │                                                           │
│  ├─ AI Code Analysis (LLaMA 3.3 70B)                        │
│  │   └─ Calculate: quality_score = (AI_score/100) * 30     │
│  │                                                           │
│  ├─ Calculate approach_score = (approach_quality/100) * 10  │
│  ├─ Calculate communication_score = (comm_score/100) * 10   │
│  ├─ Calculate hint_penalty = hints_used * 5                 │
│  │                                                           │
│  └─ Final Score = test + quality + approach + comm - hints  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  💾 SAVE TO JSON                                            │
│                                                              │
│  File: interview_results/CAND_001/interview_20250129.json  │
│                                                              │
│  {                                                           │
│    "metadata": {                                            │
│      "candidate_id": "CAND_001",                           │
│      "timestamp": "20250129_143022",                        │
│      "date": "2025-01-29T14:30:22"                         │
│    },                                                        │
│    "interview_data": {                                      │
│      "problem": "Two Sum",                                  │
│      "approach_quality": 85,                                │
│      "communication_score": 90,                             │
│      "hints_used": 1,                                       │
│      "conversation_history": [...]                          │
│    },                                                        │
│    "scoring": {                                             │
│      "test_score": 45.0,        // 9/10 tests               │
│      "quality_score": 27.0,     // 90% quality              │
│      "approach_score": 8.5,     // 85% approach             │
│      "communication_score": 9.0, // 90% communication       │
│      "hint_penalty": -5,        // 1 hint used              │
│      "final_score": 84.5        // TOTAL                    │
│    }                                                         │
│  }                                                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ✅ SHOW CONFIRMATION                                        │
│  "Code submitted and analyzed! Final Score: 84.5/100"       │
│  "💾 Results saved to: interview_results/CAND_001/..."     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Score Components Visual

```
┌──────────────────────────────────────────────────┐
│          FINAL SCORE = 84.5 / 100                │
├──────────────────────────────────────────────────┤
│                                                  │
│  🧪 Test Score         45.0 / 50  (50%)         │
│     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░ 90%                   │
│     9 out of 10 tests passed                    │
│                                                  │
│  ✨ Code Quality       27.0 / 30  (30%)         │
│     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░ 90%                   │
│     AI analysis: Optimal solution               │
│                                                  │
│  🎯 Approach          8.5 / 10  (10%)          │
│     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ 85%                   │
│     Good problem-solving strategy               │
│                                                  │
│  💬 Communication     9.0 / 10  (10%)          │
│     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░ 90%                   │
│     Clear articulation of ideas                 │
│                                                  │
│  💡 Hint Penalty      -5.0                      │
│     1 hint used (max 3)                         │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 📂 JSON File Structure

```json
{
  "metadata": {
    "candidate_id": "CAND_001",
    "timestamp": "20250129_143022",
    "date": "2025-01-29T14:30:22.123456"
  },
  
  "interview_data": {
    "interview_id": "INT_20250129_143022",
    "problem": "Two Sum",
    "submission_date": "2025-01-29T14:30:22.123456",
    "language": "python",
    
    "stages_completed": [
      "introduction",
      "clarification",
      "approach",
      "coding",
      "review"
    ],
    
    "approach_quality": 85,
    "communication_score": 90,
    "hints_used": 1,
    
    "conversation_history": [
      {
        "role": "assistant",
        "content": "Let's solve Two Sum. Can you explain your approach?",
        "stage": "introduction"
      },
      {
        "role": "user",
        "content": "I'll use a hash map to store seen numbers...",
        "stage": "approach"
      }
    ],
    
    "total_messages": 12,
    "duration_estimate": 24
  },
  
  "scoring": {
    "test_score": 45.0,
    "quality_score": 27.0,
    "approach_score": 8.5,
    "communication_score": 9.0,
    "hint_penalty": -5,
    "final_score": 84.5,
    
    "test_results": {
      "passed": 9,
      "total": 10,
      "all_passed": false
    },
    
    "code_quality_details": {
      "code_quality_score": 90,
      "overall_feedback": "Excellent hash map solution with O(n) complexity...",
      "strengths": [
        "Optimal time complexity",
        "Clean code structure",
        "Good variable naming"
      ],
      "improvements": [
        "Add edge case handling",
        "Consider input validation"
      ]
    },
    
    "breakdown": {
      "tests": "45.0/50",
      "quality": "27.0/30",
      "interview": "17.5/20"
    }
  }
}
```

---

## 🎯 Access Methods

### 1️⃣ Admin UI (Visual Interface)

```
Login → Admin Portal → 📈 Interview Results
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  Select Candidate: CAND_001 ▼        │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  📊 Summary                            │
        │  • Total Interviews: 3                 │
        │  • Average Score: 82.3/100            │
        │  • Highest Score: 95.0/100            │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  📝 Individual Interviews              │
        │  🟢 Interview #1: Two Sum - 84.5/100  │
        │  🟢 Interview #2: Valid () - 95.0/100 │
        │  🟡 Interview #3: Merge K - 67.5/100  │
        └───────────────────────────────────────┘
```

### 2️⃣ Python API

```python
from interview_storage import InterviewStorage

storage = InterviewStorage()

# Load all interviews
interviews = storage.load_candidate_interviews("CAND_001")
# Returns: [interview1, interview2, interview3]

# Get summary
summary = storage.get_candidate_summary("CAND_001")
# Returns: {total_interviews: 3, average_score: 82.3, ...}

# Export all
path = storage.export_all_results()
# Saves: interview_results/all_interviews.json
```

### 3️⃣ Direct File Access

```
Windows Explorer → Navigate to:
C:\Users\siyad\OneDrive\Desktop\Main Project\HR_Agent\interview_results\

Open any JSON file with:
- Notepad
- VS Code
- JSON viewer
```

---

## 🔄 Complete Workflow

```
START INTERVIEW
      │
      ▼
┌─────────────┐
│ Chat with AI│──→ Stores conversation
└──────┬──────┘    in memory
       │
       ▼
┌─────────────┐
│ Write Code  │──→ Stores in session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Submit Code │
└──────┬──────┘
       │
       ├──→ Run Tests      ──→ test_score
       ├──→ AI Analysis    ──→ quality_score
       ├──→ Check Approach ──→ approach_score
       ├──→ Check Comm     ──→ communication_score
       └──→ Count Hints    ──→ hint_penalty
       │
       ▼
┌──────────────────┐
│ Calculate Final  │
│ Score            │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ 💾 SAVE TO JSON │ ← YOU ARE HERE!
│                  │
│ File: interview_results/
│       CAND_001/
│       interview_20250129.json
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Show Results     │
│ to Candidate     │
└──────────────────┘
       │
       ▼
    END
```

---

## 📍 Key Points

1. **Location**: All results stored in `interview_results/` folder
2. **Format**: JSON files (human-readable)
3. **Organization**: One folder per candidate
4. **Naming**: `interview_{timestamp}.json`
5. **Automatic**: Saves without any manual action
6. **Permanent**: Files persist forever (until manually deleted)
7. **Accessible**: Via Admin UI, Python API, or direct file access

---

## 🚀 Quick Start

### To View Results:
1. Complete any technical interview
2. Login as Admin
3. Go to: **📈 Interview Results**
4. Select candidate
5. View complete history!

### To Access Programmatically:
```python
from interview_storage import InterviewStorage
storage = InterviewStorage()
interviews = storage.load_candidate_interviews("YOUR_CANDIDATE_ID")
```

### To Find Files:
Navigate to: `HR_Agent/interview_results/{candidate_id}/`

---

**That's it! Your scores are safely stored in JSON files. 🎉**
