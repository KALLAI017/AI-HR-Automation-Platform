# 🎬 Quick Start Guide - Test & Hire Feature

## 🚀 Try It Now (5-Minute Demo)

### Option 1: Without Email (Fastest)
**Time:** 2 minutes  
**Setup:** None required

### Option 2: With Email (Complete Experience)
**Time:** 7 minutes (6 min setup + 2 min demo)  
**Setup:** Configure Gmail (see EMAIL_SETUP_GUIDE.md)

---

## 🎯 Demo Walkthrough

### Step 1: Access Candidate Portal (10 seconds)

```
1. Open browser: http://localhost:8501
2. Click on "Candidate" tab in login page
3. You're in! (No login required for candidates)
```

---

### Step 2: Apply for a Position (30 seconds)

**Choose:** Senior Developer OR Marketing Manager

**Fill Form:**
```
Name: Your Name
Email: your.email@gmail.com  ← Use real email if you set up SMTP
Phone: 1234567890
```

**Upload Resume:**
- Use any PDF resume
- System will parse it automatically with LLM

**Click:** 🚀 Submit Application

---

### Step 3: View Evaluation (10 seconds)

You'll see one of these results:

#### ✅ Accepted (Score ≥ 50%)
```
🎉 Congratulations! Application Accepted
Score: 75%
Next Step: You are invited to take a technical assessment test!

[📝 Start Technical Assessment Test]  ← Click this!
```

#### ⏳ Pending Review (Score 40-49%)
```
⏳ Application Under Review
Score: 45%
Your application will be reviewed by our HR team.
```

#### ❌ Rejected (Score < 40%)
```
❌ Application Not Accepted
Score: 25%
We encourage you to apply for other positions.
```

---

### Step 4: Take the Test (1 minute)

**Test Interface:**
```
📝 Technical Assessment Test - Senior Developer

Candidate: Your Name
Position: Senior Developer

Instructions:
- Total Questions: 5
- Passing Score: 60%
- Please select the best answer for each question

─────────────────────────────────────────

Question 1
Which of the following is used to define a function in Python?

○ function
○ def          ← Select this for correct answer
○ func
○ define

─────────────────────────────────────────

[Continue for questions 2-5...]

─────────────────────────────────────────

               [✅ Submit Test]
```

**Tips to Pass:**
- For Senior Developer: Basic Python/SQL knowledge
- For Marketing Manager: Basic digital marketing knowledge
- Need 60% (3 out of 5 correct)

---

### Step 5: View Results (Instant)

#### 🎉 If You Pass (≥60%)

```
🎉 Congratulations! You Passed!
Score: 80.0% (4/5 correct)
Status: You are now hired as a Senior Developer!

─────────────────────────────────────────

🔐 Your Employee Portal Credentials

Employee ID: EMP003
Username: yourname          ← Save this!
Password: aB3dE5fG7h        ← Save this!

⚠️ Please save these credentials securely!

─────────────────────────────────────────

📧 Email Notification
✅ Email sent successfully to your.email@gmail.com

📄 Email Content
Subject: Congratulations! You've been selected for Senior Developer

Dear Your Name,

Congratulations! We are pleased to inform you that you have 
successfully passed the assessment test for the Senior Developer 
position with a score of 80.0%.

We are excited to welcome you to our team! Below are your 
credentials to access the Employee Portal:

Username: yourname
Password: aB3dE5fG7h

Please log in to the Employee Portal to complete your onboarding 
process and access company resources.

We look forward to working with you!

Best regards,
HR Department
```

**What You Get:**
1. ✅ Employee ID
2. ✅ Username & Password (shown immediately)
3. ✅ Email confirmation (sent to your inbox)
4. ✅ Access to Employee Portal

---

#### 📊 If You Don't Pass (<60%)

```
📊 Test Results
Score: 40.0% (2/5 correct)
Passing Score: 60%
Status: Unfortunately, you did not pass the test.

We encourage you to improve your skills and apply again in the future!

─────────────────────────────────────────

📧 Email Notification
✅ Email sent successfully to your.email@gmail.com

📄 Email Content
Subject: Test Results for Senior Developer Position

Dear Your Name,

Thank you for taking the assessment test for the Senior Developer 
position.

After careful evaluation, we regret to inform you that your test 
score of 40.0% did not meet our current requirements for this position.

We appreciate your interest in our company and encourage you to 
apply for other positions that match your skills and experience 
in the future.

Best regards,
HR Department
```

---

### Step 6: Login to Employee Portal (If Passed)

```
1. Click [🔙 Return to Main Page]
2. Go to "Employee" tab
3. Enter your credentials:
   Username: yourname
   Password: aB3dE5fG7h
4. Click [🔐 Login]
5. You're now an employee! 🎉
```

**As Employee You Can:**
- 📝 Request leave
- ❓ Ask HR policy questions
- 👤 View your profile
- 📊 Check leave balance

---

## 📧 Check Your Email

### If Email Configured:
```
1. Open Gmail
2. Check inbox for email from HR Agent
3. Email contains:
   - Your test score
   - Pass/Fail status
   - Credentials (if passed)
   - Professional AI-generated message
```

### If Email NOT Configured:
```
Don't worry! You still get:
✅ Credentials shown on screen immediately
✅ Email content displayed in app
✅ Fully functional system

Just can't send actual emails.
```

---

## 🎓 Test Answers (For Quick Demo)

Want to pass quickly? Here are the answers:

### Senior Developer Test
1. **def**
2. **Representational State Transfer**
3. **SELECT**
4. **urls.py**
5. **<class 'list'>**

### Marketing Manager Test
1. **Search Engine Optimization**
2. **Bounce Rate**
3. **Testing two different versions to see which performs better**
4. **LinkedIn**
5. **Call To Action**

*Select these answers to get 100% and pass!*

---

## 🔄 Try Again

Want to test again?

```
1. Click [🔙 Return to Main Page]
2. Apply with different name/email
3. Upload resume again
4. Take test with different answers
5. See different results!
```

---

## 📊 What's Happening Behind the Scenes

```
Your Actions          →  System Actions
─────────────────────────────────────────────────────────
Upload Resume         →  LLM parses PDF
                      →  Extracts skills, experience
                      →  Matches against job requirements
                      →  Calculates score

Score ≥ 50%          →  Accept for test
                      →  Show "Start Test" button

Click Start Test      →  Load position-specific questions
                      →  Create test session

Submit Answers        →  Calculate score
                      →  Pass if ≥ 60%

If Passed            →  Generate Employee ID
                      →  Create username (from email)
                      →  Generate random password
                      →  Add to employee database
                      →  Create user account
                      →  LLM generates email content
                      →  Send email via Gmail SMTP
                      →  Log everything in audit

If Failed            →  Mark as rejected
                      →  LLM generates encouragement email
                      →  Send email
                      →  Log result
```

---

## 🎯 Success Indicators

You know it worked if you see:

✅ **Resume Parsed:**
```
📊 Your Profile Summary
Skills Detected: Python, Django, SQL
Experience: 5 years
Education: Bachelor's Degree
```

✅ **Test Loaded:**
```
📝 Technical Assessment Test - [Position]
Total Questions: 5
```

✅ **Results Calculated:**
```
Score: 80.0% (4/5 correct)
```

✅ **Credentials Generated:**
```
Employee ID: EMP003
Username: yourname
Password: aB3dE5fG7h
```

✅ **Email Sent (if configured):**
```
📧 Email Notification
✅ Email sent successfully to your.email@gmail.com
```

---

## 🐛 Something Wrong?

### Resume Not Parsed
❌ **Issue:** PDF not readable  
✅ **Fix:** Use a standard PDF (not scanned image)

### Test Not Appearing
❌ **Issue:** Score too low  
✅ **Fix:** Need ≥50% to qualify for test

### Email Not Sending
❌ **Issue:** SMTP not configured  
✅ **Fix:** Add SENDER_EMAIL and SENDER_PASSWORD to .env  
✅ **Or:** Just use without email (credentials still shown!)

### Can't Login as Employee
❌ **Issue:** Wrong credentials  
✅ **Fix:** Copy exact username/password shown after passing

---

## 🎬 Video Tutorial (Text Version)

**[0:00-0:30] Introduction**
- Open HR Agent at localhost:8501
- Click Candidate tab

**[0:30-1:00] Application**
- Fill name, email, phone
- Upload PDF resume
- Click Submit

**[1:00-1:30] Evaluation**
- Wait for LLM to parse resume
- See acceptance message
- Click "Start Test"

**[1:30-2:30] Take Test**
- Read 5 questions
- Select answers
- Click Submit Test

**[2:30-3:00] Results**
- See score and pass/fail
- Get credentials (if passed)
- Email confirmation

**[3:00-3:30] Login**
- Go to Employee tab
- Enter credentials
- Access employee dashboard

**Done! 🎉**

---

## 💡 Pro Tips

1. **Use Real Email:** If you set up Gmail, use your real email to receive credentials
2. **Save Credentials:** Screenshot or write down username/password immediately
3. **Check Spam:** Sometimes emails go to spam folder
4. **Test Both Positions:** Try Senior Developer AND Marketing Manager
5. **Try Failing:** Submit wrong answers to see failure email
6. **Multiple Candidates:** Use different emails to test multiple times

---

## 🏆 Challenge Yourself

1. ⭐ **Bronze:** Pass test with 60% (3/5 correct)
2. ⭐⭐ **Silver:** Pass test with 80% (4/5 correct)  
3. ⭐⭐⭐ **Gold:** Pass test with 100% (5/5 correct)
4. ⭐⭐⭐⭐ **Platinum:** Set up email and receive real credentials via Gmail
5. ⭐⭐⭐⭐⭐ **Diamond:** Login to Employee Portal and request leave!

---

## 🎉 Enjoy!

You now have a **fully automated hiring system** that:
- Evaluates resumes with AI
- Tests candidates automatically
- Hires qualified candidates
- Sends professional emails
- Creates employee accounts

**All in 15 minutes with zero manual work!** 🚀

---

*Ready? Go to http://localhost:8501 and start! 🎯*
