import argparse
from.shell import shell
from . import about
import haaaash
gui = None
if haaaash.the != 'haaaash':
    from . import gui

def main():
    parser = argparse.ArgumentParser(
                        prog='haaaash',
                        description='详细解析：',
                        epilog='By Gudupao (MIT License)')
    parser.add_argument('file',help='文件(夹)路径（默认为当前目录）',nargs='*',default='.')
    parser.add_argument('-m','--method',help='哈希方法（默认为 sha256）',default='sha256')
    parser.add_argument('-l','--length',help='哈希长度（算法为 shake_128 shake_256 时）',type=int,default=20)
    parser.add_argument('-o','--outmod',help='输出模式',type=str,default="default")
    parser.add_argument('-f','--outfile',help='输出文件',type=str,default="NO")
    parser.add_argument('-r','--reverse',help='是否反向输出（深层路径在前）',action='store_true')
    parser.add_argument('-a','--about',help='关于',action='store_true')
    parser.add_argument('-g','--gui',help='启动图形界面',action='store_true')
    parser.add_argument('--TEST',help='测试模式，激活高级版',action='store_true')
    
    args = parser.parse_args()
    
    if args.about:
        about.main()
        return
        
    if args.gui:
        global gui
        if haaaash.the != 'haaaash':
            if gui:
                gui.main()
            else:
                print("GUI 模块加载失败")
        elif args.TEST:
            try:
                from . import gui
                gui.main()
            except ImportError:
                print("GUI 模块加载失败")
        else:
            print("请安装 haaaash-expansion 扩展版")
        return

    args = args.__dict__
    shell(args)

if __name__ == '__main__':
    main()