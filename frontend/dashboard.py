import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Compliance Audit Dashboard", layout="wide", initial_sidebar_state="expanded")

# Dark Mode Styling
st.markdown("""
    <style>
        :root {
            --primary-color: #1f77b4;
            --text-color: #f0f2f6;
            --background-color: #0e1117;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117;
            color: #f0f2f6;
        }
        
        [data-testid="stSidebar"] {
            background-color: #161b22;
        }
        
        .main {
            background-color: #0e1117;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #58a6ff !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #58a6ff;
        }
        
        [data-testid="stMetricLabel"] {
            color: #f0f2f6;
        }
        
        [data-testid="stMetricContainer"] {
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 12px;
            background-color: #161b22;
        }
        
        .info-box {
            background-color: #161b22;
            border-left: 4px solid #58a6ff;
            padding: 12px;
        }
        
        .success-box {
            background-color: #161b22;
            border-left: 4px solid #3fb950;
            padding: 12px;
        }
        
        .error-box {
            background-color: #161b22;
            border-left: 4px solid #f85149;
            padding: 12px;
        }
        
        [data-testid="stDataFrame"] {
            background-color: #0e1117;
        }
        
        .stDataFrame {
            background-color: #161b22;
        }
        
        [data-testid="stDownloadButton"] {
            border: 1px solid #30363d;
        }
        
        /* Navigation and Sidebar text visibility */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] p,
        .stRadio > label,
        .stSelectbox label,
        .stSelectbox span {
            color: #f0f2f6 !important;
        }
        
        /* Selectbox dropdown text */
        [data-baseweb="select"] {
            color: #f0f2f6 !important;
        }
        
        [data-baseweb="select"] > div {
            color: #f0f2f6 !important;
        }
        
        /* Ensure selectbox option text is visible */
        [data-baseweb="popover"] {
            color: #f0f2f6 !important;
        }
        
        /* Fix for all text in sidebar */
        .sidebar-text {
            color: #f0f2f6 !important;
        }
        
        /* Info/Success/Error/Warning containers text */
        [data-testid="stMarkdownContainer"] {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] strong,
        [data-testid="stMarkdownContainer"] em {
            color: #f0f2f6 !important;
        }
        
        /* Info box text */
        [data-testid="stInfo"] {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stInfo"] > div {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stInfo"] span,
        [data-testid="stInfo"] p,
        [data-testid="stInfo"] strong {
            color: #f0f2f6 !important;
        }
        
        /* Success box text */
        [data-testid="stSuccess"] {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stSuccess"] > div,
        [data-testid="stSuccess"] span,
        [data-testid="stSuccess"] p {
            color: #f0f2f6 !important;
        }
        
        /* Error box text */
        [data-testid="stError"] {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stError"] > div,
        [data-testid="stError"] span,
        [data-testid="stError"] p {
            color: #f0f2f6 !important;
        }
        
        /* Warning box text */
        [data-testid="stWarning"] {
            color: #f0f2f6 !important;
        }
        
        [data-testid="stWarning"] > div,
        [data-testid="stWarning"] span,
        [data-testid="stWarning"] p {
            color: #f0f2f6 !important;
        }
        
        /* Button styling */
        button {
            background-color: #238636 !important;
            color: #f0f2f6 !important;
            border: 1px solid #3fb950 !important;
        }
        
        button:hover {
            background-color: #2ea043 !important;
            color: #f0f2f6 !important;
        }
        
        [data-testid="stBaseButton-secondary"] {
            background-color: #238636 !important;
            color: #f0f2f6 !important;
        }
        
        [data-testid="stBaseButton-secondary"]:hover {
            background-color: #2ea043 !important;
        }
        
        /* Selectbox styling */
        [data-baseweb="select"] > div:first-child {
            background-color: #161b22 !important;
            border-color: #30363d !important;
            color: #f0f2f6 !important;
        }
        
        [data-baseweb="input"] {
            background-color: #161b22 !important;
            border-color: #30363d !important;
            color: #f0f2f6 !important;
        }
        
        /* Dropdown menu styling */
        [data-baseweb="menu"] {
            background-color: #161b22 !important;
            color: #f0f2f6 !important;
        }
        
        [data-baseweb="menu"] li {
            color: #f0f2f6 !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background-color: #30363d !important;
        }
        
        /* Option styling in dropdowns */
        [data-baseweb="option"] {
            color: #f0f2f6 !important;
            background-color: #161b22 !important;
        }
        
        /* Selectbox value text */
        [data-baseweb="select"] span {
            color: #f0f2f6 !important;
        }
        
        [data-baseweb="select"] div {
            color: #f0f2f6 !important;
        }
        
        /* Dropdown options list items */
        [role="option"] {
            color: #f0f2f6 !important;
            background-color: #161b22 !important;
        }
        
        [role="option"]:hover {
            background-color: #30363d !important;
            color: #f0f2f6 !important;
        }
        
        /* Plotly chart text labels */
        text {
            fill: #f0f2f6 !important;
            color: #f0f2f6 !important;
        }
        
        .slice text,
        .pietext,
        [data-testid="plotly-chart"] text {
            fill: #f0f2f6 !important;
            font-weight: bold;
        }
        
        /* SVG text in Plotly charts */
        svg text {
            fill: #f0f2f6 !important;
            color: #f0f2f6 !important;
        }
        
        /* Selectbox dropdown content */
        [data-baseweb="select"] [role="listbox"] {
            background-color: #161b22 !important;
        }
        
        [data-baseweb="select"] [role="option"] {
            color: #f0f2f6 !important;
            background-color: #161b22 !important;
        }
        
        /* Ensure select value is readable */
        [data-baseweb="select"] > div > div {
            color: #f0f2f6 !important;
        }
        
        /* All container text */
        div {
            color: #f0f2f6 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Compliance Audit Dashboard")

# Load the CSV file
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../data/audit_results.csv")
        return df
    except FileNotFoundError:
        st.error("audit_results.csv not found. Please run scoring_engine.py first.")
        return None

df = load_data()

if df is not None:
    # Separate final row from chunk data
    final_row = df[df['Chunk'] == 'FINAL']
    chunk_df = df[df['Chunk'] != 'FINAL'].copy()
    
    # Convert chunk to numeric
    chunk_df['Chunk'] = pd.to_numeric(chunk_df['Chunk'])
    
    if not final_row.empty:
        final_empathy = final_row['empathy'].values[0]
        final_professionalism = final_row['professionalism'].values[0]
        final_compliance = final_row['compliance'].values[0]
        final_violations = final_row['violations'].values[0] if 'violations' in final_row.columns else "None"
        final_suggestions = final_row['suggestions'].values[0] if 'suggestions' in final_row.columns else "None"
    else:
        final_empathy = chunk_df['empathy'].mean()
        final_professionalism = chunk_df['professionalism'].mean()
        final_compliance = "Pending"
        final_violations = "None"
        final_suggestions = "None"
    
    # Parse violations and suggestions
    violations_list = [v.strip() for v in final_violations.split('|') if v.strip() and v.strip() != "None"]
    suggestions_list = [s.strip() for s in final_suggestions.split('|') if s.strip() and s.strip() != "None"]
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["🏠 Home", "📊 Reports", "🔍 Chunk-wise Analysis"])
    
    st.markdown("---")
    
    # ========================= HOME PAGE =========================
    if page == "🏠 Home":
        st.header("Welcome to Compliance Audit Dashboard")
        
        # Overall Scores
        st.subheader("📈 Overall Performance Scores")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Average Empathy Score",
                value=f"{final_empathy:.2f}",
                delta=None,
                delta_color="off"
            )
        
        with col2:
            st.metric(
                label="Average Professionalism Score",
                value=f"{final_professionalism:.2f}",
                delta=None,
                delta_color="off"
            )
        
        with col3:
            compliance_color = "🔴" if final_compliance == "FAIL" else "🟡" if final_compliance == "WARN" else "🟢"
            st.metric(
                label="Overall Compliance",
                value=f"{compliance_color} {final_compliance}",
                delta=None,
                delta_color="off"
            )
        
        st.markdown("---")
        
        # Top 3 Violations
        st.subheader("⚠️ Top 3 Violations")
        if violations_list:
            top_3_violations = violations_list[:3]
            for i, violation in enumerate(top_3_violations, 1):
                st.error(f"**{i}. {violation}**")
        else:
            st.success("✓ No violations detected")
        
        st.markdown("---")
        
        # Top 5 Suggestion Points
        st.subheader("💡 Top 5 Improvement Suggestions")
        if suggestions_list:
            top_5_suggestions = suggestions_list[:5]
            for i, suggestion in enumerate(top_5_suggestions, 1):
                st.info(f"**{i}. {suggestion}**")
        else:
            st.success("✓ No improvement suggestions needed")
        
        st.markdown("---")
        
        # Download Results
        st.subheader("📥 Download Results")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Audit Results (CSV)",
            data=csv,
            file_name=f"audit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # ========================= REPORTS PAGE =========================
    elif page == "📊 Reports":
        st.header("Reports & Analytics")
        
        # Empathy Score Trend
        st.subheader("📉 Empathy Score Trend")
        fig_empathy = go.Figure()
        fig_empathy.add_trace(go.Scatter(
            x=chunk_df['Chunk'],
            y=chunk_df['empathy'],
            mode='lines+markers',
            name='Empathy',
            line=dict(color='#58a6ff', width=2),
            marker=dict(size=8, color='#58a6ff')
        ))
        fig_empathy.add_hline(y=final_empathy, line_dash="dash", line_color="#f85149", annotation_text="Average")
        fig_empathy.update_layout(
            xaxis_title="Chunk Number",
            yaxis_title="Score (0-100)",
            hovermode='x unified',
            height=400,
            plot_bgcolor='#161b22',
            paper_bgcolor='#0e1117',
            font=dict(color='#f0f2f6'),
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d')
        )
        st.plotly_chart(fig_empathy, use_container_width=True)
        
        st.markdown("---")
        
        # Professionalism Score Trend
        st.subheader("📉 Professionalism Score Trend")
        fig_prof = go.Figure()
        fig_prof.add_trace(go.Scatter(
            x=chunk_df['Chunk'],
            y=chunk_df['professionalism'],
            mode='lines+markers',
            name='Professionalism',
            line=dict(color='#3fb950', width=2),
            marker=dict(size=8, color='#3fb950')
        ))
        fig_prof.add_hline(y=final_professionalism, line_dash="dash", line_color="#f85149", annotation_text="Average")
        fig_prof.update_layout(
            xaxis_title="Chunk Number",
            yaxis_title="Score (0-100)",
            hovermode='x unified',
            height=400,
            plot_bgcolor='#161b22',
            paper_bgcolor='#0e1117',
            font=dict(color='#f0f2f6'),
            xaxis=dict(gridcolor='#30363d'),
            yaxis=dict(gridcolor='#30363d')
        )
        st.plotly_chart(fig_prof, use_container_width=True)
        
        st.markdown("---")
        
        # Compliance Distribution & Overall Average
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Compliance Distribution")
            compliance_counts = chunk_df['compliance'].value_counts()
            colors = {'Pass': '#3fb950', 'Warn': '#d29922', 'Fail': '#f85149'}
            fig_compliance = go.Figure(data=[go.Pie(
                labels=compliance_counts.index,
                values=compliance_counts.values,
                marker=dict(colors=[colors.get(x, '#8b949e') for x in compliance_counts.index], line=dict(color='#0e1117', width=2)),
                textposition='inside',
                textinfo='label+percent',
                textfont=dict(color='#f0f2f6', size=12)
            )])
            fig_compliance.update_layout(
                title="Compliance Distribution",
                height=400,
                paper_bgcolor='#0e1117',
                font=dict(color='#f0f2f6', size=12),
                showlegend=True
            )
            st.plotly_chart(fig_compliance, use_container_width=True)
        
        with col2:
            st.subheader("📊 Overall Average Scores")
            fig_scores = go.Figure(data=[
                go.Bar(x=['Empathy', 'Professionalism'], y=[final_empathy, final_professionalism],
                       marker=dict(color=['#58a6ff', '#3fb950'], line=dict(color='#f0f2f6', width=1.5)))
            ])
            fig_scores.update_layout(
                xaxis_title="Score Type",
                yaxis_title="Score",
                height=400,
                showlegend=False,
                plot_bgcolor='#161b22',
                paper_bgcolor='#0e1117',
                font=dict(color='#f0f2f6'),
                xaxis=dict(gridcolor='#30363d'),
                yaxis=dict(gridcolor='#30363d')
            )
            st.plotly_chart(fig_scores, use_container_width=True)
        
        st.markdown("---")
        
        # Full Results Table
        st.subheader("📋 Full Results Table")
        display_df = chunk_df.copy()
        display_df = display_df.astype(str)
        st.dataframe(display_df, use_container_width=True, height=500)
    
    # ========================= CHUNK-WISE ANALYSIS PAGE =========================
    elif page == "🔍 Chunk-wise Analysis":
        st.header("Detailed Chunk-wise Analysis")
        
        selected_chunk = st.selectbox(
            "Select a chunk to view detailed analysis:",
            options=chunk_df['Chunk'].astype(int).unique(),
            format_func=lambda x: f"Chunk {x}"
        )
        
        chunk_data = chunk_df[chunk_df['Chunk'] == selected_chunk].iloc[0]
        
        # Scores for selected chunk
        st.subheader(f"Chunk {selected_chunk} - Performance Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Empathy Score", value=f"{chunk_data['empathy']:.0f}/100")
        
        with col2:
            st.metric(label="Professionalism Score", value=f"{chunk_data['professionalism']:.0f}/100")
        
        with col3:
            compliance_status = chunk_data['compliance']
            compliance_emoji = "🔴" if compliance_status == "Fail" else "🟡" if compliance_status == "Warn" else "🟢"
            st.metric(label="Compliance Status", value=f"{compliance_emoji} {compliance_status}")
        
        st.markdown("---")
        
        # Assessment Reason
        st.subheader("📝 Assessment Reason")
        st.info(chunk_data['reason'])
        
        st.markdown("---")
        
        # Violations for this chunk
        st.subheader("⚠️ Violations in This Chunk")
        if 'violations' in chunk_data and pd.notna(chunk_data['violations']):
            chunk_violations = [v.strip() for v in str(chunk_data['violations']).split('|') if v.strip()]
            if chunk_violations:
                for i, violation in enumerate(chunk_violations, 1):
                    st.error(f"**{i}. {violation}**")
            else:
                st.success("✓ No violations in this chunk")
        else:
            st.success("✓ No violations in this chunk")
        
        st.markdown("---")
        
        # Suggestions for this chunk
        st.subheader("💡 Improvement Suggestions for This Chunk")
        if 'suggestions' in chunk_data and pd.notna(chunk_data['suggestions']):
            chunk_suggestions = [s.strip() for s in str(chunk_data['suggestions']).split('|') if s.strip()]
            if chunk_suggestions:
                for i, suggestion in enumerate(chunk_suggestions, 1):
                    st.success(f"✅ {i}. {suggestion}")
            else:
                st.info("No specific suggestions for this chunk")
        else:
            st.info("No specific suggestions for this chunk")
        
        st.markdown("---")
        
        # Navigation between chunks
        col1, col2, col3 = st.columns(3)
        with col1:
            if selected_chunk > chunk_df['Chunk'].min():
                if st.button("⬅️ Previous Chunk"):
                    st.rerun()
        
        with col3:
            if selected_chunk < chunk_df['Chunk'].max():
                if st.button("Next Chunk ➡️"):
                    st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.info("Dashboard Version 2.0\nLast Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

