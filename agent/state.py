from typing import TypedDict, Optional, List, Dict, Any

class ReviewState(TypedDict):
    username: str
    
    # 1. Profile Extractor
    extracted_profile: Optional[Dict[str, Any]]
    
    # 2. Repository Analyzer
    repository_analysis: Optional[List[Dict[str, Any]]]
    repo_impact_score: Optional[float]
    
    # 3. README Evaluation
    readme_scores: Optional[Dict[str, Any]]
    overall_readme_score: Optional[float]
    
    # 4. Contribution Intelligence
    contribution_intelligence: Optional[Dict[str, Any]]
    consistency_score: Optional[float]
    
    # 5. Code Quality Analyzer
    code_quality_analysis: Optional[Dict[str, Any]]
    
    # 6. Open Source Collaboration
    open_source_collaboration: Optional[Dict[str, Any]]
    collaboration_score: Optional[float]
    
    # 7. Recruiter Readiness
    recruiter_readiness_score: Optional[float]
    
    # 8. AI Mentor
    mentor_feedback: Optional[Dict[str, Any]]
    
    # System
    errors: Optional[List[str]]