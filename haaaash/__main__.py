import argparse
from . import outs
from .hashs import hash

parser = argparse.ArgumentParser(
                    prog='python3 -m haaaash',
                    description='详细解析：',
                    epilog='By Gudupao (MIT License)')
parser.add_argument('file',help='文件(夹)路径')
parser.add_argument('-m','--method',help='哈希方法（默认为 sha256）',default='sha256')
parser.add_argument('-l','--length',help='哈希长度（算法为 shake_128 shake_256 时）',type=int,default=20)
parser.add_argument('-o','--outmod',help='输出模式',type=str,default="default")

args = parser.parse_args()
hash_list = hash(args.file,args.method,args.length)
out = outs.chmod(hash_list,args.outmod)
print(out)