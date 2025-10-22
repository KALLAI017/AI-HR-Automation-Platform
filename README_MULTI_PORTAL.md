# HR Agent - Multi-Portal Enterprise Platform 🤖

A complete AI-powered HR automation system with **three role-based portals**: Candidate, Employee, and Admin. Features automatic resume parsing, candidate evaluation, and seamless employee onboarding.

---

## ✨ Key Features

### 👤 **Candidate Portal**
- Browse and apply for active job positions
- Upload resume in PDF format
- **Automatic resume parsing** (skills, experience, education extraction)
- **Intelligent evaluation** against job requirements
- Instant feedback (Accepted/Pending/Rejected)
- Auto-onboarding trigger for accepted candidates

### 💼 **Employee Portal**
- Personal dashboard with leave balance overview
- Submit leave requests (Casual, Sick, Annual, Unpaid)
- Ask HR policy questions with AI-powered answers
- View and manage personal profile
- Track leave request status

### ⚙️ **Admin Portal**
- Comprehensive admin dashboard with metrics
- **Set eligibility criteria** for automatic candidate evaluation
- Manage all job positions (add, edit, close, reopen)
- Review and manage candidate applications
- **Trigger employee onboarding** with one click
- Generate audit reports with detailed activity logs
- View all employees and their details

---

## 🚀 Quick Start Guide

### 1. Installation

```powershell
# Navigate to project directory
cd "C:\Users\KALLAI\Desktop\Main Project\HR_Agent"

# Activate virtual environment (already set up)
# All dependencies are installed in .venv

# If you need to reinstall dependencies:
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

### 2. Configure API Key

The `.env` file is already configured with your Groq API key. The system will automatically load it.

### 3. Run the Application

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run app.py
```

The app will launch at: **http://localhost:8501**

---

## 🔐 Login Credentials

### 👤 Candidate Portal
- **No login required** - Click "Apply for a Position" to start

### 💼 Employee Portal
Demo accounts:
- **Username:** `john.doe` | **Password:** `pass123`
- **Username:** `jane.smith` | **Password:** `pass123`

### ⚙️ Admin Portal
- **Username:** `admin` | **Password:** `admin123`

---

## 📋 Complete Workflow

### **Scenario: New Candidate Application**

1. **Candidate applies:**
   - Opens the portal and clicks "Apply for a Position"
   - Selects a job (e.g., "Senior Developer")
   - Fills in personal details (name, email, phone)
   - Uploads PDF resume
   - Submits application

2. **System processes automatically:**
   - Parses PDF resume using PyPDF2
   - Extracts: Skills, Experience (years), Education level
   - Evaluates against job requirements
   - Calculates match score
   - Makes decision based on admin-configured criteria

3. **Evaluation outcomes:**
   - **Score ≥ 80% + meets all requirements** → **Accepted** ✅
   - **Score ≥ 50% but < 80%** → **Pending Review** ⏳
   - **Score < 50% or missing requirements** → **Rejected** ❌

4. **Admin reviews applications:**
   - Logs in to Admin Portal
   - Goes to "Manage Applications"
   - Views all candidates with scores and evaluations
   - For accepted candidates: clicks "Start Onboarding"

5. **Automatic onboarding:**
   - Creates employee profile
   - Generates employee ID (e.g., EMP003)
   - Assigns leave balances
   - Creates login credentials
   - Sends welcome email (simulated)

6. **New employee login:**
   - Employee receives credentials
   - Logs in via Employee Portal
   - Can now request leave, ask HR questions, view profile

---

## 🎯 Eligibility Criteria (Admin Configurable)

Admins can configure automatic evaluation rules:

| Setting | Default | Description |
|---------|---------|-------------|
| **Skill Match Threshold** | 50% | Minimum % of required skills candidate must have |
| **Auto-Accept Threshold** | 80% | Candidates scoring above this are auto-accepted |
| **Experience Required** | ✅ Yes | Strict check on minimum experience |
| **Education Required** | ✅ Yes | Strict check on minimum education |

### How to Configure:
1. Login as Admin
2. Go to "🎯 Eligibility Criteria"
3. Adjust sliders and checkboxes
4. Click "💾 Save Criteria"

---

## 📄 Resume Parsing Details

The system automatically extracts:

### **Skills Detected:**
- Programming languages: Python, Java, JavaScript, C++, C#, Ruby, PHP, etc.
- Frameworks: React, Angular, Django, Flask, Spring, Node.js, etc.
- Databases: SQL, MySQL, PostgreSQL, MongoDB, Redis
- Cloud: AWS, Azure, GCP, Docker, Kubernetes
- Marketing: SEO, Digital Marketing, Content Strategy, Analytics
- Soft skills: Leadership, Project Management, Agile, etc.

### **Experience:**
- Extracts patterns like "5 years of experience", "3+ years in", etc.
- Returns total years of experience

### **Education:**
- Detects: PhD, Master's Degree, Bachelor's Degree, Diploma, High School
- Returns highest qualification found

---

## 💼 Portal Features Breakdown

### **Candidate Portal**
- ✅ View all active job positions
- ✅ Upload PDF resume
- ✅ Real-time application processing
- ✅ Instant evaluation feedback
- ✅ View extracted profile data
- ✅ See matched skills vs required skills

### **Employee Portal**
- ✅ Dashboard with leave balances
- ✅ Submit leave requests
- ✅ AI-powered HR policy assistant
- ✅ Personal profile management
- ✅ Leave approval notifications
- ✅ Quick action shortcuts

### **Admin Portal**
- ✅ System-wide dashboard with metrics
- ✅ Manage eligibility criteria
- ✅ Add/edit/close job positions
- ✅ Review all applications with scores
- ✅ One-click employee onboarding
- ✅ View all employees
- ✅ Generate audit reports
- ✅ Download reports as JSON

---

## 🏗️ Project Structure

```
HR_Agent/
├── app.py                    # NEW: Multi-portal Streamlit interface
├── hr_agent.py               # UPDATED: Core logic + new functions
├── .env                      # Environment variables (API key)
├── .env.example              # Template for .env
├── requirements.txt          # UPDATED: Added PyPDF2
├── README.md                 # This file
├── app_old.py                # Backup of original single-portal app
└── .venv/                    # Virtual environment
```

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.13 |
| **AI/LLM** | Groq API (Llama 3.1) |
| **Frontend** | Streamlit |
| **PDF Parsing** | PyPDF2 |
| **Authentication** | Session-based (in-memory) |
| **Database** | In-memory simulation (Dict-based) |

---

## 📊 Sample Job Positions

The system comes with 2 pre-configured job positions:

### 1. **Senior Developer**
- Department: Engineering
- Required Skills: Python, Django, REST API, SQL
- Min Experience: 3 years
- Min Education: Bachelor's Degree

### 2. **Marketing Manager**
- Department: Marketing
- Required Skills: Digital Marketing, SEO, Content Strategy, Analytics
- Min Experience: 5 years
- Min Education: Bachelor's Degree

Admins can add more positions via the Admin Portal → Job Positions page.

---

## 🎓 Testing the Complete Flow

### **Test Scenario 1: Successful Application**

1. **Prepare a test PDF resume** with:
   - Text mentioning "Python, Django, SQL, 5 years experience"
   - Education section with "Bachelor's Degree in Computer Science"

2. **Apply as Candidate:**
   - Go to http://localhost:8501
   - Click "Apply for a Position"
   - Select "Senior Developer"
   - Fill details and upload PDF
   - Submit

3. **Expected Result:**
   - Score ≥ 80% (has all required skills + meets experience)
   - Status: **Accepted** ✅
   - Shows matched skills

4. **Admin onboards candidate:**
   - Login as admin (`admin`/`admin123`)
   - Go to Dashboard → See application
   - Click "Onboard [Name]"
   - System creates employee profile

5. **New employee logs in:**
   - Use generated credentials (shown after onboarding)
   - Access Employee Portal
   - Request leave or ask HR questions

### **Test Scenario 2: Partial Match**

1. Create PDF with only 2 out of 4 required skills
2. Apply for position
3. Expected: Score 50-79% → **Pending Review** ⏳
4. Admin can manually review

### **Test Scenario 3: Rejection**

1. Create PDF with no matching skills or insufficient experience
2. Apply for position
3. Expected: Score < 50% → **Rejected** ❌

---

## 🆘 Troubleshooting

### **Resume not parsing correctly**
- Ensure PDF is text-based (not scanned image)
- Check if PDF has extractable text
- Try saving resume as PDF from Word/Google Docs

### **Skills not detected**
- Skills must be mentioned as-is (e.g., "Python", not "Pythonic")
- Check the skill keywords list in `hr_agent.py` → `parse_resume_text()`
- Admin can adjust thresholds if needed

### **Application stuck on "Processing"**
- Check terminal for errors
- Verify Groq API key is valid
- Restart Streamlit app

### **Login not working**
- Double-check username/password (case-sensitive)
- Use demo credentials provided above
- Clear browser cache and retry

---

## 🎨 Customization

### **Add New Skills to Parser**

Edit `hr_agent.py`, find `parse_resume_text()` method:

```python
skill_keywords = [
    'python', 'java', 'javascript',  # Add your skills here
    'your_custom_skill',
]
```

### **Modify Evaluation Logic**

Edit `hr_agent.py`, find `evaluate_candidate()` method and adjust scoring formulas.

### **Change UI Colors**

Edit `app.py`, find the `<style>` section and modify CSS:

```css
.metric-card {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

---

## 🔒 Security Notes

- **Current Setup:** Demo/development mode with in-memory storage
- **Production Considerations:**
  - Use real database (PostgreSQL, MySQL)
  - Implement proper password hashing (bcrypt, argon2)
  - Add JWT/OAuth for authentication
  - Store resumes in secure cloud storage
  - Add HTTPS/SSL
  - Implement rate limiting
  - Add input validation and sanitization

---

## 📈 Future Enhancements

- [ ] Database persistence (PostgreSQL)
- [ ] Email notifications (SMTP integration)
- [ ] Advanced resume parsing (AI-powered with GPT)
- [ ] Interview scheduling system
- [ ] Candidate messaging portal
- [ ] Employee performance reviews
- [ ] Payroll integration
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard with charts

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure API key is configured
4. Review terminal output for errors

---

## 📄 License

© 2025 All Rights Reserved

---

**Enjoy your complete HR automation platform! 🎉**

**Quick Access:**
- **Run App:** `& ".\.venv\Scripts\python.exe" -m streamlit run app.py`
- **URL:** http://localhost:8501
- **Admin Login:** admin / admin123
