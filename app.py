"""
HR Agent - Multi-Portal Web Interface with Role-Based Access
Portals: Candidate, Employee, Admin
Built with Streamlit
"""

import streamlit as st
import datetime
from dotenv import load_dotenv
import os
import json
import PyPDF2
import io

# Import the HR Agent components
from hr_agent import (
    Database, LLMInterface, HRAgent, Employee, Candidate,
    JobPosition, User, LeaveRequest
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HR Agent - Enterprise Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling with animations
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Enhanced Button Styles */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        height: 3.5em;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        border: none;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Card Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Success Box with Animation */
    .success-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        color: #155724;
        margin: 1rem 0;
        animation: slideInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    /* Info Box with Animation */
    .info-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid #17a2b8;
        color: #0c5460;
        margin: 1rem 0;
        animation: slideInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.2);
    }
    
    /* Warning Box with Animation */
    .warning-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        color: #856404;
        margin: 1rem 0;
        animation: slideInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
    }
    
    /* Error Box with Animation */
    .error-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        color: #721c24;
        margin: 1rem 0;
        animation: slideInUp 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.2);
    }
    
    /* Enhanced Metric Card */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.4s ease;
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Typography */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 0.8s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
        animation: slideInUp 0.6s ease-out;
    }
    
    h3 {
        color: #34495e;
        font-weight: 500;
    }
    
    /* Form Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        transition: all 0.3s ease;
        font-size: 14px;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stSelectbox>div>div>select:focus,
    .stDateInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        animation: slideInLeft 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Radio Buttons */
    .stRadio>div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateX(5px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #667eea;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInUp 0.6s ease-out;
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Toast Notifications */
    .stAlert {
        border-radius: 12px;
        animation: slideInUp 0.4s ease-out;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()
    
if 'llm' not in st.session_state:
    api_key = os.getenv("GROQ_API_KEY")
    st.session_state.llm = LLMInterface(api_key, st.session_state.db)
    
if 'agent' not in st.session_state:
    st.session_state.agent = HRAgent(st.session_state.db, st.session_state.llm)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# ==================== UTILITY FUNCTIONS ====================

def parse_pdf_resume(uploaded_file):
    """Extract text from uploaded PDF resume"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error parsing PDF: {str(e)}")
        return None

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# ==================== LOGIN PAGE ====================

def show_login_page():
    """Display login page with role selection"""
    
    # Hero Section with Animation
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0 2rem 0; animation: fadeIn 1s ease-out;'>
            <div style='font-size: 5rem; animation: pulse 2s ease-in-out infinite;'>🤖</div>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>HR Agent Portal</h1>
            <p style='font-size: 1.3rem; color: #7f8c8d; font-weight: 300;'>
                AI-Powered Enterprise Automation Platform
            </p>
            <div style='width: 100px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); 
                        margin: 1.5rem auto; border-radius: 2px; animation: slideInUp 0.8s ease-out;'></div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Role selection tabs with enhanced styling
        tab1, tab2, tab3 = st.tabs(["👤 Candidate", "💼 Employee", "⚙️ Admin"])
        
        with tab1:
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                           box-shadow: 0 8px 25px rgba(0,0,0,0.1); animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>
                        <span style='font-size: 2rem;'>👤</span> Candidate Portal
                    </h3>
                    <p style='color: #7f8c8d; font-size: 1.1rem;'>
                        ✨ Apply for job positions and track your applications
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📝 Apply for a Position", use_container_width=True, type="primary"):
                st.session_state.show_application_form = True
                st.rerun()
        
        with tab2:
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                           box-shadow: 0 8px 25px rgba(0,0,0,0.1); animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>
                        <span style='font-size: 2rem;'>💼</span> Employee Login
                    </h3>
                    <p style='color: #7f8c8d;'>Access your employee dashboard and portal</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("employee_login"):
                e_user = st.text_input("Username", key="emp_user")
                e_pass = st.text_input("Password", type="password", key="emp_pass")
                login_btn = st.form_submit_button("Login as Employee", use_container_width=True)
                
                if login_btn:
                    user = st.session_state.db.authenticate_user(e_user, e_pass)
                    if user and user.role == "Employee":
                        st.session_state.logged_in = True
                        st.session_state.current_user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials or not an employee account")
            
            st.markdown("""
                <div class='info-box' style='margin-top: 1rem;'>
                    <strong>📝 Demo Employees:</strong><br>
                    • Username: <code>john.doe</code>, Password: <code>pass123</code><br>
                    • Username: <code>jane.smith</code>, Password: <code>pass123</code>
                </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                           box-shadow: 0 8px 25px rgba(0,0,0,0.1); animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>
                        <span style='font-size: 2rem;'>⚙️</span> Admin Login
                    </h3>
                    <p style='color: #7f8c8d;'>Access administrative dashboard and controls</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.form("admin_login"):
                a_user = st.text_input("Username", key="admin_user")
                a_pass = st.text_input("Password", type="password", key="admin_pass")
                login_btn = st.form_submit_button("Login as Admin", use_container_width=True)
                
                if login_btn:
                    user = st.session_state.db.authenticate_user(a_user, a_pass)
                    if user and user.role == "Admin":
                        st.session_state.logged_in = True
                        st.session_state.current_user = user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials or not an admin account")
            
            st.markdown("""
                <div class='info-box' style='margin-top: 1rem;'>
                    <strong>📝 Demo Admin:</strong><br>
                    • Username: <code>admin</code>, Password: <code>admin123</code>
                </div>
            """, unsafe_allow_html=True)

# ==================== CANDIDATE PORTAL ====================

def show_candidate_portal():
    """Candidate portal for job applications and tests"""
    
    # Check if candidate has a test scheduled
    if 'candidate_id' in st.session_state and st.session_state.get('test_mode', False):
        show_test_interface()
        return
    
    # Modern header with gradient
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; 
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); animation: fadeIn 0.8s ease-out;'>
            <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                👤 Candidate Portal
            </h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                Discover opportunities and showcase your talent
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Show available positions
    st.markdown("""
        <h2 style='display: flex; align-items: center; gap: 0.5rem;'>
            📋 <span>Available Positions</span>
        </h2>
    """, unsafe_allow_html=True)
    
    active_jobs = {jid: job for jid, job in st.session_state.db.job_positions.items() if job.status == "Active"}
    
    if not active_jobs:
        st.info("No active job positions available at the moment.")
        return
    
    # Check if there's a pending test invitation
    if 'test_invitation' in st.session_state and st.session_state.test_invitation:
        invitation = st.session_state.test_invitation
        
        st.balloons()
        st.markdown(f"""
            <div class="success-box">
                <h3>🎉 Congratulations! Application Accepted</h3>
                <p><strong>Score:</strong> {invitation['score']}%</p>
                <p><strong>Message:</strong> {invitation['message']}</p>
                <p><strong>Next Step:</strong> You are invited to take a technical assessment test!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show extracted information
        with st.expander("📊 Your Profile Summary"):
            st.write(f"**Skills Detected:** {', '.join(invitation['skills'])}")
            st.write(f"**Experience:** {invitation['experience']} years")
            st.write(f"**Education:** {invitation['education']}")
            st.write(f"**Matched Skills:** {', '.join(invitation['matched_skills'])}")
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📝 Start Technical Assessment Test", use_container_width=True, type="primary", key="start_test_btn"):
                st.session_state.test_mode = True
                st.session_state.test_invitation = None  # Clear invitation
                st.rerun()
        
        st.markdown("---")
        if st.button("🔙 Apply for Another Position", use_container_width=True):
            st.session_state.test_invitation = None
            st.rerun()
        
        return  # Don't show application forms
    
    # Display job cards in a grid
    cols = st.columns(2)
    for idx, (job_id, job) in enumerate(active_jobs.items()):
        with cols[idx % 2]:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                           box-shadow: 0 6px 20px rgba(0,0,0,0.1); margin-bottom: 1.5rem;
                           border-left: 5px solid #667eea; transition: all 0.3s ease;
                           animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 0.5rem;'>📌 {job.title}</h3>
                    <p style='color: #7f8c8d; font-size: 0.95rem; margin-bottom: 0.5rem;'>
                        <strong>Department:</strong> {job.department}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with st.expander(f"View Details & Apply: {job.title}", expanded=False):
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                    <p><strong>📝 Description:</strong> {job.description}</p>
                    <p><strong>💼 Required Skills:</strong> {', '.join(job.required_skills)}</p>
                    <p><strong>⏳ Min. Experience:</strong> {job.min_experience} years</p>
                    <p><strong>🎓 Education:</strong> {job.min_education}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📄 Apply for this Position")
            
            with st.form(f"apply_form_{job_id}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name *")
                    email = st.text_input("Email *")
                
                with col2:
                    phone = st.text_input("Phone Number *")
                    
                st.markdown("### 📎 Upload Your Resume (PDF)")
                resume_file = st.file_uploader("Upload Resume", type=['pdf'], key=f"resume_{job_id}")
                
                submit = st.form_submit_button("🚀 Submit Application", use_container_width=True)
            
            # Process form submission outside the form
            if submit:
                if name and email and phone and resume_file:
                    with st.spinner("Processing your application..."):
                        # Parse resume
                        resume_text = parse_pdf_resume(resume_file)
                        
                        if resume_text:
                            # Extract information from resume
                            parsed_data = st.session_state.agent.parse_resume_text(resume_text)
                            
                            # Create candidate record
                            candidate_id = f"CAND{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                            candidate = Candidate(
                                candidate_id=candidate_id,
                                name=name,
                                email=email,
                                phone=phone,
                                applied_position=job.title,
                                resume_text=resume_text[:500],  # Store first 500 chars
                                extracted_skills=parsed_data['skills'],
                                experience_years=parsed_data['experience_years'],
                                education=parsed_data['education'],
                                application_date=datetime.datetime.now().isoformat(),
                                status="Pending",
                                test_taken=False,
                                test_score=None
                            )
                            
                            st.session_state.db.add_candidate(candidate)
                            
                            # Evaluate candidate
                            result = st.session_state.agent.evaluate_candidate(candidate, job)
                            
                            evaluation = result['evaluation']
                            
                            # Show result
                            if evaluation['decision'] == "Accepted":
                                # Update candidate status
                                candidate.status = "Test_Scheduled"
                                st.session_state.db.candidates[candidate_id] = candidate
                                
                                # Store candidate ID for test
                                st.session_state.candidate_id = candidate_id
                                st.session_state.candidate_job_id = job_id
                                
                                # Store invitation in session state so it persists across reruns
                                st.session_state.test_invitation = {
                                    'score': evaluation['score'],
                                    'message': evaluation['message'],
                                    'skills': parsed_data['skills'],
                                    'experience': parsed_data['experience_years'],
                                    'education': parsed_data['education'],
                                    'matched_skills': evaluation['matched_skills']
                                }
                                
                                st.rerun()  # Rerun to show the invitation
                            
                            elif evaluation['decision'] == "Pending Review":
                                st.markdown(f"""
                                    <div class="warning-box">
                                        <h3>⏳ Application Under Review</h3>
                                        <p><strong>Score:</strong> {evaluation['score']}%</p>
                                        <p><strong>Message:</strong> {evaluation['message']}</p>
                                        <p>Your application will be reviewed by our HR team.</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            else:  # Rejected
                                st.markdown(f"""
                                    <div class="error-box">
                                        <h3>❌ Application Not Accepted</h3>
                                        <p><strong>Score:</strong> {evaluation['score']}%</p>
                                        <p><strong>Reason:</strong> {evaluation['message']}</p>
                                        <p>We encourage you to apply for other positions that match your profile.</p>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        else:
                            st.error("Failed to parse resume. Please ensure it's a valid PDF.")
                else:
                    st.error("Please fill all required fields and upload your resume.")
    
    # Back button
    st.markdown("---")
    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state.show_application_form = False
        st.session_state.logged_in = False
        st.rerun()


def show_test_interface():
    """Display test interface for selected candidates"""
    
    candidate_id = st.session_state.candidate_id
    job_id = st.session_state.candidate_job_id
    
    candidate = st.session_state.db.candidates.get(candidate_id)
    job = st.session_state.db.job_positions.get(job_id)
    
    if not candidate or not job:
        st.error("Test session invalid. Please apply again.")
        st.session_state.test_mode = False
        st.rerun()
        return
    
    st.title(f"📝 Technical Assessment Test - {job.title}")
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;">
            <h3 style="margin:0; color: white;">Candidate: {candidate.name}</h3>
            <p style="margin:0.5rem 0 0 0; color: white;">Position: {job.title}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not job.test_questions:
        st.error("No test questions available for this position.")
        return
    
    st.markdown("### 📋 Instructions")
    st.info(f"""
        - Total Questions: {len(job.test_questions)}
        - Passing Score: 60%
        - Please select the best answer for each question
        - Click Submit when you're ready
    """)
    
    st.markdown("---")
    
    # Initialize answers in session state
    if 'test_answers' not in st.session_state:
        st.session_state.test_answers = {}
    
    # Display questions
    with st.form("test_form"):
        for idx, question in enumerate(job.test_questions, 1):
            st.markdown(f"### Question {idx}")
            st.markdown(f"**{question['question']}**")
            
            answer = st.radio(
                "Select your answer:",
                options=question['options'],
                key=f"q_{idx}",
                label_visibility="collapsed"
            )
            
            st.session_state.test_answers[idx] = answer
            st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_test = st.form_submit_button("✅ Submit Test", use_container_width=True, type="primary")
    
    if submit_test:
        # Calculate score
        correct_answers = 0
        total_questions = len(job.test_questions)
        
        for idx, question in enumerate(job.test_questions, 1):
            user_answer = st.session_state.test_answers.get(idx)
            if user_answer == question['correct_answer']:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100
        passed = score >= 60  # 60% passing score
        
        # Update candidate record
        st.session_state.db.update_candidate_test_status(candidate_id, score, passed)
        
        with st.spinner("Processing your test results..."):
            if passed:
                # Convert to employee
                username, password, employee_id = st.session_state.db.convert_candidate_to_employee(candidate_id)
                
                if username and password:
                    # Debug: Show what credentials were created
                    print(f"✅ Created employee credentials:")
                    print(f"   Username: {username}")
                    print(f"   Password: {password}")
                    print(f"   Employee ID: {employee_id}")
                    
                    # Verify user was added to database
                    test_user = st.session_state.db.authenticate_user(username, password)
                    print(f"   Verification: {test_user is not None}")
                    
                    # Send email with LLM-generated content
                    email_result = st.session_state.agent.send_test_result_email(
                        candidate_email=candidate.email,
                        candidate_name=candidate.name,
                        passed=True,
                        test_score=score,
                        position=job.title,
                        username=username,
                        password=password
                    )
                    
                    st.balloons()
                    st.markdown(f"""
                        <div class="success-box">
                            <h2>🎉 Congratulations! You Passed!</h2>
                            <p><strong>Score:</strong> {score:.1f}% ({correct_answers}/{total_questions} correct)</p>
                            <p><strong>Status:</strong> You are now hired as a {job.title}!</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### � Email Notification")
                    if email_result['status'] == 'success':
                        st.success(f"✅ {email_result['message']}")
                        st.info("🔐 Your employee portal credentials have been sent to your email. Please check your inbox!")
                    else:
                        st.warning(f"⚠️ {email_result['message']}")
                    
            else:
                # Send rejection email
                email_result = st.session_state.agent.send_test_result_email(
                    candidate_email=candidate.email,
                    candidate_name=candidate.name,
                    passed=False,
                    test_score=score,
                    position=job.title
                )
                
                st.markdown(f"""
                    <div class="error-box">
                        <h2>📊 Test Results</h2>
                        <p><strong>Score:</strong> {score:.1f}% ({correct_answers}/{total_questions} correct)</p>
                        <p><strong>Passing Score:</strong> 60%</p>
                        <p><strong>Status:</strong> Unfortunately, you did not pass the test.</p>
                        <p>We encourage you to improve your skills and apply again in the future!</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📧 Email Notification")
                if email_result['status'] == 'success':
                    st.success(f"✅ {email_result['message']}")
                else:
                    st.warning(f"⚠️ {email_result['message']}")
        
        # Mark test as submitted to persist results
        st.session_state.test_submitted = True
        
    # Always show return button after test (check if test was submitted OR if currently submitting)
    if st.session_state.get('test_submitted', False) or submit_test:
        # Clear test session
        st.markdown("---")
        if st.button("🔙 Return to Main Page", use_container_width=True, key="return_btn"):
            st.session_state.test_mode = False
            st.session_state.logged_in = False
            st.session_state.test_submitted = False
            if 'test_answers' in st.session_state:
                del st.session_state.test_answers
            st.rerun()

# ==================== EMPLOYEE PORTAL ====================

def show_employee_portal():
    """Employee portal for leave requests and HR queries"""
    
    user = st.session_state.current_user
    employee = st.session_state.db.get_employee(user.employee_id)
    
    with st.sidebar:
        # Enhanced sidebar with gradient background
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       padding: 2rem 1rem; border-radius: 15px; margin-bottom: 1.5rem;
                       text-align: center; animation: fadeIn 0.8s ease-out;'>
                <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>💼</div>
                <h3 style='color: white; margin: 0.5rem 0; -webkit-text-fill-color: white;'>{employee.name}</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem; margin: 0.3rem 0;'>{employee.position}</p>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>ID: {employee.employee_id}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        page = st.radio(
            "Navigate:",
            ["🏠 Dashboard", "📝 Leave Request", "❓ Ask HR Policy", "👤 My Profile"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    if page == "🏠 Dashboard":
        # Modern dashboard header
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    🏠 Welcome, {employee.name}!
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    Here's your dashboard overview
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; color:white;">{employee.leave_balance.get('Casual Leave', 0)}</h3>
                    <p style="margin:0.5rem 0; color:white;">Casual Leave</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3 style="margin:0; color:white;">{employee.leave_balance.get('Sick Leave', 0)}</h3>
                    <p style="margin:0.5rem 0; color:white;">Sick Leave</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3 style="margin:0; color:white;">{employee.leave_balance.get('Annual Leave', 0)}</h3>
                    <p style="margin:0.5rem 0; color:white;">Annual Leave</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick Actions Section
        st.markdown("""
            <h2 style='margin-bottom: 1.5rem;'>⚡ Quick Actions</h2>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("📝 Request Leave", use_container_width=True)
        with col2:
            st.button("❓ Ask HR Question", use_container_width=True)
    
    elif page == "📝 Leave Request":
        # Modern leave request header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    📝 Request Leave
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    Submit your leave application
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("leave_request_form"):
            leave_type = st.selectbox(
                "Leave Type",
                options=["Casual Leave", "Sick Leave", "Annual Leave", "Unpaid Leave"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=datetime.date.today())
            with col2:
                end_date = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=1))
            
            reason = st.text_area("Reason for Leave", placeholder="Enter reason...", height=100)
            
            submitted = st.form_submit_button("🚀 Submit Request", use_container_width=True)
        
        # Process outside the form to avoid state issues
        if submitted:
            if not reason.strip():
                st.error("❌ Please provide a reason for your leave request.")
            elif start_date > end_date:
                st.error("❌ End date must be after or equal to start date.")
            else:
                result = st.session_state.agent.process_leave_request(
                    employee_id=employee.employee_id,
                    leave_type=leave_type,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    reason=reason
                )
                
                if result['status'] == 'success':
                    decision = result['decision']
                    email_result = result.get('email_result', {})
                    
                    if decision == 'Approved':
                        st.success(f"✅ Leave Approved! Request ID: {result['request_id']}")
                    elif decision == 'Rejected':
                        st.error(f"❌ Leave Rejected: {result['message']}")
                    else:
                        st.warning(f"⏳ Leave Pending: {result['message']}")
                    
                    # Show email notification status
                    st.markdown("---")
                    st.markdown("### 📧 Email Notification")
                    if email_result.get('status') == 'success':
                        st.success(f"✅ {email_result['message']}")
                        st.info("📬 A detailed notification has been sent to your email!")
                    else:
                        st.warning(f"⚠️ {email_result.get('message', 'Email could not be sent')}")
                    
                    with st.expander("📄 View Email Content"):
                        st.markdown(f"**Subject:** {email_result.get('subject', 'N/A')}")
                        st.text(email_result.get('email_content', 'No content available'))
                
                elif result['status'] == 'error':
                    st.error(f"❌ Error: {result['message']}")
                    
                    # Check if there's an email result for date conflict
                    email_result = result.get('email_result', {})
                    if email_result:
                        st.markdown("### 📧 Email Notification")
                        if email_result.get('status') == 'success':
                            st.info("📬 A notification has been sent to your email.")
                        with st.expander("📄 View Email Content"):
                            st.markdown(f"**Subject:** {email_result.get('subject', 'N/A')}")
                            st.text(email_result.get('email_content', 'No content available'))
        
        # Show leave balance with enhanced cards
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <h2 style='margin-bottom: 1.5rem;'>📊 Your Leave Balance</h2>
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(employee.leave_balance))
        colors = [
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        ]
        
        for idx, (leave_type, balance) in enumerate(employee.leave_balance.items()):
            with cols[idx]:
                st.markdown(f"""
                    <div style='background: {colors[idx % len(colors)]};
                               padding: 2rem; border-radius: 15px; text-align: center;
                               box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                               transition: transform 0.3s ease; animation: fadeIn 0.8s ease-out;'>
                        <h2 style='color: white; margin: 0; font-size: 2.5rem;'>{balance}</h2>
                        <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 1rem;'>
                            {leave_type}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
    elif page == "❓ Ask HR Policy":
        # Modern HR Policy header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    ❓ Ask HR Policy Questions
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    Get instant answers powered by AI
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        question = st.text_area("Your Question", placeholder="Ask anything about HR policies...", height=100)
        
        if st.button("🤖 Get Answer", use_container_width=True):
            if question.strip():
                with st.spinner("AI is thinking..."):
                    result = st.session_state.agent.ask_hr_policy_question(question, employee.employee_id)
                
                if result['status'] == 'success':
                    st.markdown("### 💬 Answer")
                    st.info(result['answer'])
                    
                    if result['relevant_policies']:
                        with st.expander("📚 Relevant Policies"):
                            for policy in result['relevant_policies']:
                                st.write(f"• {policy}")
    
    elif page == "👤 My Profile":
        # Modern profile header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    👤 My Profile
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    View and manage your information
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 15px;
                           box-shadow: 0 6px 20px rgba(0,0,0,0.1); animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>👤 Personal Information</h3>
                </div>
            """, unsafe_allow_html=True)
            st.write(f"**Name:** {employee.name}")
            st.write(f"**Employee ID:** {employee.employee_id}")
            st.write(f"**Email:** {employee.email}")
            st.write(f"**Department:** {employee.department}")
        
        with col2:
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 15px;
                           box-shadow: 0 6px 20px rgba(0,0,0,0.1); animation: slideInUp 0.6s ease-out;'>
                    <h3 style='color: #667eea; margin-bottom: 1rem;'>💼 Employment Details</h3>
                </div>
            """, unsafe_allow_html=True)
            st.write(f"**Position:** {employee.position}")
            st.write(f"**Join Date:** {employee.join_date}")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <h2 style='margin-bottom: 1.5rem;'>📊 Leave Balance Summary</h2>
        """, unsafe_allow_html=True)
        
        for leave_type, balance in employee.leave_balance.items():
            st.progress(balance / 20, text=f"{leave_type}: {balance} days")

# ==================== ADMIN PORTAL ====================

def show_admin_portal():
    """Admin portal for managing system"""
    
    with st.sidebar:
        # Enhanced admin sidebar
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                       padding: 2rem 1rem; border-radius: 15px; margin-bottom: 1.5rem;
                       text-align: center; animation: fadeIn 0.8s ease-out;'>
                <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>⚙️</div>
                <h3 style='color: white; margin: 0.5rem 0; -webkit-text-fill-color: white;'>Admin Portal</h3>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem;'>Administrator</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        page = st.radio(
            "Navigate:",
            ["🏠 Dashboard", "🎯 Eligibility Criteria", "👥 View Employees", 
             "📋 Manage Applications", "📊 Audit Report", "💼 Job Positions"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    if page == "🏠 Dashboard":
        # Modern admin dashboard header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    ⚙️ Admin Dashboard
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    Manage your organization efficiently
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_data = [
            ("Total Employees", len(st.session_state.db.employees), "👥", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
            ("Active Jobs", sum(1 for j in st.session_state.db.job_positions.values() if j.status == "Active"), "💼", "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"),
            ("Applications", len(st.session_state.db.candidates), "📋", "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"),
            ("Audit Logs", len(st.session_state.db.audit_logs), "📊", "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)")
        ]
        
        for col, (label, value, icon, gradient) in zip([col1, col2, col3, col4], metrics_data):
            with col:
                st.markdown(f"""
                    <div style='background: {gradient}; padding: 2rem 1rem; border-radius: 15px;
                               text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                               animation: fadeIn 0.8s ease-out; transition: transform 0.3s ease;'>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
                        <h2 style='color: white; margin: 0; font-size: 2rem;'>{value}</h2>
                        <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; font-size: 0.9rem;'>
                            {label}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📋 Recent Applications")
        
        if st.session_state.db.candidates:
            for cand_id, cand in list(st.session_state.db.candidates.items())[-5:]:
                job = st.session_state.db.get_job_position(cand.applied_position)
                with st.expander(f"{cand.name} - {job.title if job else 'Unknown'} ({cand.status})"):
                    st.write(f"**Email:** {cand.email}")
                    st.write(f"**Phone:** {cand.phone}")
                    st.write(f"**Experience:** {cand.experience_years} years")
                    st.write(f"**Education:** {cand.education}")
                    st.write(f"**Skills:** {', '.join(cand.extracted_skills)}")
                    
                    if cand.evaluation_result:
                        st.write(f"**Score:** {cand.evaluation_result['score']}%")
                        st.write(f"**Decision:** {cand.evaluation_result['decision']}")
                    
                    if cand.status == "Accepted":
                        if st.button(f"✅ Onboard {cand.name}", key=f"onboard_{cand_id}"):
                            # Trigger onboarding
                            result = st.session_state.agent.handle_employee_onboarding(
                                name=cand.name,
                                email=cand.email,
                                department=job.department if job else "General",
                                position=job.title if job else "Employee",
                                join_date=datetime.date.today().strftime("%Y-%m-%d")
                            )
                            
                            if result['status'] == 'success':
                                st.success(f"✅ {cand.name} onboarded successfully! Employee ID: {result['employee_id']}")
                                # Create employee login
                                username = cand.email.split('@')[0]
                                new_user = User(
                                    username=username,
                                    password="welcome123",
                                    role="Employee",
                                    employee_id=result['employee_id']
                                )
                                st.session_state.db.add_user(new_user)
                                st.info(f"Login created - Username: {username}, Password: welcome123")
        else:
            st.info("No applications yet")
    
    elif page == "🎯 Eligibility Criteria":
        st.title("🎯 Set Eligibility Criteria")
        
        criteria = st.session_state.db.eligibility_criteria
        
        with st.form("criteria_form"):
            st.markdown("### Configure Automatic Evaluation Rules")
            
            skill_threshold = st.slider(
                "Minimum Skill Match Percentage",
                min_value=0,
                max_value=100,
                value=criteria.get('skill_match_threshold', 50),
                help="Minimum percentage of required skills candidate must have"
            )
            
            auto_accept_threshold = st.slider(
                "Auto-Accept Threshold",
                min_value=0,
                max_value=100,
                value=criteria.get('auto_accept_threshold', 50),
                help="Candidates scoring above this are automatically accepted"
            )
            
            exp_required = st.checkbox(
                "Experience Required (Strict)",
                value=criteria.get('experience_required', True),
                help="Reject if minimum experience not met"
            )
            
            edu_required = st.checkbox(
                "Education Required (Strict)",
                value=criteria.get('education_required', True),
                help="Reject if minimum education not met"
            )
            
            if st.form_submit_button("💾 Save Criteria", use_container_width=True):
                new_criteria = {
                    'skill_match_threshold': skill_threshold,
                    'auto_accept_threshold': auto_accept_threshold,
                    'experience_required': exp_required,
                    'education_required': edu_required
                }
                st.session_state.db.update_eligibility_criteria(new_criteria)
                st.success("✅ Eligibility criteria updated successfully!")
        
        st.markdown("---")
        st.markdown("### Current Criteria")
        st.json(st.session_state.db.eligibility_criteria)
    
    elif page == "👥 View Employees":
        st.title("👥 Employee Directory")
        
        if st.session_state.db.employees:
            for emp_id, emp in st.session_state.db.employees.items():
                with st.expander(f"{emp.name} - {emp.position}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {emp.employee_id}")
                        st.write(f"**Email:** {emp.email}")
                        st.write(f"**Department:** {emp.department}")
                    with col2:
                        st.write(f"**Position:** {emp.position}")
                        st.write(f"**Join Date:** {emp.join_date}")
                    
                    st.markdown("**Leave Balance:**")
                    for leave_type, balance in emp.leave_balance.items():
                        st.write(f"- {leave_type}: {balance} days")
        else:
            st.info("No employees in the system")
    
    elif page == "📋 Manage Applications":
        st.title("📋 Manage Candidate Applications")
        
        if st.session_state.db.candidates:
            # Filter options
            filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Accepted", "Rejected", "Pending Review"])
            
            for cand_id, cand in st.session_state.db.candidates.items():
                if filter_status == "All" or cand.status == filter_status:
                    job = st.session_state.db.get_job_position(cand.applied_position)
                    
                    with st.expander(f"📄 {cand.name} - {job.title if job else 'N/A'} [{cand.status}]"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Email:** {cand.email}")
                            st.write(f"**Phone:** {cand.phone}")
                            st.write(f"**Applied:** {cand.application_date[:10]}")
                            st.write(f"**Experience:** {cand.experience_years} years")
                            st.write(f"**Education:** {cand.education}")
                            st.write(f"**Skills:** {', '.join(cand.extracted_skills)}")
                        
                        with col2:
                            if cand.evaluation_result:
                                st.metric("Score", f"{cand.evaluation_result['score']}%")
                                st.write(f"**Status:** {cand.evaluation_result['decision']}")
                        
                        if cand.evaluation_result:
                            with st.expander("📊 Evaluation Details"):
                                st.json(cand.evaluation_result)
                        
                        if cand.status == "Accepted":
                            st.success("✅ This candidate has been accepted")
                            if st.button(f"👤 Start Onboarding", key=f"onboard_mgmt_{cand_id}"):
                                result = st.session_state.agent.handle_employee_onboarding(
                                    name=cand.name,
                                    email=cand.email,
                                    department=job.department if job else "General",
                                    position=job.title if job else "Employee",
                                    join_date=datetime.date.today().strftime("%Y-%m-%d")
                                )
                                if result['status'] == 'success':
                                    st.balloons()
                                    st.success(f"🎉 Onboarding complete! Employee ID: {result['employee_id']}")
        else:
            st.info("No applications received yet")
    
    elif page == "📊 Audit Report":
        # Modern audit report header
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                       padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem;
                       box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
                       animation: fadeIn 0.8s ease-out;'>
                <h1 style='color: white; margin: 0; -webkit-text-fill-color: white;'>
                    📊 Audit Report
                </h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;'>
                    Generate comprehensive activity reports
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.date.today())
        
        if st.button("📊 Generate Report", use_container_width=True):
            try:
                with st.spinner("Generating report..."):
                    result = st.session_state.agent.generate_audit_report(
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d")
                    )
                
                if result.get('status') == 'error':
                    st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
                elif result.get('summary'):
                    summary = result['summary']
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Activities", summary.get('total_activities', 0))
                    with col2:
                        leave_data = summary.get('leave_requests', {})
                        st.metric("Leave Requests", leave_data.get('total', 0))
                    with col3:
                        st.metric("Onboarding", summary.get('onboarding', 0))
                    
                    st.markdown("---")
                    
                    # Display detailed logs
                    if result.get('detailed_logs'):
                        st.markdown("### 📋 Activity Logs")
                        logs_to_show = result['detailed_logs'][:10]
                        if logs_to_show:
                            for log in logs_to_show:
                                with st.expander(f"🔹 {log.get('action', 'N/A')} - {log.get('timestamp', '')[:19]}"):
                                    st.write(f"**User:** {log.get('user', 'N/A')}")
                                    if log.get('details'):
                                        st.json(log['details'])
                        else:
                            st.info("No activity logs found for the selected period.")
                    else:
                        st.info("No detailed logs available for this period.")
                    
                    # Download button
                    if result.get('report_id'):
                        st.download_button(
                            "📥 Download Report (JSON)",
                            data=json.dumps(result, indent=2),
                            file_name=f"audit_{result['report_id']}.json",
                            mime="application/json"
                        )
                else:
                    st.warning("⚠️ No data available for the selected period.")
                    
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
                st.exception(e)
    
    elif page == "💼 Job Positions":
        st.title("💼 Manage Job Positions")
        
        st.markdown("### ➕ Add New Position")
        with st.form("new_job_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Job Title")
                department = st.text_input("Department")
            with col2:
                min_exp = st.number_input("Min Experience (years)", min_value=0, value=2)
                min_edu = st.selectbox("Min Education", ["High School", "Bachelor's Degree", "Master's Degree", "PhD"])
            
            description = st.text_area("Description")
            skills = st.text_input("Required Skills (comma-separated)")
            
            if st.form_submit_button("➕ Add Position"):
                if title and department and skills:
                    job_id = f"JOB{len(st.session_state.db.job_positions) + 1:03d}"
                    job = JobPosition(
                        job_id=job_id,
                        title=title,
                        department=department,
                        description=description,
                        required_skills=[s.strip() for s in skills.split(',')],
                        min_experience=min_exp,
                        min_education=min_edu,
                        status="Active"
                    )
                    st.session_state.db.add_job_position(job)
                    st.success(f"✅ Job position '{title}' added!")
        
        st.markdown("---")
        st.markdown("### Current Job Positions")
        
        for job_id, job in st.session_state.db.job_positions.items():
            with st.expander(f"📌 {job.title} - {job.department} [{job.status}]"):
                st.write(f"**Description:** {job.description}")
                st.write(f"**Required Skills:** {', '.join(job.required_skills)}")
                st.write(f"**Min Experience:** {job.min_experience} years")
                st.write(f"**Min Education:** {job.min_education}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if job.status == "Active":
                        if st.button(f"❌ Close Position", key=f"close_{job_id}"):
                            job.status = "Closed"
                            st.success("Position closed")
                            st.rerun()
                with col2:
                    if job.status == "Closed":
                        if st.button(f"✅ Reopen Position", key=f"open_{job_id}"):
                            job.status = "Active"
                            st.success("Position reopened")
                            st.rerun()

# ==================== MAIN APP LOGIC ====================

def main():
    """Main application logic"""
    
    # Check if user wants to see application form
    if hasattr(st.session_state, 'show_application_form') and st.session_state.show_application_form:
        show_candidate_portal()
    elif not st.session_state.logged_in:
        show_login_page()
    else:
        user = st.session_state.current_user
        
        if user.role == "Candidate":
            show_candidate_portal()
        elif user.role == "Employee":
            show_employee_portal()
        elif user.role == "Admin":
            show_admin_portal()
        else:
            st.error("Unknown user role")
            logout()

# Enhanced Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;
               box-shadow: 0 -5px 20px rgba(102, 126, 234, 0.3); animation: fadeIn 1s ease-out;'>
        <p style='color: white; margin: 0; font-size: 1.1rem; font-weight: 500;'>
            🤖 <strong>HR Agent Enterprise Platform</strong>
        </p>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
            AI-Powered Multi-Portal Access System | © 2025
        </p>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
