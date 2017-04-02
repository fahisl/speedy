import yaml

config_file = "config.yaml"

try:
    with open(config_file, "r") as f:
        config = yaml.load(f)
        print("Config successfully loaded")

except Exception as e:
    print("Config file could not be opened")
    raise e
