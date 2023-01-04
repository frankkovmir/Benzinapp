import sys
import subprocess

def installation():
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'Pillow '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'numpy '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'pygame'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'geocoder'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'geopy'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'requests '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'fpdf2 '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'pandas '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'dash '])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'dash-bootstrap-components '])
    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip',
    'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    print(installed_packages)
