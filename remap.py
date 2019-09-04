import os, json, urllib.request

def main():
    version = get_version()
    get_mappings(version)

def get_version():
    with open('version.config') as f:
        config = f.readlines()[0]
        return config.split('=')[-1].strip()

def get_mappings(version):
    jdir = os.getenv('APPDATA') + f'\\.minecraft\\versions\\{version}\\{version}.json'
    with open(jdir) as f:
        jfile = json.load(f)
        url = jfile['downloads']['client_mappings']['url']
        
        print(f'Downloading the mappings for {version}...')
        download_file(url, 'mappings/client.txt')
        print('Done!')

def download_file(url, out):
    urllib.request.urlretrieve(url, out)






if __name__ == "__main__": main()