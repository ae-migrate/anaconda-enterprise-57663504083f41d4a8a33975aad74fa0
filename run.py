import subprocess, os
from tabulate import tabulate
print('--------')
data = []
for x in subprocess.check_output(['env']).decode().splitlines():
    if '=' not in x:
        continue
    key, value = x.strip().split('=', 1)
    if key.startswith('ANACONDA_') and not key.startswith('ANACONDA_PROJECT_') or key.startswith('KUBERNETES_'):
        continue
    data.append((key, value))
for x in tabulate(sorted(data), tablefmt='plain').splitlines():
    if not x.startswith('-'):
        print(x)
print('--------')
for x in subprocess.check_output(['conda', 'info']).decode().splitlines():
    if x.strip():
        print(x)
print('--------')
for x in subprocess.check_output(['conda', 'env', 'list']).decode().splitlines():
    if x.strip():
        print(x)
print('--------')
data = []
for x in subprocess.check_output(['mount']).decode().splitlines():
    if ' on ' in x:
        dev, _, mount, _, type, flags = x.split()
        if type in ('nfs', 'nfs3', 'nfs4', 'ext4', 'xfs'):
            data.append((mount, 'rw' if 'rw' in flags else 'ro', '' if dev == '/dev/vda1' else dev))
for x in tabulate(sorted(data), tablefmt='plain').splitlines():
    if not x.startswith('-'):
        print(x)
print('--------')
if os.path.isdir('/opt/continuum/.persistence'):
    project_id = os.readlink('/opt/continuum/.conda/envs').rsplit('/', 2)[-2]
else:
    project_id = '@@@'
for dname in ('.persistence', '.persistence/' + project_id, '.conda',
              'data', 'user', 'user/home', 'project'):
    dpath = os.path.join('/opt/continuum', dname)
    if os.path.isdir(dpath):
        os.chdir(dpath)
        print(dpath)
        for x in subprocess.check_output(['ls', '-Al']).decode().splitlines():
            if x.strip():
                print(x)
print('--------')
