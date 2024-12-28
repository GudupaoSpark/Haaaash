import json
import importlib
from . import file_mod

outfuncs = {}

# 注册输出格式
def register(name=""):
    if name == "":
        def func(tf):
            outfuncs[tf.__name__] = tf
            return tf
    else:
        def func(tf):
            outfuncs[name] = tf
            return tf
    return func

@register()
def default(hlist: list):
    # 计算文件路径的最大长度
    max_file_length = max(len(item["file"]) for item in hlist)
    
    # 加上4个空格
    max_file_length += 4
    
    output = [f"""{"File":<{max_file_length}}Hash"""]
    for i in hlist:
        output += [f"""{i["file"]:<{max_file_length}}{i["hash"]}"""]
    return "\n".join(output)


@register()
def md(hlist:list):
    output = ["|File|Hash|", "|-|-|"]
    for i in hlist:
        output += [f"""|{i["file"]}|{i["hash"]}|"""]
    return "\n".join(output)

@register()
def csv(hlist:list):
    output = ["File,Hash"]
    for i in hlist:
        output += [f"""{i["file"]},{i["hash"]}"""]
    return "\n".join(output)

@register("json")
def thejson(hlist:list):
    return json.dumps(hlist, indent=4)

def chmod(hlist:list,modname:str="default"):
    if modname not in outfuncs: 
        full = modname.split('|')
        mod=file_mod.get_function_object(full[0],full[1])
    else: mod=outfuncs[modname]
    return mod(hlist)
