"""Prepara y perfila archivos SNIES sin modificar los archivos originales.
Dependencias: Python estándar; matplotlib solamente para figura opcional.
"""
import csv, json, re, zipfile, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from lxml import etree as ET
ROOT=Path(__file__).resolve().parents[1]
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
COLS={'institucion':'INSTITUCIÓN DE EDUCACIÓN SUPERIOR (IES)','sector':'SECTOR IES','caracter':'CARACTER IES','programa':'PROGRAMA ACADÉMICO','nivel':'NIVEL DE FORMACIÓN','area':'ÁREA DE CONOCIMIENTO','cine':'CINE CAMPO AMPLIO','departamento':'DEPARTAMENTO DE OFERTA DEL PROGRAMA','sexo':'SEXO','ano':'AÑO','semestre':'SEMESTRE','graduados':'GRADUADOS','codigo_programa':'CÓDIGO SNIES DEL PROGRAMA','codigo_ies':'CÓDIGO DE LA INSTITUCIÓN'}
FIELDS=['ano','semestre','codigo_ies','institucion','sector','caracter','codigo_programa','programa','nivel','area','cine','departamento','sexo','graduados']
GROUP=[x for x in FIELDS if x not in ('sexo','graduados')]
def norm(s):
 s=unicodedata.normalize('NFKD',str(s or ''));s=''.join(c for c in s if not unicodedata.combining(c))
 return ' '.join(s.upper().replace('\t',' ').split())
def read_rows(path):
 with zipfile.ZipFile(path) as z:
  ss=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   with z.open('xl/sharedStrings.xml') as f:
    for _,e in ET.iterparse(f,events=('end',)):
     if e.tag==NS+'si':ss.append(''.join(t.text or '' for t in e.iter(NS+'t')));e.clear()
  sheets=[s for s in z.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',s)]
  sheet=max(sheets,key=lambda n:int(re.search(r'sheet(\d+)',n).group(1)))
  with z.open(sheet) as f:
   for _,e in ET.iterparse(f,events=('end',)):
    if e.tag!=NS+'row':continue
    out={}
    for c in e.findall(NS+'c'):
     v=c.find(NS+'v');i=c.find(NS+'is')
     val=v.text if v is not None else ''.join(t.text or '' for t in i.iter(NS+'t')) if i is not None else ''
     if c.get('t')=='s' and val is not None:val=ss[int(val)]
     if val not in (None,''):out[re.match(r'[A-Z]+',c.get('r')).group()]=str(val).strip()
    e.clear()
    if out:yield out

def main():
 target=ROOT/'data/processed';target.mkdir(parents=True,exist_ok=True)
 counter=defaultdict(Counter);dims=defaultdict(lambda:defaultdict(Counter));allgroup=defaultdict(Counter)
 bad=[];headers={};counts={};unknown=Counter()
 with (target/'graduados_normalizados.csv').open('w',newline='',encoding='utf-8-sig') as f:
  writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader()
  for year in range(2020,2026):
   names=None;mapping=None;counts[year]=0
   for r in read_rows(ROOT/f'data/raw/{year}.xlsx'):
    if names is None and 'GRADUADOS' in [norm(v) for v in r.values()]:
     names={norm(v):k for k,v in r.items()}
     mapping={key:names.get(norm(alias)) for key,alias in COLS.items()}
     # Common variation: CHARACTER accents, DESC CINE CAMPO AMPLIO
     for key,aliases in {'caracter':['CARÁCTER IES'],'cine':['DESC CINE CAMPO AMPLIO']}.items():
      if not mapping[key]:
       for a in aliases:
        if names.get(norm(a)):mapping[key]=names[norm(a)];break
     headers[year]={'missing':[k for k,v in mapping.items() if not v],'columns':len(names)}
     continue
    if mapping is None:continue
    d={k:r.get(mapping[k],'') if mapping[k] else '' for k in COLS}
    if not d['ano'] or not d['graduados']:continue
    try:num=int(float(d['graduados']))
    except ValueError:bad.append([year,d['graduados']]);continue
    if num<0:bad.append([year,d['graduados']]);continue
    sex=norm(d['sexo'])
    sex='Mujer' if sex in ('MUJER','FEMENINO','FEMENINA') else 'Hombre' if sex in ('HOMBRE','MASCULINO') else 'Otro/no informado'
    d['sexo']=sex;d['graduados']=num;d['ano']=str(year)
    for k in ('sector','caracter','nivel','area','cine','departamento'):d[k]=' '.join(d[k].strip().split())
    d['sector']= 'Oficial' if norm(d['sector'])=='OFICIAL' else 'Privado' if norm(d['sector'])=='PRIVADO' else d['sector']
    writer.writerow(d);counts[year]+=1
    counter[year][sex]+=num
    for k in ('area','nivel','sector','departamento','cine','caracter'):
     dims[k][d[k] or '(Sin dato)'][sex]+=num
    allgroup[tuple(d[k] for k in GROUP)][sex]+=num
 with (target/'modelo_agregado.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(GROUP+['mujeres','hombres','otros','total','participacion_femenina'])
  for grp,c in allgroup.items():
   m=c['Mujer'];h=c['Hombre'];o=c['Otro/no informado'];total=m+h+o
   w.writerow(list(grp)+[m,h,o,total,round(m/total,6) if total else ''])
 summary={'registros_por_ano':counts,'total_registros':sum(counts.values()),'totales_por_ano':{},'variables':headers,'grupos_modelo':len(allgroup),'valores_invalidos':len(bad),'top_dimensiones':{}}
 for year,c in counter.items():
  total=sum(c.values());summary['totales_por_ano'][year]={'mujeres':c['Mujer'],'hombres':c['Hombre'],'otros':c['Otro/no informado'],'total':total,'participacion_femenina_pct':round(100*c['Mujer']/total,2) if total else None}
 for dim,cats in dims.items():
  records=[]
  for cat,c in cats.items():
   t=sum(c.values());records.append({'categoria':cat,'total':t,'mujeres':c['Mujer'],'participacion_femenina_pct':round(100*c['Mujer']/t,2) if t else None})
  summary['top_dimensiones'][dim]=sorted(records,key=lambda d:d['total'],reverse=True)[:15]
 (ROOT/'reports/resumen_eda.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in summary.items() if k!='top_dimensiones'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
