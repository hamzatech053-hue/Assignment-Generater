"""
Analytics and visualization utilities for resume and portfolio analysis
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd


def create_skill_analysis_chart(skills_data):
    """
    Create a visualization chart for skill analysis
    
    Args:
        skills_data: Dictionary or list of skills with proficiency levels
        
    Returns:
        plotly figure object
    """
    if not skills_data:
        skills_data = {"Python": 0.8, "JavaScript": 0.7, "React": 0.6}
    
    if isinstance(skills_data, dict):
        skills = list(skills_data.keys())
        proficiencies = list(skills_data.values())
    else:
        skills = [s.get("name", "Skill") for s in skills_data]
        proficiencies = [s.get("level", 0.5) for s in skills_data]
    
    fig = go.Figure(data=[
        go.Bar(x=skills, y=proficiencies, marker_color='rgb(0, 102, 204)')
    ])
    
    fig.update_layout(
        title="Skills Proficiency Analysis",
        xaxis_title="Skills",
        yaxis_title="Proficiency Level",
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_career_timeline(experience_data):
    """
    Create a timeline visualization for career progression
    
    Args:
        experience_data: List of experience dictionaries with dates
        
    Returns:
        plotly figure object
    """
    if not experience_data:
        experience_data = [
            {"title": "Junior Developer", "company": "Tech Corp", "start": "2020-01", "end": "2021-12"},
            {"title": "Senior Developer", "company": "Tech Corp", "start": "2022-01", "end": "2024-12"}
        ]
    
    df = pd.DataFrame(experience_data)
    
    fig = px.timeline(
        df,
        x_start="start" if "start" in df.columns else None,
        x_end="end" if "end" in df.columns else None,
        y="title" if "title" in df.columns else None,
        color="company" if "company" in df.columns else None,
        title="Career Timeline",
        height=400
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig


def generate_ats_score(resume_text, job_description=""):
    """
    Generate an ATS (Applicant Tracking System) compatibility score
    
    Args:
        resume_text: Full resume text content
        job_description: Job description to match against
        
    Returns:
        Dictionary with score and recommendations
    """
    score = 75  # Default score
    recommendations = []
    
    # Check for common keywords
    ats_keywords = ["experience", "education", "skills", "phone", "email"]
    found_keywords = sum(1 for keyword in ats_keywords if keyword.lower() in resume_text.lower())
    
    score = int((found_keywords / len(ats_keywords)) * 100)
    
    if found_keywords < len(ats_keywords):
        recommendations.append("Add missing standard resume sections")
    
    if len(resume_text) < 200:
        recommendations.append("Resume appears too short, add more details")
    elif len(resume_text) > 5000:
        recommendations.append("Resume may be too long, consider condensing")
    
    # Check for formatting issues
    if "\n" not in resume_text:
        recommendations.append("Add proper line breaks and formatting")
    
    return {
        "score": min(100, max(0, score)),
        "recommendations": recommendations,
        "sections_found": found_keywords,
        "total_sections": len(ats_keywords)
    }
