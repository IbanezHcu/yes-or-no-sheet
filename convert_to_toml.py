import json

with open("utility-chimera-462014-j5-697d9dc3758e.json", "r") as f:
    data = json.load(f)

# Escape \n สำหรับ TOML
data["private_key"] = data["private_key"].replace("\n", "\\n")

print("[gsheets]")
for k, v in data.items():
    print(f'{k} = "{v}"')
