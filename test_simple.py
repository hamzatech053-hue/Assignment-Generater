#!/usr/bin/env python3
"""
Test script to verify the AI Resume Analyzer fixes
"""

import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work correctly"""
    try:
        from config.settings import CV_TEMPLATES, CV_REGIONS
        from services.ai_service import create_regional_prompt
        from components.cv_generator import create_enhanced_cv_docx, DOCX_AVAILABLE
        
        print("SUCCESS: All imports successful!")
        print(f"CV Templates: {CV_TEMPLATES}")
        print(f"CV Regions: {CV_REGIONS}")
        print(f"DOCX Available: {DOCX_AVAILABLE}")
        
        return True
    except Exception as e:
        print(f"ERROR: Import error: {e}")
        return False

def test_prompt_generation():
    """Test prompt generation with different templates and regions"""
    try:
        from services.ai_service import create_regional_prompt
        
        user_details = """
        Name: John Doe
        Job Title: Software Engineer
        Email: john.doe@email.com
        Phone: +1-555-123-4567
        Skills: Python, JavaScript, React, AWS
        Experience Years: 5
        """
        
        # Test USA Standard + Executive Premium
        prompt = create_regional_prompt(user_details, "🇺🇸 USA Standard", "Executive Premium", True, True)
        if prompt and len(prompt) > 100:
            print("SUCCESS: Prompt generated successfully")
            return True
        else:
            print("ERROR: Failed to generate prompt")
            return False
        
    except Exception as e:
        print(f"ERROR: Prompt generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing AI Resume Analyzer Fixes...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Prompt Generation Test", test_prompt_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
            print(f"PASSED: {test_name}")
        else:
            print(f"FAILED: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! The fixes are working correctly.")
        print("\nYou can now run the application with:")
        print("   streamlit run app_new.py")
    else:
        print("WARNING: Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)