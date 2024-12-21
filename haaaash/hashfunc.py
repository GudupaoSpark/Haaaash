import hashlib
import os

def file_hash(file_path: str, hash_method:str="sha256") -> str:
    if not os.path.isfile(file_path):
        return ''
    h = hashlib.new(hash_method)
    with open(file_path, 'rb') as f:
        while b := f.read(8192):
            h.update(b)
    return h.hexdigest()

# 自定义长度
def file_hash_len(file_path: str, hash_method:str, length: int) -> str:
    if not os.path.isfile(file_path):
        return ''
    h = hashlib.new(hash_method)
    with open(file_path, 'rb') as f:
        while b := f.read(8192):
            h.update(b)
    return h.hexdigest(length)