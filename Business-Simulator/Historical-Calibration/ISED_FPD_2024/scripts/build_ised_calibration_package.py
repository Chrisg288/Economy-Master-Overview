from pathlib import Path
from collections import Counter, defaultdict
import csv, json, hashlib, re, shutil, zipfile

SRC_ZIP=Path('/mnt/data/ISED_Financial_Performance_Data_2024_Raw_CSV.zip.zip')
WORK=Path('/mnt/data/ised_fpd_processing')
PKG=Path('/mnt/data/ISED_FPD_2024_Small_Business_Calibration_GitHub_Import_v0_1')
ROOT=PKG/'Business-Simulator'/'Historical-Calibration'/'ISED_FPD_2024'
OUTZIP=Path('/mnt/data/ISED_FPD_2024_Small_Business_Calibration_GitHub_Import_v0_1.zip')

PRIORITY=[
('food_truck','722330','Food truck / mobile food service'),
('full_service_restaurant','722511','Full-service restaurant'),
('limited_service_restaurant','722512','Limited-service restaurant / fast food'),
('auto_repair_shop','811111','General automotive repair shop'),
('tire_shop','441340','Tire dealer / tire shop'),
('hair_salon','812116','Unisex hair salon'),
('beauty_salon','812115','Beauty salon'),
('small_motel','721114','Motel'),
('janitorial_cleaning_company','561722','Janitorial service company'),
('security_systems_installer','561621','Security systems service / installer'),
('pet_grooming_care','812910','Pet care / grooming service'),
('tax_preparation_service','541213','Tax preparation service'),
('bookkeeping_payroll_service','541215','Bookkeeping and payroll service'),
('cabinet_shop','337110','Wood kitchen cabinet and countertop manufacturer'),
('landscaping_company','561730','Landscaping service company'),
('software_publisher','513211','Software publisher (except video games)'),
('computer_systems_design','541514','Computer systems design service')]
PCODES={x[1] for x in PRIORITY}
INC={'1':('Unincorporated businesses','T1'),'2':('Incorporated businesses','T2'),'3':('All businesses','T1 + T2')}
GEO={'00':'Canada','0':'Canada','10':'Newfoundland and Labrador','11':'Prince Edward Island','12':'Nova Scotia','13':'New Brunswick','15':'Atlantic region','24':'Quebec','35':'Ontario','46':'Manitoba','47':'Saskatchewan','48':'Alberta','49':'Prairies region','59':'British Columbia','60':'Yukon','61':'Northwest Territories','62':'Nunavut','63':'Territories region'}
QUAL={'A':'Excellent','B':'Very good','C':'Good','D':'Acceptable','E':'Use with caution'}
SENT={9999.0,9999.9,99999.9,999999.0}
EXP=['cost_of_sales','wages_and_benefits','purchases_materials_subcontracts','opening_inventory','closing_inventory','operating_expenses_indirect','labour_and_commissions','amortization_and_depletion','repairs_and_maintenance','utilities_and_telecommunications','rent','interest_and_bank_charges','professional_and_business_fees','advertising_and_promotion','delivery_shipping_and_warehouse','insurance','other_expenses','total_expenses','net_profit_loss']
BAL=['total_assets','total_current_assets','accounts_receivable','closing_inventory','other_current_assets','net_tangible_and_intangible_assets','all_other_assets_and_adjustments','total_liabilities','total_current_liabilities','current_bank_loans','other_current_liabilities','long_term_liabilities','total_equity']
RAT=[('current_ratio','ratio'),('debt_to_equity_ratio','ratio'),('interest_coverage_ratio','ratio'),('debt_ratio','ratio'),('revenue_to_equity_ratio','ratio'),('revenue_to_closing_inventory_ratio','ratio'),('current_debt_to_equity','percent'),('net_profit_to_equity','percent'),('net_fixed_assets_to_equity','percent'),('gross_margin','percent'),('return_on_total_assets','percent'),('collection_period_accounts_receivable','days')]
PROF=['profitable_total_revenue','profitable_total_expenses','profitable_net_profit','non_profitable_total_revenue','non_profitable_total_expenses','non_profitable_net_loss']

def hsh(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def num(v,integer=False):
 if v is None:return None
 s=v.strip().replace(',','')
 if not s or s.lower() in {'x','n/a','na','..','...','-'}:return None
 try:x=float(s)
 except:return None
 if x in SENT:return None
 return int(x) if integer and x.is_integer() else x

def suppressed(row):
 return len(row)>3 and (row[3].strip()=='999999' or sum(v.strip() in {'9999','9999.9','99999.9','999999'} for v in row)>=3)

def filemeta(name):
 n=name.lower()
 if n=='naics_descriptors_2024.csv':return ('naics','na','na')
 dist='profit_margin' if n.startswith('profit_margin_') else 'total_revenue'
 band='5m_20m' if '5m_20m' in n else '30k_5m'
 if 'financial_ratios_canada_incorporated' in n:typ='ratios_limited'
 elif 'profit_non_profit_businesses' in n:typ='profitability'
 elif 'total_expenses_percentage' in n:typ='expenses_pct'
 elif 'total_expenses_value' in n:typ='expenses_value'
 elif 'total_revenue' in n:typ='revenue'
 elif 'balance_sheet' in n:typ='balance'
 elif 'financial_ratios' in n:typ='ratios'
 else:return None
 return typ,dist,band

def rows(path):
 anomalies=[]
 with path.open('r',encoding='cp1252',newline='') as f:
  r=csv.reader(f); header=next(r); pending=None
  for ln,row in enumerate(r,2):
   if not row or all(not c.strip() for c in row):anomalies.append((ln,'blank'));continue
   if len(row)==1 and row[0].strip() in INC:pending=row[0].strip();anomalies.append((ln,'split_prefix'));continue
   if pending and len(row)==len(header) and not row[0].strip():row[0]=pending;pending=None;anomalies.append((ln,'split_repaired'))
   if len(row)!=len(header):
    anomalies.append((ln,f'columns_{len(row)}_expected_{len(header)}'))
    row=(row+['']*len(header))[:len(header)]
   yield header,row,anomalies

def block(row,whole,q,quart,unit,report=None):
 d={'unit':unit,'whole_industry':num(row[whole]),'bottom_quartile':num(row[quart]),'lower_middle':num(row[quart+1]),'upper_middle':num(row[quart+2]),'top_quartile':num(row[quart+3])}
 if q is not None:
  code=row[q].strip() or None;d['quality_code']=code;d['quality_label']=QUAL.get(code)
 if report is not None:d['businesses_reporting_percent']=num(row[report])
 return d

def parse(typ,dist,row):
 if typ=='revenue':
  return {'year':num(row[34],True),'number_of_businesses':num(row[3],True),'distribution_boundaries':{'unit':'thousands_cad' if dist=='total_revenue' else 'profit_margin_ratio','whole_industry':{'low':num(row[4]),'high':num(row[5])},'bottom_quartile':{'low':num(row[6]),'high':num(row[7])},'lower_middle':{'low':num(row[8]),'high':num(row[9])},'upper_middle':{'low':num(row[10]),'high':num(row[11])},'top_quartile':{'low':num(row[12]),'high':num(row[13])}},'total_revenue':block(row,14,15,16,'thousands_cad'),'sales_of_goods_and_services':block(row,20,21,22,'thousands_cad',32),'all_other_revenue':block(row,26,27,28,'thousands_cad',33)}
 if typ in {'expenses_pct','expenses_value'}:
  unit='percent_of_total_revenue' if typ=='expenses_pct' else 'thousands_cad';m={}
  for i,n in enumerate(EXP):
   b=3+i*7;m[n]=block(row,b,b+1,b+2,unit,b+6)
  return {'year':num(row[-1],True),'metrics':m}
 if typ=='balance':
  m={}
  for i,n in enumerate(BAL):
   b=3+i*6;m[n]=block(row,b,b+1,b+2,'thousands_cad')
  return {'year':num(row[-1],True),'metrics':m}
 if typ=='ratios':
  m={}
  for i,(n,u) in enumerate(RAT):
   b=3+i*5;m[n]=block(row,b,None,b+1,u)
  return {'year':num(row[-1],True),'metrics':m}
 if typ=='ratios_limited':
  return {'year':num(row[3],True),'metrics':{'interest_coverage_ratio':block(row,4,None,5,'ratio'),'gross_margin':block(row,9,None,10,'percent')},'source_layout_correction':'Year is actual column 4'}
 if typ=='profitability':
  m={}
  for n,b in zip(PROF,[4,10,16,22,28,34]):m[n]=block(row,b,b+1,b+2,'thousands_cad')
  return {'year':num(row[40],True),'profitable_businesses_percent':num(row[3]),'metrics':m}

def get(ctx,*keys):
 v=ctx
 for k in keys:
  if not isinstance(v,dict):return None
  v=v.get(k)
 return v

def summary(ctx):
 return {'profile_id':ctx['profile_id'],'business_type_id':ctx['business_type_id'],'business_label':ctx['business_label'],'naics_code':ctx['naics_code'],'naics_title':ctx['naics_title'],'geography_code':ctx['geography']['code'],'geography':ctx['geography']['label'],'incorporation_status_code':ctx['incorporation_status']['code'],'incorporation_status':ctx['incorporation_status']['label'],'revenue_band':ctx['revenue_band'],'distribution':ctx['distribution'],'year':ctx['year'],'data_suppressed':ctx['data_suppressed'],'partial_suppression':ctx['partial_suppression'],'business_count':get(ctx,'revenue','number_of_businesses'),'average_revenue_kcad':get(ctx,'revenue','total_revenue','whole_industry'),'average_total_expenses_kcad':get(ctx,'expenses_value','metrics','total_expenses','whole_industry'),'average_net_profit_loss_kcad':get(ctx,'expenses_value','metrics','net_profit_loss','whole_industry'),'net_profit_loss_percent':get(ctx,'expenses_percentage','metrics','net_profit_loss','whole_industry'),'cost_of_sales_percent':get(ctx,'expenses_percentage','metrics','cost_of_sales','whole_industry'),'wages_benefits_percent':get(ctx,'expenses_percentage','metrics','wages_and_benefits','whole_industry'),'labour_commissions_percent':get(ctx,'expenses_percentage','metrics','labour_and_commissions','whole_industry'),'materials_subcontracts_percent':get(ctx,'expenses_percentage','metrics','purchases_materials_subcontracts','whole_industry'),'rent_percent':get(ctx,'expenses_percentage','metrics','rent','whole_industry'),'advertising_percent':get(ctx,'expenses_percentage','metrics','advertising_and_promotion','whole_industry'),'insurance_percent':get(ctx,'expenses_percentage','metrics','insurance','whole_industry'),'profitable_businesses_percent':get(ctx,'profitability','profitable_businesses_percent'),'current_ratio':get(ctx,'financial_ratios','metrics','current_ratio','whole_industry'),'debt_to_equity_ratio':get(ctx,'financial_ratios','metrics','debt_to_equity_ratio','whole_industry'),'gross_margin_percent':get(ctx,'financial_ratios','metrics','gross_margin','whole_industry'),'return_on_assets_percent':get(ctx,'financial_ratios','metrics','return_on_total_assets','whole_industry'),'total_assets_kcad':get(ctx,'balance_sheet','metrics','total_assets','whole_industry'),'total_liabilities_kcad':get(ctx,'balance_sheet','metrics','total_liabilities','whole_industry'),'total_equity_kcad':get(ctx,'balance_sheet','metrics','total_equity','whole_industry'),'revenue_quality_code':get(ctx,'revenue','total_revenue','quality_code'),'total_expenses_quality_code':get(ctx,'expenses_value','metrics','total_expenses','quality_code')}

def main():
 if WORK.exists():shutil.rmtree(WORK)
 WORK.mkdir();
 with zipfile.ZipFile(SRC_ZIP) as z:z.extractall(WORK)
 data=next(WORK.rglob('ised_fpd_2024'))
 if PKG.exists():shutil.rmtree(PKG)
 for s in ['raw','catalog','lookups','profiles/priority_businesses','summaries','scripts','schemas','docs','validation']:(ROOT/s).mkdir(parents=True,exist_ok=True)
 shutil.copy2(SRC_ZIP,ROOT/'raw'/'ISED_Financial_Performance_Data_2024_Raw_CSV.zip')
 # descriptors
 desc={};drecs=[]
 with (data/'naics_descriptors_2024.csv').open('r',encoding='cp1252',newline='') as f:
  for r in csv.DictReader(f):
   if r['Year\nAnnée'].strip()=='2024':
    c=r['Naics code\nCode Scian'].strip();x={'naics_code':c,'description_en':r['Description_English'].strip(),'description_fr':r['Description_French'].strip(),'year':2024};desc[c]=x;drecs.append(x)
 drecs.sort(key=lambda x:(len(x['naics_code']),x['naics_code']))
 for ext in ['json']:(ROOT/'lookups'/f'naics_2024.{ext}').write_text(json.dumps({'count':len(drecs),'records':drecs},indent=2,ensure_ascii=False),encoding='utf-8')
 with (ROOT/'lookups'/'naics_2024.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=drecs[0].keys());w.writeheader();w.writerows(drecs)
 for name,recs in [('incorporation_statuses',[{'code':k,'label':v[0],'tax_source':v[1]} for k,v in INC.items()]),('geographies',[{'code':k,'label':v} for k,v in GEO.items() if k!='0']),('quality_indicators',[{'code':k,'label':v} for k,v in QUAL.items()])]:
  (ROOT/'lookups'/f'{name}.json').write_text(json.dumps({'records':recs},indent=2),encoding='utf-8')
  with (ROOT/'lookups'/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=recs[0].keys());w.writeheader();w.writerows(recs)
 selected=defaultdict(dict);catalog=[];fields=[];validation={'files':{},'repairs':[]}
 for p in sorted(data.glob('*.csv')):
  meta=filemeta(p.name)
  if not meta:continue
  typ,dist,band=meta
  if typ=='naics':
   catalog.append({'filename':p.name,'dataset_type':'naics','distribution':'na','revenue_band':'na','rows':22333,'columns':4,'bytes':p.stat().st_size,'sha256':hsh(p),'statuses':'','geographies':'','unique_naics':len(drecs),'sentinel_rows':0});continue
  rc=0;sent=0;sts=Counter();ges=Counter();nset=set();head=None;anref=[]
  for h,r,an in rows(p):
   head=head or h;anref=an;rc+=1
   st,na,ge=r[0].strip(),r[1].strip(),r[2].strip();ge='00' if band=='5m_20m' and ge=='0' else ge
   sts[st]+=1;ges[ge]+=1;nset.add(na);sent+=1 if suppressed(r) else 0
   if na in PCODES and ge in {'00','48'}:selected[(band,dist,typ)][(st,na,ge)]=r
  validation['files'][p.name]={'rows_loaded':rc,'sentinel_rows':sent,'anomalies':anref[:100]}
  for a in anref:
   if a[1] in {'blank','split_repaired'}:validation['repairs'].append({'file':p.name,'line':a[0],'repair':a[1]})
  catalog.append({'filename':p.name,'dataset_type':typ,'distribution':dist,'revenue_band':band,'rows':rc,'columns':len(head),'bytes':p.stat().st_size,'sha256':hsh(p),'statuses':'|'.join(sorted(sts)),'geographies':'|'.join(sorted(ges)),'unique_naics':len(nset),'sentinel_rows':sent})
  seen=Counter()
  for i,h in enumerate(head):
   base=re.sub(r'[^a-z0-9]+','_',h.split('/')[0].replace('\n',' ').lower()).strip('_') or 'field';seen[base]+=1;can=base if seen[base]==1 else f'{base}_{seen[base]}'
   fields.append({'filename':p.name,'column_index':i,'original_header':h.replace('\n',' / '),'canonical_header':can,'dataset_type':typ,'distribution':dist,'revenue_band':band})
 # write catalog
 (ROOT/'catalog'/'dataset_catalog.json').write_text(json.dumps({'files':catalog},indent=2),encoding='utf-8')
 allkeys=[]
 for x in catalog:
  for k in x:
   if k not in allkeys:allkeys.append(k)
 with (ROOT/'catalog'/'dataset_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=allkeys,extrasaction='ignore');w.writeheader();w.writerows(catalog)
 (ROOT/'catalog'/'field_catalog.json').write_text(json.dumps({'fields':fields},indent=2,ensure_ascii=False),encoding='utf-8')
 with (ROOT/'catalog'/'field_catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields[0].keys());w.writeheader();w.writerows(fields)
 contexts=[];sums=[];idx=[]
 source_by_sig={filemeta(p.name):p.name for p in data.glob('*.csv') if filemeta(p.name)}
 for bid,code,label in PRIORITY:
  bp={'business_type_id':bid,'business_label':label,'naics_code':code,'naics_title':desc.get(code,{}).get('description_en',label),'year':2024,'contexts':[]}
  req=[('30k_5m',d,s,g) for g in ['00','48'] for s in ['1','2','3'] for d in ['total_revenue','profit_margin']]+[('5m_20m',d,'2','00') for d in ['total_revenue','profit_margin']]
  for band,dist,st,ge in req:
   ctx={'profile_id':f'ISED_2024_{bid}_{ge}_{st}_{band}_{dist}','business_type_id':bid,'business_label':label,'naics_code':code,'naics_title':bp['naics_title'],'geography':{'code':ge,'label':GEO.get(ge,ge)},'incorporation_status':{'code':st,'label':INC[st][0],'tax_source':INC[st][1]},'revenue_band':band,'distribution':dist,'year':2024,'data_suppressed':False,'partial_suppression':False,'suppressed_sections':[],'source_files':[]}
   found=False
   for typ,sec in [('revenue','revenue'),('expenses_pct','expenses_percentage'),('expenses_value','expenses_value'),('balance','balance_sheet'),('ratios','financial_ratios'),('ratios_limited','financial_ratios'),('profitability','profitability')]:
    r=selected.get((band,dist,typ),{}).get((st,code,ge))
    if r is None:continue
    found=True
    if suppressed(r):ctx['partial_suppression']=True;ctx['suppressed_sections'].append(typ)
    val=parse(typ,dist,r)
    if sec=='financial_ratios' and sec in ctx:
     ctx[sec].setdefault('metrics',{}).update(val.get('metrics',{}))
    else:ctx[sec]=val
    src=source_by_sig.get((typ,dist,band));
    if src:ctx['source_files'].append(src)
   if found:
    rev=ctx.get('revenue',{});ctx['year']=rev.get('year') or 2024;ctx['data_suppressed']=rev.get('number_of_businesses') is None or (rev.get('total_revenue') or {}).get('whole_industry') is None
    bp['contexts'].append(ctx);contexts.append(ctx);sums.append(summary(ctx));idx.append({'profile_id':ctx['profile_id'],'business_type_id':bid,'naics_code':code,'geography_code':ge,'incorporation_status_code':st,'revenue_band':band,'distribution':dist,'data_suppressed':ctx['data_suppressed'],'partial_suppression':ctx['partial_suppression']})
  (ROOT/'profiles'/'priority_businesses'/f'{bid}.json').write_text(json.dumps(bp,indent=2,ensure_ascii=False),encoding='utf-8')
 (ROOT/'profiles'/'priority_business_profiles_all.json').write_text(json.dumps({'business_count':len(PRIORITY),'context_count':len(contexts),'contexts':contexts},indent=2,ensure_ascii=False),encoding='utf-8')
 for name,recs in [('available_contexts_index',idx)]:
  (ROOT/'profiles'/f'{name}.json').write_text(json.dumps({'records':recs},indent=2),encoding='utf-8')
  with (ROOT/'profiles'/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=recs[0].keys());w.writeheader();w.writerows(recs)
 with (ROOT/'summaries'/'priority_business_calibration_summary.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=sums[0].keys());w.writeheader();w.writerows(sums)
 (ROOT/'summaries'/'priority_business_calibration_summary.json').write_text(json.dumps({'records':sums},indent=2,ensure_ascii=False),encoding='utf-8')
 focus=[r for r in sums if r['revenue_band']=='30k_5m' and r['distribution']=='total_revenue' and r['incorporation_status_code']=='3' and r['geography_code'] in {'00','48'}]
 with (ROOT/'summaries'/'priority_business_canada_alberta_all_businesses.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=sums[0].keys());w.writeheader();w.writerows(focus)
 validation['summary']={'raw_csv_files':24,'naics_2024_count':len(drecs),'priority_business_types':len(PRIORITY),'contexts':len(contexts),'fully_suppressed_contexts':sum(c['data_suppressed'] for c in contexts),'partially_suppressed_contexts':sum(c['partial_suppression'] for c in contexts),'raw_archive_sha256':hsh(SRC_ZIP)}
 (ROOT/'validation'/'validation_report.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
 # docs
 (ROOT/'README.md').write_text(f'''# ISED Financial Performance Data 2024 — Small Business Calibration v0.1\n\nGitHub-ready calibration library built from the uploaded 24 official CSV files.\n\n- 2024 NAICS descriptions: **{len(drecs):,}**\n- Priority business types: **{len(PRIORITY)}**\n- Parsed benchmark contexts: **{len(contexts)}**\n- Fully suppressed contexts: **{sum(c['data_suppressed'] for c in contexts)}**\n- Partially suppressed contexts: **{sum(c['partial_suppression'] for c in contexts)}**\n\nInstall by merging the included `Business-Simulator` folder into the Economy-Master-Overview repository.\n\nValues in revenue, expense-value and balance-sheet sections are thousands of Canadian dollars. Expense percentage files are percentages of total revenue.\n''',encoding='utf-8')
 (ROOT/'docs'/'DATA_DICTIONARY.md').write_text('''# Data Dictionary\n\nIncorporation codes: `1` unincorporated/T1, `2` incorporated/T2, `3` all/T1+T2. Alberta is geography `48`; Canada is `00` (`0` in the $5M–$20M raw files). Quality: A excellent, B very good, C good, D acceptable, E use with caution. Numeric sentinels `9999`, `9999.9`, `99999.9`, and `999999` are converted to null in parsed profiles.\n''',encoding='utf-8')
 (ROOT/'docs'/'SIMULATOR_CALIBRATION_GUIDE.md').write_text('''# Simulator Calibration Guide\n\nSelect a business type, geography, incorporation status and revenue band. Match the simulated annual revenue to the appropriate quartile, then compare revenue, expense structure, net margin, balance sheet and ratios. Store calibration error and evidence strength. These are industry averages, not mandatory targets.\n''',encoding='utf-8')
 (ROOT/'docs'/'SOURCE_AND_METHODS.md').write_text('''# Source and Methods\n\nOfficial source: ISED / Statistics Canada Financial Performance Data 2024. The target population includes businesses earning $30,000–$5 million and $5 million–$20 million. Data are administrative T1/T2 tax records published as industry/geography aggregates.\n\nSources:\n- https://ised-isde.canada.ca/site/financial-performance-data/en\n- https://ised-isde.canada.ca/site/financial-performance-data/en/glossary\n- https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&SDDS=5028\n''',encoding='utf-8')
 # scripts and schema
 shutil.copy2(Path(__file__),ROOT/'scripts'/'build_ised_calibration_package.py')
 (ROOT/'scripts'/'query_priority_profile.py').write_text("""from pathlib import Path\nimport json,argparse\np=argparse.ArgumentParser();p.add_argument('business_type_id');p.add_argument('--geography',default='48');p.add_argument('--status',default='3');p.add_argument('--band',default='30k_5m');p.add_argument('--distribution',default='total_revenue');a=p.parse_args();root=Path(__file__).resolve().parents[1];d=json.loads((root/'profiles'/'priority_businesses'/f'{a.business_type_id}.json').read_text());print(json.dumps(next(c for c in d['contexts'] if c['geography']['code']==a.geography and c['incorporation_status']['code']==a.status and c['revenue_band']==a.band and c['distribution']==a.distribution),indent=2))\n""",encoding='utf-8')
 (ROOT/'schemas'/'ISED_FPD_BenchmarkContext.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema','title':'ISED FPD Benchmark Context','type':'object','required':['profile_id','business_type_id','naics_code','geography','incorporation_status','revenue_band','distribution']},indent=2),encoding='utf-8')
 PKG.mkdir(exist_ok=True);(PKG/'README.md').write_text('Merge the included `Business-Simulator` folder into the root of the Economy-Master-Overview repository.\n',encoding='utf-8')
 if OUTZIP.exists():OUTZIP.unlink()
 with zipfile.ZipFile(OUTZIP,'w',allowZip64=True) as z:
  for p in PKG.rglob('*'):
   if p.is_file():z.write(p,p.relative_to(PKG),compress_type=zipfile.ZIP_STORED if p.suffix=='.zip' else zipfile.ZIP_DEFLATED)
 print(json.dumps({'output':str(OUTZIP),'size_mb':round(OUTZIP.stat().st_size/1024/1024,2),'contexts':len(contexts),'fully_suppressed':sum(c['data_suppressed'] for c in contexts),'partially_suppressed':sum(c['partial_suppression'] for c in contexts)},indent=2))
if __name__=='__main__':main()
