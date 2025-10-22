# HR Agent - Enterprise Automation Platform 🤖

A modern, AI-powered HR automation platform with an attractive web interface built using Python, Groq AI, and Streamlit.

## ✨ Features

- **📝 Leave Request Management** - Automated leave approval workflow with balance tracking
- **🎉 Employee Onboarding** - Streamlined onboarding process for new employees
- **❓ AI-Powered HR Assistant** - Ask policy questions and get instant AI responses with database access
- **📊 Audit Reports** - Comprehensive audit trail and compliance tracking
- **👥 Employee Directory** - View and search all employees with detailed information
- **🔐 Secure API Key Management** - Environment-based configuration

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- A Groq API key (free at https://console.groq.com/)

### 2. Installation

```powershell
# Navigate to the project directory
cd "C:\Users\KALLAI\Desktop\Main Project\HR_Agent"

# The virtual environment is already set up at .venv
# Install dependencies (if needed)
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

### 3. Configure API Key

Edit the `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

Get your free API key from: https://console.groq.com/

### 4. Run the Web Interface

```powershell
# Launch the Streamlit web app
& ".\.venv\Scripts\python.exe" -m streamlit run app.py
```

The app will open automatically in your browser at: **http://localhost:8501**

### 5. Run the CLI Version (Optional)

```powershell
# Run the command-line version
& ".\.venv\Scripts\python.exe" hr_agent.py
```

## 🎨 Web Interface Features

### Dashboard
- Real-time statistics and metrics
- Recent activity feed
- Quick action buttons
- Attractive gradient cards

### Leave Request Management
- Interactive form with employee selection
- Date pickers and leave type selection
- Real-time balance display
- Instant approval/rejection feedback
- Email notifications

### Employee Onboarding
- Step-by-step onboarding wizard
- Automatic credential generation
- Document checklist
- Welcome email automation

### AI HR Assistant
- Quick question templates
- Natural language processing
- Access to employee database
- Policy section recommendations
- Instant AI-powered responses

### Audit Reports
- Customizable date range
- Activity breakdowns
- Compliance status checks
- Downloadable JSON reports
- Visual metrics and charts

### Employee Directory
- Searchable employee list
- Department and position filtering
- Leave balance viewing
- Clean, card-based layout

## 📦 Dependencies

- **groq** (0.33.0) - AI/LLM integration
- **python-dotenv** (1.1.1) - Environment variable management
- **streamlit** (1.50.0) - Web interface framework

## 🏗️ Project Structure

```
HR_Agent/
├── app.py                 # Streamlit web interface (NEW!)
├── hr_agent.py            # Core HR Agent logic
├── .env                   # Environment variables (API keys)
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .venv/                 # Virtual environment
```

## 🎯 Usage Examples

### Process Leave Request
1. Navigate to "📝 Leave Request" from the sidebar
2. Select an employee
3. Choose leave type and dates
4. Enter reason and submit
5. Get instant approval/rejection with updated balance

### Onboard New Employee
1. Go to "🎉 Employee Onboarding"
2. Fill in employee details
3. Submit to generate credentials
4. System sends welcome email automatically

### Ask HR Questions
1. Visit "❓ Ask HR Policy"
2. Use quick question templates or type your own
3. Get AI-powered answers with policy references
4. Access employee database information

### Generate Reports
1. Select "📊 Audit Report"
2. Choose date range
3. View comprehensive activity summary
4. Download full report as JSON

## 🔒 Security

- API keys stored in `.env` file (not in code)
- `.env` file should not be committed to version control
- Use `.env.example` as a template

## 🆘 Troubleshooting

### "No module named 'groq'" error
```powershell
& ".\.venv\Scripts\python.exe" -m pip install groq python-dotenv
```

### "No module named 'streamlit'" error
```powershell
& ".\.venv\Scripts\python.exe" -m pip install streamlit
```

### API Key Not Loading
- Make sure `.env` file exists in the project root
- Verify `GROQ_API_KEY=your_key` is properly set
- No quotes needed around the key

### Port Already in Use
If port 8501 is busy, run with a different port:
```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run app.py --server.port 8502
```

## 🎨 UI Customization

The web interface uses custom CSS for an attractive design:
- Gradient backgrounds
- Modern color schemes
- Responsive layout
- Smooth animations
- Professional cards and boxes

You can customize colors and styles in `app.py` by editing the CSS in the `st.markdown()` section.

## 📊 Tech Stack

- **Backend**: Python 3.13
- **AI/LLM**: Groq API with Llama 3.1
- **Frontend**: Streamlit (Python web framework)
- **State Management**: Session state
- **Styling**: Custom CSS with gradients

## 🌟 Highlights

- ✅ Zero external database required (in-memory simulation)
- ✅ Beautiful, modern web interface
- ✅ AI-powered with database access
- ✅ Complete audit trail
- ✅ Automatic workflows
- ✅ Real-time updates
- ✅ Mobile-responsive design

## 📝 License

© 2025 All Rights Reserved

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure API key is properly configured

---

**Enjoy using the HR Agent! 🚀**
