
import duckdb
import streamlit as st

from pipeline.config import DB_PATH

st.set_page_config(page_title="Weather & Air Quality", layout="wide")
st.title("Weather & Air Quality Dashboard")


@st.cache_data(ttl=300)
def load_data():
    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        return con.execute(
            "select * from main_marts.daily_city_metrics order by date, city"
        ).df()
    finally:
        con.close()


try:
    df = load_data()
except Exception as exc:  # table missing before the first pipeline run
    st.error(f"Could not read the mart. Run the pipeline first (`make run`).\n\n{exc}")
    st.stop()

cities = st.sidebar.multiselect("Cities", sorted(df.city.unique()), default=sorted(df.city.unique()))
view = df[df.city.isin(cities)]

c1, c2, c3 = st.columns(3)
c1.metric("Cities", view.city.nunique())
c2.metric("Hot days (>= 35 C)", int(view.is_hot_day.sum()))
c3.metric("Worst AQI", "n/a" if view.max_aqi.isna().all() else int(view.max_aqi.max()))

st.subheader("Average temperature (C)")
st.line_chart(view.pivot(index="date", columns="city", values="avg_temp_c"))

st.subheader("Average PM2.5 (ug/m3)")
st.bar_chart(view.pivot(index="date", columns="city", values="avg_pm25_ugm3"))

st.subheader("Daily metrics")
st.dataframe(view)