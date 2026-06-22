from pathlib import Path
import re

import matplotlib.pyplot as plt
import streamlit as st

from agents.reviewer import run_full_review

st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🧠",
    layout="wide",
)

st.title("AI Code Review & Mentorship Agent")
st.caption("Upload a source file or paste code to generate a full review.")

if "review_results" not in st.session_state:
    st.session_state.review_results = None
if "report_path" not in st.session_state:
    st.session_state.report_path = None


def detect_language(file_name: str) -> str:
    ext = Path(file_name).suffix.lower()
    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".go": "Go",
        ".rb": "Ruby",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
    }
    return mapping.get(ext, "Unknown")


def safe_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", Path(name).stem).strip("_") or "review"


def build_summary_metrics(results: dict) -> dict:
    metrics = {}
    for key, value in results.items():
        text = value or ""
        metrics[key] = max(1, len(re.findall(r"(?i)(bug|issue|error|warning|vulnerability|risk|security|improve|refactor)", text)))
    return metrics


def save_markdown_report(results: dict, source_name: str) -> Path:
    output_dir = Path("output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / f"{safe_name(source_name)}_review.md"
    report_content = f"# Code Review Report for {source_name}\n\n"
    for section, content in results.items():
        heading = section.replace("_", " ").title()
        report_content += f"## {heading}\n\n{content}\n\n"

    report_path.write_text(report_content, encoding="utf-8")
    return report_path


def save_summary_charts(results: dict, count: int) -> list[Path]:
    output_dir = Path("output/charts")
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics = build_summary_metrics(results)
    labels = list(metrics.keys())
    values = list(metrics.values())
    chart_paths = []

    for i in range(1, count + 1):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values, color=["#ff6b6b", "#feca57", "#48dbfb"])
        ax.set_title(f"Review Summary Chart {i}")
        ax.set_ylabel("Signal Count")
        ax.tick_params(axis="x", rotation=15)
        fig.tight_layout()

        chart_path = output_dir / f"review_summary_{i}.png"
        fig.savefig(chart_path, bbox_inches="tight")
        plt.close(fig)
        chart_paths.append(chart_path)

    return chart_paths


with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader(
        "Upload code file",
        type=["py", "js", "ts", "java", "c", "cpp", "cs", "go", "rb", "php", "html", "css"],
    )
    code_input = st.text_area(
        "Or paste code here",
        height=300,
        placeholder="Paste your code snippet here...",
    )
    language_hint = st.text_input(
        "Language (optional)",
        placeholder="Python, Java, JavaScript, ...",
    )
    chart_count = st.slider(
        "How many charts to save?",
        min_value=1,
        max_value=5,
        value=3,
    )
    run_button = st.button("Run Full Review", type="primary")

col1, col2 = st.columns([2, 1])

with col1:
    if uploaded_file is not None:
        raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
        st.code(raw_text, language=detect_language(uploaded_file.name))
        code_input = raw_text if not code_input else code_input

with col2:
    if uploaded_file is not None:
        st.info(f"File: {uploaded_file.name}")

if run_button:
    code_to_review = code_input.strip()
    if not code_to_review:
        st.warning("Please upload a file or paste code before running the review.")
    else:
        selected_language = language_hint.strip() or detect_language(uploaded_file.name if uploaded_file else "code.txt")

        with st.spinner("Reviewing your code..."):
            try:
                review_results = run_full_review(code=code_to_review, language=selected_language)
                st.session_state.review_results = review_results
                st.session_state.report_path = save_markdown_report(review_results, uploaded_file.name if uploaded_file else "pasted_code")
            except Exception as e:
                st.error(f"An error happened while running the review: {e}")
                st.stop()

        st.success("Review completed successfully.")

        if st.session_state.report_path is not None:
            with open(st.session_state.report_path, "r", encoding="utf-8") as f:
                report_markdown = f.read()
            st.download_button(
                label="Download Markdown Report",
                data=report_markdown,
                file_name=st.session_state.report_path.name,
                mime="text/markdown",
            )

        metrics = build_summary_metrics(st.session_state.review_results)
        st.subheader("Review Summary")
        metric_cols = st.columns(3)
        for idx, (label, value) in enumerate(metrics.items()):
            metric_cols[idx].metric(label.replace("_", " ").title(), value)

        if chart_count:
            chart_paths = save_summary_charts(st.session_state.review_results, chart_count)
            st.subheader("Saved Charts")
            chart_cols = st.columns(min(chart_count, 3))
            for idx, chart_path in enumerate(chart_paths):
                with chart_cols[idx % len(chart_cols)]:
                    st.image(str(chart_path), caption=f"Chart {idx + 1}")
            st.caption(f"Saved {len(chart_paths)} charts to {Path('output/charts').resolve()}")

        st.subheader("Detailed Review")
        tab_labels = ["Bugs", "Security", "Deep Review"]
        tabs = st.tabs(tab_labels)
        for tab, label in zip(tabs, tab_labels):
            with tab:
                content = st.session_state.review_results.get(label.lower().replace(" ", "_"), "")
                st.markdown(content)

if st.session_state.review_results:
    st.caption("Showing the latest generated review.")


