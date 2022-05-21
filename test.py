import requests

r = requests.get('https://api.github.com/repos/jellayy/ez.gg/releases/latest')
print(r.json())