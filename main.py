from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.graph import github_reviewer_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "GitHub Reviewer backend is running perfectly!"}

@app.post("/review")
def review_portfolio(username: str):
    initial_state = {"username": username}
    result = github_reviewer_app.invoke(initial_state)
    
    return {
        "username": result.get("username"),
        "profile": result.get("extracted_profile"),
        "repositories": result.get("repository_analysis"),
        "metrics": {
            "impact_score": result.get("repo_impact_score"),
            "readme_score": result.get("overall_readme_score"),
            "consistency_score": result.get("consistency_score"),
            "collaboration_score": result.get("collaboration_score"),
            "readiness_score": result.get("recruiter_readiness_score")
        },
        "details": {
            "readme_scores_breakdown": result.get("readme_scores"),
            "contribution": result.get("contribution_intelligence"),
            "code_quality": result.get("code_quality_analysis"),
            "collaboration": result.get("open_source_collaboration")
        },
        "feedback": result.get("mentor_feedback"),
        "workflow": result.get("workflow_summary"),
        "errors": result.get("errors", [])
    }
