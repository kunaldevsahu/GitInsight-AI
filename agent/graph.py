from langgraph.graph import StateGraph, START, END
from .state import ReviewState
from .nodes import (
    profile_extractor_agent,
    repository_analyzer_agent,
    readme_evaluation_agent,
    contribution_intelligence_agent,
    code_quality_analyzer_agent,
    open_source_collaboration_agent,
    recruiter_readiness_agent,
    ai_mentor_agent
)

builder = StateGraph(ReviewState)

builder.add_node("profile_extractor", profile_extractor_agent)
builder.add_node("repository_analyzer", repository_analyzer_agent)
builder.add_node("readme_evaluator", readme_evaluation_agent)
builder.add_node("contribution_intelligence", contribution_intelligence_agent)
builder.add_node("code_quality", code_quality_analyzer_agent)
builder.add_node("os_collaboration", open_source_collaboration_agent)
builder.add_node("recruiter_readiness", recruiter_readiness_agent)
builder.add_node("ai_mentor", ai_mentor_agent)

# Start with the profile, then analyze repositories once.
builder.add_edge(START, "profile_extractor")
builder.add_edge("profile_extractor", "repository_analyzer")

# Fan out into specialized agents after repository analysis.
builder.add_edge("repository_analyzer", "readme_evaluator")
builder.add_edge("repository_analyzer", "contribution_intelligence")
builder.add_edge("repository_analyzer", "code_quality")
builder.add_edge("repository_analyzer", "os_collaboration")

# Fan in once the specialist agents have produced their signals.
builder.add_edge("readme_evaluator", "recruiter_readiness")
builder.add_edge("contribution_intelligence", "recruiter_readiness")
builder.add_edge("code_quality", "recruiter_readiness")
builder.add_edge("os_collaboration", "recruiter_readiness")
builder.add_edge("recruiter_readiness", "ai_mentor")
builder.add_edge("ai_mentor", END)

github_reviewer_app = builder.compile()
