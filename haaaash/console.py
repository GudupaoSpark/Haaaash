import sys

class Manager:
    def __init__(self):
        self.output_lines = 0  # 记录输出的行数

    def print(self, *text, end="\n"):
        """打印文本并统计换行符"""
        # 计算文本中包含的换行符数量
        if len(text) == 0:
            outtext = str(end)
        else:
            outtext = str(text[0])
            for t in text[1:]:
                outtext += " " + str(t)
            outtext += str(end)

        self.output_lines += outtext.count("\n")  # 每个换行符算一行
        sys.stdout.write(outtext)
        sys.stdout.flush()

    def clear(self):
        """清除所有输出行"""
        # 将光标移动到顶部
        sys.stdout.write("\r")
        # 清除所有输出行
        for _ in range(self.output_lines + 1):
            sys.stdout.write("\033[K\033[F")  # 光标向上移动一行并且清除
        sys.stdout.write("\n")  # 确保光标移动到下一行
        sys.stdout.flush()
        self.output_lines = 0

if __name__ == "__main__":
    import time
    manager = Manager()
    manager.print("Hello, World!\n666")
    manager.print("This is a test.")
    time.sleep(2)
    manager.clear()
        