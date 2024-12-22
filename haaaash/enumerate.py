import os

def get_file_or_folder_contents(path):
    # 判断路径是否存在
    if not os.path.exists(path):
        raise ValueError(f"路径 {path} 不存在")
    
    # 判断是文件还是文件夹
    if os.path.isfile(path):
        return [path]  # 如果是文件，返回原路径作为列表
    elif os.path.isdir(path):
        file_paths = []
        # 遍历文件夹中的文件
        for root, dirs, files in os.walk(path):
            for file in files:
                file_paths.append(os.path.join(root, file))
        return file_paths  # 返回文件路径列表
    else:
        raise ValueError(f"路径 {path} 既不是文件也不是文件夹")
