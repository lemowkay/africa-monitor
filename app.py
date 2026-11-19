"""Streamlit dashboard for World Bank indicators, with visibly marked demo mode."""
import pandas as pd
import plotly.express as px
import streamlit as st
from pipeline import COUNTRIES,INDICATORS,generate_demo,fetch_worldbank,validate_indicators,comparable_year_data

st.set_page_config(page_title='South Africa Opportunity Monitor',page_icon='🌍',layout='wide')
st.title('South Africa Opportunity Monitor')
st.caption('Youth unemployment • internet use • GDP per capita • African comparisons')
source=st.sidebar.radio('Data source',['Synthetic demonstration','Live World Bank API'],index=0)
if source=='Live World Bank API':
    @st.cache_data(ttl=60*60*12,show_spinner='Loading World Bank indicators...')
    def get_real():return fetch_worldbank()
    try:raw=get_real()
    except Exception as e:st.error(f'Could not load World Bank data: {e}');st.stop()
    st.success('Live World Bank source selected. Check dates; indicators may be revised or delayed.')
else:
    raw=generate_demo()
    st.warning('SYNTHETIC DEMO: fictional values — not South African statistics. Select live World Bank data for factual charts.')
df,audit=validate_indicators(raw)
selected_codes=st.sidebar.multiselect('Countries',list(COUNTRIES),default=list(COUNTRIES),format_func=lambda code:COUNTRIES[code])
metric=st.sidebar.selectbox('Indicator',list(INDICATORS),format_func=lambda code:INDICATORS[code])
df=df[df.country_code.isin(selected_codes)]
if df.empty:st.warning('Select at least one country');st.stop()
left,right,third=st.columns(3)
left.metric('Countries',df.country_code.nunique());right.metric('Data records',f'{len(df):,}')
third.metric('Latest reported year (any series)',int(df.year.max()))
view=df[df.indicator_code==metric].sort_values('year')
st.plotly_chart(px.line(view,x='year',y='value',color='country',markers=True,
                         title=INDICATORS[metric],labels={'year':'Year','value':'Indicator value'}),use_container_width=True)
latest=(view.sort_values('year').groupby('country',as_index=False).tail(1)
        [['country','year','value']].sort_values('value',ascending=False))
st.subheader('Latest available observation for each country')
st.dataframe(latest,use_container_width=True,hide_index=True)
matched,year=comparable_year_data(df)
if year is not None and len(matched)>0:
    st.plotly_chart(px.scatter(matched,x='IT.NET.USER.ZS',y='SL.UEM.1524.ZS',text='country',
        title=f'Internet use vs youth unemployment — same year ({year}); no causal inference',
        labels={'IT.NET.USER.ZS':'Internet users (% population)',
                'SL.UEM.1524.ZS':'Youth unemployment (% youth labour force)'}),use_container_width=True)
with st.expander('Methodology and data quality'):
    st.dataframe(audit,use_container_width=True)
    st.write('No missing-year imputation. “Latest” can differ by country and indicator. Youth unemployment and internet usage have different population denominators. Trends and cross-country associations are not proof of causation.')
