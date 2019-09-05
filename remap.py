

import os, json, urllib.request, subprocess as cmd

def main():
    version = get_version()
    get_mappings(version)
    reformat_mappings(version)
    remap_jar(version)

def get_version():
    with open('version.config') as f:
        config = f.readlines()[0]
        return config.split('=')[-1].strip()

def get_mappings(version):
    jdir = os.getenv('APPDATA') + f'\\.minecraft\\versions\\{version}\\{version}.json'

    odir = f'mappings/{version}.mojang_mappings'

    if os.path.exists(odir) and os.path.isfile(odir):
        print('Skipping mapping download')
        return

    if not os.path.exists(jdir) or not os.path.isfile(jdir):
        print('{version}.json not found, please run the game at least once before running this script')
        exit()
    print(f'Found {version}.json')

    with open(jdir) as f:
        jfile = json.load(f)
        url = jfile['downloads']['client_mappings']['url']

        print(f'Downloading the mappings for {version}...')
        download_file(url, odir)
        print('Done!')

def download_file(url, out):
    urllib.request.urlretrieve(url, out)

def reformat_mappings(version):
    out = ['v1\tofficial\tnamed']
    print(f'Creating {version}.tiny mappings...')

    counter = [0,0,0] # M,F,C

    with open(f'mappings/{version}.mojang_mappings') as f:

        current_class = None

        for line in f.readlines():
            
            line = line.replace('.' ,'/')

            if line.startswith('#'): continue
            
            elif line.startswith('    '):
                if '(' in line:  new_line = parse_method(line, current_class) ; counter[0] += 1
                else:            new_line = parse_field(line, current_class)  ; counter[1] += 1
            else: current_class, new_line = parse_class(line)                 ; counter[2] += 1
            out.append(new_line)
    
    out.append(f'# NAMED-COUNTER method {counter[0]}')
    out.append(f'# NAMED-COUNTER field {counter[1]}')
    out.append(f'# NAMED-COUNTER class {counter[2]}')

    with open(f'mappings/{version}.tiny', 'w') as f:
        f.write('\n'.join(out))
    print('Done!')

def parse_class(line):
    #com.mojang.blaze3d.Blaze3D -> cve:
    #CLASS	a	net/minecraft/class_1158

    deobf_name, obf_name = line.split(' -> ')
    obf_name = obf_name[:-2]
    return obf_name, f'CLASS\t{obf_name}\t{deobf_name}'

def parse_field(line, current_class):
    #    int source -> b
    #FIELD	co	Ljava/util/Collection;	b	field_9871

    fieldtype, deobf_name, _, obf_name = line.strip().split(' ')
    fieldtype = parse_type(fieldtype)

    return f'FIELD\t{current_class}\t{fieldtype}\t{obf_name}\t{deobf_name}'

def parse_method(line, current_class):
    #    852:865:void teleport(double,double,double,float,float,java.util.Set) -> a
    #METHOD	wc	(DDDFFLjava/util/Set;)V	a	method_14360

    returntype, temp, _, obf_name = line.strip().split(' ')
    
    deobf_name, temp = temp.split('(')

    params = ''
    for param in temp[:-1].split(','): params += parse_type(param)
    
    returntype = parse_type(returntype.split(':')[-1])

    return f'METHOD\t{current_class}\t({params}){returntype}\t{obf_name}\t{deobf_name}'

def parse_type(string):
    if string == '': return ''
    mapp = {
        'byte':'B',
        'char':'C',
        'double':'D',
        'float':'F',
        'int':'I',
        'long':'J',
        'short':'S',
        'boolean':'Z',
        'void':'V'
    }
    
    out = ''

    for x in range(string.count('[')): out += '['
    
    string = string.replace('[]','')

    if string in mapp: out += mapp[string]
    else: out += f'L{string};'
    
    return out

def remap_jar(version):
    jardir = os.getenv('APPDATA') + f'\\.minecraft\\versions\\{version}\\{version}.jar'
    outdir = f'output/{version}-remapped.jar'
    mapdir = f'mappings/{version}.tiny'

    cmd.run(['java','-jar','bin/tiny-remapper-0.1.0.9-fat.jar',jardir,outdir,mapdir,'official','named', '--ignoreconflicts'])


if __name__ == "__main__": main()