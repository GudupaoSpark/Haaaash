import importlib.util
import os

def get_function_object(file_path, function_name):
    # 获取文件的绝对路径
    file_path = os.path.abspath(file_path)

    # 获取文件名和模块名
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 动态加载模块
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 获取函数对象
    if hasattr(module, function_name):
        return getattr(module, function_name)
    else:
        return None  # 如果没有找到指定的函数，返回None

if __name__ == "__main__":
    # 使用示例
    full = 'D:/python/Haaaash/example.test.py|my_function'
    full = full.split('|')
    file_path = full[0]
    function_name = full[1]
    func = get_function_object(file_path, function_name)

    if func:
        print(f"成功获取函数对象: {func}")
        # 可以调用这个函数
        func()  # 假设函数没有参数
    else:
        print(f"未找到函数 {function_name}")
