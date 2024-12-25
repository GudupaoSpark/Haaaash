
outfuncs = {}

# 注册输出格式
def register(func:callable):
    outfuncs[func.__name__] = func

@register
def default(hlist: list):
    # 计算文件路径的最大长度
    max_file_length = max(len(item["file"]) for item in hlist)
    
    # 加上4个空格
    max_file_length += 4
    
    output = [f"""{"File":<{max_file_length}}Hash"""]
    for i in hlist:
        output += [f"""{i["file"]:<{max_file_length}}{i["hash"]}"""]
    return "\n".join(output)


@register
def md(hlist:list):
    output = ["|File|Hash|", "|-|-|"]
    for i in hlist:
        output += [f"""|{i["file"]}|{i["hash"]}|"""]
    return "\n".join(output)

def chmod(hlist:list,modname:str="default"):
    
    mod = outfuncs[modname]
    return mod(hlist)