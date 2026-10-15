"""Verified MATCHDAY 99 v0.9.3 patch installer; Python 3 standard library only.
Never modifies source files. --auto supports the double-click Windows launcher.
"""
from pathlib import Path
import sys,json,hashlib,shutil,os,zlib,struct

def apply(source,patch):
    if patch[:4]!=b'BPS1':raise ValueError('Not a BPS patch')
    source_crc,target_crc,patch_crc=struct.unpack('<III',patch[-12:])
    if zlib.crc32(patch[:-4])!=patch_crc:raise ValueError('Patch CRC mismatch')
    if zlib.crc32(source)!=source_crc:raise ValueError('Source CRC mismatch')
    pos=4
    def integer():
        nonlocal pos
        value=0;shift=1
        while True:
            if pos>=len(patch)-12:raise ValueError('Truncated patch')
            x=patch[pos];pos+=1;value+=(x&127)*shift
            if x&128:return value
            shift<<=7;value+=shift
    source_size=integer();target_size=integer();metadata_size=integer();pos+=metadata_size
    if source_size!=len(source):raise ValueError('Source size mismatch')
    out=bytearray();source_relative=target_relative=0
    while len(out)<target_size:
        action=integer();mode=action&3;length=(action>>2)+1
        if len(out)+length>target_size:raise ValueError('Invalid output length')
        if mode==0:
            start=len(out);out.extend(source[start:start+length])
        elif mode==1:
            if pos+length>len(patch)-12:raise ValueError('Truncated literal data')
            out.extend(patch[pos:pos+length]);pos+=length
        else:
            delta=integer();delta=-(delta>>1) if delta&1 else delta>>1
            if mode==2:
                source_relative+=delta
                if not 0<=source_relative<=len(source)-length:raise ValueError('Invalid source copy')
                out.extend(source[source_relative:source_relative+length]);source_relative+=length
            else:
                target_relative+=delta
                if not 0<=target_relative<len(out):raise ValueError('Invalid target copy')
                for _ in range(length):out.append(out[target_relative]);target_relative+=1
    if pos!=len(patch)-12 or zlib.crc32(out)!=target_crc:raise ValueError('Output CRC mismatch')
    return out


def digest(data):return hashlib.sha256(data).hexdigest()
def verified_folder(folder,m):
    for name,sha in [(m['target_file'],m['target_sha256']),(m['cue_file'],m['cue_sha256'])]+[(x['file'],x['sha256']) for x in m['audio_tracks']]:
        p=folder/name
        if not p.is_file() or digest(p.read_bytes())!=sha:return False
    return True

def desktops():
    found=[Path.home()/'Desktop']
    if os.name=='nt':
        try:
            import ctypes
            buf=ctypes.create_unicode_buffer(32768)
            if ctypes.windll.shell32.SHGetFolderPathW(None,0x10,None,0,buf)==0:found.insert(0,Path(buf.value))
        except (AttributeError,OSError):pass
    found.extend(p/'Desktop' for p in Path.home().glob('OneDrive*') if p.is_dir())
    return list(dict.fromkeys(found))

def source_candidates(given,m):
    if given.is_file():
        if given.suffix.lower()=='.bin':return [given]
        given=given.parent
    known=[given/x['file'] for x in m['sources']]
    others=[p for p in given.glob('*.bin') if p not in known and p.stat().st_size==m['target_bytes']]
    return [p for p in known+others if p.is_file()]

def find_auto(m):
    roots=[]
    for desk in desktops():roots.extend([desk/'ePSXe205/roms',desk/'roms'])
    roots.extend([Path(__file__).resolve().parent,Path.cwd()])
    folders=[]
    for root in roots:
        for name in ['MATCHDAY99_v09_2','MATCHDAY99_v09_1','MATCHDAY99_v09','MATCHDAY99_v08','']:
            p=root/name
            if p.is_dir() and p not in folders:folders.append(p)
    for folder in folders:
        for p in source_candidates(folder,m):
            sha=digest(p.read_bytes())
            if any(v['sha256']==sha for v in m['sources']):return p
    if os.name=='nt':
        try:
            from tkinter import Tk,filedialog
            win=Tk();win.withdraw()
            selected=filedialog.askdirectory(title='Mevcut MATCHDAY99 BIN ve ses dosyalarinin klasorunu secin',mustexist=True)
            win.destroy()
            if selected:return Path(selected)
        except ImportError:pass
    raise ValueError('Source not found. Drag your current game folder onto KUR_V09_3.cmd, or run: py apply_v09_3.py "source folder" "new output folder"')

def main():
    here=Path(__file__).resolve().parent;m=json.loads((here/'manifest.json').read_text(encoding='utf-8'))
    args=sys.argv[1:]
    if args==['--auto']:given=find_auto(m)
    elif len(args) in [1,2]:given=Path(args[0]).expanduser().resolve()
    else:
        print('Usage: py apply_v09_3.py "source BIN, CUE or folder" [new empty output folder]')
        return 1
    source_dir=given.parent if given.is_file() else given
    print('Checking source: '+str(source_dir),flush=True)
    source=variant=None
    for p in source_candidates(given,m):
        data=p.read_bytes();sha=digest(data)
        if sha==m['target_sha256']:
            if verified_folder(source_dir,m):print('Already verified v0.9.3. Open: '+str(source_dir/m['cue_file']));return 0
            continue
        variant=next((q for q in m['sources'] if q['sha256']==sha),None)
        if variant:source=data;break
    if variant is None:raise ValueError('No supported original v0.8 / v0.9 / v0.9.1 / v0.9.2 BIN found; source not modified.')
    for x in m['audio_tracks']:
        p=source_dir/x['file']
        if not p.is_file() or digest(p.read_bytes())!=x['sha256']:raise ValueError('Missing or changed audio: '+x['file'])
    if len(args)==2 and args!=['--auto']:output=Path(args[1]).expanduser().resolve()
    else:
        parent=source_dir.parent if source_dir.name.startswith('MATCHDAY99_') else source_dir
        output=parent/'MATCHDAY99_v09_3';n=2
        while output.exists() and (not output.is_dir() or any(output.iterdir())):
            if output.is_dir() and verified_folder(output,m):print('Already verified v0.9.3. Open: '+str(output/m['cue_file']));return 0
            output=parent/('MATCHDAY99_v09_3_'+str(n));n+=1
    if output==source_dir or (output.exists() and (not output.is_dir() or any(output.iterdir()))):raise ValueError('Output must be a NEW or empty folder. Original files will not be overwritten.')
    patch=(here/variant['patch']).read_bytes()
    if digest(patch)!=variant['patch_sha256']:raise ValueError('Patch SHA-256 mismatch')
    target=apply(source,patch)
    if digest(target)!=m['target_sha256']:raise ValueError('Resulting BIN SHA-256 mismatch')
    cue=(here/m['cue_file']).read_bytes()
    if digest(cue)!=m['cue_sha256']:raise ValueError('CUE SHA-256 mismatch')
    ancestor=output
    while not ancestor.exists():ancestor=ancestor.parent
    needed=len(target)+sum((source_dir/x['file']).stat().st_size for x in m['audio_tracks'])+1024*1024
    if shutil.disk_usage(ancestor).free<needed:raise ValueError('Not enough free space for a separate BIN/CUE and audio copy')
    output.mkdir(parents=True,exist_ok=True)
    with (output/m['target_file']).open('xb') as f:f.write(target)
    with (output/m['cue_file']).open('xb') as f:f.write(cue)
    for x in m['audio_tracks']:
        with (source_dir/x['file']).open('rb') as src,(output/x['file']).open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
    if not verified_folder(output,m):raise ValueError('Written game files failed SHA-256 validation')
    print('SUCCESS: verified MATCHDAY 99 v0.9.3 from '+variant['version'])
    print('Leeds United name + skin tones; all existing kits, flags and player stats preserved.')
    print('Open: '+str(output/m['cue_file']))
    print('Cold boot this NEW CUE. Do not load an older save state. Original files were preserved.')
    if os.name=='nt':
        import subprocess
        try:subprocess.Popen(['explorer.exe','/select,',str(output/m['cue_file'])])
        except OSError:pass # File browser is optional; verified output remains usable.
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,KeyError,TypeError) as e:
        print('ERROR:',e,file=sys.stderr);sys.exit(2)
