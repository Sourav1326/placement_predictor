import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_placement_probability_gauge(probability):
    """Create a gauge chart for placement probability"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Placement Probability (%)"},
        delta = {'reference': 50, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#ffcccb'},
                {'range': [30, 60], 'color': '#ffeb9c'},
                {'range': [60, 80], 'color': '#90ee90'},
                {'range': [80, 100], 'color': '#008000'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        font={'color': "darkblue", 'family': "Arial"},
        paper_bgcolor="white"
    )
    return fig

def create_feature_importance_chart(feature_importance, top_n=10):
    """Create horizontal bar chart for feature importance"""
    # Sort features by importance
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    features, importance = zip(*sorted_features)
    
    fig = go.Figure(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        marker=dict(
            color=importance,
            colorscale='viridis',
            showscale=True,
            colorbar=dict(title="Importance")
        )
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Feature Importance",
        xaxis_title="Importance Score",
        yaxis_title="Features",
        height=400 + top_n * 20,
        template="plotly_white"
    )
    
    return fig

def create_placement_trends_chart(df):
    """Create placement trends by branch"""
    branch_stats = df.groupby('branch').agg({
        'placed': ['count', 'sum'],
        'cgpa': 'mean'
    }).round(2)
    
    branch_stats.columns = ['Total', 'Placed', 'Avg_CGPA']
    branch_stats['Placement_Rate'] = (branch_stats['Placed'] / branch_stats['Total'] * 100).round(1)
    branch_stats = branch_stats.reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Placement Rate by Branch', 'Total Students by Branch', 
                       'Average CGPA by Branch', 'Placed Students by Branch'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Placement rate
    fig.add_trace(
        go.Bar(x=branch_stats['branch'], y=branch_stats['Placement_Rate'], 
               name='Placement Rate (%)', marker_color='lightblue'),
        row=1, col=1
    )
    
    # Total students
    fig.add_trace(
        go.Bar(x=branch_stats['branch'], y=branch_stats['Total'], 
               name='Total Students', marker_color='orange'),
        row=1, col=2
    )
    
    # Average CGPA
    fig.add_trace(
        go.Bar(x=branch_stats['branch'], y=branch_stats['Avg_CGPA'], 
               name='Avg CGPA', marker_color='green'),
        row=2, col=1
    )
    
    # Placed students
    fig.add_trace(
        go.Bar(x=branch_stats['branch'], y=branch_stats['Placed'], 
               name='Placed Students', marker_color='red'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, template="plotly_white")
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_skills_analysis_chart(df):
    """Create skills impact analysis"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Projects vs Placement', 'Internships vs Placement', 
                       'CGPA vs Placement', 'Coding Score vs Placement')
    )
    
    placed = df[df['placed'] == 1]
    not_placed = df[df['placed'] == 0]
    
    # Projects analysis
    fig.add_trace(
        go.Box(y=placed['num_projects'], name='Placed', boxpoints='outliers'),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(y=not_placed['num_projects'], name='Not Placed', boxpoints='outliers'),
        row=1, col=1
    )
    
    # Internships analysis
    fig.add_trace(
        go.Box(y=placed['num_internships'], name='Placed', boxpoints='outliers', showlegend=False),
        row=1, col=2
    )
    fig.add_trace(
        go.Box(y=not_placed['num_internships'], name='Not Placed', boxpoints='outliers', showlegend=False),
        row=1, col=2
    )
    
    # CGPA analysis
    fig.add_trace(
        go.Box(y=placed['cgpa'], name='Placed', boxpoints='outliers', showlegend=False),
        row=2, col=1
    )
    fig.add_trace(
        go.Box(y=not_placed['cgpa'], name='Not Placed', boxpoints='outliers', showlegend=False),
        row=2, col=1
    )
    
    # Coding score analysis (LeetCode)
    fig.add_trace(
        go.Box(y=placed['leetcode_score'], name='Placed', boxpoints='outliers', showlegend=False),
        row=2, col=2
    )
    fig.add_trace(
        go.Box(y=not_placed['leetcode_score'], name='Not Placed', boxpoints='outliers', showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(height=600, template="plotly_white")
    
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for numerical features"""
    numerical_cols = ['cgpa', 'tenth_percentage', 'twelfth_percentage', 
                     'num_projects', 'num_internships', 'num_certifications',
                     'leetcode_score', 'codechef_rating', 'communication_score',
                     'leadership_score', 'num_hackathons', 'club_participation',
                     'online_courses', 'placed']
    
    # Filter only existing columns
    available_cols = [col for col in numerical_cols if col in df.columns]
    correlation_matrix = df[available_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Feature Correlation Matrix",
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_salary_distribution_chart(df):
    """Create salary package distribution analysis"""
    placed_df = df[df['placed'] == 1]
    
    if len(placed_df) == 0 or 'salary_package' not in df.columns:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Salary Distribution', 'Salary by Branch', 
                       'Salary vs CGPA', 'Package Categories')
    )
    
    # Salary distribution histogram
    fig.add_trace(
        go.Histogram(x=placed_df['salary_package'], nbinsx=20, name='Salary Distribution'),
        row=1, col=1
    )
    
    # Salary by branch
    fig.add_trace(
        go.Box(x=placed_df['branch'], y=placed_df['salary_package'], name='Salary by Branch'),
        row=1, col=2
    )
    
    # Salary vs CGPA scatter
    fig.add_trace(
        go.Scatter(x=placed_df['cgpa'], y=placed_df['salary_package'], 
                  mode='markers', name='Salary vs CGPA'),
        row=2, col=1
    )
    
    # Package categories
    if 'package_category' in df.columns:
        package_counts = placed_df['package_category'].value_counts()
        fig.add_trace(
            go.Pie(labels=package_counts.index, values=package_counts.values, 
                  name='Package Categories'),
            row=2, col=2
        )
    
    fig.update_layout(height=600, showlegend=False, template="plotly_white")
    
    return fig

def generate_recommendations(student_data, prediction_result):
    """Generate personalized recommendations based on student profile"""
    recommendations = []
    probability = prediction_result['probability']
    
    # Academic recommendations
    if student_data['cgpa'] < 8.0:
        recommendations.append({
            'category': '📚 Academic',
            'priority': 'High',
            'recommendation': f"Focus on improving CGPA from {student_data['cgpa']:.1f} to 8.0+",
            'impact': 'High - Can increase placement probability by 15-20%'
        })
    
    # Technical skills recommendations
    if student_data['num_projects'] < 3:
        recommendations.append({
            'category': '💻 Technical',
            'priority': 'High',
            'recommendation': f"Build more projects (current: {student_data['num_projects']}, target: 3+)",
            'impact': 'Medium - Each project can add 5-8% to placement probability'
        })
    
    if student_data['num_internships'] == 0:
        recommendations.append({
            'category': '🏢 Experience',
            'priority': 'Critical',
            'recommendation': "Complete at least 1-2 internships",
            'impact': 'Very High - Internships can increase probability by 20-25%'
        })
    
    # Coding skills recommendations
    if student_data['leetcode_score'] < 1500:
        recommendations.append({
            'category': '🏆 Coding',
            'priority': 'Medium',
            'recommendation': f"Improve LeetCode score from {student_data['leetcode_score']} to 1500+",
            'impact': 'Medium - Better coding skills add 8-12% probability'
        })
    
    # Soft skills recommendations
    if student_data['communication_score'] < 7.0:
        recommendations.append({
            'category': '🗣️ Soft Skills',
            'priority': 'Medium',
            'recommendation': "Improve communication skills through practice and training",
            'impact': 'Medium - Good communication adds 5-10% probability'
        })
    
    # Certifications
    if student_data['num_certifications'] < 2:
        recommendations.append({
            'category': '🏅 Certifications',
            'priority': 'Low',
            'recommendation': "Earn industry-relevant certifications",
            'impact': 'Low-Medium - Certifications add 3-7% probability'
        })
    
    return recommendations

def calculate_improvement_impact(current_profile, improved_profile):
    """Calculate potential impact of improvements"""
    impact_factors = {
        'cgpa': 15,  # 15% impact per unit improvement
        'num_projects': 8,  # 8% impact per additional project
        'num_internships': 12,  # 12% impact per additional internship
        'leetcode_score': 0.005,  # 0.005% impact per point
        'codechef_rating': 0.003,  # 0.003% impact per point
        'num_certifications': 3,  # 3% impact per certification
        'communication_score': 2,  # 2% impact per unit improvement
        'leadership_score': 1.5,  # 1.5% impact per unit improvement
        'num_hackathons': 2  # 2% impact per hackathon
    }
    
    total_impact = 0
    detailed_impact = {}
    
    for factor, multiplier in impact_factors.items():
        if factor in current_profile and factor in improved_profile:
            improvement = improved_profile[factor] - current_profile[factor]
            if improvement > 0:
                impact = improvement * multiplier
                total_impact += impact
                detailed_impact[factor] = {
                    'improvement': improvement,
                    'impact': impact,
                    'description': f"Improve {factor.replace('_', ' ')} by {improvement}"
                }
    
    return {
        'total_impact': min(total_impact, 50),  # Cap at 50%
        'detailed_impact': detailed_impact
    }

class RecommendationEngine:
    """Advanced recommendation engine for placement improvement"""
    
    def __init__(self):
        self.priority_weights = {
            'cgpa': 0.25,
            'num_internships': 0.20,
            'num_projects': 0.15,
            'leetcode_score': 0.10,
            'communication_score': 0.10,
            'num_certifications': 0.08,
            'leadership_score': 0.05,
            'num_hackathons': 0.07
        }
    
    def analyze_profile(self, student_data):
        """Analyze student profile and identify improvement areas"""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'overall_score': 0
        }
        
        # Define thresholds for good performance
        thresholds = {
            'cgpa': 8.0,
            'num_projects': 3,
            'num_internships': 1,
            'leetcode_score': 1500,
            'communication_score': 7.0,
            'num_certifications': 2,
            'leadership_score': 6.0,
            'num_hackathons': 2
        }
        
        total_weighted_score = 0
        
        for factor, threshold in thresholds.items():
            if factor in student_data:
                value = student_data[factor]
                weight = self.priority_weights.get(factor, 0)
                
                if value >= threshold:
                    analysis['strengths'].append(f"{factor.replace('_', ' ').title()}: {value}")
                    score = 1.0
                else:
                    analysis['weaknesses'].append(f"{factor.replace('_', ' ').title()}: {value} (target: {threshold})")
                    score = value / threshold if threshold > 0 else 0
                
                total_weighted_score += score * weight
        
        analysis['overall_score'] = total_weighted_score
        return analysis
    
    def generate_action_plan(self, student_data, target_probability=0.8):
        """Generate detailed action plan to reach target probability"""
        analysis = self.analyze_profile(student_data)
        current_score = analysis['overall_score']
        
        # Calculate required improvement
        required_improvement = target_probability - current_score
        
        action_plan = {
            'current_score': current_score,
            'target_score': target_probability,
            'required_improvement': max(0, required_improvement),
            'timeline': '6-12 months',
            'actions': []
        }
        
        # Prioritize actions based on impact and feasibility
        if required_improvement > 0:
            # High impact, achievable actions
            if student_data.get('cgpa', 0) < 8.0:
                action_plan['actions'].append({
                    'action': 'Improve CGPA to 8.0+',
                    'timeline': '1-2 semesters',
                    'difficulty': 'High',
                    'impact': 'Very High',
                    'steps': [
                        'Focus on understanding core concepts',
                        'Maintain consistent study schedule',
                        'Seek help from professors/peers',
                        'Practice regularly and solve previous papers'
                    ]
                })
            
            if student_data.get('num_internships', 0) == 0:
                action_plan['actions'].append({
                    'action': 'Complete 1-2 internships',
                    'timeline': '3-6 months',
                    'difficulty': 'Medium',
                    'impact': 'Very High',
                    'steps': [
                        'Apply to relevant companies early',
                        'Prepare for technical interviews',
                        'Build a strong resume',
                        'Network with industry professionals'
                    ]
                })
            
            if student_data.get('num_projects', 0) < 3:
                action_plan['actions'].append({
                    'action': 'Build 2-3 meaningful projects',
                    'timeline': '2-4 months',
                    'difficulty': 'Medium',
                    'impact': 'High',
                    'steps': [
                        'Choose projects relevant to target domain',
                        'Use modern technologies and frameworks',
                        'Document projects well on GitHub',
                        'Deploy projects for live demonstration'
                    ]
                })
        
        return action_plan