"""
Chat-Based Technical Interview UI with Split Screen
Left: AI Interview Chat | Right: Code Editor
"""
import streamlit as st
from streamlit_ace import st_ace
import datetime
import time
from typing import Dict, Optional, List
from code_executor import CodeExecutor
from technical_interview_chat import TechnicalInterviewChat
from interview_storage import InterviewStorage


def show_chat_technical_interview(db, candidate_id: str):
    """
    Display chat-based technical interview with split screen
    AI interviewer guides through problem-solving process
    """
    candidate = db.get_candidate(candidate_id)
    
    # Custom CSS for split-screen layout
    st.markdown("""
    <style>
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stage-indicator {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
    .stage-item {
        flex: 1;
        text-align: center;
        padding: 0.5rem;
        border-radius: 5px;
        font-size: 0.85rem;
    }
    .stage-active {
        background: #667eea;
        color: white;
        font-weight: bold;
    }
    .stage-complete {
        background: #48bb78;
        color: white;
    }
    .stage-pending {
        background: #e2e8f0;
        color: #718096;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 8px;
        animation: fadeIn 0.3s;
    }
    .chat-ai {
        background: white;
        border-left: 4px solid #667eea;
    }
    .chat-user {
        background: #e6f2ff;
        border-left: 4px solid #4299e1;
        margin-left: 2rem;
    }
    .chat-hint {
        background: #fff5e6;
        border-left: 4px solid #f6ad55;
    }
    .hint-badge {
        display: inline-block;
        background: #f6ad55;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'chat_interview' not in st.session_state:
        st.session_state.chat_interview = TechnicalInterviewChat()
        st.session_state.chat_messages = []
        st.session_state.chat_stage = 'INTRODUCTION'
        st.session_state.chat_started = False
        st.session_state.selected_problem_id = None
        st.session_state.code_submitted = False
        st.session_state.test_results = []
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <h2>💬 AI Technical Interview</h2>
        <p>Chat with AI Interviewer • Get Hints • Debug Together</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem selection (if not started)
    if not st.session_state.chat_started:
        show_problem_selection_chat(db)
        return
    
    # Get current problem
    problem = db.get_technical_problem(st.session_state.selected_problem_id)
    
    # Stage indicator
    show_stage_indicator(st.session_state.chat_interview.current_stage)
    
    # Split screen: Chat (left) | Code (right)
    col_chat, col_code = st.columns([1, 1])
    
    with col_chat:
        st.markdown("### 💬 Interview Chat")
        show_chat_interface(st.session_state.chat_interview, problem)
    
    with col_code:
        st.markdown("### 💻 Code Editor")
        show_code_editor_with_chat(db, candidate_id, problem)


def show_problem_selection_chat(db):
    """Problem selection screen for chat interview"""
    st.markdown("### 🎯 Select a Problem to Start Interview")
    st.markdown("The AI interviewer will guide you through the entire process.")
    
    problems = list(db.technical_problems.values())
    
    cols = st.columns(2)
    for i, problem in enumerate(problems):
        with cols[i % 2]:
            difficulty_colors = {
                'Easy': '#48bb78',
                'Medium': '#f6ad55',
                'Hard': '#f56565'
            }
            color = difficulty_colors.get(problem.difficulty, '#718096')
            
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 8px; 
                        border-left: 4px solid {color}; margin: 1rem 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="margin: 0;">{problem.title}</h3>
                <p style="color: {color}; font-weight: bold; margin: 0.5rem 0;">
                    {problem.difficulty}
                </p>
                <p style="color: #718096; font-size: 0.9rem;">
                    {', '.join(problem.tags[:3])}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🎯 Start Interview", key=f"start_{problem.problem_id}"):
                st.session_state.selected_problem_id = problem.problem_id
                st.session_state.chat_started = True
                
                # Start interview with AI introduction
                intro = st.session_state.chat_interview.start_interview({
                    'title': problem.title,
                    'difficulty': problem.difficulty,
                    'description': problem.description,
                    'examples': problem.examples,
                })
                
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': intro,
                    'stage': 'introduction',
                    'type': 'intro'
                })
                
                st.rerun()


def show_stage_indicator(current_stage: str):
    """Show interview progress stages"""
    stages = [
        ('INTRODUCTION', '👋 Intro'),
        ('CLARIFICATION', '❓ Questions'),
        ('APPROACH', '💡 Approach'),
        ('CODING', '💻 Coding'),
        ('REVIEW', '✅ Review')
    ]
    
    stage_order = [s[0] for s in stages]
    current_idx = stage_order.index(current_stage.upper()) if current_stage.upper() in stage_order else 0
    
    stage_html = '<div class="stage-indicator">'
    for idx, (stage_key, stage_label) in enumerate(stages):
        if idx < current_idx:
            css_class = "stage-item stage-complete"
        elif idx == current_idx:
            css_class = "stage-item stage-active"
        else:
            css_class = "stage-item stage-pending"
        
        stage_html += f'<div class="{css_class}">{stage_label}</div>'
    
    stage_html += '</div>'
    st.markdown(stage_html, unsafe_allow_html=True)


def show_chat_interface(chat: TechnicalInterviewChat, problem: Dict):
    """Display chat messages and input"""
    
    # Use Streamlit's native container for better rendering
    chat_container = st.container()
    
    with chat_container:
        # Display messages using Streamlit's chat components
        for msg in st.session_state.chat_messages:
            role_icon = "🤖 AI Interviewer" if msg['role'] == 'assistant' else "👤 You"
            
            # Add hint badge if it's a hint message
            if msg.get('type') == 'hint':
                hint_num = msg.get('hint_number', 0)
                with st.chat_message("assistant", avatar="💡"):
                    st.markdown(f"**Hint #{hint_num}**")
                    st.markdown(msg["content"])
            else:
                # Use Streamlit's native chat message
                with st.chat_message(msg['role']):
                    st.markdown(msg["content"])
    
    # Add spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Action buttons based on stage
    current_stage = chat.current_stage.upper()
    
    if current_stage in ['INTRODUCTION', 'CLARIFICATION']:
        show_clarification_actions(chat, problem)
    elif current_stage == 'APPROACH':
        show_approach_actions(chat)
    elif current_stage == 'CODING':
        show_coding_actions(chat)
    elif current_stage == 'REVIEW':
        show_review_actions(chat)


def show_clarification_actions(chat: TechnicalInterviewChat, problem: Dict):
    """Actions for clarification stage"""
    st.markdown("---")
    st.markdown("**💭 Ask Questions or Discuss Your Approach**")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            key="clarification_input",
            placeholder="Ask about edge cases, constraints, or explain your approach..."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 Send", key="send_clarification"):
            if user_input:
                # Add user message
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': user_input,
                    'stage': 'clarification'
                })
                
                # Get AI response
                response = chat.handle_clarification(user_input)
                
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': response,
                    'stage': 'clarification'
                })
                
                st.rerun()
    
    if st.button("✅ I'm Ready to Discuss My Approach", key="ready_approach"):
        st.session_state.chat_interview.current_stage = 'APPROACH'
        
        prompt_msg = "Great! Please explain how you plan to solve this problem. What data structures will you use? What's your approach?"
        
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': prompt_msg,
            'stage': 'approach'
        })
        
        st.rerun()


def show_approach_actions(chat: TechnicalInterviewChat):
    """Actions for approach discussion stage"""
    st.markdown("---")
    st.markdown("**💡 Explain Your Approach**")
    
    approach_text = st.text_area(
        "Describe your solution approach:",
        key="approach_input",
        placeholder="I'll use a hash map to... Time complexity is O(n)...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Submit Approach", key="submit_approach"):
            if approach_text:
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': approach_text,
                    'stage': 'approach'
                })
                
                # Evaluate approach
                feedback = chat.discuss_approach(approach_text)
                
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': feedback.get('feedback_message', 'Good approach!'),
                    'stage': 'approach',
                    'feedback': feedback
                })
                
                st.rerun()
    
    with col2:
        if st.button("💻 Start Coding", key="start_coding"):
            st.session_state.chat_interview.current_stage = 'CODING'
            
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': "Perfect! Go ahead and implement your solution. I'm here if you need hints or help debugging!",
                'stage': 'coding'
            })
            
            st.rerun()


def show_coding_actions(chat: TechnicalInterviewChat):
    """Actions during coding stage"""
    st.markdown("---")
    st.markdown("**💻 Coding Assistance**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Get a Hint", key="get_hint"):
            current_code = st.session_state.get('current_code', '')
            hint = chat.get_context_aware_hint(current_code)
            
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': hint,
                'stage': 'coding',
                'type': 'hint',
                'hint_number': chat.hint_count
            })
            
            st.rerun()
    
    with col2:
        if st.button("🐛 Help Debug", key="help_debug"):
            current_code = st.session_state.get('current_code', '')
            test_results = st.session_state.get('test_results', [])
            
            prompt_msg = "Sure! Tell me what's going wrong. Which test cases are failing? What do you think might be the issue?"
            
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': prompt_msg,
                'stage': 'debugging'
            })
            
            st.session_state.chat_interview.current_stage = 'DEBUGGING'
            st.rerun()
    
    # Debug conversation input
    if chat.current_stage == 'DEBUGGING':
        st.markdown("---")
        debug_msg = st.text_area(
            "Describe the bug:",
            key="debug_input",
            placeholder="Test case 3 is failing. I think the issue is...",
            height=80
        )
        
        if st.button("📤 Send Debug Message", key="send_debug"):
            if debug_msg:
                current_code = st.session_state.get('current_code', '')
                test_results = st.session_state.get('test_results', [])
                
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': debug_msg,
                    'stage': 'debugging'
                })
                
                response = chat.debug_conversation(debug_msg, current_code, test_results)
                
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': response,
                    'stage': 'debugging'
                })
                
                st.rerun()


def show_review_actions(chat: TechnicalInterviewChat):
    """Actions for code review stage"""
    st.markdown("---")
    st.markdown("**✅ Post-Solution Discussion**")
    
    # Follow-up questions
    if st.button("💬 Ask Follow-up Question", key="followup"):
        question = chat.ask_follow_up_question("optimization")
        
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': question,
            'stage': 'follow_up'
        })
        
        st.rerun()
    
    # Answer follow-up
    answer_text = st.text_area(
        "Your answer:",
        key="followup_answer",
        placeholder="To optimize further, we could...",
        height=80
    )
    
    if st.button("📤 Submit Answer", key="submit_answer"):
        if answer_text:
            st.session_state.chat_messages.append({
                'role': 'user',
                'content': answer_text,
                'stage': 'follow_up'
            })
            
            evaluation = chat.evaluate_explanation(answer_text)
            
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': evaluation.get('feedback', 'Good explanation!'),
                'stage': 'follow_up'
            })
            
            st.rerun()
    
    if st.button("🎉 Complete Interview", key="complete"):
        st.session_state.chat_interview.current_stage = 'COMPLETE'
        st.success("Interview completed! Check your final report below.")
        
        # Show final report
        report = chat.get_final_report()
        st.json(report)


def show_code_editor_with_chat(db, candidate_id: str, problem: Dict):
    """Code editor integrated with chat system"""
    
    # Language selector
    language_options = {
        'Python': 'python',
        'Java': 'java',
        'C++': 'cpp'
    }
    
    selected_lang = st.selectbox(
        "Language:",
        list(language_options.keys()),
        key="chat_language_select"
    )
    
    language = language_options[selected_lang]
    starter_code = problem.starter_code.get(language, f"# Write your {selected_lang} solution here")
    
    # Code editor
    if 'current_code' not in st.session_state:
        st.session_state.current_code = starter_code
    
    code = st_ace(
        value=st.session_state.current_code,
        language=language,
        theme='github',
        key='chat_code_editor',
        height=350,
        font_size=14
    )
    
    st.session_state.current_code = code
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Run Code", key="chat_run"):
            run_code_with_chat(db, code, language, problem, visible_only=True)
    
    with col2:
        if st.button("✅ Submit", key="chat_submit"):
            submit_code_with_chat(db, candidate_id, code, language, problem)
    
    with col3:
        if st.button("🔄 Reset", key="chat_reset"):
            st.session_state.current_code = starter_code
            st.rerun()
    
    # Show test results
    if st.session_state.get('test_results'):
        st.markdown("---")
        st.markdown("### 🧪 Test Results")
        st.caption(f"Last run: {datetime.datetime.now().strftime('%H:%M:%S')}")
        display_test_results_compact(st.session_state.test_results)


def run_code_with_chat(db, code: str, language: str, problem: Dict, visible_only: bool = True):
    """Run code and show results"""
    # Clear old test results first
    if 'test_results' in st.session_state:
        del st.session_state.test_results
    
    executor = CodeExecutor()
    
    # Get test cases
    test_cases = [tc for tc in problem.test_cases if tc.get('visible', True)] if visible_only else problem.test_cases
    
    # Show execution method
    if language.lower() == 'python':
        st.info("💻 Running Python code locally (instant execution)")
    
    with st.spinner("🚀 Running tests..."):
        results = executor.run_test_cases(code, language, test_cases)
    
    # Store the full results dict with timestamp to force refresh
    st.session_state.test_results = results
    st.session_state.test_results_timestamp = time.time()
    st.rerun()


def submit_code_with_chat(db, candidate_id: str, code: str, language: str, problem: Dict):
    """Submit code for full evaluation"""
    executor = CodeExecutor()
    chat = st.session_state.chat_interview
    
    with st.spinner("🔍 Running all tests and analyzing code..."):
        # Run all tests
        results = executor.run_test_cases(code, language, problem.test_cases)
        st.session_state.test_results = results
        
        # AI analysis - pass test_results list
        test_results_list = results.get('test_results', [])
        analysis = chat.analyze_code_submission(code, test_results_list)
        
        # Calculate scores
        test_score = (results.get('passed', 0) / results.get('total', 1)) * 50  # 50% weight
        quality_score = (analysis.get('code_quality_score', 70) / 100) * 30  # 30% weight
        approach_score = (chat.approach_quality / 100) * 10  # 10% weight
        communication_score = (chat.communication_score / 100) * 10  # 10% weight
        hint_penalty = chat.hint_count * 5  # -5 points per hint
        
        final_score = test_score + quality_score + approach_score + communication_score - hint_penalty
        final_score = max(0, min(100, final_score))  # Clamp between 0-100
        
        # Get interview report
        interview_report = chat.get_final_report()
        
        # Prepare scoring data
        scoring_data = {
            'test_score': test_score,
            'quality_score': quality_score,
            'approach_score': approach_score,
            'communication_score': communication_score,
            'hint_penalty': -hint_penalty,
            'final_score': final_score,
            'test_results': {
                'passed': results.get('passed', 0),
                'total': results.get('total', 0),
                'all_passed': results.get('all_passed', False)
            },
            'code_quality_details': analysis
        }
        
        # Save to JSON
        storage = InterviewStorage()
        saved_path = storage.save_interview_result(
            candidate_id=candidate_id,
            interview_data=interview_report,
            scoring_data=scoring_data
        )
        
        # Store path in session for display
        st.session_state.saved_interview_path = saved_path
        
        # Add to chat
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': analysis.get('overall_feedback', 'Analysis complete!'),
            'stage': 'review',
            'analysis': analysis,
            'final_score': final_score
        })
        
        # Move to review stage
        chat.current_stage = 'REVIEW'
        st.session_state.code_submitted = True
        
        # Mark technical interview as completed if tests passed
        if results.get('all_passed', False):
            st.session_state.technical_completed = True
    
    st.success(f"✅ Code submitted and analyzed! Final Score: {final_score:.1f}/100")
    st.info(f"💾 Results saved to: {st.session_state.saved_interview_path}")
    st.rerun()


def display_test_results_compact(results):
    """Compact test results display"""
    # Handle different result formats
    if isinstance(results, dict):
        # If results is a dict with test_results key
        if 'test_results' in results:
            test_list = results['test_results']
            total = results.get('total', len(test_list))
            passed = results.get('passed', 0)
        else:
            return  # Invalid format
    elif isinstance(results, list):
        # If results is already a list
        test_list = results
        passed = sum(1 for r in test_list if isinstance(r, dict) and r.get('status') == 'passed')
        total = len(test_list)
    else:
        st.error("Invalid test results format")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Passed", passed, delta=f"{(passed/total*100):.0f}%" if total > 0 else "0%")
    col3.metric("Failed", total - passed)
    
    # Show detailed results with actual vs expected
    for i, result in enumerate(test_list[:5]):  # Show first 5
        if isinstance(result, dict):
            status = result.get('status', 'unknown')
            status_emoji = "✅" if status == 'passed' else "❌" if status == 'failed' else "⚠️"
            
            with st.expander(f"{status_emoji} Test {i+1}: {status.upper()}", expanded=(status != 'passed')):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.text(f"Input:\n{result.get('input', 'N/A')}")
                    st.text(f"Expected:\n{result.get('expected', 'N/A')}")
                with col_b:
                    actual = result.get('actual', '')
                    st.text(f"Your Output:\n{actual if actual else '(no output)'}")
                    if result.get('error'):
                        st.error(f"Error:\n{result.get('error')}")
                    
                # Show execution details
                if status != 'passed':
                    st.caption(f"⏱️ Time: {result.get('time', 0):.3f}s | 💾 Memory: {result.get('memory', 0)} KB")
