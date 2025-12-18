"""
HR Agent - Enterprise Automation Platform
Complete implementation with all required functionalities
UPDATED: LLM can access database + Fixed Audit Report
"""

import os
import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import re
from dotenv import load_dotenv

# Install required packages (run in Colab first cell)
# !pip install groq python-dotenv

# Using Groq API with free Llama model (faster than Ollama in Colab)
from groq import Groq

# ==================== DATA MODELS ====================

class LeaveType(Enum):
    CASUAL = "Casual Leave"
    SICK = "Sick Leave"
    ANNUAL = "Annual Leave"
    UNPAID = "Unpaid Leave"

class LeaveStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    position: str
    join_date: str
    leave_balance: Dict[str, int]
    
@dataclass
class LeaveRequest:
    request_id: str
    employee_id: str
    employee_name: str
    leave_type: str
    start_date: str
    end_date: str
    days: int
    reason: str
    status: str
    submitted_date: str
    processed_date: Optional[str] = None
    
@dataclass
class AuditLog:
    log_id: str
    timestamp: str
    agent: str
    action: str
    details: Dict
    user: str

@dataclass
class JobPosition:
    job_id: str
    title: str
    department: str
    description: str
    required_skills: List[str]
    min_experience: int  # in years
    min_education: str
    status: str  # Active, Closed
    test_questions: Optional[List[Dict]] = None  # List of {"question": str, "options": List[str], "correct_answer": str}

@dataclass
class Candidate:
    candidate_id: str
    name: str
    email: str
    phone: str
    applied_position: str
    resume_text: str
    extracted_skills: List[str]
    experience_years: int
    education: str
    application_date: str
    status: str  # Pending, Accepted, Rejected, Test_Scheduled, Hired
    evaluation_result: Optional[Dict] = None
    test_score: Optional[float] = None
    test_taken: bool = False

@dataclass 
class User:
    username: str
    password: str
    role: str  # Candidate, Employee, Admin
    employee_id: Optional[str] = None

@dataclass
class TechnicalProblem:
    problem_id: str
    title: str
    difficulty: str  # Easy, Medium, Hard
    description: str
    input_format: str
    output_format: str
    constraints: str
    examples: List[Dict]  # [{"input": str, "output": str, "explanation": str}]
    test_cases: List[Dict]  # [{"input": str, "expected": str, "visible": bool}]
    time_limit: float  # seconds
    memory_limit: int  # KB
    tags: List[str]  # ["Array", "Hash Table", etc.]
    starter_code: Dict[str, str]  # {"python": "...", "java": "...", "cpp": "..."}

@dataclass
class CodeSubmission:
    submission_id: str
    candidate_id: str
    problem_id: str
    code: str
    language: str
    submitted_at: str
    test_results: Optional[Dict] = None
    ai_analysis: Optional[Dict] = None
    interview_qa: Optional[List[Dict]] = None  # [{"question": str, "answer": str, "score": int}]
    conversation_transcript: Optional[List[Dict]] = None  # Full chat history
    hints_used: int = 0
    approach_score: int = 0
    communication_score: int = 0
    final_interview_score: Optional[int] = None
    final_score: Optional[float] = None

# ==================== DATABASE SIMULATOR ====================

class Database:
    """Simulated database for storing HR data"""
    
    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.leave_requests: Dict[str, LeaveRequest] = {}
        self.audit_logs: List[AuditLog] = []
        self.hr_policies: Dict[str, str] = {}
        self.job_positions: Dict[str, JobPosition] = {}
        self.candidates: Dict[str, Candidate] = {}
        self.users: Dict[str, User] = {}
        self.eligibility_criteria: Dict[str, Dict] = {}
        self.technical_problems: Dict[str, TechnicalProblem] = {}
        self.code_submissions: Dict[str, CodeSubmission] = {}
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize with sample data"""
        # Sample employees
        self.employees = {
            "EMP001": Employee(
                employee_id="EMP001",
                name="John Doe",
                email="john.doe@company.com",
                department="Engineering",
                position="Senior Developer",
                join_date="2023-01-15",
                leave_balance={"Casual Leave": 10, "Sick Leave": 12, "Annual Leave": 15}
            ),
            "EMP002": Employee(
                employee_id="EMP002",
                name="Jane Smith",
                email="jane.smith@company.com",
                department="Marketing",
                position="Marketing Manager",
                join_date="2022-06-01",
                leave_balance={"Casual Leave": 8, "Sick Leave": 10, "Annual Leave": 12}
            )
        }
        
        # HR Policies
        self.hr_policies = {
            "leave_policy": """
            COMPANY LEAVE POLICY:
            
            1. Leave Types:
               - Casual Leave: 12 days per year
               - Sick Leave: 15 days per year
               - Annual Leave: 20 days per year
               - Unpaid Leave: Available on request
            
            2. Leave Application:
               - Must be submitted at least 3 days in advance (except sick leave)
               - Requires manager approval
               - Medical certificate required for sick leave > 3 days
            
            3. Leave Balance:
               - Unused leave expires at year-end (except Annual Leave)
               - Annual leave can be carried forward up to 5 days
            
            4. Notice Period:
               - Casual/Sick Leave: 1 day advance notice
               - Annual Leave: 7 days advance notice
            """,
            
            "onboarding_policy": """
            EMPLOYEE ONBOARDING POLICY:
            
            1. Documentation Required:
               - Government ID proof
               - Educational certificates
               - Previous employment documents
               - Bank account details
            
            2. Onboarding Process:
               - Day 1: Orientation and system access
               - Week 1: Department introduction
               - Month 1: Initial performance review
            
            3. Probation Period:
               - Duration: 3 months
               - Evaluation at end of probation
            """,
            
            "working_hours": """
            WORKING HOURS POLICY:
            
            - Standard hours: 9 AM - 6 PM (Monday to Friday)
            - Lunch break: 1 hour
            - Flexible timing: ±2 hours with manager approval
            - Remote work: 2 days per week allowed
            """,
            
            "code_of_conduct": """
            CODE OF CONDUCT:
            
            1. Professional Behavior
            2. Confidentiality and Data Protection
            3. Anti-Harassment Policy
            4. Dress Code: Business casual
            5. Communication Guidelines
            """
        }
        
        # Initialize Users (for login)
        self.users = {
            "admin": User(username="admin", password="admin123", role="Admin"),
            "john.doe": User(username="john.doe", password="pass123", role="Employee", employee_id="EMP001"),
            "jane.smith": User(username="jane.smith", password="pass123", role="Employee", employee_id="EMP002"),
        }
        
        # Initialize Job Positions
        self.job_positions = {
            "JOB001": JobPosition(
                job_id="JOB001",
                title="Senior Developer",
                department="Engineering",
                description="Looking for an experienced developer with strong Python skills",
                required_skills=["Python", "Django", "REST API", "SQL"],
                min_experience=3,
                min_education="Bachelor's Degree",
                status="Active",
                test_questions=[
                    {
                        "question": "Which of the following is used to define a function in Python?",
                        "options": ["function", "def", "func", "define"],
                        "correct_answer": "def"
                    },
                    {
                        "question": "What does REST stand for in REST API?",
                        "options": [
                            "Representational State Transfer",
                            "Remote Execution State Transfer",
                            "Representational System Transfer",
                            "Remote State Transfer"
                        ],
                        "correct_answer": "Representational State Transfer"
                    },
                    {
                        "question": "Which SQL command is used to retrieve data from a database?",
                        "options": ["GET", "RETRIEVE", "SELECT", "FETCH"],
                        "correct_answer": "SELECT"
                    },
                    {
                        "question": "In Django, which file is used to define URL patterns?",
                        "options": ["views.py", "models.py", "urls.py", "settings.py"],
                        "correct_answer": "urls.py"
                    },
                    {
                        "question": "What is the output of: print(type([]))?",
                        "options": ["<class 'dict'>", "<class 'list'>", "<class 'tuple'>", "<class 'set'>"],
                        "correct_answer": "<class 'list'>"
                    }
                ]
            ),
            "JOB002": JobPosition(
                job_id="JOB002",
                title="Marketing Manager",
                department="Marketing",
                description="Experienced marketing professional to lead our marketing team",
                required_skills=["Digital Marketing", "SEO", "Content Strategy", "Analytics"],
                min_experience=5,
                min_education="Bachelor's Degree",
                status="Active",
                test_questions=[
                    {
                        "question": "What does SEO stand for?",
                        "options": [
                            "Search Engine Optimization",
                            "Social Engagement Optimization",
                            "Site Enhancement Operation",
                            "Search Engine Operation"
                        ],
                        "correct_answer": "Search Engine Optimization"
                    },
                    {
                        "question": "Which metric measures the percentage of visitors who leave after viewing only one page?",
                        "options": ["Exit Rate", "Bounce Rate", "Conversion Rate", "Click-Through Rate"],
                        "correct_answer": "Bounce Rate"
                    },
                    {
                        "question": "What is A/B testing in digital marketing?",
                        "options": [
                            "Testing two different versions to see which performs better",
                            "Testing advertising budgets",
                            "Testing audience behavior",
                            "Testing browser compatibility"
                        ],
                        "correct_answer": "Testing two different versions to see which performs better"
                    },
                    {
                        "question": "Which platform is primarily used for B2B marketing?",
                        "options": ["Instagram", "TikTok", "LinkedIn", "Snapchat"],
                        "correct_answer": "LinkedIn"
                    },
                    {
                        "question": "What does CTA stand for in marketing?",
                        "options": [
                            "Call To Action",
                            "Customer Target Analysis",
                            "Content Type Allocation",
                            "Click Through Analytics"
                        ],
                        "correct_answer": "Call To Action"
                    }
                ]
            )
        }
        
        # Initialize Technical Problems
        self.technical_problems = {
            "PROB001": TechnicalProblem(
                problem_id="PROB001",
                title="Two Sum",
                difficulty="Easy",
                description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
                input_format="First line: space-separated integers (the array)\nSecond line: target integer",
                output_format="Two space-separated integers (the indices)",
                constraints="2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9",
                examples=[
                    {
                        "input": "2 7 11 15\n9",
                        "output": "0 1",
                        "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                    },
                    {
                        "input": "3 2 4\n6",
                        "output": "1 2",
                        "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
                    }
                ],
                test_cases=[
                    {"input": "2 7 11 15\n9", "expected": "0 1", "visible": True},
                    {"input": "3 2 4\n6", "expected": "1 2", "visible": True},
                    {"input": "3 3\n6", "expected": "0 1", "visible": False},
                    {"input": "1 2 3 4 5\n9", "expected": "3 4", "visible": False},
                ],
                time_limit=2.0,
                memory_limit=128000,
                tags=["Array", "Hash Table"],
                starter_code={
                    "python": """# Read input
nums = list(map(int, input().split()))
target = int(input())

# Your solution here
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return None

# Call function and print result
result = two_sum(nums, target)
if result:
    print(result[0], result[1])""",
                    "java": """import java.util.*;

public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        // Your code here
        return new int[]{0, 0};
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] numsStr = sc.nextLine().split(" ");
        int[] nums = new int[numsStr.length];
        for (int i = 0; i < numsStr.length; i++) {
            nums[i] = Integer.parseInt(numsStr[i]);
        }
        int target = sc.nextInt();
        
        int[] result = twoSum(nums, target);
        System.out.println(result[0] + " " + result[1]);
    }
}""",
                    "cpp": """#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    // Your code here
    return {0, 0};
}

int main() {
    string line;
    getline(cin, line);
    istringstream iss(line);
    vector<int> nums;
    int num;
    while (iss >> num) {
        nums.push_back(num);
    }
    
    int target;
    cin >> target;
    
    vector<int> result = twoSum(nums, target);
    cout << result[0] << " " << result[1] << endl;
    
    return 0;
}"""
                }
            ),
            "PROB002": TechnicalProblem(
                problem_id="PROB002",
                title="Valid Parentheses",
                difficulty="Easy",
                description="""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.""",
                input_format="A single line containing the string s",
                output_format="true if valid, false otherwise",
                constraints="1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'",
                examples=[
                    {
                        "input": "()",
                        "output": "true",
                        "explanation": "The string is valid."
                    },
                    {
                        "input": "()[]{}",
                        "output": "true",
                        "explanation": "All brackets are properly closed."
                    },
                    {
                        "input": "(]",
                        "output": "false",
                        "explanation": "Mismatched bracket types."
                    }
                ],
                test_cases=[
                    {"input": "()", "expected": "true", "visible": True},
                    {"input": "()[]{}", "expected": "true", "visible": True},
                    {"input": "(]", "expected": "false", "visible": True},
                    {"input": "([)]", "expected": "false", "visible": False},
                    {"input": "{[]}", "expected": "true", "visible": False},
                ],
                time_limit=2.0,
                memory_limit=128000,
                tags=["String", "Stack"],
                starter_code={
                    "python": """s = input().strip()

def is_valid(s):
    # Your code here
    pass

print(str(is_valid(s)).lower())""",
                    "java": """import java.util.*;

public class Solution {
    public static boolean isValid(String s) {
        // Your code here
        return false;
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        System.out.println(isValid(s));
    }
}""",
                    "cpp": """#include <iostream>
#include <string>
using namespace std;

bool isValid(string s) {
    // Your code here
    return false;
}

int main() {
    string s;
    cin >> s;
    cout << (isValid(s) ? "true" : "false") << endl;
    return 0;
}"""
                }
            )
        }
        
        # Default Eligibility Criteria (can be updated by Admin)
        self.eligibility_criteria = {
            "skill_match_threshold": 50,  # % of skills that must match
            "experience_required": True,
            "education_required": True,
            "auto_accept_threshold": 50  # Auto-accept if score >= 50%
        }
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        return self.employees.get(employee_id)
    
    def add_employee(self, employee: Employee):
        self.employees[employee.employee_id] = employee
    
    def add_leave_request(self, leave_request: LeaveRequest):
        self.leave_requests[leave_request.request_id] = leave_request
    
    def update_leave_balance(self, employee_id: str, leave_type: str, days: int):
        if employee_id in self.employees:
            self.employees[employee_id].leave_balance[leave_type] -= days
    
    def add_audit_log(self, log: AuditLog):
        self.audit_logs.append(log)
    
    def get_hr_policy(self, policy_type: str) -> str:
        return self.hr_policies.get(policy_type, "Policy not found")
    
    def get_all_policies(self) -> str:
        return "\n\n".join([f"=== {k.upper()} ===\n{v}" for k, v in self.hr_policies.items()])
    
    def get_employee_summary(self) -> str:
        """Get summary of all employees for LLM context"""
        summary = "CURRENT EMPLOYEE DATABASE:\n\n"
        for emp_id, emp in self.employees.items():
            summary += f"""
Employee ID: {emp.employee_id}
Name: {emp.name}
Email: {emp.email}
Department: {emp.department}
Position: {emp.position}
Join Date: {emp.join_date}
Leave Balance:
  - Casual Leave: {emp.leave_balance.get('Casual Leave', 0)} days
  - Sick Leave: {emp.leave_balance.get('Sick Leave', 0)} days
  - Annual Leave: {emp.leave_balance.get('Annual Leave', 0)} days

---
"""
        return summary
    
    def search_employee_by_name(self, name: str) -> Optional[Employee]:
        """Search employee by name (case-insensitive)"""
        name_lower = name.lower()
        for emp in self.employees.values():
            if name_lower in emp.name.lower():
                return emp
        return None
    
    # New methods for candidate and job management
    def add_candidate(self, candidate: Candidate):
        self.candidates[candidate.candidate_id] = candidate
    
    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        return self.candidates.get(candidate_id)
    
    def add_job_position(self, job: JobPosition):
        self.job_positions[job.job_id] = job
    
    def get_job_position(self, job_id: str) -> Optional[JobPosition]:
        return self.job_positions.get(job_id)
    
    def update_eligibility_criteria(self, criteria: Dict):
        self.eligibility_criteria.update(criteria)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None
    
    def add_user(self, user: User):
        self.users[user.username] = user
    
    def check_leave_date_conflict(self, employee_id: str, start_date: str, end_date: str) -> Optional[LeaveRequest]:
        """Check if employee already has leave approved for the given dates"""
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        for request_id, leave_req in self.leave_requests.items():
            if leave_req.employee_id == employee_id and leave_req.status == LeaveStatus.APPROVED.value:
                existing_start = datetime.datetime.strptime(leave_req.start_date, "%Y-%m-%d")
                existing_end = datetime.datetime.strptime(leave_req.end_date, "%Y-%m-%d")
                
                # Check if dates overlap
                if not (end < existing_start or start > existing_end):
                    return leave_req
        
        return None
    
    def update_candidate_test_status(self, candidate_id: str, test_score: float, passed: bool):
        """Update candidate's test score and status"""
        if candidate_id in self.candidates:
            self.candidates[candidate_id].test_score = test_score
            self.candidates[candidate_id].test_taken = True
            if passed:
                self.candidates[candidate_id].status = "Hired"
            else:
                self.candidates[candidate_id].status = "Rejected"
    
    def convert_candidate_to_employee(self, candidate_id: str) -> tuple[str, str, str]:
        """Convert a hired candidate to an employee and create credentials"""
        candidate = self.candidates.get(candidate_id)
        if not candidate or candidate.status != "Hired":
            return None, None, None
        
        # Generate employee ID
        employee_id = f"EMP{str(len(self.employees) + 1).zfill(3)}"
        
        # Generate username and password
        username = candidate.email.split('@')[0].lower()
        import random
        import string
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Create employee record
        employee = Employee(
            employee_id=employee_id,
            name=candidate.name,
            email=candidate.email,
            department=self.job_positions[self.get_job_id_by_title(candidate.applied_position)].department,
            position=candidate.applied_position,
            join_date=datetime.datetime.now().strftime("%Y-%m-%d"),
            leave_balance={"Casual Leave": 12, "Sick Leave": 15, "Annual Leave": 20}
        )
        
        # Add employee to database
        self.employees[employee_id] = employee
        
        # Create user account for employee portal
        user = User(
            username=username,
            password=password,
            role="Employee",
            employee_id=employee_id
        )
        self.users[username] = user
        
        return username, password, employee_id
    
    def get_job_id_by_title(self, title: str) -> Optional[str]:
        """Get job ID by job title"""
        for job_id, job in self.job_positions.items():
            if job.title == title:
                return job_id
        return None
    
    # ==================== TECHNICAL PROBLEMS METHODS ====================
    
    def get_technical_problem(self, problem_id: str) -> Optional[TechnicalProblem]:
        """Get a technical problem by ID"""
        return self.technical_problems.get(problem_id)
    
    def get_problems_by_difficulty(self, difficulty: str) -> List[TechnicalProblem]:
        """Get all problems of a specific difficulty"""
        return [p for p in self.technical_problems.values() if p.difficulty == difficulty]
    
    def add_code_submission(self, submission: CodeSubmission):
        """Add a code submission"""
        self.code_submissions[submission.submission_id] = submission
    
    def get_candidate_submissions(self, candidate_id: str) -> List[CodeSubmission]:
        """Get all submissions for a candidate"""
        return [s for s in self.code_submissions.values() if s.candidate_id == candidate_id]
    
    def update_submission_results(self, submission_id: str, test_results: Dict, ai_analysis: Dict):
        """Update submission with test results and AI analysis"""
        if submission_id in self.code_submissions:
            self.code_submissions[submission_id].test_results = test_results
            self.code_submissions[submission_id].ai_analysis = ai_analysis
    
    def update_submission_interview_qa(self, submission_id: str, qa_entry: Dict):
        """Add interview Q&A to submission"""
        if submission_id in self.code_submissions:
            if self.code_submissions[submission_id].interview_qa is None:
                self.code_submissions[submission_id].interview_qa = []
            self.code_submissions[submission_id].interview_qa.append(qa_entry)
    
    def update_submission_final_score(self, submission_id: str, final_score: float):
        """Update final score for submission"""
        if submission_id in self.code_submissions:
            self.code_submissions[submission_id].final_score = final_score

# ==================== LLM INTERFACE ====================

class LLMInterface:
    """Interface for interacting with free LLM (Groq API with Llama)"""
    
    def __init__(self, api_key: Optional[str] = None, database: Optional[Database] = None):
        """
        Initialize LLM Interface
        Get free API key from: https://console.groq.com/
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.database = database
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama-3.1-8b-instant"  # Free fast model
        else:
            self.client = None
            print("⚠️ No API key provided. Using rule-based responses.")
    
    def generate_response(self, prompt: str, system_prompt: str = "", include_employee_data: bool = False) -> str:
        """Generate response using LLM or fallback to rules"""
        if not self.client:
            return self._fallback_response(prompt)
        
        try:
            messages = []
            
            # Build system prompt with optional employee database access
            full_system_prompt = system_prompt
            if include_employee_data and self.database:
                employee_data = self.database.get_employee_summary()
                full_system_prompt += f"\n\n{employee_data}\n\nYou have access to the current employee database. Use this information to answer specific questions about employees."
            
            if full_system_prompt:
                messages.append({"role": "system", "content": full_system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Rule-based fallback when LLM is unavailable"""
        prompt_lower = prompt.lower()
        
        # Try to extract employee info from database if available
        if self.database and ("employee" in prompt_lower or "who is" in prompt_lower):
            # Try to find employee by name
            words = prompt.split()
            for word in words:
                emp = self.database.search_employee_by_name(word)
                if emp:
                    return f"{emp.name} (ID: {emp.employee_id}) works as {emp.position} in {emp.department} department. Email: {emp.email}. Leave balance: Casual: {emp.leave_balance.get('Casual Leave', 0)}, Sick: {emp.leave_balance.get('Sick Leave', 0)}, Annual: {emp.leave_balance.get('Annual Leave', 0)} days."
        
        if "leave" in prompt_lower and "balance" in prompt_lower:
            return "You can check your leave balance in the employee portal or contact HR."
        elif "policy" in prompt_lower:
            return "Please refer to the employee handbook or ask HR for specific policy details."
        return "I understand your query. Please contact HR for detailed assistance."

# ==================== HR AGENT ====================

class HRAgent:
    """Main HR Agent with all functionalities"""
    
    def __init__(self, database: Database, llm: LLMInterface):
        self.db = database
        self.llm = llm
        # Update LLM with database reference
        self.llm.database = database
        self.agent_name = "HR Agent"
    
    def _log_action(self, action: str, details: Dict, user: str = "System"):
        """Log all actions for audit"""
        log = AuditLog(
            log_id=f"LOG{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            timestamp=datetime.datetime.now().isoformat(),
            agent=self.agent_name,
            action=action,
            details=details,
            user=user
        )
        self.db.add_audit_log(log)
    
    # ==================== FUNCTION 1: PROCESS LEAVE REQUEST ====================
    
    def process_leave_request(
        self,
        employee_id: str,
        leave_type: str,
        start_date: str,
        end_date: str,
        reason: str
    ) -> Dict:
        """
        Process employee leave request
        Checks balance, validates dates, and approves/rejects
        """
        print(f"\n{'='*60}")
        print(f"📝 PROCESSING LEAVE REQUEST")
        print(f"{'='*60}")
        
        # Get employee
        employee = self.db.get_employee(employee_id)
        if not employee:
            result = {"status": "error", "message": "Employee not found"}
            self._log_action("Process Leave Request", result, employee_id)
            return result
        
        # Check for date conflicts
        conflict = self.db.check_leave_date_conflict(employee_id, start_date, end_date)
        if conflict:
            message = f"Leave dates conflict with existing approved leave (Request ID: {conflict.request_id}, Dates: {conflict.start_date} to {conflict.end_date})"
            result = {
                "status": "error",
                "message": message,
                "decision": LeaveStatus.REJECTED.value
            }
            print(f"\n❌ REJECTED: {message}")
            
            # Send rejection email for date conflict
            email_result = self._send_leave_email(
                employee=employee,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                days=(datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days + 1,
                reason=reason,
                status=LeaveStatus.REJECTED.value,
                message=message,
                request_id="N/A"
            )
            
            result['email_result'] = email_result
            
            self._log_action("Process Leave Request", result, employee_id)
            return result
        
        # Calculate days
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        # Check leave balance
        current_balance = employee.leave_balance.get(leave_type, 0)
        
        print(f"\n👤 Employee: {employee.name} ({employee_id})")
        print(f"📅 Leave Period: {start_date} to {end_date} ({days} days)")
        print(f"🏷️  Leave Type: {leave_type}")
        print(f"💰 Current Balance: {current_balance} days")
        print(f"📝 Reason: {reason}")
        
        # Decision logic
        if days > current_balance:
            status = LeaveStatus.REJECTED.value
            message = f"Insufficient leave balance. Available: {current_balance} days, Requested: {days} days"
            print(f"\n❌ REJECTED: {message}")
        elif days > 10:
            status = LeaveStatus.PENDING.value
            message = "Leave request requires manager approval (>10 days)"
            print(f"\n⏳ PENDING: {message}")
        else:
            status = LeaveStatus.APPROVED.value
            message = "Leave request approved automatically"
            print(f"\n✅ APPROVED: {message}")
            
            # Update leave balance
            self.db.update_leave_balance(employee_id, leave_type, days)
            print(f"📊 Updated Balance: {current_balance - days} days")
        
        # Create leave request record
        request_id = f"LR{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        leave_request = LeaveRequest(
            request_id=request_id,
            employee_id=employee_id,
            employee_name=employee.name,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days=days,
            reason=reason,
            status=status,
            submitted_date=datetime.datetime.now().isoformat(),
            processed_date=datetime.datetime.now().isoformat() if status == LeaveStatus.APPROVED.value else None
        )
        
        self.db.add_leave_request(leave_request)
        
        # Send email notification with LLM-generated content
        email_result = self._send_leave_email(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days=days,
            reason=reason,
            status=status,
            message=message,
            request_id=request_id
        )
        
        print(f"\n📧 Email: {email_result.get('message', 'Sent')}")
        
        result = {
            "status": "success",
            "request_id": request_id,
            "decision": status,
            "message": message,
            "notification_sent": True,
            "email_result": email_result
        }
        
        self._log_action("Process Leave Request", result, employee_id)
        print(f"\n{'='*60}\n")
        
        return result
    
    def _send_leave_email(self, employee: Employee, leave_type: str, start_date: str, 
                         end_date: str, days: int, reason: str, status: str, 
                         message: str, request_id: str) -> Dict:
        """Send email notification for leave request with LLM-generated content"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        print("\n" + "="*60)
        print("🔍 DEBUG: _send_leave_email called")
        print(f"   Employee: {employee.name} ({employee.email})")
        print(f"   Leave Type: {leave_type}")
        print(f"   Status: {status}")
        print("="*60)
        
        print(f"\n{'='*60}")
        print(f"📧 SENDING LEAVE NOTIFICATION EMAIL")
        print(f"{'='*60}")
        
        # Generate email content using LLM
        prompt = f"""
        Generate a professional email to inform an employee about their leave request status.
        
        Employee Name: {employee.name}
        Leave Type: {leave_type}
        Leave Period: {start_date} to {end_date} ({days} days)
        Reason for Leave: {reason}
        Status: {status}
        Additional Information: {message}
        Request ID: {request_id}
        
        IMPORTANT: Tailor the tone and message appropriately based on the leave type and reason:
        - For Sick Leave: Express concern for their health, wish them a speedy recovery
        - For Casual Leave: Wish them a pleasant time off
        - For Annual Leave: Mention they deserve the break, wish them a refreshing vacation
        - For Unpaid Leave: Be supportive and professional
        
        Consider the reason provided when crafting your message. Be empathetic and appropriate.
        
        Email should include:
        1. Professional greeting
        2. Acknowledge the leave request and the specific reason provided
        3. Clearly state the decision (Approved/Rejected/Pending)
        4. If approved: Provide appropriate well-wishes based on leave type (recovery for sick, enjoyment for vacation, etc.)
        5. If rejected: Politely explain why and suggest alternatives if applicable
        6. If pending: Explain next steps and timeline
        7. Reference the Request ID
        8. Professional closing
        
        Keep it concise, warm, empathetic, and professionally appropriate for the situation. Return ONLY the email body text, no subject line.
        """
        
        try:
            email_body = self.llm.ask_question(prompt)
            
            # Generate subject line using LLM
            subject_prompt = f"""
            Generate a short professional email subject line for a leave request {status.lower()}.
            Leave type: {leave_type}
            Status: {status}
            Keep it under 10 words. Return ONLY the subject line, nothing else.
            """
            subject = self.llm.ask_question(subject_prompt).strip().strip('"').strip("'")
            
        except Exception as e:
            print(f"⚠️ LLM email generation failed: {e}")
            # Fallback email content with context-aware messages
            
            # Determine appropriate closing message based on leave type
            if status == LeaveStatus.APPROVED.value:
                if "sick" in leave_type.lower():
                    closing_message = "We wish you a speedy recovery and hope you feel better soon. Please take care of yourself."
                elif "annual" in leave_type.lower() or "vacation" in leave_type.lower():
                    closing_message = "Enjoy your well-deserved break and return refreshed!"
                elif "unpaid" in leave_type.lower():
                    closing_message = "We hope everything goes well during your time off."
                else:  # Casual leave or other
                    closing_message = "We hope you have a pleasant time off."
                
                subject = f"Leave Request Approved - {leave_type}"
                email_body = f"""
Dear {employee.name},

Your leave request has been approved!

Request Details:
- Request ID: {request_id}
- Leave Type: {leave_type}
- Period: {start_date} to {end_date} ({days} days)
- Reason: {reason}

Status: APPROVED ✓

{message}

{closing_message}

Best regards,
HR Department
                """
            elif status == LeaveStatus.REJECTED.value:
                subject = f"Leave Request Status - {leave_type}"
                email_body = f"""
Dear {employee.name},

Thank you for submitting your leave request.

Request Details:
- Request ID: {request_id}
- Leave Type: {leave_type}
- Period: {start_date} to {end_date} ({days} days)
- Reason: {reason}

Status: NOT APPROVED

{message}

If you have any questions or would like to discuss alternative dates, please don't hesitate to contact HR.

Best regards,
HR Department
                """
            else:  # Pending
                subject = f"Leave Request Under Review - {leave_type}"
                email_body = f"""
Dear {employee.name},

Your leave request has been received and is under review.

Request Details:
- Request ID: {request_id}
- Leave Type: {leave_type}
- Period: {start_date} to {end_date} ({days} days)
- Reason: {reason}

Status: PENDING APPROVAL

{message}

You will be notified once your leave request has been reviewed by management.

Best regards,
HR Department
                """
        
        # Get email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            print("⚠️ Email credentials not configured in .env file")
            return {
                "status": "error",
                "message": "Email credentials not configured. Notification not sent.",
                "email_content": email_body
            }
        
        try:
            # Create message
            message_obj = MIMEMultipart()
            message_obj["From"] = sender_email
            message_obj["To"] = employee.email
            message_obj["Subject"] = subject
            message_obj.attach(MIMEText(email_body, "plain"))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message_obj)
            
            print(f"✅ Email sent successfully to {employee.email}")
            print(f"📨 Subject: {subject}")
            
            # Log the action
            self._log_action(
                "Send Leave Notification Email",
                {
                    "employee_email": employee.email,
                    "leave_type": leave_type,
                    "status": status,
                    "request_id": request_id
                }
            )
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {employee.email}",
                "subject": subject,
                "email_content": email_body
            }
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "email_content": email_body
            }
    
    # ==================== FUNCTION 2: HANDLE EMPLOYEE ONBOARDING ====================
    
    def handle_employee_onboarding(
        self,
        name: str,
        email: str,
        department: str,
        position: str,
        join_date: str
    ) -> Dict:
        """
        Handle new employee onboarding
        Creates profile, assigns ID, sends welcome email
        """
        print(f"\n{'='*60}")
        print(f"🎉 EMPLOYEE ONBOARDING PROCESS")
        print(f"{'='*60}")
        
        # Generate employee ID
        employee_count = len(self.db.employees) + 1
        employee_id = f"EMP{employee_count:03d}"
        
        print(f"\n📋 New Employee Details:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Department: {department}")
        print(f"   Position: {position}")
        print(f"   Join Date: {join_date}")
        
        # Create employee profile
        employee = Employee(
            employee_id=employee_id,
            name=name,
            email=email,
            department=department,
            position=position,
            join_date=join_date,
            leave_balance={
                "Casual Leave": 12,
                "Sick Leave": 15,
                "Annual Leave": 20
            }
        )
        
        self.db.add_employee(employee)
        print(f"\n✅ Employee Profile Created")
        print(f"   Employee ID: {employee_id}")
        
        # Generate credentials (simulated)
        credentials = {
            "username": email.split('@')[0],
            "temp_password": f"Welcome@{employee_id}",
            "portal_url": "https://company.portal.com"
        }
        print(f"\n🔐 Credentials Generated:")
        print(f"   Username: {credentials['username']}")
        print(f"   Temporary Password: {credentials['temp_password']}")
        
        # Prepare onboarding documents
        documents = [
            "Employee Handbook",
            "Company Policies",
            "IT Security Guidelines",
            "Benefits Information",
            "Tax Forms"
        ]
        
        print(f"\n📄 Onboarding Documents Prepared:")
        for doc in documents:
            print(f"   ✓ {doc}")
        
        # Send welcome email
        welcome_email = self._send_welcome_email(employee, credentials, documents)
        print(f"\n📧 {welcome_email}")
        
        # Schedule orientation
        orientation_date = datetime.datetime.strptime(join_date, "%Y-%m-%d")
        print(f"\n📅 Orientation Scheduled:")
        print(f"   Date: {orientation_date.strftime('%B %d, %Y')}")
        print(f"   Time: 9:00 AM")
        print(f"   Location: Conference Room A")
        
        result = {
            "status": "success",
            "employee_id": employee_id,
            "credentials": credentials,
            "documents": documents,
            "welcome_email_sent": True,
            "orientation_scheduled": True
        }
        
        self._log_action("Employee Onboarding", result, employee_id)
        print(f"\n{'='*60}\n")
        
        return result
    
    def _send_welcome_email(self, employee: Employee, credentials: Dict, documents: List[str]) -> str:
        """Send welcome email (simulated)"""
        email_body = f"""
        Dear {employee.name},
        
        Welcome to our company! We're excited to have you join our {employee.department} team as {employee.position}.
        
        Your Employee ID: {employee.employee_id}
        Start Date: {employee.join_date}
        
        Login Credentials:
        Username: {credentials['username']}
        Temporary Password: {credentials['temp_password']}
        Portal: {credentials['portal_url']}
        
        Attached documents:
        {chr(10).join(f'- {doc}' for doc in documents)}
        
        Please change your password on first login.
        
        Looking forward to working with you!
        
        Best regards,
        HR Team
        """
        return f"Welcome email sent to {employee.email}"
    
    # ==================== FUNCTION 3: ASK HR POLICY QUESTION (UPDATED) ====================
    
    def ask_hr_policy_question(self, question: str, employee_id: str = "GUEST") -> Dict:
        """
        Answer HR policy questions using LLM with DATABASE ACCESS
        Available 24/7 for instant responses
        CAN ACCESS AND DISPLAY CURRENT EMPLOYEE DETAILS
        """
        print(f"\n{'='*60}")
        print(f"❓ HR POLICY INQUIRY")
        print(f"{'='*60}")
        print(f"\n📝 Question: {question}")
        
        # Get relevant policies
        all_policies = self.db.get_all_policies()
        
        # Create prompt for LLM with database access
        system_prompt = f"""You are an HR assistant helping employees understand company policies and employee information.

Here are the company policies:

{all_policies}

IMPORTANT: You have access to the current employee database. When asked about specific employees, their details, leave balances, or any employee-related information, provide accurate information from the database.

Answer the employee's question based on the policies and employee data. Be helpful, professional, and concise.
If asked about a specific employee, include their:
- Name and Employee ID
- Department and Position
- Email address
- Current leave balances
- Join date

If the question is not covered in the policies or database, politely let them know and suggest contacting HR directly."""
        
        # Generate response using LLM WITH DATABASE ACCESS
        print(f"\n🤖 Processing with AI (Database Access Enabled)...")
        answer = self.llm.generate_response(question, system_prompt, include_employee_data=True)
        
        print(f"\n💬 Answer:\n{answer}")
        
        # Find relevant policy sections
        relevant_policies = self._find_relevant_policies(question)
        if relevant_policies:
            print(f"\n📚 Relevant Policy Sections:")
            for policy in relevant_policies:
                print(f"   • {policy}")
        
        # Check if question is about a specific employee
        employee_mentioned = self._extract_employee_from_question(question)
        if employee_mentioned:
            print(f"\n👤 Employee Data Retrieved: {employee_mentioned.name} ({employee_mentioned.employee_id})")
        
        result = {
            "status": "success",
            "question": question,
            "answer": answer,
            "relevant_policies": relevant_policies,
            "employee_data_accessed": employee_mentioned is not None,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self._log_action("HR Policy Question", {"question": question, "db_access": employee_mentioned is not None}, employee_id)
        print(f"\n{'='*60}\n")
        
        return result
    
    def _extract_employee_from_question(self, question: str) -> Optional[Employee]:
        """Try to identify if question mentions a specific employee"""
        question_lower = question.lower()
        
        # Check for employee ID pattern
        emp_id_match = re.search(r'EMP\d{3}', question, re.IGNORECASE)
        if emp_id_match:
            emp_id = emp_id_match.group(0).upper()
            return self.db.get_employee(emp_id)
        
        # Check for employee names
        for emp in self.db.employees.values():
            if emp.name.lower() in question_lower:
                return emp
            # Check first name only
            first_name = emp.name.split()[0].lower()
            if first_name in question_lower:
                return emp
        
        return None
    
    def _find_relevant_policies(self, question: str) -> List[str]:
        """Find relevant policy sections based on keywords"""
        question_lower = question.lower()
        relevant = []
        
        if any(word in question_lower for word in ["leave", "vacation", "time off"]):
            relevant.append("Leave Policy")
        if any(word in question_lower for word in ["onboard", "joining", "new employee"]):
            relevant.append("Onboarding Policy")
        if any(word in question_lower for word in ["hours", "timing", "schedule", "remote"]):
            relevant.append("Working Hours Policy")
        if any(word in question_lower for word in ["conduct", "behavior", "dress"]):
            relevant.append("Code of Conduct")
        
        return relevant
    
    # ==================== FUNCTION 4: GENERATE AUDIT REPORT (FIXED) ====================
    
    def generate_audit_report(self, start_date: str = None, end_date: str = None) -> Dict:
        """
        Generate comprehensive audit report
        Tracks all HR activities and compliance
        FIXED: Now properly filters and displays audit logs
        """
        print(f"\n{'='*60}")
        print(f"📊 GENERATING AUDIT REPORT")
        print(f"{'='*60}")
        
        if not start_date:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        print(f"\n📅 Report Period: {start_date} to {end_date}")
        
        # Check if there are any logs
        if not self.db.audit_logs:
            print("\n⚠️  No audit logs found in the system.")
            print("💡 Tip: Perform some actions first (leave requests, onboarding, policy questions)")
            result = {
                "status": "success",
                "report_id": f"AUDIT{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                "message": "No audit logs available",
                "summary": {"total_activities": 0}
            }
            self._log_action("Generate Audit Report", {"report_id": result['report_id']}, "Admin")
            return result
        
        # Filter logs by date range
        try:
            start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
            end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        except ValueError as e:
            print(f"\n❌ Error: Invalid date format. Use YYYY-MM-DD")
            return {"status": "error", "message": "Invalid date format"}
        
        filtered_logs = []
        for log in self.db.audit_logs:
            try:
                log_dt = datetime.datetime.fromisoformat(log.timestamp)
                if start_dt <= log_dt <= end_dt:
                    filtered_logs.append(log)
            except:
                continue
        
        # Analyze activities
        leave_requests = [log for log in filtered_logs if log.action == "Process Leave Request"]
        onboarding_activities = [log for log in filtered_logs if log.action == "Employee Onboarding"]
        policy_questions = [log for log in filtered_logs if log.action == "HR Policy Question"]
        
        print(f"\n📈 Activity Summary:")
        print(f"   Total Activities: {len(filtered_logs)}")
        print(f"   Leave Requests: {len(leave_requests)}")
        print(f"   Onboarding Activities: {len(onboarding_activities)}")
        print(f"   Policy Questions: {len(policy_questions)}")
        
        # Leave request analysis
        if leave_requests:
            print(f"\n🏖️  Leave Request Details:")
            approved = sum(1 for log in leave_requests if log.details.get('decision') == 'Approved')
            rejected = sum(1 for log in leave_requests if log.details.get('decision') == 'Rejected')
            pending = sum(1 for log in leave_requests if log.details.get('decision') == 'Pending')
            
            print(f"   ✅ Approved: {approved}")
            print(f"   ❌ Rejected: {rejected}")
            print(f"   ⏳ Pending: {pending}")
            
            # Show detailed leave requests
            print(f"\n   Detailed Leave Requests:")
            for log in leave_requests:
                print(f"   - {log.timestamp[:19]} | User: {log.user} | Status: {log.details.get('decision', 'N/A')}")
        
        # Onboarding analysis
        if onboarding_activities:
            print(f"\n👥 Onboarding Details:")
            for log in onboarding_activities:
                emp_id = log.details.get('employee_id', 'N/A')
                timestamp = log.timestamp[:19]
                print(f"   • {timestamp} | New Employee: {emp_id}")
        
        # Policy questions analysis
        if policy_questions:
            print(f"\n💬 Policy Questions Summary:")
            print(f"   Total Questions: {len(policy_questions)}")
            print(f"   Average Response Time: < 1 second")
            
            # Show sample questions
            print(f"\n   Recent Questions:")
            for log in policy_questions[:5]:  # Show last 5 questions
                question = log.details.get('question', 'N/A')
                timestamp = log.timestamp[:19]
                db_access = log.details.get('db_access', False)
                access_marker = "🔍" if db_access else "📝"
                print(f"   {access_marker} {timestamp} | {question[:50]}...")
        
        # Compliance check
        compliance_issues = self._check_compliance()
        print(f"\n✓ Compliance Status:")
        if compliance_issues:
            for issue in compliance_issues:
                print(f"   ⚠️  {issue}")
        else:
            print(f"   ✅ No compliance issues detected")
        
        # Generate report document
        report = {
            "report_id": f"AUDIT{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "generated_date": datetime.datetime.now().isoformat(),
            "period": {"start": start_date, "end": end_date},
            "summary": {
                "total_activities": len(filtered_logs),
                "leave_requests": {
                    "total": len(leave_requests),
                    "approved": sum(1 for log in leave_requests if log.details.get('decision') == 'Approved'),
                    "rejected": sum(1 for log in leave_requests if log.details.get('decision') == 'Rejected'),
                    "pending": sum(1 for log in leave_requests if log.details.get('decision') == 'Pending')
                },
                "onboarding": len(onboarding_activities),
                "policy_questions": len(policy_questions)
            },
            "detailed_logs": [
                {
                    "log_id": log.log_id,
                    "timestamp": log.timestamp,
                    "agent": log.agent,
                    "action": log.action,
                    "user": log.user,
                    "details": log.details
                }
                for log in filtered_logs
            ],
            "compliance_status": "COMPLIANT" if not compliance_issues else "ISSUES_FOUND",
            "compliance_issues": compliance_issues
        }
        
         # Save report (simulated)
        report_filename = f"audit_report_{report['report_id']}.json"
        print(f"\n💾 Report saved: {report_filename}")
        
        self._log_action("Generate Audit Report", {"report_id": report['report_id']}, "Admin")
        print(f"\n{'='*60}\n")
        
        return report
    
    def _check_compliance(self) -> List[str]:
        """Check for compliance issues"""
        issues = []
        
        # Check for pending leave requests > 7 days
        for req_id, req in self.db.leave_requests.items():
            if req.status == LeaveStatus.PENDING.value:
                submitted = datetime.datetime.fromisoformat(req.submitted_date)
                if (datetime.datetime.now() - submitted).days > 7:
                    issues.append(f"Leave request {req_id} pending for >7 days")
        
        return issues
    
    # ==================== FUNCTION 5: EVALUATE CANDIDATE ====================
    
    def evaluate_candidate(self, candidate: Candidate, job_position: JobPosition) -> Dict:
        """
        Evaluate candidate against job requirements and eligibility criteria
        Returns evaluation result with score and decision
        """
        print(f"\n{'='*60}")
        print(f"📋 EVALUATING CANDIDATE")
        print(f"{'='*60}")
        
        print(f"\n👤 Candidate: {candidate.name}")
        print(f"📧 Email: {candidate.email}")
        print(f"💼 Applied Position: {job_position.title}")
        
        # Get eligibility criteria
        criteria = self.db.eligibility_criteria
        
        # Calculate skill match score
        required_skills = set(s.lower() for s in job_position.required_skills)
        candidate_skills = set(s.lower() for s in candidate.extracted_skills)
        
        matched_skills = required_skills.intersection(candidate_skills)
        skill_match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0
        
        print(f"\n🎯 Skill Analysis:")
        print(f"   Required Skills: {', '.join(job_position.required_skills)}")
        print(f"   Candidate Skills: {', '.join(candidate.extracted_skills)}")
        print(f"   Matched Skills: {', '.join(matched_skills)}")
        print(f"   Match Score: {skill_match_percentage:.1f}%")
        
        # Check experience
        experience_met = candidate.experience_years >= job_position.min_experience
        print(f"\n📅 Experience Check:")
        print(f"   Required: {job_position.min_experience} years")
        print(f"   Candidate: {candidate.experience_years} years")
        print(f"   Status: {'✅ Met' if experience_met else '❌ Not Met'}")
        
        # Check education
        education_met = job_position.min_education.lower() in candidate.education.lower()
        print(f"\n🎓 Education Check:")
        print(f"   Required: {job_position.min_education}")
        print(f"   Candidate: {candidate.education}")
        print(f"   Status: {'✅ Met' if education_met else '❌ Not Met'}")
        
        # Get criteria settings
        criteria = self.db.eligibility_criteria
        exp_required_strict = criteria.get('experience_required', True)
        edu_required_strict = criteria.get('education_required', True)
        
        # Calculate overall score
        score = skill_match_percentage
        
        # Only apply penalties if strict mode is enabled AND requirement not met
        if exp_required_strict and not experience_met:
            score *= 0.7  # Penalty for not meeting experience
        if edu_required_strict and not education_met:
            score *= 0.8  # Penalty for not meeting education
        
        print(f"\n📊 Overall Score: {score:.1f}%")
        
        # Make decision based on criteria
        skill_threshold = criteria.get('skill_match_threshold', 50)
        auto_accept_threshold = criteria.get('auto_accept_threshold', 50)
        
        # Decision logic - if score meets threshold, accept (penalties already applied)
        if score >= auto_accept_threshold:
            decision = "Accepted"
            message = f"Candidate meets requirements with {score:.1f}% match score"
            print(f"\n✅ DECISION: {decision}")
            print(f"   {message}")
        elif score >= skill_threshold:
            decision = "Pending Review"
            message = f"Candidate shows potential with {score:.1f}% match. Manual review recommended."
            print(f"\n⏳ DECISION: {decision}")
            print(f"   {message}")
        else:
            decision = "Rejected"
            message = f"Candidate does not meet minimum requirements. Score: {score:.1f}%"
            print(f"\n❌ DECISION: {decision}")
            print(f"   {message}")
        
        evaluation_result = {
            "score": round(score, 2),
            "skill_match_percentage": round(skill_match_percentage, 2),
            "matched_skills": list(matched_skills),
            "experience_met": experience_met,
            "education_met": education_met,
            "decision": decision,
            "message": message,
            "evaluated_date": datetime.datetime.now().isoformat()
        }
        
        # Update candidate record
        candidate.status = decision
        candidate.evaluation_result = evaluation_result
        
        # Log the evaluation
        self._log_action("Candidate Evaluation", {
            "candidate_id": candidate.candidate_id,
            "candidate_name": candidate.name,
            "job_position": job_position.title,
            "decision": decision,
            "score": round(score, 2)
        }, "System")
        
        print(f"\n{'='*60}\n")
        
        return {
            "status": "success",
            "evaluation": evaluation_result,
            "candidate_id": candidate.candidate_id
        }
    
    # ==================== FUNCTION 6: PARSE RESUME (LLM-POWERED) ====================
    
    def parse_resume_text(self, resume_text: str) -> Dict:
        """
        Parse resume text to extract skills, experience, and education
        Uses LLM for intelligent parsing (more accurate than pattern matching)
        """
        import re
        
        # If LLM is available, use it for intelligent parsing
        if self.llm.client:
            try:
                prompt = f"""Analyze this resume and extract the following information in JSON format:

RESUME TEXT:
{resume_text[:3000]}

Please extract:
1. "skills": List of technical and professional skills mentioned (programming languages, frameworks, tools, methodologies, soft skills)
2. "experience_years": Total years of professional work experience (as a number, e.g., 5)
3. "education": Highest education level (choose from: "PhD", "Master's Degree", "Bachelor's Degree", "Diploma", "High School", "Not Specified")

IMPORTANT:
- For experience_years: Calculate total years from all job experiences. If resume says "2020-2023", that's 3 years. If it says "5 years of experience", use 5.
- For skills: Include all technical skills, tools, frameworks, programming languages, and relevant professional skills
- For education: Return only the highest degree mentioned

Return ONLY valid JSON in this exact format:
{{
  "skills": ["Python", "Django", "SQL", "AWS"],
  "experience_years": 5,
  "education": "Bachelor's Degree"
}}"""

                system_prompt = "You are an expert HR assistant specialized in parsing resumes. Extract information accurately and return only valid JSON."
                
                response = self.llm.generate_response(prompt, system_prompt, include_employee_data=False)
                
                # Try to parse JSON from response
                import json
                
                # Extract JSON from response (in case LLM adds extra text)
                json_match = re.search(r'\{[\s\S]*\}', response)
                if json_match:
                    parsed_data = json.loads(json_match.group(0))
                    
                    # Validate and return
                    return {
                        "skills": parsed_data.get("skills", []),
                        "experience_years": int(parsed_data.get("experience_years", 0)),
                        "education": parsed_data.get("education", "Not Specified")
                    }
                else:
                    print("⚠️ LLM parsing failed, falling back to pattern matching")
                    return self._fallback_parse(resume_text)
                    
            except Exception as e:
                print(f"⚠️ LLM parsing error: {e}, falling back to pattern matching")
                return self._fallback_parse(resume_text)
        else:
            # No LLM available, use fallback
            print("⚠️ No LLM available, using pattern matching")
            return self._fallback_parse(resume_text)
    
    def _fallback_parse(self, resume_text: str) -> Dict:
        """Fallback pattern matching parser (used when LLM is unavailable)"""
        import re
        
        # Common skills to look for
        skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data science', 'analytics',
            'rest api', 'graphql', 'microservices',
            'git', 'agile', 'scrum', 'ci/cd',
            'marketing', 'seo', 'content strategy', 'digital marketing', 'social media',
            'project management', 'leadership', 'communication'
        ]
        
        resume_lower = resume_text.lower()
        
        # Extract skills
        extracted_skills = []
        for skill in skill_keywords:
            if skill in resume_lower:
                extracted_skills.append(skill.title())
        
        # Extract experience (look for patterns like "5 years", "3+ years")
        experience_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+in'
        ]
        
        experience_years = 0
        for pattern in experience_patterns:
            match = re.search(pattern, resume_lower)
            if match:
                experience_years = max(experience_years, int(match.group(1)))
        
        # Extract education
        education_keywords = {
            "PhD": ["phd", "ph.d", "doctor of philosophy"],
            "Master's Degree": ["master", "msc", "m.sc", "mba", "m.b.a"],
            "Bachelor's Degree": ["bachelor", "bsc", "b.sc", "b.tech", "b.e", "ba", "b.a"],
            "Diploma": ["diploma"],
            "High School": ["high school", "secondary"]
        }
        
        education = "Not Specified"
        for edu_level, keywords in education_keywords.items():
            if any(keyword in resume_lower for keyword in keywords):
                education = edu_level
                break
        
        return {
            "skills": extracted_skills,
            "experience_years": experience_years,
            "education": education
        }
    
    def send_test_result_email(self, candidate_email: str, candidate_name: str, 
                               passed: bool, test_score: float, position: str,
                               username: str = None, password: str = None) -> Dict:
        """
        Send email to candidate with test results using LLM-generated content
        If passed, includes employee portal credentials
        """
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        print(f"\n{'='*60}")
        print(f"📧 SENDING TEST RESULT EMAIL")
        print(f"{'='*60}")
        
        # Generate email content using LLM
        prompt = f"""
        Generate a professional email to inform a job candidate about their test results.
        
        Candidate Name: {candidate_name}
        Position Applied: {position}
        Test Score: {test_score:.1f}%
        Result: {'PASSED' if passed else 'FAILED'}
        
        {'Username: ' + username if username else ''}
        {'Password: ' + password if password else ''}
        
        Email should include:
        1. Professional greeting
        2. {'Congratulations on passing the test' if passed else 'Thank you for taking the test'}
        3. Mention their score: {test_score:.1f}%
        4. {'Welcome them to the company and provide login credentials for the Employee Portal' if passed else 'Encourage them to apply for other positions in the future'}
        5. Professional closing
        
        Keep it concise, warm, and professional. Return ONLY the email body text, no subject line.
        """
        
        try:
            email_body = self.llm.ask_question(prompt)
            
            # Generate subject line using LLM
            subject_prompt = f"""
            Generate a short professional email subject line for a job application test result.
            The candidate {'passed' if passed else 'did not pass'} the test for {position} position.
            Keep it under 10 words. Return ONLY the subject line, nothing else.
            """
            subject = self.llm.ask_question(subject_prompt).strip().strip('"').strip("'")
            
        except Exception as e:
            print(f"⚠️ LLM email generation failed: {e}")
            # Fallback email content
            if passed:
                subject = f"Congratulations! You've been selected for {position}"
                email_body = f"""
Dear {candidate_name},

Congratulations! We are pleased to inform you that you have successfully passed the assessment test for the {position} position with a score of {test_score:.1f}%.

We are excited to welcome you to our team! Below are your credentials to access the Employee Portal:

Username: {username}
Password: {password}

Please log in to the Employee Portal to complete your onboarding process and access company resources.

We look forward to working with you!

Best regards,
HR Department
                """
            else:
                subject = f"Test Results for {position} Position"
                email_body = f"""
Dear {candidate_name},

Thank you for taking the assessment test for the {position} position.

After careful evaluation, we regret to inform you that your test score of {test_score:.1f}% did not meet our current requirements for this position.

We appreciate your interest in our company and encourage you to apply for other positions that match your skills and experience in the future.

Best regards,
HR Department
                """
        
        # Get email configuration from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            print("⚠️ Email credentials not configured in .env file")
            print("   Please add SENDER_EMAIL and SENDER_PASSWORD to .env")
            return {
                "status": "error",
                "message": "Email credentials not configured. Please contact admin.",
                "email_content": email_body  # Still return the generated content for testing
            }
        
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = candidate_email
            message["Subject"] = subject
            message.attach(MIMEText(email_body, "plain"))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"✅ Email sent successfully to {candidate_email}")
            print(f"📨 Subject: {subject}")
            
            # Log the action
            self._log_action(
                "Send Test Result Email",
                {
                    "candidate_email": candidate_email,
                    "position": position,
                    "passed": passed,
                    "score": test_score
                }
            )
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {candidate_email}",
                "subject": subject,
                "email_content": email_body
            }
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "email_content": email_body  # Still return content for manual sending
            }

# ==================== DEMO / TESTING INTERFACE ====================

def run_demo():
    """Run demonstration of all HR Agent functionalities"""
    
    print("\n" + "="*60)
    print("🤖 HR AGENT - ENTERPRISE AUTOMATION PLATFORM")
    print("="*60)
    
    # Initialize system
    print("\n⚙️  Initializing system...")
    db = Database()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment or prompt user
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n💡 Tip: Create a .env file with GROQ_API_KEY=your_key_here to avoid this prompt")
        print("💡 Get a free API key from https://console.groq.com/")
        api_key = input("\n🔑 Enter Groq API key (or press Enter to skip): ").strip()
        if not api_key:
            api_key = None
    else:
        print(f"✅ Loaded API key from .env file")
    
    llm = LLMInterface(api_key)
    agent = HRAgent(db, llm)
    
    print("✅ System initialized successfully!\n")
    
    # Demo menu
    while True:
        print("\n" + "="*60)
        print("📋 HR AGENT MENU")
        print("="*60)
        print("\n1. 📝 Process Leave Request")
        print("2. 🎉 Handle Employee Onboarding")
        print("3. ❓ Ask HR Policy Question")
        print("4. 📊 Generate Audit Report")
        print("5. 👥 View All Employees")
        print("6. 🚪 Exit")
        
        choice = input("\n👉 Select option (1-6): ").strip()
        
        if choice == "1":
            # Process Leave Request
            print("\n--- Process Leave Request ---")
            emp_id = input("Employee ID (e.g., EMP001): ").strip() or "EMP001"
            leave_type = input("Leave Type (Casual Leave/Sick Leave/Annual Leave): ").strip() or "Casual Leave"
            start_date = input("Start Date (YYYY-MM-DD): ").strip() or "2025-11-01"
            end_date = input("End Date (YYYY-MM-DD): ").strip() or "2025-11-03"
            reason = input("Reason: ").strip() or "Personal work"
            
            result = agent.process_leave_request(emp_id, leave_type, start_date, end_date, reason)
            
        elif choice == "2":
            # Handle Employee Onboarding
            print("\n--- Employee Onboarding ---")
            name = input("Full Name: ").strip() or "Alice Johnson"
            email = input("Email: ").strip() or "alice.johnson@company.com"
            department = input("Department: ").strip() or "Sales"
            position = input("Position: ").strip() or "Sales Executive"
            join_date = input("Join Date (YYYY-MM-DD): ").strip() or "2025-11-01"
            
            result = agent.handle_employee_onboarding(name, email, department, position, join_date)
            
        elif choice == "3":
            # Ask HR Policy Question
            print("\n--- Ask HR Policy Question ---")
            question = input("Your question: ").strip() or "How many sick leave days do I get?"
            
            result = agent.ask_hr_policy_question(question)
            
        elif choice == "4":
            # Generate Audit Report
            print("\n--- Generate Audit Report ---")
            start = input("Start Date (YYYY-MM-DD, press Enter for last 30 days): ").strip()
            end = input("End Date (YYYY-MM-DD, press Enter for today): ").strip()
            
            result = agent.generate_audit_report(start or None, end or None)
            
        elif choice == "5":
            # View All Employees
            print("\n--- All Employees ---")
            for emp_id, emp in db.employees.items():
                print(f"\n{emp_id}: {emp.name}")
                print(f"   Department: {emp.department}")
                print(f"   Position: {emp.position}")
                print(f"   Email: {emp.email}")
                print(f"   Leave Balance: {emp.leave_balance}")
            
        elif choice == "6":
            print("\n👋 Thank you for using HR Agent!")
            print("="*60 + "\n")
            break
        
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\n⏸️  Press Enter to continue...")

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    run_demo()