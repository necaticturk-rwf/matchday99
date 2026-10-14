"""Create verified MATCHDAY 99 v0.9.1 from original v0.8 or affected v0.9.
Python 3 standard library only. Source files are never modified.
"""
from pathlib import Path
import sys,json,hashlib,zlib,struct,shutil

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
def main():
    here=Path(__file__).resolve().parent
    if len(sys.argv) not in [2,3]:
        print('Usage: py apply_v09_1.py "folder_with_v08_or_v09_BIN_and_audio_tracks" [new_empty_output_folder]')
        return 1
    manifest=json.loads((here/'manifest.json').read_text(encoding='utf-8'))
    given=Path(sys.argv[1]).expanduser().resolve();source_dir=given.parent if given.is_file() else given
    output=Path(sys.argv[2]).expanduser().resolve() if len(sys.argv)==3 else source_dir/'MATCHDAY99_v09_1'
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Output folder must be empty. Choose a NEW folder; originals will not be overwritten.')
    candidates=[given] if given.is_file() else [source_dir/q['file'] for q in manifest['sources']]
    source=variant=None
    for p in candidates:
        if not p.is_file():continue
        data=p.read_bytes();sha=digest(data)
        if sha==manifest['target_sha256']:
            raise ValueError('This BIN is already the corrected v0.9.1. Open its CUE; no further patch is needed.')
        variant=next((q for q in manifest['sources'] if q['sha256']==sha),None)
        if variant:source=data;break
    if variant is None:
        raise ValueError('No matching v0.8 or affected v0.9 Track 01 found. Choose the folder containing the BIN and all 11 audio tracks.')
    for track in manifest['audio_tracks']:
        p=source_dir/track['file']
        if not p.is_file() or digest(p.read_bytes())!=track['sha256']:
            raise ValueError('Missing or changed audio track: '+track['file'])
    patch=(here/variant['patch']).read_bytes()
    if digest(patch)!=variant['patch_sha256']:raise ValueError('Patch SHA-256 mismatch')
    target=apply(source,patch)
    if digest(target)!=manifest['target_sha256']:raise ValueError('Output SHA-256 mismatch')
    cue=(here/manifest['cue_file']).read_bytes()
    if digest(cue)!=manifest['cue_sha256']:raise ValueError('CUE SHA-256 mismatch')
    output.mkdir(parents=True,exist_ok=True)
    (output/manifest['target_file']).write_bytes(target)
    (output/manifest['cue_file']).write_bytes(cue)
    for track in manifest['audio_tracks']:shutil.copy2(source_dir/track['file'],output/track['file'])
    # Validate the actual written files before reporting success.
    if digest((output/manifest['target_file']).read_bytes())!=manifest['target_sha256']:
        raise ValueError('Written BIN SHA-256 mismatch')
    for track in manifest['audio_tracks']:
        if digest((output/track['file']).read_bytes())!=track['sha256']:
            raise ValueError('Written audio track SHA-256 mismatch: '+track['file'])
    print('Verified MATCHDAY 99 v0.9.1 created from '+variant['version']+': '+str(output))
    print('Open '+manifest['cue_file']+' in your emulator.')
    print('Cold boot the new CUE. Do not load an old emulator save state. All source files were preserved.')
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,KeyError,TypeError) as e:
        print('ERROR:',e,file=sys.stderr);sys.exit(2)
