"""World Bank socio-economic analytics for South Africa and regional comparators."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
COUNTRIES={'ZAF':'South Africa','BWA':'Botswana','NAM':'Namibia','KEN':'Kenya','NGA':'Nigeria'}
INDICATORS={
    'SL.UEM.1524.ZS':'Youth unemployment (% labor force ages 15–24)',
    'IT.NET.USER.ZS':'Individuals using internet (% population)',
    'NY.GDP.PCAP.CD':'GDP per capita (current US$)',
    'SL.UEM.TOTL.ZS':'Total unemployment (% labor force)',
}


def generate_demo(seed:int=2026) -> pd.DataFrame:
    """Invented illustration only, never a representation of World Bank observations."""
    rng=np.random.default_rng(seed)
    rows=[]
    starts={
        'ZAF':(43,8,3100,25), 'BWA':(31,6,3900,17),'NAM':(37,5,2400,22),
        'KEN':(21,3,900,11),'NGA':(18,2,850,9)
    }
    for code,name in COUNTRIES.items():
        youth0,net0,gdp0,total0=starts[code]
        for year in range(2005,2026):
            t=year-2005
            values=[youth0+0.55*t+2*np.sin(t/3)+rng.normal(0,1.1),
                    min(97,net0+3.1*t+rng.normal(0,1.3)),
                    max(50,gdp0*(1+.021*t)+rng.normal(0,gdp0*.03)),
                    total0+0.26*t+1.0*np.sin(t/3)+rng.normal(0,.7)]
            for key,value in zip(INDICATORS,values):
                rows.append({'country_code':code,'country':name,'year':year,'indicator_code':key,
                             'indicator':INDICATORS[key],'value':round(float(value),2)})
    return pd.DataFrame(rows)


def parse_worldbank_payload(payload:list,indicator_code:str) -> pd.DataFrame:
    if not isinstance(payload,list) or len(payload)!=2 or not isinstance(payload[1],list):
        raise ValueError(f'Unexpected World Bank API response for {indicator_code}')
    rows=[]
    for obs in payload[1]:
        value=obs.get('value')
        if value is None:continue  # No zero-imputation or forward-fill
        iso=obs.get('countryiso3code') or ''
        if iso not in COUNTRIES: continue
        try: year=int(obs['date']); value=float(value)
        except (ValueError,TypeError,KeyError):continue
        rows.append({'country_code':iso,'country':COUNTRIES[iso], 'year':year,
                     'indicator_code':indicator_code,'indicator':INDICATORS[indicator_code], 'value':value})
    return pd.DataFrame(rows,columns=['country_code','country','year','indicator_code','indicator','value'])


def fetch_worldbank(start:int=2005,end:int=2025) -> pd.DataFrame:
    """Requires internet. The World Bank may revise historical observations."""
    frames=[]
    country_ids=';'.join(COUNTRIES)
    for key in INDICATORS:
        url=f'https://api.worldbank.org/v2/country/{country_ids}/indicator/{key}'
        try:
            response=requests.get(url,params={'format':'json','date':f'{start}:{end}', 'per_page':2000},timeout=40)
            response.raise_for_status()
            frame=parse_worldbank_payload(response.json(),key)
            frames.append(frame)
        except (requests.RequestException,ValueError) as e:
            raise RuntimeError(f'Could not fetch {key} from World Bank API: {e}') from e
    return pd.concat(frames,ignore_index=True)


def validate_indicators(df:pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    needed={'country_code','country','year','indicator_code','indicator','value'}
    if not needed.issubset(df.columns):raise ValueError(f'Missing columns: {sorted(needed-set(df.columns))}')
    d=df.copy()
    d['year']=pd.to_numeric(d['year'],errors='coerce')
    d['value']=pd.to_numeric(d['value'],errors='coerce')
    raw=len(d)
    d=d.dropna(subset=['year','value']).copy()
    d=d[d['country_code'].isin(COUNTRIES)&d['indicator_code'].isin(INDICATORS)].copy()
    d['year']=d['year'].astype(int)
    # Duplicate country/year/indicator values: keep the last provided observation.
    dup=int(d.duplicated(['country_code','year','indicator_code']).sum())
    d=d.drop_duplicates(['country_code','year','indicator_code'],keep='last')
    pct_codes=[k for k in INDICATORS if k!='NY.GDP.PCAP.CD']
    bad_pct=d['indicator_code'].isin(pct_codes)&~d['value'].between(0,100)
    invalid=int(bad_pct.sum())
    d=d[~bad_pct].copy()
    quality=pd.DataFrame([{'raw_observations':raw,'retained_observations':len(d),
                           'missing_or_unsupported_removed':raw-(len(d)+dup+invalid),
                           'duplicate_keys_removed':dup,'out_of_range_pct_removed':invalid,
                           'countries':d.country_code.nunique(),'years':d.year.nunique()}])
    return d,quality


def comparable_year_data(d:pd.DataFrame) -> tuple[pd.DataFrame,int|None]:
    chosen=['SL.UEM.1524.ZS','IT.NET.USER.ZS']
    base=d[d['indicator_code'].isin(chosen)]
    wide=base.pivot_table(index=['country_code','country','year'],columns='indicator_code',values='value',aggfunc='last').reset_index()
    wide=wide.dropna(subset=chosen)
    if wide.empty:return wide,None
    latest=int(wide.year.max())
    return wide.loc[wide.year==latest].copy(),latest


def make_outputs(raw:pd.DataFrame,out:Path,reports:Path,mode:str) -> dict:
    out.mkdir(parents=True,exist_ok=True);reports.mkdir(parents=True,exist_ok=True)
    d,audit=validate_indicators(raw)
    if d.empty:raise ValueError('No usable indicator observations')
    d=d.sort_values(['country','indicator_code','year'])
    # Latest available dates can DIFFER across indicators/countries.
    latest=(d.sort_values('year').groupby(['country_code','country','indicator_code','indicator'],as_index=False).tail(1)
            .sort_values(['indicator_code','country']))
    comparable,year=comparable_year_data(d)
    kpis={'data_mode':mode,'available_observations':len(d),'countries':d.country_code.nunique(),
          'first_year':int(d.year.min()),'latest_any_indicator_year':int(d.year.max()),
          'latest_shared_youth_internet_year':year if year is not None else ''}
    for name,df in [('indicator_observations',d),('latest_by_indicator',latest),
                    ('latest_joint_year',comparable),('data_quality',audit),('kpis',pd.DataFrame([kpis]))]:
        df.to_csv(out/f'{name}.csv',index=False)
    plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':10})
    fig,ax=plt.subplots(figsize=(10,5.2))
    sel=d[d.indicator_code=='SL.UEM.1524.ZS']
    for country,g in sel.groupby('country'):
        ax.plot(g.year,g.value,label=country,linewidth=2)
    ax.set_title('Youth unemployment — country comparison',loc='left',fontweight='bold')
    ax.set_ylabel('Percent of youth labour force');ax.set_xlabel('Year')
    ax.legend(frameon=False,ncol=2,fontsize=8);ax.grid(axis='y',alpha=.18)
    fig.tight_layout();fig.savefig(reports/'youth_unemployment.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    sel=d[d.indicator_code=='IT.NET.USER.ZS']
    for country,g in sel.groupby('country'):
        ax.plot(g.year,g.value,label=country,linewidth=2)
    ax.set_title('Internet use — country comparison',loc='left',fontweight='bold')
    ax.set_ylabel('Percent of total population');ax.set_xlabel('Year')
    ax.legend(frameon=False,ncol=2,fontsize=8);ax.grid(axis='y',alpha=.18)
    fig.tight_layout();fig.savefig(reports/'internet_access.png',dpi=170);plt.close(fig)
    print('Opportunity monitor:',kpis)
    return kpis


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    selector=parser.add_mutually_exclusive_group()
    selector.add_argument('--real',action='store_true',help='Fetch the actual World Bank API (requires internet)')
    selector.add_argument('--input',type=Path,help='Load previously downloaded long-form indicator CSV')
    selector.add_argument('--demo',action='store_true',help='Use visibly fictional data (default)')
    args=parser.parse_args()
    if args.real:
        raw=fetch_worldbank();mode='REAL — World Bank Indicators API'
        raw.to_csv(ROOT/'data'/'world_bank_real.csv',index=False)
    elif args.input:
        raw=pd.read_csv(args.input);mode='USER-SUPPLIED INDICATOR DATA'
    else:
        raw=generate_demo();mode='SYNTHETIC DEMO — NOT WORLD BANK STATISTICS'
        raw.to_csv(ROOT/'data'/'demo_indicators.csv',index=False)
    make_outputs(raw,ROOT/'outputs',ROOT/'reports',mode)

if __name__=='__main__':main()
