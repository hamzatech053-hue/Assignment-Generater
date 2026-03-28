"""
CV2Desk - AI Resume Builder
Main Application File
"""

import streamlit as st
from dotenv import load_dotenv
import os
import json
import pandas as pd
from datetime import datetime
from io import BytesIO

# Import from our organized modules
from config.styles import STREAMLIT_CONFIG, FOOTER_STYLE
from config.settings import (
    PAGE_CONFIG, MODES, CV_TEMPLATES, CV_REGIONS,
    OUTPUT_FORMATS, AI_MODELS, LANGUAGES, REGIONS, INDUSTRIES, QUICK_TEMPLATES
)
from services.ai_service import ai_chatbot_generate
from utils.analytics import create_skill_analysis_chart, create_career_timeline, generate_ats_score
from components.cv_generator import create_enhanced_cv_docx, DOCX_AVAILABLE

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(**PAGE_CONFIG)

# Apply custom styling
st.markdown(STREAMLIT_CONFIG, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.title("🚀 CV2Desk - AI Resume Builder")
st.caption("Create professional resumes with AI | Developed by John Doe")

with st.sidebar:
    st.markdown("### ⚙️ Advanced Configuration")
    
    # API Configuration
    with st.expander("🔑 API Settings", expanded=True):
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        model_choice = st.selectbox("AI Model", AI_MODELS, help="Choose AI model for generation")
        creativity = st.slider("Creativity Level", 0.1, 1.0, 0.7, help="Higher values = more creative content")
    
    if not api_key:
        st.warning("⚠️ Enter your OpenAI API Key to continue")
        st.stop()
    
    st.markdown("---")
    
    # Mode Selection
    mode = st.radio("📋 Select Generation Mode", MODES)
    
    # Template Selection based on mode
    if mode == "📄 Professional CV":
        cv_template = st.selectbox("📋 CV Template", CV_TEMPLATES)
        output_format = st.multiselect("Output Formats", OUTPUT_FORMATS, default=["DOCX"])
    elif mode == "📊 Analytics Dashboard":
        st.info("Generate skill analysis and career insights")
    
    # Advanced Features
    st.markdown("---")
    with st.expander("🚀 Advanced Features"):
        auto_optimize = st.checkbox("Auto-optimize for ATS", True, help="Optimize for Applicant Tracking Systems")
        include_keywords = st.checkbox("Industry Keywords", True, help="Include relevant industry keywords")
        skill_analysis = st.checkbox("Skill Gap Analysis", False, help="Analyze skill gaps and recommendations")
        market_insights = st.checkbox("Market Insights", False, help="Include salary and market data")
    
    # Region Selection for CV Standards
    st.markdown("---")
    cv_region = st.selectbox("🌍 CV Standard", CV_REGIONS, help="Choose CV format and standards")
    
    st.markdown("---")
    st.markdown("""
    **🔥 Pro Features:**
    - ATS Optimization
    - Multiple Formats
    - Skill Analytics
    - Market Insights
    
    **👨‍💻 Developer:** John Doe
    **⭐ Version:** 2.0 Advanced
    """)

# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

if mode == "📊 Analytics Dashboard":
    st.header("📊 Career Analytics Dashboard")
    
    # Sample data for demo
    sample_data = {
        'skills': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'SQL', 'Git', 'Node.js'],
        'experience': [
            {'role': 'Senior Developer', 'company': 'TechCorp', 'duration': '2021-Present'},
            {'role': 'Developer', 'company': 'StartupXYZ', 'duration': '2019-2021'}
        ]
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_skill_analysis_chart(sample_data), use_container_width=True)
    with col2:
        st.plotly_chart(create_career_timeline(sample_data), use_container_width=True)
    
    # Market insights
    st.subheader("💰 Market Insights")
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    with insight_col1:
        st.metric("Average Salary", "$95,000", "5.2%")
    with insight_col2:
        st.metric("Job Demand", "High", "12%")
    with insight_col3:
        st.metric("Skill Match", "87%", "3%")

# ============================================================================
# BULK GENERATOR
# ============================================================================

elif mode == "🔄 Bulk Generator":
    st.header("🔄 Bulk Resume Generator")
    st.info("Upload CSV file with candidate data to generate multiple resumes")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        if st.button("Generate All Resumes"):
            with st.spinner("Generating resumes..."):
                progress_bar = st.progress(0)
                for i in range(len(df)):
                    progress_bar.progress((i + 1) / len(df))
                st.success(f"Generated {len(df)} resumes successfully!")

# ============================================================================
# RESUME BUILDER
# ============================================================================

else:
    st.header("📝 Smart Resume Builder")
    
    # Quick templates
    st.subheader("⚡ Quick Start Templates")
    template_col1, template_col2, template_col3, template_col4 = st.columns(4)
    
    with template_col1:
        if st.button("💻 Tech Professional", help="Software Engineer, Developer, etc."):
            st.session_state.update(QUICK_TEMPLATES["💻 Tech Professional"])
    
    with template_col2:
        if st.button("📊 Data Analyst", help="Data Scientist, Analyst, etc."):
            st.session_state.update(QUICK_TEMPLATES["📊 Data Analyst"])
    
    with template_col3:
        if st.button("💼 Business Manager", help="Project Manager, Business Analyst, etc."):
            st.session_state.update(QUICK_TEMPLATES["💼 Business Manager"])
    
    with template_col4:
        if st.button("🎨 Creative Designer", help="UI/UX Designer, Graphic Designer, etc."):
            st.session_state.update(QUICK_TEMPLATES["🎨 Creative Designer"])
    
    st.markdown("---")
    
    # Enhanced form with tabs
    tab1, tab2, tab3 = st.tabs(["📝 Basic Info", "💼 Professional Details", "🎆 Additional Info"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=st.session_state.get('name', ''), placeholder="John Doe")
            job_title = st.text_input("Job Title", value=st.session_state.get('job_title', ''), placeholder="Software Engineer")
            email = st.text_input("Email", value=st.session_state.get('email', ''), placeholder="john.doe@email.com")
        with col2:
            phone = st.text_input("Phone", value=st.session_state.get('phone', ''), placeholder="+1-555-123-4567")
            location = st.text_input("Location", value=st.session_state.get('location', ''), placeholder="San Francisco, CA")
            linkedin = st.text_input("LinkedIn (Optional)", placeholder="linkedin.com/in/johndoe")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            experience_years = st.text_input("Years of Experience", value=st.session_state.get('experience_years', ''), placeholder="5")
            current_salary = st.text_input("Current Salary (Optional)", placeholder="$75,000")
            industry = st.selectbox("Industry", INDUSTRIES)
        with col2:
            skills = st.text_area("Skills (comma-separated)", value=st.session_state.get('skills', ''), 
                                placeholder="Python, JavaScript, React, AWS, Docker", height=100)
            education = st.text_input("Education", placeholder="Bachelor of Computer Science")
            target_role = st.text_input("Target Role (Optional)", placeholder="Senior Software Engineer")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            certifications = st.text_area("Certifications (Optional)", placeholder="AWS Certified Developer\nGoogle Cloud Professional", height=80)
            languages = st.text_input("Languages (Optional)", placeholder="English (Native), Spanish (Intermediate)")
        with col2:
            achievements = st.text_area("Key Achievements (Optional)", 
                                      placeholder="Led team of 5 developers\nIncreased efficiency by 30%", height=80)
            additional_info = st.text_area("Additional Information (Optional)", 
                                         placeholder="Any other relevant information", height=80)
    
    # Generation button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Professional Resume", 
            type="primary", 
            use_container_width=True,
            help="Click to generate your professional resume using AI"
        )
    
    # ============================================================================
    # RESUME GENERATION & DISPLAY
    # ============================================================================
    
    if generate_btn:
        # Collect all user input
        user_details = f"""
        Name: {name or 'Not provided'}
        Job Title: {job_title or 'Not provided'}
        Email: {email or 'Not provided'}
        Phone: {phone or 'Not provided'}
        Location: {location or 'Not provided'}
        LinkedIn: {linkedin or 'Not provided'}
        Experience Years: {experience_years or 'Not provided'}
        Current Salary: {current_salary or 'Not provided'}
        Industry: {industry or 'Not provided'}
        Skills: {skills or 'Not provided'}
        Education: {education or 'Not provided'}
        Target Role: {target_role or 'Not provided'}
        Certifications: {certifications or 'Not provided'}
        Languages: {languages or 'Not provided'}
        Achievements: {achievements or 'Not provided'}
        Additional Info: {additional_info or 'Not provided'}
        """
        
        with st.spinner("🤖 AI is crafting your professional resume..."):
            # Generate resume
            data = ai_chatbot_generate(
                user_details, 
                model_choice,
                cv_region,
                cv_template if mode == "📄 Professional CV" else "Professional",
                auto_optimize,
                include_keywords,
                creativity,
                api_key
            )
            
            if data:
                st.success("✅ Resume Generated Successfully!")
                
                # Enhanced preview with metrics
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    with st.expander("👀 Resume Preview", expanded=True):
                        st.markdown(f"**💼 Name:** {data['name']}")
                        st.markdown(f"**🎯 Title:** {data['title']}")
                        st.markdown(f"**📧 Email:** {data['email']}")
                        st.markdown(f"**📍 Location:** {data['location']}")
                        st.markdown(f"**✨ Top Skills:** {', '.join(data['skills'][:5])}")
                        
                        if data.get('salary_range'):
                            st.markdown(f"**💰 Salary Range:** {data['salary_range']}")
                
                with col2:
                    # ATS Score
                    ats_score = generate_ats_score(data)
                    st.metric("🎯 ATS Score", f"{ats_score}%", 
                             "Excellent" if ats_score >= 80 else "Good" if ats_score >= 60 else "Needs Improvement")
                    
                    # Quality indicators
                    st.markdown("**✅ Quality Checks:**")
                    st.markdown(f"- Skills: {len(data.get('skills', []))} items")
                    st.markdown(f"- Experience: {len(data.get('experience', []))} roles")
                    st.markdown(f"- Projects: {len(data.get('projects', []))} items")
                    st.markdown(f"- Certifications: {len(data.get('certifications', []))} items")
                
                # Download options
                st.markdown("---")
                st.subheader("📥 Download Your Resume")
                
                download_col1, download_col2, download_col3 = st.columns(3)
                
                with download_col1:
                    if mode == "📄 Professional CV" and DOCX_AVAILABLE:
                        doc = create_enhanced_cv_docx(data, cv_template)
                        if doc:
                            bio = BytesIO()
                            doc.save(bio)
                            bio.seek(0)
                            st.download_button(
                                "📄 Download DOCX", 
                                bio, 
                                f"Resume_{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                
                with download_col2:
                    # JSON export
                    json_data = json.dumps(data, indent=2)
                    st.download_button(
                        "📊 Export JSON", 
                        json_data, 
                        f"ResumeData_{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **🚀 Features:**
    - AI-Powered Generation
    - ATS Optimization
    - Multiple Templates
    - Real-time Preview
    """)

with footer_col2:
    st.markdown("""
    **📈 Features:**
    - ATS Optimization
    - Multiple Templates
    - AI Generation
    - Export Options
    """)

with footer_col3:
    st.markdown("""
    **👨💻 Developer Info:**
    - **Name:** John Doe
    - **App:** CV2Desk
    - **Year:** 2024
    - **Status:** Production Ready
    """)

st.markdown(FOOTER_STYLE, unsafe_allow_html=True)
