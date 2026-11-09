import sys, re, py_compile, os, traceback
sys.stdout.reconfigure(encoding='utf-8')

def repair(path):
    for _ in range(30):
        try:
            py_compile.compile(path, doraise=True)
            print('OK', path); return True
        except py_compile.PyCompileError as e:
            msg = str(e)
            m = re.search(r'line (\d+)', msg)
            if not m: print(msg); return False
            ln = int(m.group(1))
            lines = open(path,encoding='utf-8').readlines()
            if ln<1 or ln>len(lines): print('bad ln',ln); return False
            old = lines[ln-1]
            new = old
            # common breaks from "" -> "
            if '(", "None")' in old or '(", "None")' in old: new = old.replace('(", "None")','("", "None")')
            if '(u", "None")' in old: new = old.replace('(u", "None")','("", "None")')
            if 'in (", "None")' in old: new = old.replace('in (", "None")','in ("", "None")')
            if new==old and 'unterminated string literal' in msg:
                # try to close string before ) or at line end
                s = old.rstrip('\r\n')
                if s.rstrip().endswith('")') and s.count('"')%2==1: pass
                # para(doc, ")  -> para(doc, "")
                if re.search(r',\s*"\)\s*$', s) and s.count('"')%2==1:
                    new = re.sub(r'("\)\s*)$', r'"\1', s) + ('\r\n' if old.endswith('\r\n') else '\n')
                elif s.count('"')%2==1 and s.rstrip().endswith(')'):
                    new = s[:-1] + '")' + ('\r\n' if old.endswith('\r\n') else '\n')
                elif s.count('"')%2==1:
                    new = s + '"' + ('\r\n' if old.endswith('\r\n') else '\n')
                elif s.count("'")%2==1:
                    new = s + "'" + ('\r\n' if old.endswith('\r\n') else '\n')
            if new==old and 'invalid character' in msg:
                # remove stray en-dash outside quotes? replace with -
                new = old.replace('\u2013','-').replace('\u2014','-')
            if new==old and 'unterminated triple-quoted string literal' in msg:
                # find start
                new = old
            if new==old:
                print('CANNOT FIX', path, ln, msg.splitlines()[-1])
                print(repr(old))
                return False
            print('fix', path, ln, repr(old.strip())[:80], '->', repr(new.strip())[:80])
            lines[ln-1]=new
            open(path,'w',encoding='utf-8').writelines(lines)
    return False

for root in [r'D:\UP_MobileBank\_build', r'D:\UP_NeuralDefects\_build']:
    for fn in ('make_report2.py','make_report2_part2.py'):
        repair(os.path.join(root,fn))
