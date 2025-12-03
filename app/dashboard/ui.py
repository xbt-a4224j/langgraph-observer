import json
import requests
import streamlit as st
from datetime import datetime

API_URL = "http://localhost:8000/run-graph"


# --- Helper Functions --- #
def pretty_json(data: dict) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False)


def format_timestamp(ts):
    if not ts:
        return "N/A"
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(ts)


# --- Streamlit UI --- #
st.set_page_config(page_title="LangGraph Observer", layout="wide")

st.title("🧠 LangGraph Observer Dashboard")
st.caption("End-to-end observability for your LangGraph workflow")

st.divider()

# -------------------------------
# INPUT PANEL
# -------------------------------
st.header("1. Provide Input")

user_input = st.text_area(
    "Enter a prompt for the LangGraph workflow:",
    placeholder="Explain how LangGraph works in simple terms…",
    height=150
)

run_button = st.button("▶ Run Workflow", use_container_width=True)

# -------------------------------
# RUN WORKFLOW
# -------------------------------
if run_button:
    if not user_input.strip():
        st.error("Please enter a prompt before running.")
        st.stop()

    with st.spinner("Running LangGraph workflow…"):
        try:
            response = requests.post(API_URL, json={"input": user_input})

            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)
                st.stop()

            result = response.json()

        except Exception as e:
            st.error("Failed to contact API server.")
            st.exception(e)
            st.stop()

    # ---------------------------
    # SIDEBAR — METRICS
    # ---------------------------
    st.sidebar.header("📊 Run Metadata")

    st.sidebar.write("**Start Time:**")
    st.sidebar.code(format_timestamp(result.get("start_time")))

    st.sidebar.write("**End Time:**")
    st.sidebar.code(format_timestamp(result.get("end_time")))

    st.sidebar.write("**Duration (seconds):**")
    st.sidebar.code(result.get("duration_seconds", "N/A"))

    st.sidebar.write("**Score:**")
    st.sidebar.code(result.get("score", "N/A"))

    st.sidebar.divider()

    st.sidebar.write("**Artifacts:**")
    artifacts = result.get("artifacts", [])
    if artifacts:
        for item in artifacts:
            st.sidebar.code(item)
    else:
        st.sidebar.write("No artifacts collected.")

    # ---------------------------
    # MAIN PANEL — OUTPUT
    # ---------------------------
    st.header("2. Workflow Output")

    st.subheader("LLM Output")
    st.success(result.get("llm_output", "(no output)"))

    st.divider()
    st.subheader("Full State (Pretty JSON)")
    st.code(pretty_json(result), language="json")

    # ---------------------------
    # ARTIFACT & LOG VIEWER
    # ---------------------------
    st.header("3. Artifacts & Logs")

    col1, col2 = st.columns(2)

    # Artifacts
    with col1:
        st.subheader("Artifacts")
        if artifacts:
            for path in artifacts:
                st.write(f"📄 `{path}`")
                try:
                    with open(path, "r") as f:
                        st.code(f.read())
                except Exception as e:
                    st.warning(f"Could not open artifact: {e}")
        else:
            st.info("No artifacts generated.")

    # Logs
    with col2:
        st.subheader("Run Log")
        try:
            with open("app/storage/logs/run.log", "r") as f:
                logs = f.read()
                st.code(logs)
        except FileNotFoundError:
            st.info("No log file yet.")
        except Exception as e:
            st.warning(f"Could not read log file: {e}")