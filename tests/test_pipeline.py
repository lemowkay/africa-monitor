import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import generate_demo,validate_indicators,comparable_year_data,parse_worldbank_payload


def test_demo_values_and_join():
    demo=generate_demo()
    d,quality=validate_indicators(demo)
    assert len(d)==len(demo)
    assert len(d.country.unique())==5
    both,year=comparable_year_data(d)
    assert year==2025
    assert len(both)==5
    assert quality.loc[0,'retained_observations']==len(d)


def test_api_parsing_drops_missing_and_unknown_countries():
    p=[{'page':1},[
        {'countryiso3code':'ZAF','date':'2022','value':56.1},
        {'countryiso3code':'KEN','date':'2022','value':None},
        {'countryiso3code':'USA','date':'2022','value':6.1}]]
    d=parse_worldbank_payload(p,'SL.UEM.1524.ZS')
    assert len(d)==1
    assert d.iloc[0]['country']=='South Africa'


def test_pct_range_guard():
    data=generate_demo(); data.loc[0,'value']=150
    filtered,quality=validate_indicators(data)
    assert quality.loc[0,'out_of_range_pct_removed']==1
    assert len(filtered)==len(data)-1
