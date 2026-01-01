import os, json, sys, urllib.request

# Load .env if present
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k,v=line.split('=',1)
                os.environ.setdefault(k.strip(), v.strip())

AZURE_API_BASE = os.getenv('AZURE_API_BASE')
AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_API_VERSION = os.getenv('AZURE_API_VERSION', '2024-10-01-preview')

if not AZURE_API_BASE or not AZURE_API_KEY:
    print('Missing AZURE_API_BASE or AZURE_API_KEY')
    sys.exit(2)

url = AZURE_API_BASE.rstrip('/') + f'/openai/deployments?api-version={AZURE_API_VERSION}'
req = urllib.request.Request(url)
req.add_header('api-key', AZURE_API_KEY)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode('utf-8')
        print('HTTP', resp.getcode())
        print(body[:2000])
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('ERROR', e)
