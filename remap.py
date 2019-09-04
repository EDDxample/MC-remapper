import os, json, urllib.request

def main():
    version = get_version()
    get_mappings(version)
    reformat_mappings()

def get_version():
    with open('version.config') as f:
        config = f.readlines()[0]
        return config.split('=')[-1].strip()

def get_mappings(version):
    jdir = os.getenv('APPDATA') + f'\\.minecraft\\versions\\{version}\\{version}.json'

    if os.path.exists(jdir) and  os.path.isfile(jdir):
        print(f'Found {version}.json')
        return

    with open(jdir) as f:
        jfile = json.load(f)
        url = jfile['downloads']['client_mappings']['url']

        print(f'Downloading the mappings for {version}...')
        download_file(url, 'mappings/client.txt')
        print('Done!')

def download_file(url, out):
    urllib.request.urlretrieve(url, out)

def reformat_mappings():
    out = []
    with open('mappings/client.txt') as f:
        for line in f.readlines()[1:]:
            if line.startswith('    '): pass
            else:
                deobf_name, obf_name = line.split(' -> ')
                new_line = f'CLASS\t{obf_name[:-2]}\t{deobf_name[:-1]}'
                out.append(new_line)
    print('\n'.join(out))




if __name__ == "__main__": main()