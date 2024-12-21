import argparse
from .hashfunc import file_hash,file_hash_len

parser = argparse.ArgumentParser(
                    prog='python3 -m haaaash',
                    description='详细解析：',
                    epilog='By Gudupao (MIT License)')
parser.add_argument('file',help='文件(夹)路径')
parser.add_argument('-m','--method',help='哈希方法',default='sha256')
parser.add_argument('-l','--length',help='哈希长度（算法为 shake_128 shake_256 时）',type=int,default=20)

args = parser.parse_args()

if args.method in ['shake_128','shake_256']:
    print(file_hash_len(args.file,args.method,args.length))
else:
    print(file_hash(args.file,args.method))