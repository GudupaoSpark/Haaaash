from . import outs
from .hashs import hash
from .enumerate import get_file_or_folder_contents_list
from .console import Manager
import time

manager = Manager()
def shell(args):
    start_time = time.time()
    manager.print("开始枚举文件...")
    files = get_file_or_folder_contents_list(args["file"],args["reverse"])
    manager.print(f"共找到 {len(files)} 个文件")
    manager.print("开始计算...")
    hash_list = hash(files,args["method"],args["length"],manager.print)
    manager.print("开始格式化...")
    out = outs.chmod(hash_list,args["outmod"])
    if args["outfile"] != "NO":
        with open(args["outfile"],'w') as f:
            f.write(out)
        print(f"已输出到文件： {args["outfile"]}")
        print(f"耗时：{time.time() - start_time} 秒")
    else:
        manager.clear()
        print(out)