import os, json

def main():
    version = get_version()
    get_mappings(version)

def get_version():
    with open('version.config') as f:
        config = f.readlines()[0]
        return config.split('=')[-1].strip()

def get_mappings(version):
    json_dir = os.getenv('APPDATA') + f'/.minecraft/versions/{version}/{version}.json'
    jfile = json.load(json_dir)
    print(jfile)

if __name__ == "__main__": main()