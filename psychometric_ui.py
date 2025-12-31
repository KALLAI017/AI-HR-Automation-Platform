"""
Streamlit UI for Psychometric Assessment
=========================================
Clean, professional interface with progress tracking

Features:
- Question-by-question navigation
- Visual progress bar
- Category color coding
- Instant results with detailed breakdowns
- Responsive design

Author: HR Agent System
Date: December 31, 2025
"""

import streamlit as st
from psychometric_assessment import PsychometricAssessment
from typing import Dict


def show_psychometric_assessment():
    """
    Main function to display psychometric assessment interface
    
    WORKFLOW:
    ---------
    1. Initialize assessment in session state (first time only)
    2. Show progress bar
    3. Display current question with options
    4. Handle navigation (Previous/Next/Submit)
    5. Show results when completed
    
    STATE MANAGEMENT:
    -----------------
    Uses Streamlit session state to maintain:
    - psychometric_assessment: The assessment object
    - current_question_index: Which question we're on (0-19)
    - psychometric_completed: Whether assessment is done
    - psychometric_results: Final scores (stored after submission)
    - psychometric_recommendations: Development suggestions
    """
    
    # Custom CSS for beautiful UI
    st.markdown("""
    <style>
    .assessment-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 4px solid #11998e;
    }
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .eq-badge { background: #e3f2fd; color: #1976d2; }
    .aq-badge { background: #f3e5f5; color: #7b1fa2; }
    .sq-badge { background: #e8f5e9; color: #388e3c; }
    .bq-badge { background: #fff3e0; color: #f57c00; }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    .score-excellent { color: #2e7d32; font-weight: bold; }
    .score-good { color: #558b2f; font-weight: bold; }
    .score-moderate { color: #f57c00; font-weight: bold; }
    .score-developing { color: #d32f2f; font-weight: bold; }
    
    .progress-bar-custom {
        height: 8px;
        border-radius: 10px;
        background: #e0e0e0;
        margin: 1rem 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize assessment in session state
    if 'psychometric_assessment' not in st.session_state:
        st.session_state.psychometric_assessment = PsychometricAssessment()
        st.session_state.current_question_index = 0
        st.session_state.psychometric_completed = False
    
    assessment = st.session_state.psychometric_assessment
    questions = assessment.get_questions()
    current_idx = st.session_state.current_question_index
    
    # Header with gradient background
    st.markdown("""
    <div class="assessment-header">
        <h1>🧠 Psychometric Assessment</h1>
        <p style="font-size: 1.1rem; margin: 0.5rem 0 0 0;">
            Measuring Your Adaptability, Emotional, Behavioral & Social Quotients
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show results if completed
    if st.session_state.psychometric_completed:
        show_assessment_results()
        return
    
    # Progress indicator (shows how far along the candidate is)
    progress = (current_idx / len(questions)) * 100
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #11998e;">Progress</span>
            <span style="font-weight: 600; color: #11998e;">{current_idx}/{len(questions)} Questions</span>
        </div>
        <div class="progress-bar-custom">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions (show only for first question to not be repetitive)
    if current_idx == 0:
        st.info("""
        📋 **Instructions:**
        - This assessment takes 5-7 minutes
        - 20 questions covering 4 key areas
        - Choose the response that best describes you
        - There are no right or wrong answers
        - Be honest for accurate results
        """)
    
    # Display current question
    question = questions[current_idx]
    
    # Category badge (color-coded for each quotient type)
    category_class = f"{question['category'].lower()}-badge"
    category_name = {
        'EQ': 'Emotional Quotient',
        'AQ': 'Adaptability Quotient',
        'SQ': 'Social Quotient',
        'BQ': 'Behavioral Quotient'
    }[question['category']]
    
    st.markdown(f"""
    <div class="question-card">
        <span class="category-badge {category_class}">
            {category_name} • {question['subcategory']}
        </span>
        <h3 style="margin: 1rem 0; color: #333;">Question {current_idx + 1}</h3>
        <p style="font-size: 1.1rem; color: #555; line-height: 1.6;">
            {question['question']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options (radio buttons for single selection)
    st.markdown("### Your Response:")
    selected_option = st.radio(
        "",
        options=range(len(question['options'])),
        format_func=lambda i: question['options'][i]['text'],
        key=f"q_{question['id']}",
        label_visibility="collapsed"
    )
    
    # Navigation buttons (Previous, Counter, Next/Submit)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Previous button (disabled on first question)
        if current_idx > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
    
    with col2:
        # Question counter in the middle
        st.markdown(f"<p style='text-align: center; color: #666; padding-top: 0.5rem;'>{current_idx + 1} of {len(questions)}</p>", unsafe_allow_html=True)
    
    with col3:
        # Next/Submit button (only enabled if an option is selected)
        if selected_option is not None:
            if current_idx < len(questions) - 1:
                # Next button for all questions except the last
                if st.button("Next ➡️", use_container_width=True, type="primary"):
                    # Record response before moving to next question
                    assessment.record_response(question['id'], selected_option)
                    st.session_state.current_question_index += 1
                    st.rerun()
            else:
                # Submit button on the last question
                if st.button("✅ Submit Assessment", use_container_width=True, type="primary"):
                    # Record last response
                    assessment.record_response(question['id'], selected_option)
                    # Mark as completed to trigger results view
                    st.session_state.psychometric_completed = True
                    st.rerun()


def show_assessment_results():
    """
    Display comprehensive assessment results with scores and recommendations
    
    RESULTS STRUCTURE:
    ------------------
    1. Overall Score: Weighted average of all 4 quotients
    2. Individual Quotients: EQ, AQ, SQ, BQ with interpretations
    3. Detailed Breakdowns: Sub-skills for each quotient
    4. Recommendations: Strengths, development areas, role fit
    
    VISUALIZATION:
    --------------
    - Color-coded metric cards
    - Score interpretation labels
    - Expandable breakdowns
    - Categorized recommendations
    """
    assessment = st.session_state.psychometric_assessment
    quotients = assessment.calculate_quotients()
    recommendations = assessment.get_recommendations(quotients)
    
    # Store in session state for later use (will be saved to interview results)
    st.session_state.psychometric_results = quotients
    st.session_state.psychometric_recommendations = recommendations
    
    st.success("✅ Assessment completed successfully!")
    
    # Overall Score (weighted average of all 4 quotients)
    st.markdown("---")
    st.markdown("### 🎯 Overall Psychometric Profile")
    
    overall_score = quotients['overall_psychometric_score']
    
    # Color code based on score (visual feedback)
    if overall_score >= 75:
        score_class = "score-excellent"
        emoji = "🌟"
    elif overall_score >= 60:
        score_class = "score-good"
        emoji = "✅"
    elif overall_score >= 45:
        score_class = "score-moderate"
        emoji = "⚠️"
    else:
        score_class = "score-developing"
        emoji = "📈"
    
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h2 style="-webkit-text-fill-color: white; color: white;">{emoji} Overall Score: {overall_score}/100</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Individual Quotients (2x2 grid layout)
    st.markdown("### 📊 Detailed Quotient Scores")
    
    # Row 1: EQ and AQ
    col1, col2 = st.columns(2)
    
    with col1:
        # Emotional Quotient Card
        eq_data = quotients['emotional_quotient']
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1976d2;">💙 Emotional Quotient</h3>
            <h2 class="{get_score_class(eq_data['score'])}">{eq_data['score']}/100</h2>
            <p style="color: #666; margin: 0;">{eq_data['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable breakdown showing sub-skills
        with st.expander("📋 EQ Breakdown"):
            for skill, score in eq_data['breakdown'].items():
                st.metric(skill.replace('_', ' ').title(), f"{score}/100")
    
    with col2:
        # Adaptability Quotient Card
        aq_data = quotients['adaptability_quotient']
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #7b1fa2;">🔄 Adaptability Quotient</h3>
            <h2 class="{get_score_class(aq_data['score'])}">{aq_data['score']}/100</h2>
            <p style="color: #666; margin: 0;">{aq_data['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable breakdown
        with st.expander("📋 AQ Breakdown"):
            for skill, score in aq_data['breakdown'].items():
                st.metric(skill.replace('_', ' ').title(), f"{score}/100")
    
    # Row 2: SQ and BQ
    col3, col4 = st.columns(2)
    
    with col3:
        # Social Quotient Card (FIRO-B based)
        sq_data = quotients['social_quotient']
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #388e3c;">🤝 Social Quotient</h3>
            <h2 class="{get_score_class(sq_data['score'])}">{sq_data['score']}/100</h2>
            <p style="color: #666; margin: 0;">{sq_data['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable breakdown (Inclusion, Control, Affection)
        with st.expander("📋 SQ Breakdown"):
            for skill, score in sq_data['breakdown'].items():
                st.metric(skill.replace('_', ' ').title(), f"{score}/100")
    
    with col4:
        # Behavioral Quotient Card
        bq_data = quotients['behavioral_quotient']
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #f57c00;">⚡ Behavioral Quotient</h3>
            <h2 class="{get_score_class(bq_data['score'])}">{bq_data['score']}/100</h2>
            <p style="color: #666; margin: 0;">{bq_data['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable breakdown
        with st.expander("📋 BQ Breakdown"):
            for skill, score in bq_data['breakdown'].items():
                st.metric(skill.replace('_', ' ').title(), f"{score}/100")
    
    # Recommendations Section
    st.markdown("---")
    st.markdown("### 💡 Personalized Insights")
    
    col_str, col_dev = st.columns(2)
    
    with col_str:
        # Strengths (what candidate is good at)
        st.markdown("#### ✨ Your Strengths")
        if recommendations['strengths']:
            for strength in recommendations['strengths']:
                st.success(f"✓ {strength}")
        else:
            st.info("Keep working on developing your competencies!")
    
    with col_dev:
        # Development areas (what needs improvement)
        st.markdown("#### 📈 Development Areas")
        if recommendations['development_areas']:
            for area in recommendations['development_areas']:
                st.warning(f"→ {area}")
        else:
            st.success("Excellent across all areas!")
    
    # Role fit suggestions
    st.markdown("#### 🎯 Recommended Roles")
    role_cols = st.columns(len(recommendations['role_fit']))
    for idx, role in enumerate(recommendations['role_fit']):
        with role_cols[idx]:
            st.info(f"**{role}**")
    
    st.markdown("---")
    
    # Proceed button to continue to video interview
    if st.button("➡️ Continue to Video Interview", use_container_width=True, type="primary"):
        st.session_state.psychometric_assessment_completed = True
        st.rerun()


def get_score_class(score: float) -> str:
    """
    Return CSS class based on score for color coding
    
    SCORE RANGES:
    -------------
    85-100: Exceptional (Green)
    70-84:  Strong (Light Green)
    55-69:  Moderate (Orange)
    40-54:  Developing (Red)
    0-39:   Needs Development (Dark Red)
    
    Args:
        score: Quotient score (0-100)
        
    Returns:
        CSS class name for styling
    """
    if score >= 85:
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 55:
        return "score-moderate"
    else:
        return "score-developing"
