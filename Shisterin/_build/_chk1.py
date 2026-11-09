import sys,re
sys.stdout.reconfigure(encoding='utf-8')
for path in [r'D:\UP_MobileBank\_build\make_report.py', r'D:\UP_NeuralDefects\_build\make_report.py']:
 s=open(path,encoding='utf-8').read()
 name='SH' if 'MobileBank' in path else 'MA'
 for pat in [r'MS Project',r'2026',r'БСЗР\s*=\s*[\d ]+,\d+',r'01\.04\.2025']:
  ms=re.findall('.{0,25}'+pat+'.{0,45}',s)
  if ms and (pat!='01\.04\.2025' or len(ms)<3): print(name,pat,len(ms),ms[0][:80].replace('\n',' '))
 print('---')
