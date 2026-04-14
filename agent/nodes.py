import os
import requests
import json
import base64
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from .state import ReviewState

load_dotenv()

# We will use Llama 3 for intelligent qualitative tasks
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"} if token else {}

def profile_extractor_agent(state: ReviewState):
    username = state["username"]
    try:
        user_resp = requests.get(f"https://api.github.com/users/{username}", headers=get_headers())
        user_data = user_resp.json() if user_resp.status_code == 200 else {}
        
        extracted = {
            "bio": user_data.get("bio"),
            "followers": user_data.get("followers", 0),
            "following": user_data.get("following", 0),
            "public_repos": user_data.get("public_repos", 0),
            "avatar_url": user_data.get("avatar_url"),
            "company": user_data.get("company"),
            "location": user_data.get("location"),
        }
        return {"extracted_profile": extracted, "errors": []}
    except Exception as e:
        return {"errors": [f"profile_extractor: {str(e)}"]}

def repository_analyzer_agent(state: ReviewState):
    username = state["username"]
    try:
        repos_resp = requests.get(f"https://api.github.com/users/{username}/repos?sort=updated&per_page=15", headers=get_headers())
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        
        analysis = []
        total_stars = 0
        total_forks = 0
        
        for r in repos:
            stars = r.get("stargazers_count", 0)
            forks = r.get("forks_count", 0)
            total_stars += stars
            total_forks += forks
            analysis.append({
                "name": r.get("name"),
                "stars": stars,
                "forks": forks,
                "language": r.get("language"),
                "description": r.get("description"),
                "updated_at": r.get("updated_at")
            })
            
        repo_impact_score = min(100, (total_stars * 5) + (total_forks * 3) + (len(repos) * 2))
        return {"repository_analysis": analysis, "repo_impact_score": repo_impact_score}
    except Exception as e:
        return {"errors": state.get("errors", []) + [f"repo_analyzer: {str(e)}"]}

def readme_evaluation_agent(state: ReviewState):
    username = state["username"]
    repos = state.get("repository_analysis", [])
    
    # Grab top 2 repos by stars
    top_repos = sorted(repos, key=lambda x: x["stars"], reverse=True)[:2]
    scores = {}
    total_score = 0
    
    for r in top_repos:
        repo_name = r["name"]
        url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
        resp = requests.get(url, headers=get_headers())
        
        score = 30 # Base score for missing readme
        if resp.status_code == 200:
            content = resp.json().get("content", "")
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                length_bonus = min(40, len(decoded) // 50)
                score = 50 + length_bonus
                if "installation" in decoded.lower(): score += 10
                if "usage" in decoded.lower(): score += 10
                if "```" in decoded: score += 10
            except:
                pass
        
        score = min(100, score)
        scores[repo_name] = score
        total_score += score
        
    avg_score = (total_score / len(top_repos)) if top_repos else 0
    return {"readme_scores": scores, "overall_readme_score": avg_score}

def contribution_intelligence_agent(state: ReviewState):
    username = state["username"]
    try:
        events_resp = requests.get(f"https://api.github.com/users/{username}/events/public?per_page=100", headers=get_headers())
        events = events_resp.json() if events_resp.status_code == 200 else []
        
        push_events = [e for e in events if e.get("type") == "PushEvent"]
        pr_events = [e for e in events if e.get("type") == "PullRequestEvent"]
        
        consistency_score = min(100, len(events) + (len(push_events) * 2))
        
        return {
            "contribution_intelligence": {
                "recent_commits": len(push_events),
                "recent_prs": len(pr_events),
                "total_recent_events": len(events)
            },
            "consistency_score": consistency_score
        }
    except Exception:
        return {"consistency_score": 0}

def code_quality_analyzer_agent(state: ReviewState):
    username = state["username"]
    repos = state.get("repository_analysis", [])
    if not repos:
        return {"code_quality_analysis": {"error": "No repos found"}}
    
    # Just evaluating structurally without heavy static analysis to save time/limits
    top_repo = sorted(repos, key=lambda x: x["stars"], reverse=True)[0]
    
    prompt = f"Given this repository metadata: {top_repo}, suggest 3 general coding best practices for their preferred language."
    try:
        res = llm.invoke([HumanMessage(content=prompt)])
        return {"code_quality_analysis": {"ai_report": res.content, "analyzed_repo": top_repo["name"]}}
    except:
        return {"code_quality_analysis": {"ai_report": "Unable to analyze code quality."}}

def open_source_collaboration_agent(state: ReviewState):
    username = state["username"]
    try:
        # PRs created by them, not in their own repos
        query = f"is:pr author:{username} -user:{username}"
        url = f"https://api.github.com/search/issues?q={query}"
        resp = requests.get(url, headers=get_headers())
        
        count = 0
        if resp.status_code == 200:
            count = resp.json().get("total_count", 0)
            
        collaboration_score = min(100, count * 10)
        return {
            "open_source_collaboration": {"external_prs": count},
            "collaboration_score": collaboration_score
        }
    except:
        return {"collaboration_score": 0}

def recruiter_readiness_agent(state: ReviewState):
    profile = state.get("extracted_profile", {})
    r_score = state.get("overall_readme_score", 0)
    c_score = state.get("consistency_score", 0)
    i_score = state.get("repo_impact_score", 0)
    collab_score = state.get("collaboration_score", 0)
    
    # Calculate /100 score
    readiness = (
        (i_score * 0.3) +
        (r_score * 0.2) +
        (c_score * 0.3) +
        (collab_score * 0.1) +
        (10 if profile.get("bio") else 0)
    )
    
    return {"recruiter_readiness_score": min(100, readiness)}

def ai_mentor_agent(state: ReviewState):
    prompt = f"""
    You are an expert tech recruiter and AI mentor. Analyze this GitHub profile overview and create a concise review.
    Profile: {state.get("extracted_profile")}
    Readiness Score: {state.get("recruiter_readiness_score")}/100
    Repo Impact: {state.get("repo_impact_score")}
    Consistency: {state.get("consistency_score")}
    
    Provide:
    1. 2 Strengths
    2. 2 Weaknesses
    3. 2 Actionable career/improvement steps
    
    Return pure text without conversational baggage. Use clean formatting.
    """
    try:
        res = llm.invoke([HumanMessage(content=prompt)])
        return {"mentor_feedback": {"feedback_text": res.content}}
    except:
        return {"mentor_feedback": {"feedback_text": "Error generating mentor feedback."}}
