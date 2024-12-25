from . import hashfunc

def hash(f: list[str], hash_method:str="sha256",length:int=20) -> str:
    hlist = []
    if hash_method in ['shake_128','shake_256']:
        for i in f:
            hlist.append({"file":i,"hash":hashfunc.file_hash_len(i, hash_method,length)})
    else:
        for i in f:
            hlist.append({"file":i,"hash":hashfunc.file_hash(i, hash_method)})
    return hlist