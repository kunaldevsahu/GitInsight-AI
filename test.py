from agent.graph import github_reviewer_app
import json

initial_state = {"username": "torvalds"}
result = github_reviewer_app.invoke(initial_state)

print(json.dumps({
    "extracted_profile": result.get("extracted_profile"),
    "repo_impact": result.get("repo_impact_score"),
    "readme": result.get("overall_readme_score"),
    "consistency": result.get("consistency_score"),
    "collab": result.get("collaboration_score"),
    "readiness": result.get("recruiter_readiness_score"),
    "feedback": result.get("mentor_feedback")
}, indent=2))
