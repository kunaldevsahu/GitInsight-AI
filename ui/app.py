import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="GitInsight AI", page_icon="🐙", layout="wide")

# Using st.markdown to render the GitHub logo along with the title
st.markdown(
    "<h1 style='display: flex; align-items: center;'><img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' width='50' style='margin-right: 15px;'> GitInsight AI - Portfolio Analyzer</h1>", 
    unsafe_allow_html=True
)
st.markdown("Enter a GitHub username to run the 8-Agent LangGraph intelligence pipeline.")

username = st.text_input("GitHub Username:", placeholder="e.g., torvalds")

if st.button("Analyze Portfolio"):
    if username:
        with st.spinner(f"Running multi-agent analysis for {username}... This may take a minute."):
            try:
                response = requests.post(f"https://gitinsight-ai-r0b5.onrender.com/review?username={username}")
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    
                    profile = data.get("profile", {})
                    metrics = data.get("metrics", {})
                    details = data.get("details", {})
                    feedback = data.get("feedback", {})
                    repos = data.get("repositories", [])
                    
                    # 1. Profile Overview
                    st.header("Developer Profile")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("Followers", profile.get("followers", 0))
                    col2.metric("Following", profile.get("following", 0))
                    col3.metric("Public Repos", profile.get("public_repos", 0))
                    col4.metric("External OS PRs", details.get("collaboration", {}).get("external_prs", 0))
                    col5.metric("Recruiter Readiness", f"{round(metrics.get('readiness_score', 0))}/100")
                    
                    if profile.get("bio"):
                        st.info(f"**Bio:** {profile.get('bio')}")
                    
                    st.divider()
                    
                    # 2. Visualizations
                    st.header("Metrics Visualization")
                    
                    # Create a dataframe for the bar chart
                    chart_data = pd.DataFrame({
                        "Score Type": [
                            "Impact Score", 
                            "README Quality", 
                            "Consistency", 
                            "Collaboration"
                        ],
                        "Score": [
                            metrics.get("impact_score", 0),
                            metrics.get("readme_score", 0),
                            metrics.get("consistency_score", 0),
                            metrics.get("collaboration_score", 0)
                        ]
                    })
                    
                    # Use a basic streamlit bar chart
                    st.bar_chart(chart_data.set_index("Score Type"))
                    
                    st.divider()

                    # 3. Top Repositories
                    st.header("Top Repositories Analyzed")
                    for repo in repos[:3]:
                        with st.expander(f"📦 {repo.get('name')} - ⭐ {repo.get('stars')} | 🍴 {repo.get('forks')}"):
                            st.write(f"**Language:** {repo.get('language')}")
                            st.write(f"**Description:** {repo.get('description')}")
                            
                    st.divider()
                            
                    # 4. Code Quality & AI Mentor
                    col_code, col_mentor = st.columns(2)
                    
                    with col_code:
                        st.subheader("Code Quality Analysis")
                        st.write(details.get("code_quality", {}).get("ai_report", "No code quality data available."))
                        
                    with col_mentor:
                        st.subheader("AI Mentor Feedback")
                        feedback_txt = feedback.get("feedback_text", "No mentor feedback generated.")
                        st.write(feedback_txt)
                        
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to the backend. Is FastAPI running? Error: {str(e)}")

# st.markdown(
#     "<br><br><div style='text-align: center; color: grey;'>Made with ❤️ by Kunal</div>", 
#     unsafe_allow_html=True
# )
