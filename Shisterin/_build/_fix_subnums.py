import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
def fix(path):
    s=open(path,encoding='utf-8').read()
    # find all headings in order and renumber X.Y sequentially within same X
    heads=list(re.finditer(r'heading\(doc, "([^"]+)", (\d)\)', s))
    out=[]; last=0
    cur_top=None; sub=0
    for m in heads:
        out.append(s[last:m.start()])
        text=m.group(1); lvl=m.group(2)
        mtop=re.match(r'(\d+)\s', text)
        msub=re.match(r'(\d+)\.(\d+)\s+(.*)', text)
        if msub and lvl=='2':
            top=int(msub.group(1)); sub+=1 if top==cur_top else 1
            if top!=cur_top: cur_top=top; sub=1
            text=f"{top}.{sub} {msub.group(3)}"
        elif mtop and lvl=='1':
            cur_top=int(mtop.group(1)); sub=0
        out.append(f'heading(doc, "{text}", {lvl})')
        last=m.end()
    out.append(s[last:])
    ns=''.join(out)
    if ns!=s:
        open(path,'w',encoding='utf-8').write(ns); print('fixed',path)
    else: print('no',path)
for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    for fn in ('make_report2.py','make_report2_part2.py'):
        fix(os.path.join(root,fn))
