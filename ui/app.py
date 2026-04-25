import os
from textwrap import dedent

import pandas as pd
import requests
import streamlit as st


st.set_page_config(page_title="GitInsight AI", page_icon="🐙", layout="wide")

API_URL = os.getenv("GITINSIGHT_API_URL","https://gitinsight-ai-r0b5.onrender.com")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --bg: #07111f;
            --panel: rgba(9, 23, 43, 0.84);
            --panel-soft: rgba(13, 31, 58, 0.68);
            --border: rgba(120, 180, 255, 0.18);
            --text: #eff6ff;
            --muted: #9fb7d3;
            --accent: #5eead4;
            --accent-2: #60a5fa;
            --gold: #fbbf24;
            --danger: #fb7185;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(96, 165, 250, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(94, 234, 212, 0.14), transparent 22%),
                linear-gradient(180deg, #030712 0%, var(--bg) 55%, #0b1220 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1200px;
            padding-top: 4.5rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4, p, div, span, label {
            font-family: "Space Grotesk", sans-serif !important;
        }

        code {
            font-family: "IBM Plex Mono", monospace !important;
        }

        [data-testid="stTextInput"] input {
            background: rgba(5, 16, 31, 0.88);
            border: 1px solid var(--border);
            border-radius: 16px;
            color: var(--text);
            font-size: 1rem;
            padding: 0.95rem 1rem;
        }

        [data-testid="stButton"] button {
            border: none;
            border-radius: 14px;
            color: #04111d;
            font-weight: 700;
            padding: 0.8rem 1.2rem;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 18px 45px rgba(37, 99, 235, 0.28);
        }

        [data-testid="stButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 22px 55px rgba(37, 99, 235, 0.35);
        }

        .hero {
            padding: 2rem;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(10, 26, 47, 0.88)),
                linear-gradient(135deg, rgba(94, 234, 212, 0.12), rgba(96, 165, 250, 0.08));
            border: 1px solid var(--border);
            box-shadow: 0 30px 80px rgba(2, 6, 23, 0.45);
            overflow: hidden;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.3fr 0.9fr;
            gap: 1rem;
            align-items: center;
        }

        .eyebrow {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(94, 234, 212, 0.14);
            color: var(--accent);
            font-size: 0.82rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .hero h1 {
            font-size: 3rem;
            line-height: 1;
            margin: 0.9rem 0;
        }

        .hero p {
            color: var(--muted);
            font-size: 1.02rem;
            margin-bottom: 0;
        }

        .hero-panel {
            border-radius: 22px;
            padding: 1.2rem;
            background: rgba(6, 19, 36, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .hero-stat {
            display: flex;
            justify-content: space-between;
            padding: 0.85rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            color: var(--muted);
        }

        .hero-stat:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .section-card, .metric-card, .repo-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.2rem;
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.2);
        }

        .mentor-spotlight {
            background:
                radial-gradient(circle at top right, rgba(94, 234, 212, 0.12), transparent 28%),
                linear-gradient(135deg, rgba(12, 32, 58, 0.96), rgba(8, 22, 42, 0.96));
            border: 1px solid rgba(94, 234, 212, 0.24);
            border-radius: 26px;
            padding: 1.4rem;
            box-shadow: 0 22px 60px rgba(3, 10, 22, 0.32);
        }

        .mentor-kicker {
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.78rem;
            margin-bottom: 0.55rem;
        }

        .metric-card {
            min-height: 150px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.88rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0.3rem 0;
        }

        .metric-helper {
            color: var(--muted);
            font-size: 0.95rem;
        }

        .repo-card {
            margin-bottom: 1rem;
            background: var(--panel-soft);
        }

        .repo-topline {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: center;
        }

        .repo-name {
            font-size: 1.15rem;
            font-weight: 700;
        }

        .repo-meta {
            color: var(--muted);
            font-size: 0.92rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.8rem;
        }

        .pill {
            padding: 0.35rem 0.65rem;
            border-radius: 999px;
            background: rgba(96, 165, 250, 0.12);
            border: 1px solid rgba(96, 165, 250, 0.18);
            color: #dbeafe;
            font-size: 0.82rem;
        }

        .workflow-step {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.8rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .workflow-step:last-child {
            border-bottom: none;
        }

        .status-ok {
            color: var(--accent);
            font-weight: 700;
        }

        .status-warn {
            color: var(--gold);
            font-weight: 700;
        }

        .small-muted {
            color: var(--muted);
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def score_card(title: str, value: str, helper: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-helper">{helper}</div>
    </div>
    """


def section_title(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div style="margin: 1.1rem 0 0.8rem;">
            <div style="font-size: 1.4rem; font-weight: 700;">{title}</div>
            <div class="small-muted">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_repo_card(repo: dict) -> None:
    updated = (repo.get("updated_at") or "").replace("T", " ").replace("Z", " UTC")
    description = repo.get("description") or "No repository description provided."
    language = repo.get("language") or "Unknown"
    url = repo.get("html_url") or "#"

    st.markdown(
        f"""
        <div class="repo-card">
            <div class="repo-topline">
                <div>
                    <div class="repo-name"><a href="{url}" target="_blank" style="color:#eff6ff;text-decoration:none;">{repo.get("name", "Repository")}</a></div>
                    <div class="repo-meta">{description}</div>
                </div>
                <div class="repo-meta">Updated {updated or "recently"}</div>
            </div>
            <div class="pill-row">
                <span class="pill">Language: {language}</span>
                <span class="pill">Stars: {repo.get("stars", 0)}</span>
                <span class="pill">Forks: {repo.get("forks", 0)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def fetch_analysis(username: str) -> dict:
    response = requests.post(
        f"{API_URL}/review",
        params={"username": username},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


inject_styles()

st.markdown(
    """
    <div style="margin-bottom: 1rem;">
        <div style="font-size: 2.1rem; font-weight: 700; color: #eff6ff;">GitInsight AI</div>
        <div class="small-muted">Multi-agent GitHub profile analyzer</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-grid">
            <div>
                <span class="eyebrow">Multi-Agent GitHub Intelligence</span>
                <h1>Analyze a GitHub profile with AI agents.</h1>
                <p>
                    Enter a GitHub username to see profile signals, repository insights, and AI mentor feedback.
                </p>
            </div>
            <div class="hero-panel">
                <div class="hero-stat"><span>Profile</span><strong style="color:#eff6ff;">Overview</strong></div>
                <div class="hero-stat"><span>Repositories</span><strong style="color:#eff6ff;">Insights</strong></div>
                <div class="hero-stat"><span>Workflow</span><strong style="color:#eff6ff;">Multi-agent</strong></div>
                <div class="hero-stat"><span>Mentor</span><strong style="color:#eff6ff;">Feedback</strong></div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.write("")
username = st.text_input("GitHub username", placeholder="e.g. torvalds")

if st.button("Analyze Portfolio", use_container_width=True):
    if not username.strip():
        st.warning("Enter a GitHub username to start the review.")
    else:
        with st.spinner(f"Analyzing {username} across the multi-agent workflow..."):
            try:
                data = fetch_analysis(username.strip())
            except requests.RequestException as exc:
                st.error(
                    f"Could not reach the backend at `{API_URL}`. Start FastAPI with `uvicorn main:app --reload` and try again.\n\n{exc}"
                )
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
            else:
                profile = data.get("profile") or {}
                metrics = data.get("metrics") or {}
                details = data.get("details") or {}
                feedback = data.get("feedback") or {}
                repos = data.get("repositories") or []
                workflow = data.get("workflow") or {}
                completed = set(workflow.get("completed") or [])
                errors = data.get("errors") or []

                top_languages = workflow.get("top_languages") or {}
                strongest_language = next(iter(top_languages.keys()), "Unknown")
                readiness_score = round(metrics.get("readiness_score", 0))
                impact_score = round(metrics.get("impact_score", 0))
                readme_score = round(metrics.get("readme_score", 0))
                consistency_score = round(metrics.get("consistency_score", 0))
                collab_score = round(metrics.get("collaboration_score", 0))

                section_title(
                    f"{username}'s GitHub Intelligence Report",
                    "A compact dashboard for recruiters, mentors, and portfolio tuning.",
                )

                col1, col2, col3, col4 = st.columns(4)
                col1.markdown(
                    score_card("Recruiter Readiness", f"{readiness_score}/100", "Weighted from impact, consistency, docs, and collaboration."),
                    unsafe_allow_html=True,
                )
                col2.markdown(
                    score_card("Repository Impact", str(impact_score), "Stars, forks, and repository volume converted into one signal."),
                    unsafe_allow_html=True,
                )
                col3.markdown(
                    score_card("Top Language", strongest_language, "Most common language across the analyzed repositories."),
                    unsafe_allow_html=True,
                )
                col4.markdown(
                    score_card("External PRs", str(details.get("collaboration", {}).get("external_prs", 0)), "Open-source collaboration outside personal repositories."),
                    unsafe_allow_html=True,
                )

                st.write("")
                mentor_text = feedback.get("feedback_text", "No mentor feedback generated.")
                st.markdown(
                    """
                    <div class="mentor-spotlight">
                        <div class="mentor-kicker">Primary Takeaway</div>
                        <div style="font-size:1.6rem;font-weight:700;margin-bottom:0.35rem;">AI Mentor Brief</div>
                        <div class="small-muted">This is the highest-signal summary of the profile and should be the first thing a user reads after the headline metrics.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(dedent(mentor_text).strip())

                st.write("")
                left, right = st.columns([1.5, 1])

                with left:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Profile Snapshot")
                    snap1, snap2, snap3, snap4 = st.columns(4)
                    snap1.metric("Followers", profile.get("followers", 0))
                    snap2.metric("Following", profile.get("following", 0))
                    snap3.metric("Public Repos", profile.get("public_repos", 0))
                    snap4.metric("Code Consistency", f"{consistency_score}/100")

                    bio = profile.get("bio") or "No bio found on the public profile."
                    st.markdown(f"**Bio**  \n{bio}")

                    info_line = " | ".join(
                        item for item in [profile.get("company"), profile.get("location")] if item
                    )
                    if info_line:
                        st.caption(info_line)

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.write("")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Score Breakdown")
                    chart_data = pd.DataFrame(
                        {
                            "Signal": ["Impact", "README", "Consistency", "Collaboration"],
                            "Score": [impact_score, readme_score, consistency_score, collab_score],
                        }
                    )
                    st.bar_chart(chart_data.set_index("Signal"))
                    st.progress(min(max(readiness_score / 100, 0.0), 1.0), text=f"Readiness confidence: {readiness_score}%")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.write("")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Top Repositories")
                    if repos:
                        for repo in repos[:5]:
                            render_repo_card(repo)
                    else:
                        st.info("No repositories were returned for this profile.")
                    st.markdown("</div>", unsafe_allow_html=True)

                with right:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Agent Workflow")
                    agent_names = workflow.get("agents") or [
                        "Profile Extractor",
                        "Repository Analyzer",
                        "README Evaluator",
                        "Contribution Intelligence",
                        "Code Quality Analyzer",
                        "Open Source Collaboration",
                        "Recruiter Readiness",
                        "AI Mentor",
                    ]
                    for agent in agent_names:
                        status = "Complete" if agent in completed else "Waiting"
                        status_class = "status-ok" if agent in completed else "status-warn"
                        st.markdown(
                            f'<div class="workflow-step"><span>{agent}</span><span class="{status_class}">{status}</span></div>',
                            unsafe_allow_html=True,
                        )
                    st.caption("Repository analysis fans out into multiple specialist agents before the final synthesis.")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.write("")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Language Mix")
                    if top_languages:
                        lang_df = pd.DataFrame(
                            {"Language": list(top_languages.keys()), "Repos": list(top_languages.values())}
                        )
                        st.dataframe(lang_df, use_container_width=True, hide_index=True)
                    else:
                        st.caption("No language data available.")
                    st.markdown("</div>", unsafe_allow_html=True)

                if details.get("code_quality", {}).get("ai_report"):
                    st.write("")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("Code Quality Notes")
                    analyzed_repo = details.get("code_quality", {}).get("analyzed_repo")
                    if analyzed_repo:
                        st.caption(f"Focused on: {analyzed_repo}")
                    st.markdown(details["code_quality"]["ai_report"])
                    st.markdown("</div>", unsafe_allow_html=True)

                if errors:
                    st.write("")
                    st.warning("Some parts of the workflow reported issues:")
                    for error in errors:
                        st.code(error)
