import argparse
from . import outs
from .hashs import hash
from .enumerate import get_file_or_folder_contents_list


def main():
    parser = argparse.ArgumentParser(
                        prog='haaaash',
                        description='详细解析：',
                        epilog='By Gudupao (MIT License)')
    parser.add_argument('file',help='文件(夹)路径（多个用 | 隔开）')
    parser.add_argument('-m','--method',help='哈希方法（默认为 sha256）',default='sha256')
    parser.add_argument('-l','--length',help='哈希长度（算法为 shake_128 shake_256 时）',type=int,default=20)
    parser.add_argument('-o','--outmod',help='输出模式',type=str,default="default")
    parser.add_argument('-f','--outfile',help='输出文件',type=str,default="NO")
    parser.add_argument('-r','--reverse',help='是否反向输出（深层路径在前）',action='store_true')

    args = parser.parse_args()
    files = get_file_or_folder_contents_list(args.file.split("|"),args.reverse)
    hash_list = hash(files,args.method,args.length)
    out = outs.chmod(hash_list,args.outmod)
    if args.outfile != "NO":
        with open(args.outfile,'w') as f:
            f.write(out)
        print(f"已输出到文件：{args.outfile}")
    else:
        print(out)

if __name__ == '__main__':
    main()