# Netflix Audience & Revenue Dashboard

An interactive Streamlit dashboard for exploring the Netflix viewing dataset. It includes a dark Netflix-inspired theme, custom logo and hero background, sidebar filters, summary metrics, and interactive Plotly charts.

## Run locally

From the project directory:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The dashboard reads `netflic.csv` from the same directory as `app.py`.

## Dashboard views

- Revenue by region and content category
- Monthly revenue trend
- Rating score by subscription plan
- Top 10 titles by watch count
- Watch time by device
- Filters for region, subscription plan, category, and watch date

## Project files

- `app.py` — Streamlit dashboard
- `netflic.csv` — dataset used by the dashboard
- `images.jpg` — dashboard logo
- `bg image.jpg` — hero background image
- `Untitled1.py` — original analysis script
- `requirements.txt` — Python dependencies