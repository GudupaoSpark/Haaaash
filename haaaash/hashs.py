from . import hash_func
from concurrent.futures import ProcessPoolExecutor
import math

def process_file(file_path, hash_method, length):
    if hash_method in ['shake_128', 'shake_256']:
        return {"file": file_path, "hash": hash_func.file_hash_len(file_path, hash_method, length)}
    else:
        return {"file": file_path, "hash": hash_func.file_hash(file_path, hash_method)}

def process_file_batch(file_paths, hash_method, length):
    return [process_file(file_path, hash_method, length) for file_path in file_paths]

def hash(f: list[str], hash_method: str = "sha256", length: int = 20, print_func=print) -> str:
    hlist = []
    lf = len(f)
    num_workers = ProcessPoolExecutor()._max_workers
    batch_size = math.ceil(lf / num_workers)
    file_batches = [f[i:i + batch_size] for i in range(0, lf, batch_size)]

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_file_batch, file_batch, hash_method, length): i for i, file_batch in enumerate(file_batches)}
        for future in futures:
            hlist.extend(future.result())

    return hlist