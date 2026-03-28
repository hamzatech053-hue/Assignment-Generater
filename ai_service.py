"""
AI-powered resume generation service
"""

import json
import streamlit as st
from openai import OpenAI


def create_regional_prompt(user_details, cv_region, cv_template, auto_optimize, include_keywords):
    """
    Create region-specific CV prompt based on selected standard and template
    """
    
    # Define regional standards
    regional_config = {
        "USA Standard": {
            "phone_format": "+1-555-123-4567",
            "currency": "$",
            "education_format": "Bachelor of Science, Master of Business Administration",
            "grade_system": "GPA: 3.8/4.0, Magna Cum Laude",
            "companies": "Microsoft Corporation, Google Inc, Amazon.com Inc, Apple Inc, Meta Platforms",
            "universities": "Harvard University, Stanford University, MIT, UC Berkeley, Carnegie Mellon",
            "locations": "New York, NY | San Francisco, CA | Boston, MA | Seattle, WA",
            "salary_range": "$75,000 - $120,000",
            "certifications": "AWS Certified, Google Cloud Professional, PMP Certified, Salesforce Certified"
        },
        "UK Standard": {
            "phone_format": "+44 20 7123 4567",
            "currency": "£",
            "education_format": "BSc (Hons) Computer Science, MSc Business Management",
            "grade_system": "First Class Honours, Upper Second Class (2:1)",
            "companies": "Barclays Bank plc, BP plc, Rolls-Royce Holdings, HSBC Holdings, Vodafone Group",
            "universities": "University of Oxford, University of Cambridge, Imperial College London, LSE, UCL",
            "locations": "London | Manchester | Edinburgh | Birmingham",
            "salary_range": "£45,000 - £75,000",
            "certifications": "PRINCE2 Practitioner, Chartered Institute, CIPD Qualified, BCS Certified"
        },
        "European Standard": {
            "phone_format": "+49 30 12345678 | +33 1 23 45 67 89",
            "currency": "€",
            "education_format": "Bachelor of Engineering, Master of Science",
            "grade_system": "Magna Cum Laude, Distinction",
            "companies": "SAP SE, Siemens AG, ASML Holding, Spotify AB, Adyen NV",
            "universities": "ETH Zurich, Technical University of Munich, Sorbonne University, TU Delft",
            "locations": "Berlin, Germany | Paris, France | Amsterdam, Netherlands | Zurich, Switzerland",
            "salary_range": "€55,000 - €85,000",
            "certifications": "European certifications, ISO standards, EU professional qualifications"
        },
        "Canadian Standard": {
            "phone_format": "+1-416-555-1234",
            "currency": "CAD $",
            "education_format": "Bachelor of Applied Science, Master of Engineering",
            "grade_system": "GPA: 3.7/4.0, Dean's List",
            "companies": "Royal Bank of Canada, Shopify Inc, Bombardier Inc, Magna International",
            "universities": "University of Toronto, McGill University, University of British Columbia",
            "locations": "Toronto, ON | Vancouver, BC | Montreal, QC | Calgary, AB",
            "salary_range": "CAD $70,000 - CAD $110,000",
            "certifications": "Professional Engineer (P.Eng), CPA Canada, PMI Certified"
        },
        "Australian Standard": {
            "phone_format": "+61 2 9123 4567",
            "currency": "AUD $",
            "education_format": "Bachelor of Technology, Master of Business",
            "grade_system": "High Distinction, Distinction",
            "companies": "Commonwealth Bank, BHP Group, Atlassian Corporation, Canva Pty Ltd",
            "universities": "University of Melbourne, Australian National University, University of Sydney",
            "locations": "Sydney, NSW | Melbourne, VIC | Brisbane, QLD | Perth, WA",
            "salary_range": "AUD $80,000 - AUD $130,000",
            "certifications": "Engineers Australia, CPA Australia, AIPM Certified"
        }
    }
    
    # Define template styles
    template_styles = {
        "Executive": {
            "style": "Executive-level professional format with emphasis on leadership achievements and strategic impact",
            "focus": "Leadership, Strategic Planning, P&L Management, Board Relations, Executive Decision Making",
            "tone": "Authoritative and results-driven with C-suite language"
        },
        "Professional": {
            "style": "Clean, professional format suitable for corporate environments",
            "focus": "Professional achievements, technical skills, career progression",
            "tone": "Professional and competent with industry-standard terminology"
        },
        "Modern": {
            "style": "Contemporary tech-focused format with emphasis on innovation and technical expertise",
            "focus": "Technical Skills, Innovation, Agile Methodologies, Digital Transformation",
            "tone": "Dynamic and forward-thinking with tech industry language"
        },
        "Creative Designer": {
            "style": "Creative and visually appealing format highlighting design thinking and creativity",
            "focus": "Creative Projects, Design Thinking, User Experience, Visual Communication",
            "tone": "Creative and innovative with design industry terminology"
        },
        "Academic Scholar": {
            "style": "Academic format emphasizing research, publications, and scholarly achievements",
            "focus": "Research, Publications, Teaching, Academic Achievements, Grants",
            "tone": "Scholarly and research-focused with academic language"
        },
        "Sales Professional": {
            "style": "Results-driven format highlighting sales achievements and revenue generation",
            "focus": "Sales Performance, Revenue Growth, Client Relations, Market Expansion",
            "tone": "Results-oriented and persuasive with sales terminology"
        },
        "Healthcare Expert": {
            "style": "Healthcare-focused format emphasizing patient care and medical expertise",
            "focus": "Patient Care, Medical Expertise, Healthcare Innovation, Clinical Excellence",
            "tone": "Professional and caring with medical terminology"
        }
    }
    
    config = regional_config.get(cv_region, regional_config["USA Standard"])
    template = template_styles.get(cv_template, template_styles["Professional"])
    
    prompt = f"""You are an expert resume writer specializing in {cv_region} CV standards with the {cv_template} template style. 
    Create a comprehensive, ATS-optimized professional resume using the EXACT details provided: {user_details}
    
    TEMPLATE REQUIREMENTS:
    - Style: {template['style']}
    - Focus Areas: {template['focus']}
    - Tone: {template['tone']}
    
    REGIONAL REQUIREMENTS:
    - Follow strict {cv_region} CV standards and professional formatting
    - Use the provided user information EXACTLY as given - do not ignore any details
    - Phone format: {config['phone_format']}
    - Currency: {config['currency']}
    - Education format: {config['education_format']}
    - Grading system: {config['grade_system']}
    - ATS Optimization: {auto_optimize}
    - Industry Keywords: {include_keywords}
    - Use realistic companies like: {config['companies']}
    - Use prestigious universities like: {config['universities']}
    - Use locations like: {config['locations']}
    - Salary range format: {config['salary_range']}
    - Relevant certifications: {config['certifications']}
    
    Return ONLY valid JSON in this exact format:
    {{
        "name": "Use EXACT name provided or create realistic name",
        "email": "Use EXACT email provided or create professional email",
        "phone": "Use EXACT phone provided or format as {config['phone_format']}",
        "location": "Use EXACT location provided or use format: {config['locations']}",
        "title": "Use EXACT job title provided or create professional title matching {cv_template} style",
        "summary": "Create compelling professional summary using user's experience and skills in {cv_region} style with {cv_template} focus",
        "skills": ["Use EXACT skills provided (split by comma) and add relevant skills for {cv_region} market and {cv_template} template"],
        "experience": [
            {{
                "company": "Use realistic {cv_region} company name from: {config['companies']}",
                "role": "Use provided job title or create appropriate role matching {cv_template} level",
                "duration": "Create realistic duration in {cv_region} format",
                "location": "Use {cv_region} city format from: {config['locations']}",
                "description": "Create achievements using provided skills with {config['currency']} amounts and percentages, focusing on {template['focus']}"
            }}
        ],
        "education": [
            {{
                "degree": "Use EXACT education provided or create in {config['education_format']} format",
                "institution": "Use realistic {cv_region} university from: {config['universities']}",
                "year": "Create realistic year",
                "location": "University location in {cv_region}",
                "details": "Use {config['grade_system']} format"
            }}
        ],
        "projects": [
            {{
                "name": "Create project using provided skills and {cv_template} focus",
                "duration": "6 months",
                "description": "Project description using provided skills and {template['focus']}",
                "achievements": "Results with {config['currency']} amounts and metrics",
                "technologies": ["Technologies from provided skills"]
            }}
        ],
        "certifications": ["Create relevant {cv_region} certifications: {config['certifications']}"],
        "languages": ["English (Native)", "Add other languages if provided"],
        "achievements": ["Create achievements with {config['currency']} amounts and percentages focusing on {template['focus']}"],
        "volunteer": [
            {{
                "organization": "Relevant {cv_region} organization",
                "role": "Volunteer role",
                "duration": "2020 - Present",
                "description": "Brief description"
            }}
        ],
        "interests": ["Professional interests relevant to {cv_template} and {cv_region} culture"],
        "ats_keywords": ["Keywords relevant to {template['focus']} and industry"],
        "salary_range": "{config['salary_range']}",
        "template_used": "{cv_template}",
        "region_used": "{cv_region}"
    }}"""
    
    return prompt


def ai_chatbot_generate(user_details, model, cv_region, cv_template, auto_optimize, include_keywords, creativity=0.7, api_key=None):
    """
    Generate resume using OpenAI API with specific regional standards and template
    
    Args:
        user_details: String containing user information
        model: AI model to use (gpt-4o-mini, gpt-4, etc.)
        cv_region: Target CV region/standard
        cv_template: CV template style
        auto_optimize: Boolean for ATS optimization
        include_keywords: Boolean to include industry keywords
        creativity: Temperature parameter for creativity (0.1-1.0)
        api_key: OpenAI API key
    
    Returns:
        Dictionary containing generated resume data
    """
    if not api_key:
        st.error("API key is required")
        return None
    
    client = OpenAI(api_key=api_key)
    
    prompt = create_regional_prompt(user_details, cv_region, cv_template, auto_optimize, include_keywords)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            timeout=45,
            temperature=creativity
        )
        
        content = response.choices[0].message.content.strip()
        # Clean the response to ensure it's valid JSON
        if content.startswith('```json'):
            content = content[7:-3]
        elif content.startswith('```'):
            content = content[3:-3]
            
        return json.loads(content)
        
    except Exception as e:
        st.error(f"AI Generation Error: {str(e)}")
        return get_fallback_data(user_details)


def get_fallback_data(user_details):
    """
    Return fallback resume data when AI generation fails
    """
    return {
        "name": "Alex Johnson",
        "email": "alex.johnson@email.com",
        "phone": "+1-555-123-4567",
        "location": "San Francisco, CA, USA",
        "title": "Senior Software Engineer",
        "summary": "Experienced software engineer with 5+ years of expertise in full-stack development. Proven track record of delivering scalable solutions and leading high-performing teams. Passionate about innovation and continuous learning.",
        "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes", "MongoDB", "PostgreSQL", "Git"],
        "experience": [
            {
                "company": "TechCorp Solutions",
                "role": "Senior Software Engineer",
                "duration": "2021 - Present",
                "location": "San Francisco, CA",
                "description": "• Led development of microservices architecture serving 1M+ users\n• Improved application performance by 60% through optimization\n• Mentored 5 junior developers and established coding standards"
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Computer Science",
                "institution": "Stanford University",
                "year": "2020",
                "location": "Stanford, CA",
                "details": "GPA: 3.7/4.0, Relevant coursework in Software Engineering and AI"
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "duration": "6 months",
                "description": "Full-stack e-commerce solution with payment integration",
                "achievements": "Processed $500K+ in transactions, 99.9% uptime",
                "technologies": ["React", "Node.js", "MongoDB", "Stripe"]
            }
        ],
        "certifications": ["AWS Certified Developer", "Google Cloud Professional"],
        "languages": ["English (Native)"],
        "achievements": ["Led successful product launch", "Improved team efficiency by 30%"],
        "volunteer": [],
        "interests": ["Technology", "Innovation", "Open Source"],
        "ats_keywords": ["Software Development", "Leadership", "Agile", "Problem Solving"],
        "salary_range": "$90,000 - $120,000"
    }
