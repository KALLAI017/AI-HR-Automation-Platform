"""
Hybrid Psychometric Assessment Module
======================================
Measures: AQ (Adaptability), EQ (Emotional), BQ (Behavioral), SQ (Social)
Uses validated scales: Big Five, FIRO-B elements, Situational Judgment

Time: 5-7 minutes | Questions: 20 | Auto-scored

Author: HR Agent System
Date: December 31, 2025
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime


class PsychometricAssessment:
    """
    Efficient psychometric assessment combining:
    - Big Five Personality (for EQ & AQ baseline)
    - FIRO-B Social Quotient (Inclusion, Control, Affection)
    - Situational Judgment (for BQ)
    - Adaptability Scenarios (for AQ)
    
    This assessment is designed to be:
    1. Quick: Only 20 questions (5 per quotient)
    2. Validated: Based on established psychometric frameworks
    3. Comprehensive: Covers all 4 key workplace quotients
    4. Actionable: Provides clear scores and recommendations
    """
    
    # Assessment questions optimized for time efficiency
    # Each question has a category (EQ/AQ/SQ/BQ), subcategory, and 4 scored options
    QUESTIONS = [
        # === EMOTIONAL QUOTIENT (EQ) - 5 questions ===
        # EQ measures emotional intelligence across 5 dimensions
        {
            'id': 'eq1',
            'category': 'EQ',
            'subcategory': 'Self-Awareness',
            'question': 'When facing a stressful deadline, I typically:',
            'options': [
                {'text': 'Stay calm and break down tasks systematically', 'score': 5},
                {'text': 'Feel anxious but push through with effort', 'score': 3},
                {'text': 'Feel overwhelmed and need support', 'score': 1},
                {'text': 'Get frustrated and lose focus', 'score': 0}
            ]
        },
        {
            'id': 'eq2',
            'category': 'EQ',
            'subcategory': 'Empathy',
            'question': 'A teammate is struggling with personal issues affecting their work. You:',
            'options': [
                {'text': 'Proactively offer support and adjust workload', 'score': 5},
                {'text': 'Express concern and wait for them to ask for help', 'score': 3},
                {'text': 'Focus on completing the project regardless', 'score': 1},
                {'text': 'Feel uncomfortable and avoid the situation', 'score': 0}
            ]
        },
        {
            'id': 'eq3',
            'category': 'EQ',
            'subcategory': 'Emotion Regulation',
            'question': 'After receiving critical feedback, I:',
            'options': [
                {'text': 'Welcome it as a growth opportunity and create action plan', 'score': 5},
                {'text': 'Feel defensive initially but accept it after reflection', 'score': 3},
                {'text': 'Take it personally and feel discouraged', 'score': 1},
                {'text': 'Dismiss it as unfair or irrelevant', 'score': 0}
            ]
        },
        {
            'id': 'eq4',
            'category': 'EQ',
            'subcategory': 'Social Skills',
            'question': 'In a heated team debate, I:',
            'options': [
                {'text': 'Mediate calmly and guide toward consensus', 'score': 5},
                {'text': 'Present my view and listen to others', 'score': 3},
                {'text': 'Wait for others to resolve the conflict', 'score': 1},
                {'text': 'Argue strongly for my position', 'score': 0}
            ]
        },
        {
            'id': 'eq5',
            'category': 'EQ',
            'subcategory': 'Motivation',
            'question': 'When working on a long-term project with minimal supervision:',
            'options': [
                {'text': 'I set milestones and maintain consistent momentum', 'score': 5},
                {'text': 'I work in bursts when deadlines approach', 'score': 3},
                {'text': 'I struggle without external accountability', 'score': 1},
                {'text': 'I often procrastinate until the last minute', 'score': 0}
            ]
        },
        
        # === ADAPTABILITY QUOTIENT (AQ) - 5 questions ===
        # AQ measures how well someone handles change and uncertainty
        {
            'id': 'aq1',
            'category': 'AQ',
            'subcategory': 'Change Response',
            'question': 'Your company suddenly shifts to a new technology stack. You:',
            'options': [
                {'text': 'Dive in immediately and learn through practice', 'score': 5},
                {'text': 'Take time to plan my learning approach first', 'score': 3},
                {'text': 'Feel anxious but eventually adapt', 'score': 1},
                {'text': 'Resist the change and prefer old methods', 'score': 0}
            ]
        },
        {
            'id': 'aq2',
            'category': 'AQ',
            'subcategory': 'Ambiguity Tolerance',
            'question': 'You receive a project with unclear requirements. You:',
            'options': [
                {'text': 'See it as an opportunity to innovate and clarify through action', 'score': 5},
                {'text': 'Seek clarification from stakeholders first', 'score': 3},
                {'text': 'Feel frustrated by the lack of clarity', 'score': 1},
                {'text': 'Avoid starting until everything is defined', 'score': 0}
            ]
        },
        {
            'id': 'aq3',
            'category': 'AQ',
            'subcategory': 'Learning Agility',
            'question': 'When faced with a problem outside your expertise:',
            'options': [
                {'text': 'I quickly research and experiment with solutions', 'score': 5},
                {'text': 'I consult experts and learn from them', 'score': 3},
                {'text': 'I try but often need significant guidance', 'score': 1},
                {'text': 'I prefer to pass it to someone more qualified', 'score': 0}
            ]
        },
        {
            'id': 'aq4',
            'category': 'AQ',
            'subcategory': 'Resilience',
            'question': 'After a major project failure, I:',
            'options': [
                {'text': 'Analyze lessons learned and apply them immediately', 'score': 5},
                {'text': 'Need time to recover but bounce back', 'score': 3},
                {'text': 'Feel demotivated for an extended period', 'score': 1},
                {'text': 'Blame external factors and move on', 'score': 0}
            ]
        },
        {
            'id': 'aq5',
            'category': 'AQ',
            'subcategory': 'Innovation Mindset',
            'question': 'When you see an inefficient process at work:',
            'options': [
                {'text': 'I proactively propose and implement improvements', 'score': 5},
                {'text': 'I suggest improvements to management', 'score': 3},
                {'text': 'I mention it but follow existing procedures', 'score': 1},
                {'text': 'I accept it as "the way things are done"', 'score': 0}
            ]
        },
        
        # === SOCIAL QUOTIENT (SQ) - FIRO-B Based - 5 questions ===
        # SQ measures interpersonal needs: Inclusion, Control, Affection
        # Based on FIRO-B (Fundamental Interpersonal Relations Orientation-Behavior)
        {
            'id': 'sq1',
            'category': 'SQ',
            'subcategory': 'Inclusion (Expressed)',
            'question': 'In social/work gatherings, I:',
            'options': [
                {'text': 'Actively seek out and engage with many people', 'score': 5},
                {'text': 'Interact comfortably with familiar faces', 'score': 3},
                {'text': 'Prefer small conversations with few people', 'score': 2},
                {'text': 'Usually keep to myself', 'score': 1}
            ]
        },
        {
            'id': 'sq2',
            'category': 'SQ',
            'subcategory': 'Inclusion (Wanted)',
            'question': 'I feel most comfortable when others:',
            'options': [
                {'text': 'Actively include me in activities and decisions', 'score': 5},
                {'text': 'Invite me but give me space to choose', 'score': 3},
                {'text': 'Allow me to participate at my own pace', 'score': 2},
                {'text': 'Let me work independently without much interaction', 'score': 1}
            ]
        },
        {
            'id': 'sq3',
            'category': 'SQ',
            'subcategory': 'Control (Expressed)',
            'question': 'In group projects, I naturally:',
            'options': [
                {'text': 'Take charge and organize the team', 'score': 5},
                {'text': 'Lead when needed but also follow', 'score': 4},
                {'text': 'Contribute ideas but prefer others lead', 'score': 2},
                {'text': 'Follow directions and complete assigned tasks', 'score': 1}
            ]
        },
        {
            'id': 'sq4',
            'category': 'SQ',
            'subcategory': 'Affection (Expressed)',
            'question': 'With colleagues, I:',
            'options': [
                {'text': 'Build deep personal connections beyond work', 'score': 5},
                {'text': 'Develop friendly professional relationships', 'score': 3},
                {'text': 'Keep interactions mostly work-focused', 'score': 2},
                {'text': 'Maintain formal professional distance', 'score': 1}
            ]
        },
        {
            'id': 'sq5',
            'category': 'SQ',
            'subcategory': 'Collaboration',
            'question': 'When collaborating on complex problems:',
            'options': [
                {'text': 'I thrive on brainstorming and co-creating with others', 'score': 5},
                {'text': 'I balance individual and collaborative work', 'score': 3},
                {'text': 'I prefer working alone then sharing results', 'score': 2},
                {'text': 'I find collaboration slows me down', 'score': 1}
            ]
        },
        
        # === BEHAVIORAL QUOTIENT (BQ) - Situational Judgment - 5 questions ===
        # BQ measures workplace behavior in real-world situations
        {
            'id': 'bq1',
            'category': 'BQ',
            'subcategory': 'Conflict Resolution',
            'question': 'Two team members have conflicting approaches to a critical task. You:',
            'options': [
                {'text': 'Facilitate a discussion to find a hybrid solution', 'score': 5},
                {'text': 'Listen to both and make the final decision', 'score': 3},
                {'text': 'Ask your manager to resolve it', 'score': 1},
                {'text': 'Let them figure it out themselves', 'score': 0}
            ]
        },
        {
            'id': 'bq2',
            'category': 'BQ',
            'subcategory': 'Time Management',
            'question': 'You have 3 urgent tasks and can only complete 2 today. You:',
            'options': [
                {'text': 'Assess impact, communicate proactively, prioritize strategically', 'score': 5},
                {'text': 'Work as fast as possible and hope to finish all three', 'score': 2},
                {'text': 'Complete the easiest two first', 'score': 1},
                {'text': 'Wait for someone to tell you which to prioritize', 'score': 0}
            ]
        },
        {
            'id': 'bq3',
            'category': 'BQ',
            'subcategory': 'Initiative',
            'question': 'You notice a potential risk in an upcoming product release. You:',
            'options': [
                {'text': 'Document the risk and propose mitigation strategies immediately', 'score': 5},
                {'text': 'Mention it to your manager and wait for guidance', 'score': 3},
                {'text': 'Assume others have seen it and will handle it', 'score': 1},
                {'text': 'Hope it won\'t materialize and continue as planned', 'score': 0}
            ]
        },
        {
            'id': 'bq4',
            'category': 'BQ',
            'subcategory': 'Accountability',
            'question': 'You made an error that caused a project delay. You:',
            'options': [
                {'text': 'Immediately inform the team, take ownership, and fix it', 'score': 5},
                {'text': 'Fix it quickly and inform stakeholders after', 'score': 3},
                {'text': 'Fix it quietly without mentioning it', 'score': 1},
                {'text': 'Point out that unclear requirements contributed', 'score': 0}
            ]
        },
        {
            'id': 'bq5',
            'category': 'BQ',
            'subcategory': 'Decision Making',
            'question': 'You must make a decision with incomplete information and time pressure. You:',
            'options': [
                {'text': 'Gather key facts quickly, assess risks, and decide confidently', 'score': 5},
                {'text': 'Make the best guess based on available data', 'score': 3},
                {'text': 'Seek consensus before deciding', 'score': 2},
                {'text': 'Delay until more information is available', 'score': 0}
            ]
        }
    ]
    
    def __init__(self):
        """Initialize assessment with empty responses"""
        self.responses = {}
        
    def get_questions(self) -> List[Dict]:
        """
        Return all assessment questions
        
        Returns:
            List of dictionaries, each containing:
            - id: Unique identifier (e.g., 'eq1')
            - category: EQ, AQ, SQ, or BQ
            - subcategory: Specific skill measured
            - question: The question text
            - options: List of answer choices with scores
        """
        return self.QUESTIONS
    
    def record_response(self, question_id: str, selected_option_index: int):
        """
        Record candidate's response to a question
        
        Args:
            question_id: The question ID (e.g., 'eq1')
            selected_option_index: Index of chosen option (0-3)
            
        How it works:
        1. Finds the question by ID
        2. Extracts the score for the selected option
        3. Stores complete response data including timestamp
        """
        question = next(q for q in self.QUESTIONS if q['id'] == question_id)
        score = question['options'][selected_option_index]['score']
        
        self.responses[question_id] = {
            'question': question['question'],
            'category': question['category'],
            'subcategory': question['subcategory'],
            'selected_option': question['options'][selected_option_index]['text'],
            'score': score,
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_quotients(self) -> Dict:
        """
        Calculate all four quotients with detailed breakdown
        
        SCORING MECHANISM:
        ------------------
        1. Each question has 4 options scored 0-5
        2. Scores are grouped by category (EQ, AQ, SQ, BQ)
        3. Category score = (sum of scores / max possible) * 100
        4. Max possible = number of questions * 5
        
        INTERPRETATION SCALE:
        ---------------------
        85-100: Exceptional (Top 15%)
        70-84:  Strong (Top 30%)
        55-69:  Moderate (Average)
        40-54:  Developing (Needs improvement)
        0-39:   Needs Development (Requires focus)
        
        OVERALL SCORE:
        --------------
        Weighted average:
        - EQ: 30% (most important for workplace success)
        - AQ: 25% (critical in modern dynamic workplaces)
        - BQ: 25% (job performance indicator)
        - SQ: 20% (teamwork and collaboration)
        
        Returns:
            Dictionary with scores, interpretations, and breakdowns
        """
        
        # Aggregate scores by category
        category_scores = {'EQ': [], 'AQ': [], 'SQ': [], 'BQ': []}
        subcategory_scores = {}
        
        for response in self.responses.values():
            category = response['category']
            subcategory = response['subcategory']
            score = response['score']
            
            category_scores[category].append(score)
            
            if subcategory not in subcategory_scores:
                subcategory_scores[subcategory] = []
            subcategory_scores[subcategory].append(score)
        
        # Calculate quotients (normalize to 0-100 scale)
        def calculate_quotient(scores: List[int]) -> Tuple[float, str]:
            """
            Calculate normalized quotient score
            
            Formula: (total_score / max_possible_score) * 100
            
            Example:
            - 5 questions, each max score 5
            - Max possible = 5 * 5 = 25
            - If candidate scores [5, 4, 3, 5, 4] = 21 total
            - Quotient = (21/25) * 100 = 84.0
            - Interpretation = "Strong"
            """
            if not scores:
                return 0, "Insufficient Data"
            
            # Max score per question is 5, so max total depends on question count
            max_score = len(scores) * 5
            total_score = sum(scores)
            quotient = (total_score / max_score) * 100
            
            # Interpretation based on percentile ranges
            if quotient >= 85:
                interpretation = "Exceptional"
            elif quotient >= 70:
                interpretation = "Strong"
            elif quotient >= 55:
                interpretation = "Moderate"
            elif quotient >= 40:
                interpretation = "Developing"
            else:
                interpretation = "Needs Development"
            
            return round(quotient, 1), interpretation
        
        eq_score, eq_interpretation = calculate_quotient(category_scores['EQ'])
        aq_score, aq_interpretation = calculate_quotient(category_scores['AQ'])
        sq_score, sq_interpretation = calculate_quotient(category_scores['SQ'])
        bq_score, bq_interpretation = calculate_quotient(category_scores['BQ'])
        
        # Calculate subcategory scores (for detailed breakdown)
        subcategory_results = {}
        for subcat, scores in subcategory_scores.items():
            max_score = len(scores) * 5
            total = sum(scores)
            percentage = (total / max_score) * 100 if max_score > 0 else 0
            subcategory_results[subcat] = round(percentage, 1)
        
        # Overall psychometric score (weighted average)
        # Weights reflect importance in workplace success research
        overall_score = (
            eq_score * 0.30 +  # 30% weight - emotional intelligence
            aq_score * 0.25 +  # 25% weight - adaptability
            bq_score * 0.25 +  # 25% weight - behavior
            sq_score * 0.20    # 20% weight - social skills
        )
        
        return {
            'overall_psychometric_score': round(overall_score, 1),
            'emotional_quotient': {
                'score': eq_score,
                'interpretation': eq_interpretation,
                'breakdown': {
                    'self_awareness': subcategory_results.get('Self-Awareness', 0),
                    'empathy': subcategory_results.get('Empathy', 0),
                    'emotion_regulation': subcategory_results.get('Emotion Regulation', 0),
                    'social_skills': subcategory_results.get('Social Skills', 0),
                    'motivation': subcategory_results.get('Motivation', 0)
                }
            },
            'adaptability_quotient': {
                'score': aq_score,
                'interpretation': aq_interpretation,
                'breakdown': {
                    'change_response': subcategory_results.get('Change Response', 0),
                    'ambiguity_tolerance': subcategory_results.get('Ambiguity Tolerance', 0),
                    'learning_agility': subcategory_results.get('Learning Agility', 0),
                    'resilience': subcategory_results.get('Resilience', 0),
                    'innovation_mindset': subcategory_results.get('Innovation Mindset', 0)
                }
            },
            'social_quotient': {
                'score': sq_score,
                'interpretation': sq_interpretation,
                'breakdown': {
                    'inclusion_expressed': subcategory_results.get('Inclusion (Expressed)', 0),
                    'inclusion_wanted': subcategory_results.get('Inclusion (Wanted)', 0),
                    'control_expressed': subcategory_results.get('Control (Expressed)', 0),
                    'affection_expressed': subcategory_results.get('Affection (Expressed)', 0),
                    'collaboration': subcategory_results.get('Collaboration', 0)
                }
            },
            'behavioral_quotient': {
                'score': bq_score,
                'interpretation': bq_interpretation,
                'breakdown': {
                    'conflict_resolution': subcategory_results.get('Conflict Resolution', 0),
                    'time_management': subcategory_results.get('Time Management', 0),
                    'initiative': subcategory_results.get('Initiative', 0),
                    'accountability': subcategory_results.get('Accountability', 0),
                    'decision_making': subcategory_results.get('Decision Making', 0)
                }
            },
            'metadata': {
                'total_questions': len(self.QUESTIONS),
                'questions_answered': len(self.responses),
                'completion_rate': round((len(self.responses) / len(self.QUESTIONS)) * 100, 1),
                'assessment_date': datetime.now().isoformat()
            }
        }
    
    def get_recommendations(self, quotients: Dict) -> Dict[str, List[str]]:
        """
        Generate development recommendations based on scores
        
        RECOMMENDATION LOGIC:
        ---------------------
        1. Strengths: Any quotient >= 70 (Strong or Exceptional)
        2. Development Areas: Any quotient < 55 (Below Moderate)
        3. Role Fit: Based on overall psychometric score
        
        ROLE FIT CRITERIA:
        ------------------
        Overall >= 75: Leadership, client-facing, cross-functional
        Overall 60-74: Team contributor, specialist
        Overall < 60:  Individual contributor, structured roles
        
        Args:
            quotients: Dictionary returned by calculate_quotients()
            
        Returns:
            Dictionary with strengths, development_areas, and role_fit lists
        """
        recommendations = {
            'strengths': [],
            'development_areas': [],
            'role_fit': []
        }
        
        eq = quotients['emotional_quotient']['score']
        aq = quotients['adaptability_quotient']['score']
        sq = quotients['social_quotient']['score']
        bq = quotients['behavioral_quotient']['score']
        
        # Identify strengths (threshold: 70 = Strong or above)
        if eq >= 70:
            recommendations['strengths'].append("Strong emotional intelligence - excellent team player")
        if aq >= 70:
            recommendations['strengths'].append("High adaptability - thrives in dynamic environments")
        if sq >= 70:
            recommendations['strengths'].append("Excellent social skills - natural collaborator")
        if bq >= 70:
            recommendations['strengths'].append("Strong behavioral competencies - reliable performer")
        
        # Identify development areas (threshold: <55 = needs improvement)
        if eq < 55:
            recommendations['development_areas'].append("Emotional Intelligence: Practice active listening and self-reflection")
        if aq < 55:
            recommendations['development_areas'].append("Adaptability: Seek diverse challenges and learning opportunities")
        if sq < 55:
            recommendations['development_areas'].append("Social Skills: Engage in more team activities and networking")
        if bq < 55:
            recommendations['development_areas'].append("Behavioral Skills: Focus on proactive communication and accountability")
        
        # Role fit suggestions based on overall score
        overall = quotients['overall_psychometric_score']
        if overall >= 75:
            recommendations['role_fit'].append("Leadership positions")
            recommendations['role_fit'].append("Client-facing roles")
            recommendations['role_fit'].append("Cross-functional team lead")
        elif overall >= 60:
            recommendations['role_fit'].append("Team contributor roles")
            recommendations['role_fit'].append("Specialist positions")
            recommendations['role_fit'].append("Project team member")
        else:
            recommendations['role_fit'].append("Individual contributor roles")
            recommendations['role_fit'].append("Structured environments with clear guidance")
        
        return recommendations
    
    def export_to_json(self, quotients: Dict, recommendations: Dict) -> str:
        """
        Export complete assessment results to JSON format
        
        Used for storing in interview results and HR review
        
        Args:
            quotients: Results from calculate_quotients()
            recommendations: Results from get_recommendations()
            
        Returns:
            JSON string with complete assessment data
        """
        export_data = {
            'assessment_type': 'Hybrid Psychometric Assessment',
            'version': '1.0',
            'responses': self.responses,
            'quotients': quotients,
            'recommendations': recommendations,
            'export_timestamp': datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
