from sentence_transformers import SentenceTransformer,util


def get_skill_score(resume_skill, req_skill):
    model = SentenceTransformer("anass1209/resume-job-matcher-all-MiniLM-L6-v2")
    resume_embs = model.encode(resume_skill, convert_to_tensor=True)
    job_embs = model.encode(req_skill, convert_to_tensor=True)
    cos_scores = util.cos_sim(resume_embs, job_embs)
    avg_score = cos_scores.mean().item()
    return round(avg_score*100, 2)

def get_ats_score(job_desc,resume_text):
    model=SentenceTransformer("anass1209/resume-job-matcher-all-MiniLM-L6-v2")

    embeddings = model.encode([resume_text, job_desc], convert_to_tensor=True)

    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    
    score=round(similarity*100 ,2)
    return score
