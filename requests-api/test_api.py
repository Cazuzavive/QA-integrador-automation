import requests

# Caso 1: Verificación berry/1
url_berry_1 = "https://pokeapi.co/api/v2/berry/1"
response_berry_1 = requests.get(url_berry_1)
berry_1 = response_berry_1.json()

# Verificaciones
assert berry_1['size'] == 20, f"Size expected 20 but got {berry_1['size']}"
assert berry_1['soil_dryness'] == 15, f"Soil dryness expected 15 but got {berry_1['soil_dryness']}"
assert berry_1['firmness']['name'] == "soft", f"Firmness name expected 'soft' but got {berry_1['firmness']['name']}"

print("Caso 1 passed!")

# Caso 2: Verificación berry/2
url_berry_2 = "https://pokeapi.co/api/v2/berry/2"
response_berry_2 = requests.get(url_berry_2)
berry_2 = response_berry_2.json()

# Verificaciones
assert berry_2['firmness']['name'] == "super-hard", f"Firmness name expected 'super-hard' but got {berry_2['firmness']['name']}"
assert berry_2['size'] > berry_1['size'], f"Size expected greater than {berry_1['size']} but got {berry_2['size']}"
assert berry_2['soil_dryness'] == berry_1['soil_dryness'], f"Soil dryness expected {berry_1['soil_dryness']} but got {berry_2['soil_dryness']}"

print("Caso 2 passed!")

# Caso 3: Verificación pikachu
url_pikachu = "https://pokeapi.co/api/v2/pokemon/pikachu/"
response_pikachu = requests.get(url_pikachu)
pikachu = response_pikachu.json()

# Verificaciones
assert 10 < pikachu['base_experience'] < 1000, f"Base experience expected between 10 and 1000 but got {pikachu['base_experience']}"
assert any(t['type']['name'] == 'electric' for t in pikachu['types']), f"Type expected 'electric' but got {[t['type']['name'] for t in pikachu['types']]}"

print("Caso 3 passed!")
