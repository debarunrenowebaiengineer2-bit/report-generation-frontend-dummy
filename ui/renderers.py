import streamlit as st


def render_section(data):
    if not data:
        st.warning("No data returned")
        return

    if "section" in data:
        st.subheader(data["section"])

    if "metrics" in data:
        st.markdown("### Metrics")
        st.json(data["metrics"])

    if "narrative" in data:
        st.markdown("### Narrative")
        st.write(data["narrative"])


def render_json(data):
    st.json(data)

import pandas as pd
import streamlit as st


def render_report_section(section: dict) -> None:
    """
    Renders one already-formatted report section as:
    - title
    - executive paragraph
    - metrics table
    - audit table
    - key insights
    - recommendations
    """

    st.subheader(section.get("title", "Untitled Section"))

    executive_summary = section.get("executive_summary")
    if executive_summary:
        st.write(executive_summary)

    metrics = section.get("metrics", [])
    if metrics:
        st.markdown("### Key Metrics")
        metrics_df = pd.DataFrame(metrics)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    audit_rows = section.get("audit_table", [])
    if audit_rows:
        st.markdown("### Audit Table")
        audit_df = pd.DataFrame(audit_rows)

        rename_map = {
            "area": "Area",
            "issue": "Negative Points / Issues to Revise",
            "positive": "Positive Points / What Can Be Improved Further",
            "recommendation": "Solutions / Recommendations",
            "severity": "Severity",
        }

        audit_df = audit_df.rename(columns=rename_map)
        st.dataframe(audit_df, use_container_width=True, hide_index=True)

    narrative = section.get("narrative", {})

    key_insights = narrative.get("key_insights", [])
    if key_insights:
        st.markdown("### Additional Key Insights")
        for item in key_insights:
            st.write(f"• {item}")

    recommendations = narrative.get("recommendations", [])
    if recommendations:
        st.markdown("### Recommendations")
        for item in recommendations:
            st.write(f"• {item}")

def render_full_report(report: dict) -> None:
    """
    Renders the full report returned by the backend.
    """

    st.title(f"{report.get('company_name', 'Company')} Digital Presence Report")

    sections = report.get("sections", [])
    if not sections:
        st.warning("No report sections were returned.")
        return

    for idx, section in enumerate(sections):
        render_report_section(section)
        if idx < len(sections) - 1:
            st.divider()