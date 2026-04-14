# GitInsight AI - GitHub Portfolio Intelligence Analyzer

**GitInsight AI** is an advanced, recruiter-grade developer portfolio evaluation platform. It goes far beyond a basic GitHub username lookup by performing a deep, intelligent analysis of a developer's entire GitHub profile—including coding habits, contribution patterns, documentation quality, and open-source reach—using a massive **8-Agent AI Architecture**.

## Key Features

At its core, GitInsight AI operates a cutting-edge multi-agent orchestration pipeline using **LangGraph** & **Llama 3 (via Groq)**. Once a GitHub username is inputted, our architecture spawns 8 specialized agents to evaluate the user:

1. **GitHub Profile Extractor**: Fetches core foundational data (bio, followers, active repos).
2. **Repository Analyzer**: Evaluates the developer’s active projects—calculating deep repository impact based on stars, forks, and codebase focus.
3. **README Evaluation Agent**: Decodes, parses, and statically scores documentation quality across top repositories (looking for installation instructions, usage, and examples).
4. **Contribution Intelligence Agent**: Parses public event graphs to assess commit momentum, push streaks, and overall coding consistency over time.
5. **Code Quality Analyzer Agent**: Leverages the LLM context to do a structural evaluation and pinpoint engineering gaps.
6. **Open Source Collaboration Agent**: Cross-references GitHub's issue matching API to find pull requests submitted to external/non-owned repositories.
7. **Recruiter Readiness Agent**: Synthesizes all gathered intelligence indices to calculate a final `/100` **Recruiter Readiness Score**.
8. **Final AI Mentor Agent**: Acts as an experienced software engineer and tech recruiter, outputting actionable strengths, weaknesses, and improvement areas.

## Tech Stack

**Backend / AI Application**
* **Framework**: FastAPI (for asynchronous robust routing)
* **AI Orchestration**: LangGraph, LangChain 
* **LLM**: Meta Llama 3 (via Groq Cloud API for instantaneous inference)
* **Data Layer**: GitHub REST & GraphQL APIs via `aiohttp` / `requests`

**Frontend Dashboard**
A streamlined, lightweight Streamlit dashboard focused on data visualization and columnized analytical views.

## Installation & Usage

1. **Clone & Setup the Environment**
```bash
git clone <your-repo-link>
cd github_review
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API Keys**
Ensure you have an `.env` file at the root of the project with:
```env
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_personal_access_token_here
```

3. **Start the API Backend (FastAPI)**
```bash
fastapi dev main.py
# Or run: uvicorn main:app --reload
```

4. **Launch the User Interface**
   * **To use the Streamlit Dashboard**: Open a new terminal and run:
     ```bash
     streamlit run ui/app.py
     ```


## Dashboard Previews
Once running, input any public GitHub username (e.g., `torvalds` or `timothycrosley`). The 8 internal intelligence workflows will activate sequentially—culminating in an aggregated, visually stunning readout measuring **Impact**, **Readiness**, and **Mentorship Feedback**.

### Demo Video

<video src="./demo_video/demo.mov" width="100%" controls></video>

---
*Created by the Advanced Agentic Coding pipeline.*
