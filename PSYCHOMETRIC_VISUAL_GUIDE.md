# 📊 Psychometric Assessment - Visual Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       CANDIDATE WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

    START: Login
         │
         ▼
┌─────────────────────┐
│  Step 1: Technical  │  ← Existing
│     Interview       │
│                     │
│ • Coding Test       │
│ • Chat Interview    │
└──────────┬──────────┘
           │
           ▼
     [PASS/FAIL]
           │ PASS
           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Psychometric Assessment  ★ NEW ★                      │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ Question 1/20:  EQ - Self-Awareness                       │ │
│  │ "When facing a stressful deadline, I typically..."        │ │
│  │ ○ Stay calm and break down tasks systematically           │ │
│  │ ○ Feel anxious but push through                           │ │
│  │ ○ Feel overwhelmed and need support                       │ │
│  │ ○ Get frustrated and lose focus                           │ │
│  │                                                            │ │
│  │ [← Previous]     [1/20]     [Next →]                       │ │
│  │ Progress: ████░░░░░░░░░░░░░░░ 5%                          │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Time: 5-7 minutes | 20 Questions | 4 Categories               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                      [ALL 20 ANSWERED]
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESULTS DISPLAY                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  🎯 Overall Psychometric Score: 80.0/100                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │ 💙 Emotional       │  │ 🔄 Adaptability    │               │
│  │    Quotient        │  │    Quotient        │               │
│  │                    │  │                    │               │
│  │    84.0/100        │  │    84.0/100        │               │
│  │    "Strong"        │  │    "Strong"        │               │
│  └────────────────────┘  └────────────────────┘               │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐               │
│  │ 🤝 Social          │  │ ⚡ Behavioral      │               │
│  │    Quotient        │  │    Quotient        │               │
│  │                    │  │                    │               │
│  │    64.0/100        │  │    84.0/100        │               │
│  │    "Moderate"      │  │    "Strong"        │               │
│  └────────────────────┘  └────────────────────┘               │
│                                                                 │
│  Strengths:                  Development Areas:                │
│  ✓ Strong EQ                 → Social Skills                   │
│  ✓ High Adaptability                                           │
│  ✓ Strong BQ                                                   │
│                                                                 │
│  Recommended Roles:                                            │
│  • Leadership positions                                        │
│  • Client-facing roles                                         │
│  • Cross-functional team lead                                 │
│                                                                 │
│  [Continue to Video Interview →]                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    [CLICK CONTINUE]
                             │
                             ▼
┌─────────────────────┐
│  Step 3: Video      │  ← Existing
│  Self-Introduction  │
│                     │
│ • Upload video      │
│ • AI analysis       │
└──────────┬──────────┘
           │
           ▼
     [COMPLETE]
           │
           ▼
    ✅ All Stages Done!
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        DATA FLOW                                 │
└──────────────────────────────────────────────────────────────────┘

USER ANSWERS QUESTION
         │
         ▼
┌────────────────────────┐
│  psychometric_ui.py    │  ← UI Layer
│                        │
│  st.radio() selection  │
│  Button click          │
└───────────┬────────────┘
            │
            │ calls
            ▼
┌─────────────────────────────────────┐
│  psychometric_assessment.py        │  ← Core Logic
│                                     │
│  record_response(question_id, idx)  │
│  ├─ Extract score from option      │
│  ├─ Store in self.responses        │
│  └─ Add timestamp                  │
└───────────┬─────────────────────────┘
            │
            │ after 20 questions
            ▼
┌─────────────────────────────────────┐
│  calculate_quotients()              │  ← Scoring
│                                     │
│  1. Group by category               │
│     EQ: [5,3,5,3,5] = 21/25        │
│     AQ: [5,3,5,3,5] = 21/25        │
│     SQ: [3,3,4,3,3] = 16/25        │
│     BQ: [5,5,3,5,3] = 21/25        │
│                                     │
│  2. Normalize to 0-100              │
│     EQ: 84.0                        │
│     AQ: 84.0                        │
│     SQ: 64.0                        │
│     BQ: 84.0                        │
│                                     │
│  3. Weighted average                │
│     Overall: 80.0                   │
│                                     │
│  4. Add interpretations             │
│     "Strong", "Moderate", etc.      │
└───────────┬─────────────────────────┘
            │
            │ results stored in
            ▼
┌─────────────────────────────────────┐
│  st.session_state                   │  ← Temporary Storage
│                                     │
│  'psychometric_results': {...}      │
│  'psychometric_recommendations':..  │
└───────────┬─────────────────────────┘
            │
            │ after video interview
            ▼
┌─────────────────────────────────────┐
│  interview_storage.py               │  ← Permanent Storage
│                                     │
│  save_interview_result()            │
│  ├─ Technical data                  │
│  ├─ Psychometric data ★ NEW        │
│  └─ Video analysis                  │
└───────────┬─────────────────────────┘
            │
            │ saves to
            ▼
┌─────────────────────────────────────┐
│  interview_results/                 │  ← JSON File
│    CAND123/                         │
│      interview_20251231.json        │
│        ├─ metadata                  │
│        ├─ interview_data            │
│        ├─ psychometric_assessment   │
│        └─ psychometric_recommendations│
└─────────────────────────────────────┘
```

## Scoring Algorithm Visual

```
┌──────────────────────────────────────────────────────────────────┐
│                     SCORING MECHANISM                            │
└──────────────────────────────────────────────────────────────────┘

QUESTION LEVEL
──────────────
Each question has 4 options:

Question: "When facing a stressful deadline..."
├─ Option A: "Stay calm..."           → Score: 5 ★ SELECTED
├─ Option B: "Feel anxious..."        → Score: 3
├─ Option C: "Feel overwhelmed..."    → Score: 1
└─ Option D: "Get frustrated..."      → Score: 0

Candidate selects Option A → Records score: 5


CATEGORY LEVEL (Quotient)
──────────────────────────
5 questions per quotient:

Emotional Quotient (EQ):
├─ eq1: 5 points  (Self-Awareness)
├─ eq2: 3 points  (Empathy)
├─ eq3: 5 points  (Emotion Regulation)
├─ eq4: 3 points  (Social Skills)
└─ eq5: 5 points  (Motivation)
    ─────
    21 total

Calculation:
─────────────
Max Possible = 5 questions × 5 points = 25
Total Score = 21
Normalized = (21 ÷ 25) × 100 = 84.0

Interpretation:
───────────────
84.0 falls in range [70-84] → "Strong"


SUBCATEGORY LEVEL
─────────────────
Individual skill breakdown:

Self-Awareness:
  Question eq1: 5 points
  Max: 5 points
  Score: (5 ÷ 5) × 100 = 100.0

Empathy:
  Question eq2: 3 points
  Max: 5 points
  Score: (3 ÷ 5) × 100 = 60.0

... and so on for each sub-skill


OVERALL SCORE
─────────────
Weighted average of all 4 quotients:

Overall = (EQ × 30%) + (AQ × 25%) + (BQ × 25%) + (SQ × 20%)

Example:
  EQ: 84.0
  AQ: 84.0
  SQ: 64.0
  BQ: 84.0

Overall = (84.0 × 0.30) + (84.0 × 0.25) + (84.0 × 0.25) + (64.0 × 0.20)
        = 25.2 + 21.0 + 21.0 + 12.8
        = 80.0
```

## Interpretation Scale

```
┌──────────────────────────────────────────────────────────────────┐
│                    SCORE INTERPRETATION                          │
└──────────────────────────────────────────────────────────────────┘

  0        20        40        60        80        100
  |─────────|─────────|─────────|─────────|─────────|
  
  │◄──────►│◄────────►│◄───────►│◄───────►│◄───────►│
  
  Needs      Developing  Moderate   Strong   Exceptional
  Development
  
  
  0-39:    🔴 Needs Development
           • Significant improvement needed
           • Requires focused development
           • May not be suitable for role
           
  40-54:   🟠 Developing
           • Below average performance
           • Has potential with training
           • Monitor progress
           
  55-69:   🟡 Moderate
           • Average competency
           • Meets basic requirements
           • Room for growth
           
  70-84:   🟢 Strong
           • Above average performance
           • Good fit for role
           • Minor development areas
           
  85-100:  🌟 Exceptional
           • Outstanding competency
           • Top 15% of candidates
           • Leadership potential
```

## File Interaction Map

```
┌──────────────────────────────────────────────────────────────────┐
│                    FILE INTERACTIONS                             │
└──────────────────────────────────────────────────────────────────┘

app.py (Main Controller)
   │
   ├─ imports ──→ psychometric_ui.py
   │                    │
   │                    └─ imports ──→ psychometric_assessment.py
   │                                          │
   │                                          └─ contains
   │                                              • QUESTIONS (20)
   │                                              • record_response()
   │                                              • calculate_quotients()
   │                                              • get_recommendations()
   │
   └─ imports ──→ interview_storage.py
                        │
                        └─ saves results to
                            interview_results/{candidate_id}/interview.json
                            
                            
Session State Variables
───────────────────────
st.session_state = {
    'technical_completed': bool,
    'psychometric_assessment': PsychometricAssessment object,
    'current_question_index': 0-19,
    'psychometric_completed': bool,
    'psychometric_results': dict,
    'psychometric_recommendations': dict,
    'psychometric_assessment_completed': bool,
    'video_analyzed': bool
}
```

## Question Distribution

```
┌──────────────────────────────────────────────────────────────────┐
│                   20 QUESTIONS BREAKDOWN                         │
└──────────────────────────────────────────────────────────────────┘

EMOTIONAL QUOTIENT (5 questions)
├─ Self-Awareness (1)
├─ Empathy (1)
├─ Emotion Regulation (1)
├─ Social Skills (1)
└─ Motivation (1)

ADAPTABILITY QUOTIENT (5 questions)
├─ Change Response (1)
├─ Ambiguity Tolerance (1)
├─ Learning Agility (1)
├─ Resilience (1)
└─ Innovation Mindset (1)

SOCIAL QUOTIENT (5 questions) ★ FIRO-B Based
├─ Inclusion - Expressed (1)
├─ Inclusion - Wanted (1)
├─ Control - Expressed (1)
├─ Affection - Expressed (1)
└─ Collaboration (1)

BEHAVIORAL QUOTIENT (5 questions) ★ Situational Judgment
├─ Conflict Resolution (1)
├─ Time Management (1)
├─ Initiative (1)
├─ Accountability (1)
└─ Decision Making (1)

Total: 20 questions × 5 points each = 100 max points
Time: ~15-20 seconds per question = 5-7 minutes total
```

---

## Quick Reference

**Start Assessment:** User completes technical interview  
**Assessment Trigger:** `st.session_state.technical_completed = True`  
**Question Navigation:** Previous/Next buttons  
**Answer Recording:** `assessment.record_response(q_id, option_idx)`  
**Score Calculation:** After 20th question submission  
**Results Display:** Automatic after calculation  
**Continue Flow:** Button click sets `psychometric_assessment_completed = True`  
**Data Saved:** After video interview completion  

---

**Visual Overview Complete!** 📊
