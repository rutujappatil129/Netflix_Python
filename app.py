import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DATA_FILE = Path(__file__).with_name("netflic.csv")
LOGO_FILE = Path(__file__).with_name("images.jpg")
BACKGROUND_FILE = Path(__file__).with_name("bg image.jpg")
REQUIRED_COLUMNS = {
    "Customer_ID",
    "Region",
    "Subscription_Plan",
    "Title",
    "Category",
    "Type",
    "Rating",
    "Watch_Count",
    "Watch_Date",
    "Watch_Time_Minutes",
    "Device",
    "Monthly_Revenue",
}
COLORS = [
    "#E50914",
    "#FF7185",
    "#FFB454",
    "#A78BFA",
    "#4CC9D8",
    "#62D6A5",
    "#F28AC2",
    "#F2E9D8",
]
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = COLORS
px.defaults.color_continuous_scale = ["#4A1020", "#B20710", "#E50914", "#FF7185", "#FFB454"]


def style_chart(figure: go.Figure) -> go.Figure:
    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F5F5F5", "family": "DM Sans, sans-serif"},
        title_font={"color": "#FFFFFF", "family": "Space Grotesk, sans-serif", "size": 18},
        margin={"l": 24, "r": 24, "t": 60, "b": 30},
    )
    figure.update_xaxes(
        color="#C8C5C8",
        gridcolor="rgba(255,255,255,.10)",
        zerolinecolor="rgba(255,255,255,.14)",
    )
    figure.update_yaxes(
        color="#C8C5C8",
        gridcolor="rgba(255,255,255,.10)",
        zerolinecolor="rgba(255,255,255,.14)",
    )
    return figure


st.set_page_config(
    page_title="Netflix Audience & Revenue",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

background_image = (
    base64.b64encode(BACKGROUND_FILE.read_bytes()).decode("ascii")
    if BACKGROUND_FILE.is_file()
    else ""
)
hero_background = (
    f'url("data:image/jpeg;base64,{background_image}")'
    if background_image
    else "linear-gradient(120deg, #2b080b, #101014)"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #faf9f8;
        --muted: #aaa7aa;
        --panel: #141316;
        --line: rgba(255, 255, 255, .09);
        --red: #e50914;
    }
    .stApp {
        background: #09090b;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: #101013;
        border-right: 1px solid var(--line);
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.045em; }
    h1 { font-size: clamp(2.4rem, 5vw, 4.2rem) !important; line-height: 1.04 !important; }
    [data-testid="stImage"] img { border-radius: 8px; }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1b191c, #111013);
        border: 1px solid var(--line);
        border-top: 2px solid #b20710;
        border-radius: 4px 4px 15px 15px;
        padding: 17px 19px;
        box-shadow: 0 14px 32px rgba(0,0,0,.18);
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; color: #fff; }
    div[data-testid="stPlotlyChart"] {
        background: #111013;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 7px;
        box-shadow: 0 12px 32px rgba(0,0,0,.15);
    }
    .eyebrow {
        color: #ff5962; text-transform: uppercase; letter-spacing: .22em;
        font-size: .72rem; font-weight: 700; margin-bottom: .65rem;
    }
    .subtitle { color: #d0cdd0; font-size: 1rem; margin-top: .35rem; max-width: 640px; }
    .section-label {
        display: flex; align-items: center; gap: .65rem;
        color: #f3f0f1; font-size: .78rem; text-transform: uppercase;
        letter-spacing: .19em; font-weight: 700; margin: 1.8rem 0 .8rem;
    }
    .section-label:before {
        content: ''; width: 4px; height: 17px; background: var(--red); border-radius: 4px;
    }
    .brand-note { text-align: right; padding-top: .7rem; color: #bdb9bd; font-size: .76rem; letter-spacing: .13em; text-transform: uppercase; }
    .brand-note strong { color: #fff; }
    .hero-banner {
        position: relative; overflow: hidden; min-height: 300px; display: flex;
        align-items: end; padding: clamp(24px, 5vw, 58px);
        margin: 10px 0 27px; border: 1px solid rgba(255,255,255,.12);
        border-radius: 18px;
        background-image: linear-gradient(90deg, rgba(8,8,10,.96) 0%, rgba(8,8,10,.76) 45%, rgba(8,8,10,.15) 100%),
            linear-gradient(0deg, rgba(8,8,10,.68), transparent 72%), __HERO_BACKGROUND__;
        background-size: cover; background-position: center 47%;
        box-shadow: 0 24px 65px rgba(0,0,0,.32);
    }
    .hero-banner:after {
        content: ''; position: absolute; inset: auto 0 0; height: 3px;
        background: linear-gradient(90deg, #e50914, #f05a66 36%, transparent 82%);
    }
    .hero-copy { position: relative; z-index: 1; max-width: 690px; }
    .hero-tag {
        display: inline-block; padding: 7px 11px; margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,.28); border-radius: 3px;
        background: rgba(12,11,13,.55); color: #fff; font-size: .68rem;
        font-weight: 700; letter-spacing: .19em; text-transform: uppercase;
    }
    .hero-copy h1 { margin: 0; }
    .hero-copy .subtitle { margin: 12px 0 0; }
    @media (max-width: 700px) {
        .hero-banner { min-height: 260px; background-position: 58% center; }
        .brand-note { text-align: left; padding: 0 0 .7rem; }
    }
    </style>
    """.replace("__HERO_BACKGROUND__", hero_background),
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    frame = frame.copy()
    frame["Watch_Date"] = pd.to_datetime(frame["Watch_Date"], errors="coerce")
    for column in ("Rating", "Watch_Count", "Watch_Time_Minutes", "Monthly_Revenue"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE.name}. Place it beside app.py and reload.")
    st.stop()

try:
    data = load_data(str(DATA_FILE))
except (OSError, pd.errors.ParserError, ValueError) as error:
    st.error(f"Could not load the Netflix dataset: {error}")
    st.stop()

st.sidebar.markdown("## 🎬 Netflix insights")
st.sidebar.caption("Explore audience, viewing, and revenue patterns.")
st.sidebar.markdown("---")

regions = sorted(data["Region"].dropna().unique().tolist())
plans = sorted(data["Subscription_Plan"].dropna().unique().tolist())
categories = sorted(data["Category"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_plans = st.sidebar.multiselect("Subscription plan", plans, default=plans)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

valid_dates = data["Watch_Date"].dropna()
if valid_dates.empty:
    st.sidebar.info("No valid watch dates are available to filter.")
    filtered = data[
        data["Region"].isin(selected_regions)
        & data["Subscription_Plan"].isin(selected_plans)
        & data["Category"].isin(selected_categories)
    ].copy()
else:
    date_range = st.sidebar.date_input(
        "Watch date range",
        value=(valid_dates.min().date(), valid_dates.max().date()),
        min_value=valid_dates.min().date(),
        max_value=valid_dates.max().date(),
    )
    filtered = data[
        data["Region"].isin(selected_regions)
        & data["Subscription_Plan"].isin(selected_plans)
        & data["Category"].isin(selected_categories)
    ].copy()
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
        dates = filtered["Watch_Date"].dt.date
        if start_date is not None:
            filtered = filtered[dates >= start_date]
            dates = filtered["Watch_Date"].dt.date
        if end_date is not None:
            filtered = filtered[dates <= end_date]

brand_col, note_col = st.columns([1, 2], vertical_alignment="center")
with brand_col:
    if LOGO_FILE.is_file():
        st.image(str(LOGO_FILE), width=190)
    else:
        st.markdown("## NETFLIX")
with note_col:
    st.markdown(
        '<div class="brand-note"><strong>Stories meet data</strong><br>Audience intelligence · 2026</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <section class="hero-banner">
      <div class="hero-copy">
        <div class="hero-tag">The audience edit · Netflix insights</div>
        <h1>Stories people love.<br>Insights you can use.</h1>
        <p class="subtitle">Explore what’s trending, where your viewers are watching, and the stories driving revenue.</p>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No records match these filters. Select more options in the sidebar.")
    st.stop()

customers = filtered["Customer_ID"].nunique()
revenue = filtered["Monthly_Revenue"].sum()
avg_rating = filtered["Rating"].mean()
watch_hours = filtered["Watch_Time_Minutes"].sum() / 60

metric_cols = st.columns(4)
metric_cols[0].metric("CUSTOMERS", f"{customers:,}", help="Unique customers in the filtered data")
metric_cols[1].metric(
    "REVENUE",
    f"{revenue / 1000:,.1f}K",
    help=f"Monthly revenue total: {revenue:,.0f} dataset units",
)
metric_cols[2].metric(
    "AVG RATING / 5",
    f"{avg_rating:.2f}" if pd.notna(avg_rating) else "—",
    help="Mean customer rating on a 1–5 scale",
)
metric_cols[3].metric(
    "WATCH TIME",
    f"{watch_hours:,.0f} h",
    help="Total recorded watch time, in hours",
)

st.markdown('<div class="section-label">Revenue & engagement</div>', unsafe_allow_html=True)
left, right = st.columns(2)

region_revenue = (
    filtered.groupby("Region", as_index=False)["Monthly_Revenue"]
    .sum()
    .sort_values("Monthly_Revenue", ascending=True)
)
fig_region = px.bar(
    region_revenue,
    x="Monthly_Revenue",
    y="Region",
    orientation="h",
    text_auto=",.0f",
    title="Revenue by region",
    color="Region",
    color_discrete_sequence=COLORS,
    labels={"Monthly_Revenue": "Revenue (dataset units)", "Region": ""},
)
fig_region.update_layout(showlegend=False)
style_chart(fig_region)
left.plotly_chart(fig_region, width="stretch")

category_revenue = (
    filtered.groupby("Category", as_index=False)["Monthly_Revenue"]
    .sum()
    .sort_values("Monthly_Revenue", ascending=True)
)
fig_category = px.bar(
    category_revenue,
    x="Monthly_Revenue",
    y="Category",
    orientation="h",
    text_auto=",.0f",
    title="Revenue by category",
    color="Category",
    color_discrete_sequence=COLORS,
    labels={"Monthly_Revenue": "Revenue (dataset units)", "Category": ""},
)
fig_category.update_layout(showlegend=False)
style_chart(fig_category)
right.plotly_chart(fig_category, width="stretch")

st.markdown('<div class="section-label">Trends & audience</div>', unsafe_allow_html=True)
left, right = st.columns(2)

monthly = filtered.dropna(subset=["Watch_Date"]).copy()
monthly["Month"] = monthly["Watch_Date"].dt.to_period("M").dt.to_timestamp()
monthly_revenue = (
    monthly.groupby("Month", as_index=False)["Monthly_Revenue"]
    .sum()
    .sort_values("Month")
)
fig_month = px.line(
    monthly_revenue,
    x="Month",
    y="Monthly_Revenue",
    markers=True,
    title="Monthly revenue trend",
    labels={"Monthly_Revenue": "Revenue (dataset units)", "Month": ""},
)
fig_month.update_traces(line_color="#E50914", line_width=3, fill="tozeroy", fillcolor="rgba(229,9,20,.12)")
style_chart(fig_month)
left.plotly_chart(fig_month, width="stretch")

plan_rating = (
    filtered.groupby("Subscription_Plan", as_index=False)["Rating"]
    .sum()
    .sort_values("Rating", ascending=False)
)
fig_plan = px.pie(
    plan_rating,
    names="Subscription_Plan",
    values="Rating",
    hole=0.58,
    title="Rating score by subscription plan",
    color_discrete_sequence=COLORS,
    labels={"Rating": "Total rating score", "Subscription_Plan": "Plan"},
)
fig_plan.update_traces(textposition="inside", textinfo="percent+label")
style_chart(fig_plan)
right.plotly_chart(fig_plan, width="stretch")

st.markdown('<div class="section-label">What people are watching</div>', unsafe_allow_html=True)
left, right = st.columns(2)

top_titles = (
    filtered.groupby("Title", as_index=False)
    .agg(Watch_Count=("Watch_Count", "sum"), Watch_Time_Minutes=("Watch_Time_Minutes", "sum"))
    .sort_values("Watch_Count", ascending=False)
    .head(10)
    .sort_values("Watch_Count", ascending=True)
)
fig_titles = px.bar(
    top_titles,
    x="Watch_Count",
    y="Title",
    orientation="h",
    text="Watch_Count",
    title="Top 10 titles by watch count",
    color="Watch_Count",
    color_continuous_scale=["#6b1017", "#E50914", "#ff858b"],
    labels={"Watch_Count": "Total watch count", "Title": ""},
)
fig_titles.update_layout(coloraxis_showscale=False)
style_chart(fig_titles)
left.plotly_chart(fig_titles, width="stretch")

device_views = (
    filtered.groupby("Device", as_index=False)["Watch_Time_Minutes"]
    .sum()
    .sort_values("Watch_Time_Minutes", ascending=False)
)
fig_device = px.pie(
    device_views,
    names="Device",
    values="Watch_Time_Minutes",
    hole=0.62,
    title="Watch time by device",
    color_discrete_sequence=COLORS,
)
fig_device.update_traces(textposition="inside", textinfo="percent+label")
style_chart(fig_device)
right.plotly_chart(fig_device, width="stretch")

with st.expander("View filtered dataset"):
    st.caption(f"{len(filtered):,} records · {filtered['Customer_ID'].nunique():,} unique customers")
    st.dataframe(filtered, width="stretch", hide_index=True)

st.caption("Charts and summary metrics update with the filters in the sidebar.")
