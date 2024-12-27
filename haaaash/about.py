import http.client
import json
import haaaash

def get_latest_version():
    """获取 haaaash 的最新版本信息"""
    
    # 创建连接到 PyPI 的客户端
    conn = http.client.HTTPSConnection("pypi.org")

    # 发送请求获取 haaaash 包的版本信息
    conn.request("GET", "/pypi/haaaash/json")

    # 获取响应并解析
    response = conn.getresponse()
    data = response.read()
    package_info = json.loads(data)

    # 输出最新版本信息
    latest_version = package_info["info"]["version"]
    return latest_version

def main():
    latest_version = get_latest_version()
    """主函数"""
    print(rf"""______  __                                        ______  
___  / / /______ _______ _______ _______ ____________  /_ 
__  /_/ / _  __ `/_  __ `/_  __ `/_  __ `/__  ___/__  __ \
_  __  /  / /_/ / / /_/ / / /_/ / / /_/ / _(__  ) _  / / /
/_/ /_/   \__,_/  \__,_/  \__,_/  \__,_/  /____/  /_/ /_/ 

当前版本: {haaaash.__version__}
最新版本: {latest_version}

GitHub: https://github.com/gudupaospark/haaaash
Docs: https://haaaash.gudupao.top
""")
    if haaaash.__version__ != latest_version:
        print(f"\033[32m你应该更新 haaaash 到最新版本: {latest_version}，使用 \033[34mpip install haaaash --upgrade\033[32m 更新。\033[0m")
