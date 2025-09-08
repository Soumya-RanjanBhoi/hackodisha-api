import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.extractor import extract_text_from_docx, extract_text_from_pdf, extract_all_skills
import pdfplumber
import re 
from models.rewriter import get_req_skill, get_content_score, get_tone_style_score, get_structure_score, optimize_skills_section, optimize_structure
from models.matcher import get_skill_score, get_ats_score
from models.rewriter import check_content, check_tone_and_style, suggest_additional_sections, get_professional_summary_suggestions

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    allowed_origins = [
    # "https://my-resume-app.vercel.app"
    ]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get('/')
def start():
    return {"message": "AI Resume Analyzer API is running successfully"}

@app.get('/health')
def health_check():
    return {"status": "healthy", "message": "Service is running"}

@app.get('/test')
def test_endpoint():
    return {
        "message": "Backend is working!",
        "cors_enabled": True,
        "timestamp": "2025-09-07"
    }

@app.post('/analyze_resume')
def analyze_resume(job: str, job_description: str, file: UploadFile = File(...), level: str = "entry-level"):
    try:
        if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
            raise HTTPException(status_code=400, detail="Unsupported File Format. Upload .docx or .pdf")
        
        if file.filename.endswith(".pdf"):
            res = extract_text_from_pdf(file.file)
        else:
            res = extract_text_from_docx(file.file)
        
        if not res or len(res.strip()) == 0:
            raise HTTPException(status_code=400, detail="Could not extract text from file")

        skill_text = extract_all_skills(res)
        if not skill_text:
            skill_text = []

        req_skill = get_req_skill(job, level)

        skill_score = get_skill_score(skill_text, req_skill) 
        content_score = get_content_score(res, job)
        tone_style_score = get_tone_style_score(res)
        structure_score = get_structure_score(res)
        ats_score = get_ats_score(job_description, res)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                "SKILL_SCORE": int(skill_score),
                "Content_score": int(content_score),
                'tone & style score':int(tone_style_score),
                "ats_score":int(ats_score),
                "structure_score":int(structure_score)         
        }
            }
        )
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in analyze_resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/optimize-skills")
def add_details(job_title: str, level: str = "entry-level", file: UploadFile = File(...)):
    try:
        if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
            raise HTTPException(status_code=400, detail="Unsupported File Format. Upload .docx or .pdf")

        if file.filename.endswith(".pdf"):
            res = extract_text_from_pdf(file.file)
        else:
            res = extract_text_from_docx(file.file)

        resume_skill = extract_all_skills(res)
        req_skill = get_req_skill(job_title, level)

        skills_details = optimize_skills_section(resume_skill, req_skill, job_title)

        return JSONResponse(
            status_code=200, 
            content={
                "success": True,
                "skills": skills_details
            }
        )
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in optimize-skills: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post('/optimize_structure')
def optimize_str(file: UploadFile = File(...)):
    try:
        if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
            raise HTTPException(status_code=400, detail="Unsupported file type must be .pdf or .docx")
        
        if file.filename.endswith(".pdf"):
            res = extract_text_from_pdf(file.file)
        else:
            res = extract_text_from_docx(file.file)

        opti_str = optimize_structure(res)

        return JSONResponse(
            status_code=200, 
            content={
                "success": True,
                "structure_feedback": opti_str
            }
        )
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in optimize_structure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/optimize_content")
def optimize_contents(file: UploadFile = File(...)):
    try:
        if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
            raise HTTPException(status_code=400, detail="Unsupported file type must be .pdf or .docx")
        
        if file.filename.endswith(".pdf"):
            res = extract_text_from_pdf(file.file)
        else:
            res = extract_text_from_docx(file.file)

        opti_cont = check_content(res)

        return JSONResponse(
            status_code=200, 
            content={
                'success': True,
                'content_feedback': opti_cont
            }
        )
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in optimize_content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post('/optimize_tone_style')
def optimize_tone_style(file: UploadFile = File(...)):
    try:
        if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
            raise HTTPException(status_code=400, detail="Unsupported file type must be .pdf or .docx")
        
        if file.filename.endswith(".pdf"):
            res = extract_text_from_pdf(file.file)
        else:
            res = extract_text_from_docx(file.file)

        opti_tone = check_tone_and_style(res)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "tone_style_feedback": opti_tone
            }
        )
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in optimize_tone_style: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
