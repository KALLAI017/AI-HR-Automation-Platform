"""
HR Agent - Modern Web Interface
Built with Streamlit for an attractive, professional user experience
"""

import streamlit as st
import datetime
from dotenv import load_dotenv
import os
import json

# Import the HR Agent components
from hr_agent import Database, LLMInterface, HRAgent, Employee

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="HR Agent - Enterprise Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for attractive styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .employee-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    h2, h3 {
        color: #34495e;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
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

# Sidebar navigation
with st.sidebar:
    st.markdown("# 🤖 HR Agent")
    st.markdown("### Enterprise Automation Platform")
    st.markdown("---")
    
    page = st.radio(
        "Navigate to:",
        ["🏠 Dashboard", "📝 Leave Request", "🎉 Employee Onboarding", 
         "❓ Ask HR Policy", "📊 Audit Report", "👥 View Employees"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # API Status indicator
    if st.session_state.llm.client:
        st.success("✅ AI Model: Active")
    else:
        st.warning("⚠️ AI Model: Offline (Using fallback)")
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Employees", len(st.session_state.db.employees))
    st.metric("Leave Requests", len(st.session_state.db.leave_requests))
    st.metric("Audit Logs", len(st.session_state.db.audit_logs))

# Main content area
if page == "🏠 Dashboard":
    st.title("🏠 HR Agent Dashboard")
    st.markdown("### Welcome to the Enterprise HR Automation Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h2 style="margin:0; color:white;">👥</h2>
                <h3 style="margin:0.5rem 0; color:white;">{}</h3>
                <p style="margin:0; color:white;">Total Employees</p>
            </div>
        """.format(len(st.session_state.db.employees)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h2 style="margin:0; color:white;">📝</h2>
                <h3 style="margin:0.5rem 0; color:white;">{}</h3>
                <p style="margin:0; color:white;">Leave Requests</p>
            </div>
        """.format(len(st.session_state.db.leave_requests)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h2 style="margin:0; color:white;">📊</h2>
                <h3 style="margin:0.5rem 0; color:white;">{}</h3>
                <p style="margin:0; color:white;">Audit Logs</p>
            </div>
        """.format(len(st.session_state.db.audit_logs)), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    
    if st.session_state.db.audit_logs:
        recent_logs = st.session_state.db.audit_logs[-5:][::-1]  # Last 5, reversed
        for log in recent_logs:
            with st.expander(f"🔹 {log.action} - {log.timestamp[:19]}", expanded=False):
                st.write(f"**Agent:** {log.agent}")
                st.write(f"**User:** {log.user}")
                st.write(f"**Details:** {json.dumps(log.details, indent=2)}")
    else:
        st.info("No recent activity. Start by processing a leave request or onboarding an employee!")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Process Leave Request", use_container_width=True):
            st.session_state.quick_nav = "📝 Leave Request"
            st.rerun()
    
    with col2:
        if st.button("🎉 Onboard Employee", use_container_width=True):
            st.session_state.quick_nav = "🎉 Employee Onboarding"
            st.rerun()
    
    with col3:
        if st.button("❓ Ask HR Question", use_container_width=True):
            st.session_state.quick_nav = "❓ Ask HR Policy"
            st.rerun()

elif page == "📝 Leave Request":
    st.title("📝 Process Leave Request")
    st.markdown("Submit and process employee leave requests with automatic approval workflow")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("leave_request_form"):
            st.markdown("### Leave Request Details")
            
            # Employee selection
            employee_ids = list(st.session_state.db.employees.keys())
            employee_names = [f"{emp.name} ({emp_id})" for emp_id, emp in st.session_state.db.employees.items()]
            
            selected_employee = st.selectbox(
                "Select Employee",
                options=employee_names,
                index=0
            )
            employee_id = selected_employee.split("(")[1].strip(")")
            
            # Leave type
            leave_type = st.selectbox(
                "Leave Type",
                options=["Casual Leave", "Sick Leave", "Annual Leave", "Unpaid Leave"]
            )
            
            # Date range
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                start_date = st.date_input("Start Date", value=datetime.date.today())
            with col_date2:
                end_date = st.date_input("End Date", value=datetime.date.today() + datetime.timedelta(days=2))
            
            # Reason
            reason = st.text_area("Reason for Leave", placeholder="Enter reason for leave request...")
            
            # Submit button
            submitted = st.form_submit_button("🚀 Submit Leave Request", use_container_width=True)
            
            if submitted:
                if reason.strip():
                    with st.spinner("Processing leave request..."):
                        result = st.session_state.agent.process_leave_request(
                            employee_id=employee_id,
                            leave_type=leave_type,
                            start_date=start_date.strftime("%Y-%m-%d"),
                            end_date=end_date.strftime("%Y-%m-%d"),
                            reason=reason
                        )
                    
                    if result['status'] == 'success':
                        decision = result['decision']
                        if decision == 'Approved':
                            st.markdown(f"""
                                <div class="success-box">
                                    <h3>✅ Leave Request Approved!</h3>
                                    <p><strong>Request ID:</strong> {result['request_id']}</p>
                                    <p><strong>Message:</strong> {result['message']}</p>
                                    <p>✉️ Notification has been sent to the employee.</p>
                                </div>
                            """, unsafe_allow_html=True)
                        elif decision == 'Rejected':
                            st.markdown(f"""
                                <div class="error-box">
                                    <h3>❌ Leave Request Rejected</h3>
                                    <p><strong>Request ID:</strong> {result['request_id']}</p>
                                    <p><strong>Reason:</strong> {result['message']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:  # Pending
                            st.markdown(f"""
                                <div class="warning-box">
                                    <h3>⏳ Leave Request Pending</h3>
                                    <p><strong>Request ID:</strong> {result['request_id']}</p>
                                    <p><strong>Message:</strong> {result['message']}</p>
                                    <p>📧 Manager approval required.</p>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("Please provide a reason for the leave request.")
    
    with col2:
        st.markdown("### 📊 Employee Leave Balance")
        if employee_id in st.session_state.db.employees:
            emp = st.session_state.db.employees[employee_id]
            st.markdown(f"**{emp.name}**")
            st.markdown(f"*{emp.position}*")
            st.markdown("---")
            
            for leave_type_name, balance in emp.leave_balance.items():
                st.metric(leave_type_name, f"{balance} days")

elif page == "🎉 Employee Onboarding":
    st.title("🎉 Employee Onboarding")
    st.markdown("Streamlined onboarding process for new employees")
    
    with st.form("onboarding_form"):
        st.markdown("### New Employee Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="John Smith")
            email = st.text_input("Email Address *", placeholder="john.smith@company.com")
            department = st.selectbox(
                "Department *",
                options=["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
            )
        
        with col2:
            position = st.text_input("Position *", placeholder="Senior Developer")
            join_date = st.date_input("Join Date *", value=datetime.date.today())
        
        st.markdown("---")
        
        submitted = st.form_submit_button("🚀 Start Onboarding Process", use_container_width=True)
        
        if submitted:
            if name and email and department and position:
                with st.spinner("Processing employee onboarding..."):
                    result = st.session_state.agent.handle_employee_onboarding(
                        name=name,
                        email=email,
                        department=department,
                        position=position,
                        join_date=join_date.strftime("%Y-%m-%d")
                    )
                
                if result['status'] == 'success':
                    st.balloons()
                    st.markdown(f"""
                        <div class="success-box">
                            <h3>🎉 Employee Onboarding Successful!</h3>
                            <p><strong>Employee ID:</strong> {result['employee_id']}</p>
                            <p><strong>Name:</strong> {name}</p>
                            <p><strong>Department:</strong> {department}</p>
                            <p><strong>Position:</strong> {position}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Show credentials
                    st.markdown("### 🔐 Login Credentials")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**Username:** {result['credentials']['username']}")
                    with col2:
                        st.info(f"**Temp Password:** {result['credentials']['temp_password']}")
                    
                    # Show documents
                    st.markdown("### 📄 Onboarding Documents")
                    for doc in result['documents']:
                        st.write(f"✅ {doc}")
                    
                    st.success("📧 Welcome email has been sent to the new employee!")
            else:
                st.error("Please fill in all required fields marked with *")

elif page == "❓ Ask HR Policy":
    st.title("❓ Ask HR Policy Questions")
    st.markdown("Get instant answers to HR policy questions using AI (with database access)")
    
    # Quick question templates
    st.markdown("### 💡 Quick Questions")
    quick_questions = [
        "How many sick leave days do I get per year?",
        "What is the company's remote work policy?",
        "What documents are needed for onboarding?",
        "What are the working hours?",
        "Tell me about John Doe's leave balance",
        "Who works in the Engineering department?"
    ]
    
    cols = st.columns(3)
    for idx, question in enumerate(quick_questions):
        with cols[idx % 3]:
            if st.button(f"📌 {question[:30]}...", key=f"quick_{idx}", use_container_width=True):
                st.session_state.selected_question = question
    
    st.markdown("---")
    
    # Custom question input
    if 'selected_question' in st.session_state:
        default_question = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        default_question = ""
    
    question = st.text_area(
        "Your Question",
        value=default_question,
        placeholder="Ask any question about HR policies or employee information...",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        ask_button = st.button("🤖 Ask AI", use_container_width=True, type="primary")
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    if ask_button and question.strip():
        with st.spinner("🤖 AI is thinking..."):
            result = st.session_state.agent.ask_hr_policy_question(question)
        
        if result['status'] == 'success':
            st.markdown("### 💬 Answer")
            st.markdown(f"""
                <div class="info-box">
                    {result['answer']}
                </div>
            """, unsafe_allow_html=True)
            
            # Show relevant policies
            if result['relevant_policies']:
                with st.expander("📚 Relevant Policy Sections"):
                    for policy in result['relevant_policies']:
                        st.write(f"• {policy}")
            
            # Show if database was accessed
            if result.get('employee_data_accessed'):
                st.success("🔍 Employee database was accessed for this answer")

elif page == "📊 Audit Report":
    st.title("📊 Generate Audit Report")
    st.markdown("Comprehensive audit trail of all HR activities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.date.today() - datetime.timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.date.today()
        )
    
    if st.button("📊 Generate Report", use_container_width=True, type="primary"):
        with st.spinner("Generating audit report..."):
            result = st.session_state.agent.generate_audit_report(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
        
        if result.get('summary'):
            summary = result['summary']
            
            # Summary metrics
            st.markdown("### 📈 Report Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Activities", summary['total_activities'])
            with col2:
                st.metric("Leave Requests", summary['leave_requests']['total'])
            with col3:
                st.metric("Onboarding", summary['onboarding'])
            with col4:
                st.metric("Policy Questions", summary['policy_questions'])
            
            st.markdown("---")
            
            # Leave request breakdown
            if summary['leave_requests']['total'] > 0:
                st.markdown("### 🏖️ Leave Request Analysis")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.success(f"✅ Approved: {summary['leave_requests']['approved']}")
                with col2:
                    st.error(f"❌ Rejected: {summary['leave_requests']['rejected']}")
                with col3:
                    st.warning(f"⏳ Pending: {summary['leave_requests']['pending']}")
            
            # Detailed logs
            st.markdown("---")
            st.markdown("### 📋 Detailed Activity Logs")
            
            if result.get('detailed_logs'):
                for log in result['detailed_logs'][:10]:  # Show first 10
                    with st.expander(f"🔹 {log['action']} - {log['timestamp'][:19]}"):
                        st.write(f"**User:** {log['user']}")
                        st.write(f"**Agent:** {log['agent']}")
                        st.json(log['details'])
            
            # Compliance status
            st.markdown("---")
            st.markdown("### ✓ Compliance Status")
            
            if result['compliance_status'] == 'COMPLIANT':
                st.success("✅ No compliance issues detected")
            else:
                st.warning("⚠️ Compliance issues found:")
                for issue in result.get('compliance_issues', []):
                    st.write(f"• {issue}")
            
            # Download report
            st.markdown("---")
            report_json = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download Full Report (JSON)",
                data=report_json,
                file_name=f"audit_report_{result['report_id']}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("ℹ️ No audit logs found in the selected date range. Perform some actions first!")

elif page == "👥 View Employees":
    st.title("👥 Employee Directory")
    st.markdown("View and manage all employees in the system")
    
    # Search and filter
    search = st.text_input("🔍 Search employees by name, department, or position", placeholder="Search...")
    
    st.markdown("---")
    
    # Display employees
    employees = list(st.session_state.db.employees.values())
    
    # Filter employees based on search
    if search:
        search_lower = search.lower()
        employees = [
            emp for emp in employees
            if search_lower in emp.name.lower() or 
               search_lower in emp.department.lower() or 
               search_lower in emp.position.lower()
        ]
    
    if employees:
        for emp in employees:
            st.markdown(f"""
                <div class="employee-card">
                    <h3>{emp.name}</h3>
                    <p style="color: #7f8c8d; margin: 0.5rem 0;">
                        <strong>{emp.position}</strong> | {emp.department}
                    </p>
                    <p style="margin: 0.5rem 0;">
                        📧 {emp.email} | 🆔 {emp.employee_id} | 📅 Joined: {emp.join_date}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Show leave balance in expandable section
            with st.expander(f"View {emp.name}'s Leave Balance"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Casual Leave", f"{emp.leave_balance.get('Casual Leave', 0)} days")
                with col2:
                    st.metric("Sick Leave", f"{emp.leave_balance.get('Sick Leave', 0)} days")
                with col3:
                    st.metric("Annual Leave", f"{emp.leave_balance.get('Annual Leave', 0)} days")
    else:
        st.info("No employees found matching your search criteria.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 2rem 0;">
        <p>🤖 <strong>HR Agent Enterprise Platform</strong> | Powered by AI & Automation</p>
        <p style="font-size: 0.9rem;">© 2025 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
