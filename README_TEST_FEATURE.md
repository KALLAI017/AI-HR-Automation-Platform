# 📝 Candidate Testing & Email Notification Feature

## Overview

This feature automates the complete candidate hiring workflow:
1. **Resume Evaluation** - LLM-powered resume parsing and matching
2. **Technical Assessment** - Automated multiple-choice test for qualified candidates
3. **Auto-Hiring** - Successful candidates are automatically converted to employees
4. **Email Notifications** - LLM-generated professional emails sent to candidates
5. **Credential Generation** - Automatic username/password creation for employee portal

---

## 🔄 Complete Workflow

### Step 1: Candidate Application
- Candidate uploads resume (PDF) via Candidate Portal
- System uses LLM to parse resume (skills, experience, education)
- AI evaluates candidate against job requirements
- If score ≥ 50%, candidate is accepted for test

### Step 2: Technical Assessment
- Accepted candidates are invited to take a position-specific test
- Tests contain 5 multiple-choice questions per position
- Questions are relevant to the job role (e.g., Python, SQL for developers)
- Passing score: 60% (3 out of 5 questions)

### Step 3: Auto-Hiring (If Passed)
- System automatically converts candidate to employee
- Generates unique:
  - Employee ID (e.g., EMP003)
  - Username (based on email)
  - Random password (10 characters)
- Creates employee record with default leave balance

### Step 4: Email Notification
- **LLM generates personalized email** content
- **Passed candidates** receive:
  - Congratulations message
  - Test score
  - Employee portal credentials (username & password)
  - Welcome message
  
- **Failed candidates** receive:
  - Thank you message
  - Test score
  - Encouragement to apply again

---

## 📧 Email Setup (Gmail)

### Required Configuration

The system uses Gmail SMTP to send real emails. You need to configure your Gmail account:

#### Step 1: Enable 2-Step Verification
1. Go to [Google Account](https://myaccount.google.com/)
2. Navigate to **Security**
3. Enable **2-Step Verification**

#### Step 2: Generate App Password
1. In Google Account > Security
2. Search for "App Passwords"
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Enter name: **HR Agent**
6. Click **Generate**
7. Copy the 16-character password

#### Step 3: Update .env File
```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx-xxxx-xxxx-xxxx  # The 16-char app password from Step 2
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### ⚠️ Important Notes
- **DO NOT** use your regular Gmail password
- **MUST** use App Password (16 characters)
- Keep your `.env` file secure and never commit it to git
- The app password bypasses 2FA for programmatic access

---

## 🎯 Test Questions

Each job position has 5 position-specific questions:

### Senior Developer Test
1. Which keyword defines a function in Python?
2. What does REST stand for in REST API?
3. Which SQL command retrieves data?
4. In Django, which file defines URL patterns?
5. What is the type of an empty list in Python?

### Marketing Manager Test
1. What does SEO stand for?
2. Which metric measures single-page visits?
3. What is A/B testing?
4. Best platform for B2B marketing?
5. What does CTA stand for?

---

## 🔐 Generated Credentials

When a candidate passes the test:

```
Employee ID: EMP003
Username: johndoe (from john.doe@example.com)
Password: aB3dE5fG7h (random 10-char string)

Default Leave Balance:
- Casual Leave: 12 days
- Sick Leave: 15 days
- Annual Leave: 20 days
```

These credentials are:
1. Displayed on-screen immediately after passing
2. Sent via email to candidate's registered email
3. Used to log into Employee Portal

---

## 🤖 LLM Features

### 1. Resume Parsing
```python
LLM extracts from resume:
- Skills: ["Python", "Django", "REST API", "SQL"]
- Experience: 5 years
- Education: "Bachelor's Degree"
```

### 2. Email Content Generation
```
Prompt to LLM:
"Generate professional email for candidate who [passed/failed] test
Score: X%, Position: Y
Include: [credentials if passed / encouragement if failed]"

LLM generates:
- Subject line
- Professional greeting
- Personalized content
- Credentials (if passed)
- Professional closing
```

---

## 📊 Status Flow

```
Candidate Application
    ↓
Resume Parsing (LLM)
    ↓
Evaluation Against Job Requirements
    ↓
├─ Score < 50% → Rejected
└─ Score ≥ 50% → Test_Scheduled
         ↓
    Take Test (5 questions)
         ↓
    ├─ Score < 60% → Rejected → Email Sent
    └─ Score ≥ 60% → Hired → Convert to Employee → Email Sent with Credentials
```

---

## 🎨 User Interface

### Candidate Portal Flow

1. **Job Listings Page**
   - View available positions
   - Upload resume
   - Submit application

2. **Evaluation Results**
   - If accepted: "Start Technical Assessment Test" button appears

3. **Test Interface**
   - Professional header with candidate name
   - 5 multiple-choice questions
   - One answer per question
   - Submit button

4. **Results Page**
   - **Passed**: 🎉 Congratulations + Credentials + Email confirmation
   - **Failed**: 📊 Score + Encouragement + Email confirmation

---

## 🔧 Admin Features

Admins can customize tests by editing `hr_agent.py`:

```python
JobPosition(
    job_id="JOB001",
    title="Senior Developer",
    test_questions=[
        {
            "question": "Your question here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option B"
        },
        # Add more questions...
    ]
)
```

---

## 🚀 Usage Example

### As a Candidate:
1. Go to Candidate Portal
2. Upload resume for "Senior Developer" position
3. If accepted: Click "Start Technical Assessment Test"
4. Answer 5 questions
5. Submit test
6. If score ≥ 60%:
   - See congratulations message
   - Note down credentials
   - Check email for confirmation
   - Log in to Employee Portal with new credentials

### As an Admin:
1. Monitor candidate applications in Admin Portal
2. View test results and hired candidates
3. Access audit logs for all test activities

---

## 📝 Sample Email Output

### Passed Candidate:
```
Subject: Congratulations! You've been selected for Senior Developer

Dear John Doe,

Congratulations! We are pleased to inform you that you have successfully 
passed the assessment test for the Senior Developer position with a score 
of 80.0%.

We are excited to welcome you to our team! Below are your credentials to 
access the Employee Portal:

Username: johndoe
Password: aB3dE5fG7h

Please log in to the Employee Portal to complete your onboarding process 
and access company resources.

We look forward to working with you!

Best regards,
HR Department
```

### Failed Candidate:
```
Subject: Test Results for Senior Developer Position

Dear Jane Smith,

Thank you for taking the assessment test for the Senior Developer position.

After careful evaluation, we regret to inform you that your test score of 
40.0% did not meet our current requirements for this position.

We appreciate your interest in our company and encourage you to apply for 
other positions that match your skills and experience in the future.

Best regards,
HR Department
```

---

## 🛡️ Security Features

1. **Secure Password Generation**: Random 10-character passwords
2. **Unique Usernames**: Based on email to prevent duplicates
3. **Email Validation**: Ensures proper email format
4. **Session Management**: Test sessions are isolated
5. **Audit Logging**: All test activities are logged

---

## 📈 Benefits

✅ **Automated Hiring**: No manual intervention needed
✅ **Scalable**: Can handle multiple candidates simultaneously
✅ **Consistent**: Same evaluation criteria for all candidates
✅ **Professional**: LLM-generated emails are polished and personalized
✅ **Transparent**: Candidates receive immediate feedback
✅ **Secure**: Credentials generated and delivered securely

---

## 🐛 Troubleshooting

### Email Not Sending
**Problem**: "Email credentials not configured"
**Solution**: Add SENDER_EMAIL and SENDER_PASSWORD to .env file

**Problem**: "Authentication failed"
**Solution**: 
- Make sure you're using App Password, not regular password
- Enable 2-Step Verification on Google Account
- Generate new App Password

### Test Not Appearing
**Problem**: "Start Test" button doesn't appear
**Solution**: 
- Make sure application score is ≥ 50%
- Check job position has test_questions defined
- Verify candidate status is "Test_Scheduled"

### LLM Errors
**Problem**: Email content not generated
**Solution**: 
- Check GROQ_API_KEY in .env
- System will use fallback templates if LLM fails

---

## 📚 Additional Resources

- [Gmail App Passwords Guide](https://support.google.com/accounts/answer/185833)
- [Groq API Documentation](https://console.groq.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 🎓 Future Enhancements

Potential improvements:
- [ ] Timed tests (countdown timer)
- [ ] Randomized question order
- [ ] Question difficulty levels
- [ ] Multiple test attempts
- [ ] Video interview scheduling
- [ ] Skills-based adaptive testing
- [ ] Detailed analytics dashboard

---

## ✨ Demo Credentials

After passing the test, you can log in to Employee Portal:

```
Portal: Employee
Username: [generated from your email]
Password: [sent to your email]
```

Enjoy the automated hiring experience! 🚀
