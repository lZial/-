import py_compile,re,sys
sys.stdout.reconfigure(encoding='utf-8')
def repair(path):
 for _ in range(40):
  try: py_compile.compile(path,doraise=True); print('OK',path); return
  except Exception as e:
   msg=str(e); m=re.search(r'line (\d+)',msg)
   if not m: print(msg); return
   ln=int(m.group(1)); lines=open(path,encoding='utf-8').readlines()
   old=lines[ln-1]; new=old
   if 'or ")' in old and 'unterminated' in msg: new=old.replace('or ")','or "")')
   elif old.count('"')%2==1 and 'unterminated' in msg:
     s=old.rstrip('\r\n'); eol='\r\n' if old.endswith('\r\n') else '\n'
     if re.search(r'"\)\s*[:\),]?\s*$',s): new=s[:-len(s.lstrip()[:-1][s.lstrip()[:-1].rfind('"'):])+0] # skip
     # insert " before final )
     idx=s.rfind(')')
     if idx>0 and s.count('"')%2==1: new=s[:idx]+'"' +s[idx:]+eol
     else: new=s+'"'+eol
   elif 'invalid syntax' in msg and '""' in old and old.lstrip().startswith('""'):
     new=old.replace('""','"""',1)
   elif 'invalid syntax' in msg and ('[", "' in old or '", ,"' in old or '", "' in old):
     new=old.replace('[", "','["", "').replace('", , "', '", "", "').replace('", ,"', '", "",')
   if new==old:
     print('STOP',path,ln,repr(old),msg.splitlines()[-1][:120]); return
   print('fix',ln); lines[ln-1]=new; open(path,'w',encoding='utf-8').writelines(lines)
for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
 for fn in ('make_report2.py','make_report2_part2.py'): repair(__import__('os').path.join(root,fn))
