#公用的自定义工具类
def do_index_class(index):
    '''
    返回制定索引对应的类名
    :return:
    '''
    if index == 0:
        print(1)
        return "first"
    elif index ==1:
        print(2)
        return "second"
    elif index==2:
        return "third"

    return ""