import requests
import os
from pathlib import Path

def get_ngrok_url():
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except:
        pass
    return None

def save_ngrok_url(url):
    env_file = Path(__file__).parent / '.env'
    
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    found = False
    for i, line in enumerate(lines):
        if line.startswith('NGROK_URL='):
            lines[i] = f'NGROK_URL={url}\n'
            found = True
            break
    
    if not found:
        lines.append(f'NGROK_URL={url}\n')
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def update_ngrok_url():
    url = get_ngrok_url()
    if url:
        save_ngrok_url(url)
        print(f"NGROK URL: {url}")
    else:
        print("NGROK not running")

if __name__ == "__main__":
    update_ngrok_url()
