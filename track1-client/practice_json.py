
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config)
print(config["model"])
print(config["max-tokens"])

json_text = json.dumps(config, indent=4)
print(json_text)

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(config, file, indent=4)

