from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import JSONResponse
from models.extractor import extract_text_from_docx,extract_text_from_pdf,extract_all_skills
import pdfplumber
import re 
from fastapi.middleware.cors import CORSMiddleware
from models.rewriter import get_req_skill,get_content_score,get_tone_style_score,get_structure_score,optimize_skills_section,optimize_structure
from models.matcher import  get_skill_score,get_ats_score
from models.rewriter import check_content,check_tone_and_style,suggest_additional_sections,get_professional_summary_suggestions


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def start():
    return "This is A Ai- Resume Analayzer"

@app.post('/analyze_resume')
def analyze_resume(job: str,job_description:str, file: UploadFile = File(...), level: str = "entry-level"):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return HTTPException(status_code=401 , detail="Unsupported File Format. Upload .docx or .pdf")
    

    if file.filename.endswith(".pdf"):
        res= extract_text_from_pdf(file.file)
    else:
        res =extract_text_from_docx(file.file)

    skill_text=extract_all_skills(res)

    req_skill=get_req_skill(job,level)

    skill_score=get_skill_score(skill_text,req_skill) 
    content_score=get_content_score(res,job)
    tone_style_score=get_tone_style_score(res)
    structure_score=get_structure_score(res)

    ats_score=get_ats_score(job_description,res)



    return JSONResponse(
    status_code=200,
    content={
        "text": {
            "SKILL_SCORE": int(skill_score),
            "Content_score": int(content_score),
            'tone & style score':int(tone_style_score),
            "ats_score":int(ats_score),
            "structure_score":int(structure_score)         
        }
    }
)

@app.post("/optimize-skills")
def add_details(job_title: str, level: str = "entry-level", file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=401, detail="Unsupported File Format. Upload .docx or .pdf")

    if file.filename.endswith(".pdf"):
        res = extract_text_from_pdf(file.file)
    else:
        res = extract_text_from_docx(file.file)

    resume_skill = extract_all_skills(res)
    req_skill = get_req_skill(job_title, level)

    skills_details = optimize_skills_section(resume_skill, req_skill, job_title)

    return JSONResponse(status_code=200, content={"Skills": skills_details})


@app.post('/optimize_structure')
def optimize_str(file: UploadFile=File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return HTTPException(status_code=401 , detail="Unsupported file type must be .pdf or .docx")
    
    if file.filename.endswith(".pdf"):
        res=extract_text_from_pdf(file.file)
    else:
        res=extract_text_from_docx(file.file)

    opti_str=optimize_structure(res)

    return JSONResponse(status_code=200 , content={"structure feed": opti_str})

@app.post("/optimize_content")
def optimize_contents(file: UploadFile=File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return HTTPException(status_code=401 , detail="Unsupported file type must be .pdf or .docx")
    
    if file.filename.endswith(".pdf"):
        res=extract_text_from_pdf(file.file)
    else:
        res=extract_text_from_docx(file.file)

    opti_cont=check_content(res)

    return JSONResponse(status_code=200 ,content={'text': opti_cont})

@app.post('/optimize_tone-style')
def optimize_tone_style(file:UploadFile=File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return HTTPException(status_code=401 , detail="Unsupported file type must be .pdf or .docx")
    
    if file.filename.endswith(".pdf"):
        res=extract_text_from_pdf(file.file)
    else:
        res=extract_text_from_docx(file.file)

    opti_tone=check_tone_and_style(res)

    return JSONResponse(status_code=200,content={"text": opti_tone})






    

    

    

