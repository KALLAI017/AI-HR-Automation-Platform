"""
Technical Interview Interface for Streamlit
Beautiful UI for coding problems with AI evaluation
"""
import streamlit as st
from streamlit_ace import st_ace
import datetime
from typing import Dict, Optional
from code_executor import CodeExecutor
from ai_code_analyzer import AICodeAnalyzer


def show_technical_interview(db, candidate_id: str):
    """
    Display technical interview interface
    Shows after candidate passes assessment test
    """
    candidate = db.get_candidate(candidate_id)
    
    # Custom CSS for beautiful UI
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .problem-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .code-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .test-result {
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .test-passed {
        background: #d4edda;
        border-left: 4px solid #28a745;
    }
    .test-failed {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .test-hidden {
        background: #e7f3ff;
        border-left: 4px solid #0066cc;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ai-feedback {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💻 Technical Interview</h1>
        <p>Google-Style Coding Challenge with AI Evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'selected_problem' not in st.session_state:
        st.session_state.selected_problem = None
    if 'code_submitted' not in st.session_state:
        st.session_state.code_submitted = False
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None
    if 'ai_analysis' not in st.session_state:
        st.session_state.ai_analysis = None
    if 'interview_mode' not in st.session_state:
        st.session_state.interview_mode = False
    if 'interview_questions' not in st.session_state:
        st.session_state.interview_questions = []
    
    # Problem Selection
    if st.session_state.selected_problem is None:
        show_problem_selection(db)
    else:
        show_coding_interface(db, candidate_id)


def show_problem_selection(db):
    """Display problem selection screen"""
    st.markdown("### 📚 Select a Coding Problem")
    
    col1, col2, col3 = st.columns(3)
    
    problems = list(db.technical_problems.values())
    
    for i, problem in enumerate(problems):
        col = [col1, col2, col3][i % 3]
        
        with col:
            difficulty_color = {
                "Easy": "🟢",
                "Medium": "🟡",
                "Hard": "🔴"
            }.get(problem.difficulty, "⚪")
            
            st.markdown(f"""
            <div class="problem-card">
                <h4>{difficulty_color} {problem.title}</h4>
                <p><strong>Difficulty:</strong> {problem.difficulty}</p>
                <p><strong>Tags:</strong> {', '.join(problem.tags)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Problem", key=f"select_{problem.problem_id}"):
                st.session_state.selected_problem = problem.problem_id
                st.rerun()


def show_coding_interface(db, candidate_id):
    """Display the main coding interface"""
    problem = db.get_technical_problem(st.session_state.selected_problem)
    
    if not problem:
        st.error("Problem not found!")
        return
    
    # Problem Description
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            difficulty_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}[problem.difficulty]
            st.markdown(f"## {difficulty_emoji} {problem.title}")
        
        with col2:
            if st.button("← Change Problem"):
                st.session_state.selected_problem = None
                st.session_state.code_submitted = False
                st.session_state.test_results = None
                st.session_state.ai_analysis = None
                st.rerun()
    
    # Problem Details in Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Description", "💡 Examples", "📋 Constraints"])
    
    with tab1:
        st.markdown(f"""
        <div class="problem-card">
        {problem.description}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Input Format:**")
        st.code(problem.input_format)
        
        st.markdown("**Output Format:**")
        st.code(problem.output_format)
    
    with tab2:
        for i, example in enumerate(problem.examples, 1):
            st.markdown(f"**Example {i}:**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Input:**")
                st.code(example['input'])
            with col2:
                st.markdown("**Output:**")
                st.code(example['output'])
            st.info(f"**Explanation:** {example['explanation']}")
    
    with tab3:
        st.code(problem.constraints)
        st.info(f"⏱️ Time Limit: {problem.time_limit} seconds | 💾 Memory Limit: {problem.memory_limit // 1024} MB")
    
    st.markdown("---")
    
    # Language Selection and Code Editor
    col1, col2 = st.columns([1, 3])
    
    with col1:
        language = st.selectbox(
            "Language",
            options=["python", "java", "cpp"],
            format_func=lambda x: {"python": "🐍 Python", "java": "☕ Java", "cpp": "⚡ C++"}[x]
        )
    
    st.markdown('<div class="code-section">', unsafe_allow_html=True)
    
    # Initialize code in session state
    if 'user_code' not in st.session_state:
        st.session_state.user_code = problem.starter_code.get(language, "")
    
    # Code Editor
    code = st_ace(
        value=st.session_state.user_code,
        language=language if language != "cpp" else "c_cpp",
        theme="monokai",
        key="code_editor",
        height=400,
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=False,
        wrap=True,
        auto_update=True,
    )
    
    st.session_state.user_code = code
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.button("▶️ Run Code", type="primary", use_container_width=True):
            run_code(db, candidate_id, problem, code, language)
    
    with col2:
        if st.button("✅ Submit Solution", use_container_width=True):
            submit_solution(db, candidate_id, problem, code, language)
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.user_code = problem.starter_code.get(language, "")
            st.rerun()
    
    # Display Results
    if st.session_state.test_results:
        display_test_results(st.session_state.test_results)
    
    if st.session_state.ai_analysis:
        display_ai_analysis(st.session_state.ai_analysis)
    
    # AI Interview Mode
    if st.session_state.interview_mode:
        show_ai_interview(db, candidate_id, problem, code)


def run_code(db, candidate_id, problem, code, language):
    """Run code with visible test cases only"""
    executor = CodeExecutor()
    
    with st.spinner("🔄 Running your code..."):
        visible_tests = [tc for tc in problem.test_cases if tc.get('visible', True)]
        
        if not visible_tests:
            visible_tests = problem.test_cases[:2]  # Show first 2 if none marked visible
        
        results = executor.run_test_cases(code, language, visible_tests, problem.time_limit)
        st.session_state.test_results = results
        st.rerun()


def submit_solution(db, candidate_id, problem, code, language):
    """Submit solution for full evaluation"""
    executor = CodeExecutor()
    analyzer = AICodeAnalyzer()
    
    with st.spinner("🤖 Evaluating your solution... This may take 30-60 seconds..."):
        # Run all test cases
        test_results = executor.run_test_cases(code, language, problem.test_cases, problem.time_limit)
        
        # AI Analysis
        ai_analysis = analyzer.analyze_code(code, language, problem.description)
        
        # Save submission
        submission_id = f"SUB{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        from hr_agent import CodeSubmission
        
        submission = CodeSubmission(
            submission_id=submission_id,
            candidate_id=candidate_id,
            problem_id=problem.problem_id,
            code=code,
            language=language,
            submitted_at=datetime.datetime.now().isoformat(),
            test_results=test_results,
            ai_analysis=ai_analysis
        )
        
        db.add_code_submission(submission)
        
        st.session_state.test_results = test_results
        st.session_state.ai_analysis = ai_analysis
        st.session_state.code_submitted = True
        
        # Mark technical interview as completed if tests passed
        if test_results['all_passed']:
            st.session_state.technical_completed = True
            st.session_state.interview_mode = True
        
        st.success("✅ Solution submitted successfully!")
        st.rerun()


def display_test_results(results):
    """Display test case results"""
    st.markdown("### 🧪 Test Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{results['total']}</h3>
            <p>Total Tests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <h3>{results['passed']}</h3>
            <p>Passed ✅</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);">
            <h3>{results['failed']}</h3>
            <p>Failed ❌</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>{results['error']}</h3>
            <p>Error ⚠️</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Individual Test Results
    for test in results['test_results']:
        if test.get('hidden'):
            status_class = "test-hidden"
            status_icon = "🔒"
        elif test['status'] == 'passed':
            status_class = "test-passed"
            status_icon = "✅"
        elif test['status'] == 'failed':
            status_class = "test-failed"
            status_icon = "❌"
        else:
            status_class = "test-failed"
            status_icon = "⚠️"
        
        st.markdown(f"""
        <div class="test-result {status_class}">
            <strong>{status_icon} Test Case {test['test_number']}</strong>
            {' (Hidden)' if test.get('hidden') else ''}
        </div>
        """, unsafe_allow_html=True)
        
        if not test.get('hidden') or test['status'] != 'passed':
            with st.expander("View Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Input:**")
                    st.code(test['input'])
                    st.markdown("**Expected:**")
                    st.code(test['expected'])
                with col2:
                    st.markdown("**Your Output:**")
                    st.code(test['actual'])
                    if test.get('error'):
                        st.error(f"Error: {test['error']}")
                
                st.info(f"⏱️ Time: {test['time']:.3f}s | 💾 Memory: {test['memory']} KB")


def display_ai_analysis(analysis):
    """Display AI code analysis"""
    st.markdown("### 🤖 AI Code Analysis")
    
    if analysis.get('status') == 'error':
        st.error(f"AI Analysis failed: {analysis.get('error', 'Unknown error')}")
        return
    
    # Overall Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = analysis.get('code_quality_score', 0)
        st.metric("Code Quality", f"{score}/100", 
                 delta="Good" if score >= 70 else "Needs Work")
    
    with col2:
        st.metric("Time Complexity", analysis.get('time_complexity', 'N/A'))
    
    with col3:
        st.metric("Space Complexity", analysis.get('space_complexity', 'N/A'))
    
    # Detailed Breakdown
    breakdown = analysis.get('quality_breakdown', {})
    
    st.markdown("**Quality Breakdown:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.progress(breakdown.get('naming_conventions', 0) / 100)
        st.caption(f"Naming Conventions: {breakdown.get('naming_conventions', 0)}/100")
        
        st.progress(breakdown.get('readability', 0) / 100)
        st.caption(f"Readability: {breakdown.get('readability', 0)}/100")
    
    with col2:
        st.progress(breakdown.get('modularity', 0) / 100)
        st.caption(f"Modularity: {breakdown.get('modularity', 0)}/100")
        
        st.progress(breakdown.get('comments', 0) / 100)
        st.caption(f"Comments: {breakdown.get('comments', 0)}/100")
    
    # Feedback
    st.markdown(f"""
    <div class="ai-feedback">
        <h4>💡 Overall Feedback</h4>
        <p>{analysis.get('overall_feedback', 'No feedback available')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Strengths:**")
        for strength in analysis.get('strengths', []):
            st.success(strength)
    
    with col2:
        st.markdown("**⚠️ Areas for Improvement:**")
        for weakness in analysis.get('weaknesses', []):
            st.warning(weakness)
    
    # Optimization Suggestions
    if analysis.get('optimization_suggestions'):
        st.markdown("**🚀 Optimization Suggestions:**")
        for suggestion in analysis['optimization_suggestions']:
            st.info(suggestion)


def show_ai_interview(db, candidate_id, problem, code):
    """AI interviewer asks follow-up questions"""
    st.markdown("---")
    st.markdown("### 🎤 AI Interview - Follow-up Questions")
    
    analyzer = AICodeAnalyzer()
    
    # Ask question if none asked yet
    if not st.session_state.interview_questions:
        question = analyzer.ask_followup_question(code, st.session_state.selected_problem, "")
        st.session_state.interview_questions.append({
            'question': question,
            'answer': None,
            'score': None
        })
    
    # Display questions and answers
    for i, qa in enumerate(st.session_state.interview_questions):
        st.markdown(f"**Question {i+1}:** {qa['question']}")
        
        if qa['answer'] is None:
            answer = st.text_area(f"Your Answer:", key=f"answer_{i}", height=100)
            
            if st.button("Submit Answer", key=f"submit_{i}"):
                # Evaluate answer
                evaluation = analyzer.evaluate_explanation(qa['question'], answer, code)
                
                qa['answer'] = answer
                qa['score'] = evaluation.get('overall_score', 0)
                qa['feedback'] = evaluation.get('feedback', '')
                
                # Save to database
                submissions = db.get_candidate_submissions(candidate_id)
                if submissions:
                    latest = submissions[-1]
                    db.update_submission_interview_qa(latest.submission_id, qa)
                
                st.rerun()
        else:
            st.text_area(f"Your Answer:", value=qa['answer'], key=f"shown_answer_{i}", disabled=True)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Score", f"{qa.get('score', 0)}/100")
            with col2:
                st.info(f"**Feedback:** {qa.get('feedback', '')}")
    
    # Add more questions or finish
    if len(st.session_state.interview_questions) < 3 and st.session_state.interview_questions[-1]['answer'] is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Ask Another Question"):
                context = f"Previous questions: {', '.join([q['question'] for q in st.session_state.interview_questions])}"
                question = analyzer.ask_followup_question(code, st.session_state.selected_problem, context)
                st.session_state.interview_questions.append({
                    'question': question,
                    'answer': None,
                    'score': None
                })
                st.rerun()
        
        with col2:
            if st.button("✅ Finish Interview", type="primary"):
                calculate_final_score(db, candidate_id)
                st.success("🎉 Interview Complete! Check your final score below.")
                st.rerun()
    elif len(st.session_state.interview_questions) == 3 and st.session_state.interview_questions[-1]['answer'] is not None:
        if st.button("✅ Finish Interview", type="primary", use_container_width=True):
            calculate_final_score(db, candidate_id)
            st.success("🎉 Interview Complete! Check your final score below.")
            st.rerun()


def calculate_final_score(db, candidate_id):
    """Calculate final interview score"""
    submissions = db.get_candidate_submissions(candidate_id)
    if not submissions:
        return
    
    latest = submissions[-1]
    
    # Calculate scores
    test_score = (latest.test_results['passed'] / latest.test_results['total']) * 50  # 50% weight
    quality_score = (latest.ai_analysis.get('code_quality_score', 0) / 100) * 30  # 30% weight
    
    interview_score = 0
    if latest.interview_qa:
        avg_interview = sum(qa.get('score', 0) for qa in latest.interview_qa) / len(latest.interview_qa)
        interview_score = (avg_interview / 100) * 20  # 20% weight
    
    final_score = test_score + quality_score + interview_score
    
    db.update_submission_final_score(latest.submission_id, final_score)
    
    # Display final score
    st.markdown("### 🏆 Final Interview Score")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Test Cases", f"{test_score:.1f}/50")
    with col2:
        st.metric("Code Quality", f"{quality_score:.1f}/30")
    with col3:
        st.metric("Interview", f"{interview_score:.1f}/20")
    with col4:
        st.metric("**Total**", f"{final_score:.1f}/100", 
                 delta="Pass" if final_score >= 60 else "Fail")
    
    if final_score >= 60:
        st.balloons()
        st.success("🎉 Congratulations! You passed the technical interview!")
    else:
        st.warning("Keep practicing! You can try again later.")
