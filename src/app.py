import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import joblib
import os
import sys

# Add utils to path for imports
sys.path.append('utils')

# Import our custom modules (will handle import errors gracefully)
try:
    from src.model_training import PlacementPredictor
    from data_preprocessing import PlacementDataPreprocessor
except ImportError:
    st.error("Required modules not found. Please ensure model_training.py and data_preprocessing.py are in the utils folder.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="🎯 Placement Prediction System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .prediction-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .prediction-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .feature-importance {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class PlacementApp:
    def __init__(self):
        self.predictor = PlacementPredictor()
        self.load_models()
        
    def load_models(self):
        """Load pre-trained models"""
        if not self.predictor.load_models():
            st.error("❌ Pre-trained models not found. Please run model training first.")
            st.info("🚀 Run `python model_training.py` to train the models.")
            return False
        return True
    
    def main(self):
        """Main application"""
        # Header
        st.markdown('<h1 class="main-header">🎯 Placement Prediction System</h1>', unsafe_allow_html=True)
        
        # Sidebar navigation
        st.sidebar.title("🧭 Navigation")
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["🏠 Home", "🎯 Student Prediction", "📊 Admin Dashboard", "💡 Recommendations", "📈 Model Analytics"]
        )
        
        # Route to different pages
        if page == "🏠 Home":
            self.home_page()
        elif page == "🎯 Student Prediction":
            self.prediction_page()
        elif page == "📊 Admin Dashboard":
            self.admin_dashboard()
        elif page == "💡 Recommendations":
            self.recommendations_page()
        elif page == "📈 Model Analytics":
            self.model_analytics_page()
    
    def home_page(self):
        """Home page with system overview"""
        st.markdown("## 🌟 Welcome to the Placement Prediction System")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🎯 For Students
            - **Instant Predictions**: Get your placement probability in seconds
            - **Detailed Analysis**: Understand which factors affect your chances
            - **Personalized Recommendations**: Get actionable advice to improve
            """)
        
        with col2:
            st.markdown("""
            ### 📊 For Administrators
            - **Analytics Dashboard**: Comprehensive placement statistics
            - **Trend Analysis**: Monitor placement trends by department
            - **Performance Insights**: Identify key success factors
            """)
        
        with col3:
            st.markdown("""
            ### 🔬 AI-Powered Features
            - **Multiple ML Models**: Logistic Regression, Random Forest, XGBoost
            - **Feature Importance**: SHAP-powered explanations
            - **Real-time Updates**: Dynamic predictions and insights
            """)
        
        # System statistics
        if os.path.exists('data/placement_data.csv'):
            df = pd.read_csv('data/placement_data.csv')
            
            st.markdown("## 📈 System Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Students", len(df))
            
            with col2:
                placement_rate = df['placed'].mean()
                st.metric("Overall Placement Rate", f"{placement_rate:.1%}")
            
            with col3:
                avg_cgpa = df['cgpa'].mean()
                st.metric("Average CGPA", f"{avg_cgpa:.2f}")
            
            with col4:
                top_branch = df['branch'].value_counts().index[0]
                st.metric("Top Branch", top_branch)
            
            # Quick visualization
            fig = px.bar(
                df.groupby('branch')['placed'].agg(['count', 'sum']).reset_index(),
                x='branch',
                y='sum',
                title="Placements by Branch",
                labels={'sum': 'Number of Placements', 'branch': 'Branch'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def prediction_page(self):
        """Student prediction interface"""
        st.markdown("## 🎯 Student Placement Prediction")
        
        # Create input form
        with st.form("prediction_form"):
            st.markdown("### 📝 Enter Student Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎓 Academic Information")
                cgpa = st.slider("CGPA", 0.0, 10.0, 7.5, 0.1, help="Current CGPA out of 10")
                tenth_percentage = st.slider("10th Percentage", 0.0, 100.0, 85.0, 0.1)
                twelfth_percentage = st.slider("12th Percentage", 0.0, 100.0, 85.0, 0.1)
                branch = st.selectbox("Branch", [
                    'Computer Science', 'Information Technology', 'Electronics',
                    'Mechanical', 'Civil', 'Electrical', 'Chemical'
                ])
                
                st.markdown("#### 💻 Technical Skills")
                num_projects = st.number_input("Number of Projects", 0, 20, 2)
                num_internships = st.number_input("Number of Internships", 0, 10, 1)
                num_certifications = st.number_input("Number of Certifications", 0, 20, 2)
                
                programming_languages = st.text_input(
                    "Programming Languages", 
                    "Python, Java, C++",
                    help="Enter languages separated by commas"
                )
            
            with col2:
                st.markdown("#### 🏆 Coding Platforms")
                leetcode_score = st.number_input("LeetCode Score", 0, 5000, 1200)
                codechef_rating = st.number_input("CodeChef Rating", 1000, 3000, 1400)
                
                st.markdown("#### 🗣️ Soft Skills (1-10 scale)")
                communication_score = st.slider("Communication Skills", 1.0, 10.0, 7.0, 0.1)
                leadership_score = st.slider("Leadership Skills", 1.0, 10.0, 6.0, 0.1)
                
                st.markdown("#### 🎯 Extracurricular Activities")
                num_hackathons = st.number_input("Number of Hackathons", 0, 20, 2)
                club_participation = st.number_input("Club Participation", 0, 10, 1)
                online_courses = st.number_input("Online Courses", 0, 50, 3)
            
            submitted = st.form_submit_button("🚀 Predict Placement Probability", use_container_width=True)
        
        if submitted:
            # Prepare student data (exclude output variables)
            student_data = {
                'student_id': 'PRED001',
                'branch': branch,
                'cgpa': cgpa,
                'tenth_percentage': tenth_percentage,
                'twelfth_percentage': twelfth_percentage,
                'num_projects': num_projects,
                'num_internships': num_internships,
                'num_certifications': num_certifications,
                'programming_languages': programming_languages,
                'leetcode_score': leetcode_score,
                'codechef_rating': codechef_rating,
                'communication_score': communication_score,
                'leadership_score': leadership_score,
                'num_hackathons': num_hackathons,
                'club_participation': club_participation,
                'online_courses': online_courses
                # Note: Removed output variables (placed, salary_package, package_category)
            }
            
            # Make prediction
            try:
                result = self.predictor.predict_placement(student_data)
                
                if result:
                    probability = result['probability']
                    prediction = result['prediction']
                    
                    # Display prediction result
                    if probability >= 0.7:
                        st.markdown(f"""
                        <div class="prediction-success">
                            <h2>🎉 Excellent Placement Chances!</h2>
                            <h1>{probability*100:.1f}%</h1>
                            <p>You have high chances of getting placed. Keep up the great work!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif probability >= 0.4:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); padding: 2rem; border-radius: 15px; color: #2d3436; text-align: center; margin: 1rem 0;">
                            <h2>⚠️ Moderate Placement Chances</h2>
                            <h1>{probability*100:.1f}%</h1>
                            <p>You have decent chances, but there's room for improvement!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="prediction-warning">
                            <h2>📈 Improvement Needed</h2>
                            <h1>{probability*100:.1f}%</h1>
                            <p>Focus on enhancing your skills and profile for better chances!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Probability gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = probability * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Placement Probability"},
                        delta = {'reference': 50},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 25], 'color': "lightgray"},
                                {'range': [25, 50], 'color': "yellow"},
                                {'range': [50, 75], 'color': "orange"},
                                {'range': [75, 100], 'color': "green"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Feature importance for this prediction
                    st.markdown("### 📊 What Influences Your Prediction?")
                    
                    try:
                        feature_impact = self.predictor.get_feature_importance_for_prediction(student_data)
                        if feature_impact:
                            # Show top 5 most influential features
                            top_features = list(feature_impact.items())[:5]
                            
                            for feature, details in top_features:
                                importance_pct = details['importance'] * 100
                                st.markdown(f"""
                                <div class="feature-importance">
                                    <strong>{feature.replace('_', ' ').title()}</strong>: {importance_pct:.1f}% influence<br>
                                    <small>Your value: {details['value']:.2f}</small>
                                </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.info("Feature importance analysis not available yet.")
                        
                else:
                    st.error("❌ Prediction failed. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error making prediction: {str(e)}")
                st.info("Please ensure the models are trained and available.")
    
    def admin_dashboard(self):
        """Admin analytics dashboard"""
        st.markdown("## 📊 Admin Dashboard")
        
        # Load and display dataset statistics
        if os.path.exists('data/placement_data.csv'):
            df = pd.read_csv('data/placement_data.csv')
            
            # Overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Students", len(df))
            with col2:
                placed_count = df['placed'].sum()
                st.metric("Students Placed", placed_count)
            with col3:
                placement_rate = df['placed'].mean()
                st.metric("Placement Rate", f"{placement_rate:.1%}")
            with col4:
                avg_package = df[df['placed'] == 1]['salary_package'].mean()
                st.metric("Avg Package (LPA)", f"{avg_package:.1f}")
            
            # Department-wise analysis
            st.markdown("### 🏢 Department-wise Analysis")
            
            dept_stats = df.groupby('branch').agg({
                'placed': ['count', 'sum', 'mean'],
                'cgpa': 'mean',
                'salary_package': lambda x: x[x > 0].mean()
            }).round(3)
            
            dept_stats.columns = ['Total Students', 'Placed', 'Placement Rate', 'Avg CGPA', 'Avg Package']
            dept_stats = dept_stats.fillna(0)
            
            st.dataframe(dept_stats, use_container_width=True)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Placement rate by branch
                fig1 = px.bar(
                    dept_stats.reset_index(),
                    x='branch',
                    y='Placement Rate',
                    title="Placement Rate by Branch",
                    color='Placement Rate',
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # CGPA distribution
                fig2 = px.histogram(
                    df,
                    x='cgpa',
                    color='placed',
                    title="CGPA Distribution by Placement Status",
                    nbins=20
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Skills analysis
            st.markdown("### 💻 Skills Impact Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Projects vs placement
                fig3 = px.box(
                    df,
                    x='placed',
                    y='num_projects',
                    title="Number of Projects vs Placement",
                    labels={'placed': 'Placement Status (0=No, 1=Yes)', 'num_projects': 'Number of Projects'}
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Internships vs placement
                fig4 = px.box(
                    df,
                    x='placed',
                    y='num_internships',
                    title="Internships vs Placement",
                    labels={'placed': 'Placement Status (0=No, 1=Yes)', 'num_internships': 'Number of Internships'}
                )
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.error("❌ Dataset not found. Please ensure placement_data.csv exists in the data folder.")
    
    def recommendations_page(self):
        """Recommendations for improvement"""
        st.markdown("## 💡 Placement Improvement Recommendations")
        
        st.markdown("""
        ### 🎯 How to Improve Your Placement Chances
        
        Based on our analysis of successful placements, here are key recommendations:
        """)
        
        # Recommendations based on feature importance
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📚 Academic Excellence
            - **Maintain CGPA > 8.0**: 65% of placed students have CGPA above 8
            - **Strong Foundation**: Good 10th and 12th marks indicate consistency
            - **Subject Knowledge**: Deep understanding of core subjects
            
            #### 💻 Technical Skills
            - **Build Projects**: Aim for 3+ meaningful projects
            - **Gain Experience**: Complete at least 2 internships
            - **Get Certified**: Industry-relevant certifications boost credibility
            """)
        
        with col2:
            st.markdown("""
            #### 🏆 Coding Proficiency
            - **LeetCode Score**: Target 1500+ for better chances
            - **Contest Participation**: Regular participation in coding contests
            - **Problem Solving**: Focus on data structures and algorithms
            
            #### 🤝 Soft Skills & Leadership
            - **Communication**: Practice technical communication skills
            - **Leadership Roles**: Take initiative in clubs and projects
            - **Teamwork**: Collaborate on group projects
            """)
        
        # Interactive improvement calculator
        st.markdown("### 🧮 Improvement Impact Calculator")
        
        st.info("💡 See how different improvements could affect your placement probability!")
        
        with st.expander("📈 Calculate Improvement Impact", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Current Profile**")
                current_cgpa = st.number_input("Current CGPA", 0.0, 10.0, 7.0, 0.1, key="current_cgpa")
                current_projects = st.number_input("Current Projects", 0, 20, 1, key="current_projects")
                current_internships = st.number_input("Current Internships", 0, 10, 0, key="current_internships")
            
            with col2:
                st.markdown("**Improved Profile**")
                improved_cgpa = st.number_input("Target CGPA", 0.0, 10.0, min(current_cgpa + 0.5, 10.0), 0.1, key="improved_cgpa")
                improved_projects = st.number_input("Target Projects", 0, 20, current_projects + 2, key="improved_projects")
                improved_internships = st.number_input("Target Internships", 0, 10, current_internships + 1, key="improved_internships")
            
            with col3:
                st.markdown("**Potential Impact**")
                cgpa_impact = (improved_cgpa - current_cgpa) * 15  # Rough estimate
                projects_impact = (improved_projects - current_projects) * 8
                internships_impact = (improved_internships - current_internships) * 12
                
                total_impact = cgpa_impact + projects_impact + internships_impact
                
                st.metric("CGPA Improvement", f"+{cgpa_impact:.1f}%")
                st.metric("Projects Impact", f"+{projects_impact:.1f}%")
                st.metric("Internships Impact", f"+{internships_impact:.1f}%")
                st.metric("**Total Estimated Impact**", f"+{total_impact:.1f}%", delta=f"{total_impact:.1f}%")
    
    def model_analytics_page(self):
        """Model performance analytics"""
        st.markdown("## 📈 Model Analytics & Performance")
        
        # Model performance comparison
        if hasattr(self.predictor, 'model_scores') and self.predictor.model_scores:
            st.markdown("### 🏆 Model Performance Comparison")
            
            scores_df = pd.DataFrame(self.predictor.model_scores).T
            scores_df = scores_df[['auc', 'cv_mean', 'cv_std']].round(4)
            scores_df.columns = ['AUC Score', 'CV Mean', 'CV Std']
            
            st.dataframe(scores_df, use_container_width=True)
            
            # Visualization of model performance
            fig = px.bar(
                scores_df.reset_index(),
                x='index',
                y='AUC Score',
                title="Model Performance Comparison (AUC Score)",
                labels={'index': 'Model', 'AUC Score': 'AUC Score'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance
        if hasattr(self.predictor, 'feature_importance') and self.predictor.feature_importance:
            st.markdown("### 📊 Feature Importance Analysis")
            
            # Select model for feature importance
            model_choice = st.selectbox(
                "Select Model for Feature Importance:",
                list(self.predictor.feature_importance.keys())
            )
            
            if model_choice in self.predictor.feature_importance:
                importance_dict = self.predictor.feature_importance[model_choice]
                importance_df = pd.DataFrame(
                    list(importance_dict.items()),
                    columns=['Feature', 'Importance']
                ).sort_values('Importance', ascending=False).head(15)
                
                fig = px.bar(
                    importance_df,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    title=f"Top 15 Features - {model_choice.title()}",
                    labels={'Importance': 'Feature Importance', 'Feature': 'Features'}
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
        
        # Model insights
        st.markdown("### 🔍 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📚 Most Important Factors for Placement:
            1. **CGPA & Academic Performance** - Foundation matters!
            2. **Technical Projects** - Practical experience is crucial
            3. **Internship Experience** - Industry exposure counts
            4. **Coding Skills** - Technical proficiency is key
            5. **Communication Skills** - Soft skills make the difference
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 Model Recommendations:
            - **Random Forest** typically performs best for interpretability
            - **XGBoost** offers highest accuracy for predictions
            - **Logistic Regression** provides baseline performance
            - **Ensemble approaches** could further improve accuracy
            - **Feature engineering** enhances all models significantly
            """)

def main():
    """Main application entry point"""
    app = PlacementApp()
    app.main()

if __name__ == "__main__":
    main()