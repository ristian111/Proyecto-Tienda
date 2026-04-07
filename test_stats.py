import urllib.request
import json

# Log in to get token
data = json.dumps({"username": "user1", "password": "password123"}).encode('utf-8')
req = urllib.request.Request('http://localhost:5000/v1/auth/login', data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        token = res.get('token')
        
    req2 = urllib.request.Request('http://localhost:5000/v1/estadisticas/resumen-hoy', headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req2) as resp2:
        print("resumen_hoy:", json.loads(resp2.read().decode()))

    req3 = urllib.request.Request('http://localhost:5000/v1/estadisticas/top-productos?filtro=mensual', headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req3) as resp3:
        print("top_productos:", json.loads(resp3.read().decode()))
except Exception as e:
    print("Error:", e)
