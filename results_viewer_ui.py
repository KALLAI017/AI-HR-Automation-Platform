"""
Interview Results Viewer
UI to browse and analyze saved interview results
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from interview_storage import InterviewStorage


def show_interview_results_viewer():
    """Display interface to view saved interview results"""
    
    st.title("📊 Interview Results Viewer")
    st.markdown("Browse and analyze saved interview results")
    
    storage = InterviewStorage()
    
    # Get all candidates
    candidates = storage.get_all_candidates()
    
    if not candidates:
        st.info("💡 No interview results saved yet. Complete an interview to see results here.")
        return
    
    # Sidebar for candidate selection
    st.sidebar.header("🎯 Select Candidate")
    selected_candidate = st.sidebar.selectbox(
        "Candidate ID:",
        options=candidates,
        index=0
    )
    
    # Export all button
    if st.sidebar.button("📥 Export All Results"):
        export_path = storage.export_all_results()
        st.sidebar.success(f"Exported to:\n{export_path}")
    
    # Load candidate data
    interviews = storage.load_candidate_interviews(selected_candidate)
    summary = storage.get_candidate_summary(selected_candidate)
    
    # Display summary
    st.markdown("---")
    st.subheader(f"📋 Summary for {selected_candidate}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Interviews", summary['total_interviews'])
    with col2:
        st.metric("Average Score", f"{summary['average_score']:.1f}/100")
    with col3:
        st.metric("Highest Score", f"{summary['highest_score']:.1f}/100")
    with col4:
        st.metric("Problems Attempted", summary['problems_attempted'])
    
    # Display individual interviews
    st.markdown("---")
    st.subheader("📝 Individual Interviews")
    
    for idx, interview in enumerate(interviews):
        metadata = interview.get('metadata', {})
        interview_data = interview.get('interview_data', {})
        scoring = interview.get('scoring', {})
        
        # Create expander for each interview
        timestamp = metadata.get('timestamp', 'Unknown')
        problem = interview_data.get('problem', 'Unknown Problem')
        final_score = scoring.get('final_score', 0)
        
        # Color code by score
        score_emoji = "🟢" if final_score >= 80 else "🟡" if final_score >= 60 else "🔴"
        
        with st.expander(f"{score_emoji} Interview #{idx+1}: {problem} - {final_score:.1f}/100 ({timestamp})"):
            
            # Basic info
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**📅 Date & Time**")
                date_str = metadata.get('date', 'Unknown')
                if date_str != 'Unknown':
                    try:
                        dt = datetime.fromisoformat(date_str)
                        st.write(dt.strftime("%B %d, %Y at %I:%M %p"))
                    except:
                        st.write(date_str)
                else:
                    st.write(date_str)
                
                st.markdown("**🎯 Problem**")
                st.write(problem)
                
                st.markdown("**⏱️ Duration**")
                duration = interview_data.get('duration_estimate', 'N/A')
                if duration != 'N/A':
                    st.write(f"~{duration} minutes")
                else:
                    st.write("N/A")
            
            with col_b:
                st.markdown("**📊 Score Breakdown**")
                breakdown = scoring.get('breakdown', {})
                if breakdown:
                    for key, value in breakdown.items():
                        st.write(f"• {key.title()}: {value}")
                else:
                    st.write(f"• Final Score: {final_score:.1f}/100")
                
                st.markdown("**💡 Stats**")
                st.write(f"• Hints Used: {interview_data.get('hints_used', 0)}")
                st.write(f"• Stages Completed: {len(interview_data.get('stages_completed', []))}")
            
            # Test Results
            st.markdown("---")
            st.markdown("**🧪 Test Results**")
            test_results = scoring.get('test_results', {})
            if isinstance(test_results, dict):
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Tests", test_results.get('total', 0))
                col2.metric("Passed", test_results.get('passed', 0))
                col3.metric("Pass Rate", f"{(test_results.get('passed', 0) / max(test_results.get('total', 1), 1) * 100):.0f}%")
            
            # Quality Details
            quality_details = scoring.get('code_quality_details', {})
            if quality_details:
                st.markdown("---")
                st.markdown("**✨ Code Quality Analysis**")
                
                quality_score = quality_details.get('code_quality_score', 0)
                st.progress(quality_score / 100, text=f"Quality Score: {quality_score}/100")
                
                feedback = quality_details.get('overall_feedback', '')
                if feedback:
                    st.info(feedback)
                
                # Strengths and improvements
                col_x, col_y = st.columns(2)
                
                with col_x:
                    strengths = quality_details.get('strengths', [])
                    if strengths:
                        st.markdown("**✅ Strengths**")
                        for strength in strengths[:3]:
                            st.write(f"• {strength}")
                
                with col_y:
                    improvements = quality_details.get('improvements', [])
                    if improvements:
                        st.markdown("**🔧 Improvements**")
                        for improvement in improvements[:3]:
                            st.write(f"• {improvement}")
            
            # Communication & Approach (for chat mode)
            if 'approach_quality' in interview_data:
                st.markdown("---")
                st.markdown("**💬 Interview Performance**")
                
                col_p, col_q = st.columns(2)
                with col_p:
                    approach = interview_data.get('approach_quality', 0)
                    st.metric("Approach Quality", f"{approach}/100")
                
                with col_q:
                    communication = interview_data.get('communication_score', 0)
                    st.metric("Communication", f"{communication}/100")
            
            # Conversation history (truncated)
            if 'conversation_history' in interview_data:
                st.markdown("---")
                st.markdown("**💭 Conversation Summary**")
                history = interview_data.get('conversation_history', [])
                st.caption(f"Total messages exchanged: {len(history)}")
                
                if st.checkbox(f"Show conversation details (Interview #{idx+1})", key=f"show_conv_{idx}"):
                    for msg in history[:10]:  # Show first 10 messages
                        role = msg.get('role', 'unknown')
                        content = msg.get('content', '')
                        if role == 'user':
                            st.markdown(f"**👤 Candidate:** {content[:200]}{'...' if len(content) > 200 else ''}")
                        else:
                            st.markdown(f"**🤖 AI:** {content[:200]}{'...' if len(content) > 200 else ''}")
                    
                    if len(history) > 10:
                        st.caption(f"...and {len(history) - 10} more messages")
            
            # Raw JSON view
            if st.checkbox(f"Show raw JSON (Interview #{idx+1})", key=f"show_json_{idx}"):
                st.json(interview)
    
    # Performance trends
    if len(interviews) > 1:
        st.markdown("---")
        st.subheader("📈 Performance Trends")
        
        # Create DataFrame for visualization
        scores_data = []
        for interview in reversed(interviews):  # Oldest to newest
            metadata = interview.get('metadata', {})
            scoring = interview.get('scoring', {})
            interview_data = interview.get('interview_data', {})
            
            scores_data.append({
                'Date': metadata.get('date', 'Unknown'),
                'Problem': interview_data.get('problem', 'Unknown'),
                'Score': scoring.get('final_score', 0)
            })
        
        df = pd.DataFrame(scores_data)
        
        # Line chart
        st.line_chart(df.set_index('Date')['Score'])
        
        # Data table
        st.dataframe(
            df,
            column_config={
                "Date": st.column_config.DatetimeColumn("Date"),
                "Problem": "Problem",
                "Score": st.column_config.NumberColumn("Score", format="%.1f")
            },
            hide_index=True
        )


if __name__ == "__main__":
    show_interview_results_viewer()
