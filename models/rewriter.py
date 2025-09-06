from google import genai
from google.genai import types
import re
import json
from typing import List, Dict, Any, Optional



def get_req_skill(job, level="entry-level"):
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
    
        prompt = f"List all the essential job skills (technical and soft skills) required for an {level} {job} role. Provide the skills as a simple python list of names only, without descriptions."
    
        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    
        return response.text
    except Exception as e:
        return f"Error generating Req_skills : {e}"


def get_tone_style_score(text):
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
        prompt = f"""
    You are an expert resume reviewer.
    
    Task:
    - Analyze the following resume text.
    - Evaluate it for:
    1. Professional tone
    2. Formality
    3. Style (clarity and conciseness)
    - Return a **single integer score between 0 and 100** representing the overall quality, averaging all three aspects.
    - Do **not** provide any explanations or extra text — return **only the integer**.
    
    Resume Text:
    {text}
    """
    
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    
        return response.text
    except Exception as e:
        return f"Error Generating while getting score for tone & style: {e}"

def get_content_score(text, jobtitle):
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
        prompt = f"""
    Analyze the resume text below.
    
    Evaluate only the **resume content quality**, with emphasis on:
    - Relevance to the target job
    - Clarity of responsibilities
    - Presence of quantified achievements
    - Relevance and currency of skills/keywords
    - Organization and conciseness
    - Grammar and typo issues
    
    Produce a **single integer CONTENT SCORE** between 0 and 100 (0 = unusable, 100 = outstanding).
    
    Return **only** the integer — no explanations, no punctuation, no extra whitespace or newlines.
    
    If the resume text is empty or unreadable, return 0.
    
    Job Title: {jobtitle}
    
    Resume Text: {text}
    """
    
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig()
        ),
    )
        return response.text
    except Exception as e:
        return f"failed to generate content Score: {e}"

def get_structure_score(text):
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
        prompt = f"""
    You are a resume structure evaluator.
    
    Analyze the structure of the following resume text and assign a **STRUCTURE SCORE** between 0 and 100 based on:
    - Logical section ordering (e.g., Contact Info, Summary, Experience, Education, Skills)
    - Proper use of section headers
    - Consistent formatting and spacing
    - Appropriate length and white space usage
    - Readability and visual flow (even in plain text form)
    
    Score from 0 (poorly structured or unreadable) to 100 (excellent structure and formatting).
    
    Return **only** a single integer — no text, no punctuation, no newlines, no extra spaces.
    
    If the resume text is empty or unreadable, return 0.
    
    Resume Text: {text}
    """
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig()
        ),
    )
        return response.text
    except Exception as e:
        return f"failed to get structure score: {e}"


def get_professional_summary_suggestions(resume_text: str, job_title: str, level: str = "entry-level") -> str:
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
            
        prompt = f"""
            Based on the resume content below, create 2-3 professional summary options for a {level} {job_title} position.
            
            Requirements:
            - Each summary should be 3-4 sentences
            - Highlight key achievements and skills from the resume
            - Make it ATS-friendly with relevant keywords
            - Professional and engaging tone
            - Quantify achievements where possible
            
            Resume Text:
            {resume_text}
            
            Format as:
            Option 1: [summary]
            Option 2: [summary]
            Option 3: [summary]
            """
            
        response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                ),
            )
            
        return response.text
    except Exception as e:
        return f"failed to make summary: {e}"
        



def optimize_skills_section(current_skills: str, job_requirements: str, job_title: str) -> Dict[str, Any]:
    try:
        client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")

        prompt = f"""
    Optimize the skills section for a {job_title} position.

    Current Skills: {current_skills}
    Job Requirements: {job_requirements}

    Return only the skills to add and remove in JSON format:
    {{
    "skills_to_add": ["new_skill1", "new_skill2", ...],
    "skills_to_remove": ["old_skill1", ...]
    }}
    """


        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig()
            ),
        )

        try:
            return json.loads(response.text)
        except Exception:
            return {"optimized_skills": response.text}
    
    except Exception as e:
        return f"failed to optimize skill {e}"



def suggest_additional_sections(resume_text: str, job_title: str) -> List[str]:
    suggestions = []
    
    text_lower = resume_text.lower()
    
    if 'project' not in text_lower and 'software' in job_title.lower():
        suggestions.append("Projects Section - Showcase relevant technical projects")
    
    if 'certification' not in text_lower and 'award' not in text_lower:
        suggestions.append("Certifications & Awards - Add professional certifications")
    
    if 'volunteer' not in text_lower and len(resume_text.split()) < 300:
        suggestions.append("Volunteer Experience - Show community involvement")
    
    if 'publication' not in text_lower and 'research' in job_title.lower():
        suggestions.append("Publications & Research - Highlight academic contributions")
    
    if 'language' not in text_lower:
        suggestions.append("Languages - List language proficiencies")
    
    if 'interest' not in text_lower and 'hobby' not in text_lower:
        suggestions.append("Interests - Add relevant personal interests (optional)")
    
    return suggestions




def optimize_structure(resume_text : str):
    client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
    prompt=f"""Review the resume structure and return only 4 key points for optimization. 
    Each point should be 2-3 lines max and cover:
    layout clarity, section ordering, formatting consistency, and content emphasis. 
    Focus on improving readability and professional impact.

    Text to review:
    {resume_text}
        
    Provide specific suggestions for improvement. If no issues found, say "No significant issues found."

"""
    response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig()
            ),
        )
    return {
            "feedback": response.text,
            "has_issues": "No significant issues found" not in response.text
        }


def check_content(text: str) -> Dict[str, Any]:
    client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
    
    prompt = f"""
    Review the following text focusing strictly on content quality.
    
    Provide exactly 4 key points for improvement, each 2-3 lines long, covering:
    1. Clarity and coherence of ideas
    2. Relevance and completeness of information
    3. Logical flow and structure
    4. Redundancies or unnecessary information
    
    Do NOT evaluate grammar, spelling, tone, or style.
    
    Text to review:
    {text}
    
    If no issues, respond with "No significant content issues found."
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig()
        ),
    )
    
    return {
        "feedback": response.text,
        "has_issues": "No significant content issues found" not in response.text
    }


def check_tone_and_style(text: str) -> Dict[str, Any]:
    client = genai.Client(api_key="AIzaSyCxR6B7cwN9I-H44cFnuNa1zIrQh5SKDf8")
    
    prompt = f"""
    Review the following text focusing strictly on tone and style.
    
    Provide exactly 4 key points for improvement, each 2-3 lines long, covering:
    1. Consistency and appropriateness of tone
    2. Engagement and readability
    3. Formality and professionalism
    4. Style improvements and clarity
    
    Do NOT evaluate grammar, spelling, or content accuracy.
    
    Text to review:
    {text}
    
    If no issues, respond with "No significant tone or style issues found."
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig()
        ),
    )
    
    return {
        "feedback": response.text,
        "has_issues": "No significant tone or style issues found" not in response.text
    }

