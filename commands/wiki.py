import subprocess as sp

def execute(arg = ''):
    if arg == '':
      return ''
    p = sp.Popen("dig +short txt \""+arg+".wp.dg.cx\"", stdout = sp.PIPE, stderr = sp.PIPE, shell = True)
    out, err = p.communicate()
    if len(out) == 0:
        return err
    return out
