# GitInsight AI

GitInsight AI is a simple GitHub profile analyzer built with FastAPI, Streamlit, and LangGraph.

Enter a GitHub username and the app reviews the profile using multiple AI-assisted agents, then shows:

- Profile overview
- Repository insights
- README and contribution signals
- Collaboration activity
- Recruiter readiness score
- AI mentor feedback

## How It Works

The app uses an 8-agent workflow:

1. Profile Extractor
2. Repository Analyzer
3. README Evaluator
4. Contribution Intelligence
5. Code Quality Analyzer
6. Open Source Collaboration
7. Recruiter Readiness
8. AI Mentor

The flow is not fully linear:

- `Profile Extractor` runs first
- `Repository Analyzer` collects repo data
- The analysis then fans out to README, contribution, code-quality, and collaboration agents
- Their outputs are combined by `Recruiter Readiness`
- `AI Mentor` produces the final summary and next steps

## Current UI

The current Streamlit app includes:

- A simple landing section
- Score cards for readiness, impact, language, and external PRs
- A mentor-first summary block near the top
- Profile metrics and score breakdown charts
- Repository cards with language, stars, forks, and update time
- A workflow panel showing the multi-agent pipeline

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- Agent orchestration: LangGraph
- LLM: Groq via `langchain-groq`
- Data source: GitHub REST API

## Setup

```bash
git clone <your-repo-url>
cd GitInsight
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here
```

Notes:

- `GROQ_API_KEY` is required for the AI-generated code-quality and mentor outputs.
- `GITHUB_TOKEN` is recommended to avoid strict GitHub rate limits.

## Run The App

Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

Start the Streamlit frontend in another terminal:

```bash
streamlit run ui/app.py
```

Optional:

- Set `GITINSIGHT_API_URL` if your backend is running somewhere other than `http://127.0.0.1:8000`

Example:

```bash
export GITINSIGHT_API_URL=http://127.0.0.1:8000
streamlit run ui/app.py
```

## API

### `GET /`

Health check endpoint.

### `POST /review?username=<github_username>`

Runs the GitHub analysis workflow and returns:

- `profile`
- `repositories`
- `metrics`
- `details`
- `feedback`
- `workflow`
- `errors`

## Demo

Demo video:

[demo_video/demo.mov](/Users/kunaldevsahu/Desktop/AI_Projects/GitInsight/demo_video/demo.mov)
