"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : read_and_write.py
@Created : 2018-08-00
@Updated : 2021-02-17
@Version : 1.8.10
@Desc    :
"""
from contextlib import contextmanager

from ._typing import ReadAndWriteHint as Hint


@contextmanager
def ropen(file: str, mode='r', encoding='utf-8') -> Hint.FileHandle:
    """
    Args:
        file
        mode ('r'|'rb')
        encoding ('utf-8'|'utf-8-sig')
    
    Returns:
        file_handle
    """
    # 由于大多数国内 Windows 系统默认编码为 GBK, Python 内置的 open() 函数默认使用
    # 的是它, 但在开发中经常会遇到编码问题; 所以我们明确指定编码为 UTF-8, 本函数只是
    # 为了简化此书写步骤.
    handle = open(file, mode=mode, encoding=encoding)
    try:
        yield handle
    finally:
        handle.close()


@contextmanager
def wopen(file: str, mode='w', encoding='utf-8') -> Hint.FileHandle:
    """
    Args:
        file (str):
        mode ('w'|'a'|'wb'):
            w: 写入前清空原文件已有内容
            a: 增量写入
            wb: 以二进制字节流写入
        encoding ('utf-8'|'utf-8-sig'):
        
    Returns:
        file_handle
    """
    handle = open(file, mode=mode, encoding=encoding)
    try:
        yield handle
    finally:
        handle.close()


def is_file_has_content(file: str) -> bool:
    """
    References:
        https://www.imooc.com/wenda/detail/350036?block_id=tuijian_yw
    
    Returns (bool):
        True: file has content
        False: file is empty
    """
    from os.path import exists, getsize
    return bool(exists(file) and getsize(file))


def read_file(file: str) -> str:
    with ropen(file) as f:
        content = f.read()
        # https://blog.csdn.net/liu_xzhen/article/details/79563782
        if content.startswith(u'\ufeff'):
            # 说明文件开头包含有 BOM 信息, 我们将它移除.
            # Strip BOM charset at the start of content.
            content = content.encode('utf-8')[3:].decode('utf-8')
    return content


def read_file_by_line(file: str, offset=0) -> list:
    """
    IN: file:
        offset:
            0: 表示返回完整的列表
            n: 传一个大于 0 的数字, 表示返回 list[n:]. (ps: 如果该数字大于列表的长
               度, python 会返回一个空列表, 不会报错)
    OT: [str, ...]
    
    References:
        https://blog.csdn.net/qq_40925239/article/details/81486637
    """
    with ropen(file) as f:
        out = [line.rstrip() for line in f]
    return out[offset:]


def write_file(content: iter, file: str, mode='w', adhesion='\n'):
    """ 写入文件, 传入内容可以是字符串, 也可以是数组.

    Args:
        content: 需要写入的文本, 可以是字符串, 也可以是数组. 传入数组时, 会自动
            将它转换为 "\n" 拼接的文本
        file: 写入的路径, 建议使用相对路径
        mode ('w'|'a'|'wb'): 写入模式, 有三种可选:
            a: 增量写入 (默认)
            w: 清空原内容后写入
            wb: 在 w 的基础上以比特流的形式写入
        adhesion: ('\n'|'\t'|...). 拼接方式, 只有当 content 为列表时会用到, 用于
            将列表转换为文本时选择的拼接方式
            Example:
                content = adhesion.join(content)
                # ['a', 'b', 'c'] -> 'a\nb\nc'

    Refer:
        python 在最后一行追加 https://www.cnblogs.com/zle1992/p/6138125.html
        python map https://blog.csdn.net/yongh701/article/details/50283689
    """
    if not isinstance(content, str):
        content = adhesion.join(map(str, content))
        ''' 注: 暂不支持对二维数组操作.
            如果 content 的形式为:
                content = [[1, 2, 3], [4, 5, 6]]
            会报错.
        '''
    with wopen(file, mode) as f:
        # Keep an empty line at the end of file.
        f.write(content + '\n')


def read_json(file: str) -> Hint.StructData:
    if file.endswith('.json'):
        from json import loads as _loads
        # 注意: 如果文件内容不符合 json 格式, _loads() 会报 JSONDecodeError.
    elif file.endswith('.yaml'):
        # pip install pyyaml
        # noinspection PyUnresolvedReferences
        from yaml import safe_load as _loads
    else:
        raise Exception(
            'Unknown file type! Please pass a file ends with '
            '".json" or ".yaml".'
        )
    with ropen(file) as f:
        return _loads(f.read())


def write_json(data: Hint.DumpableData, file: str, pretty_dump=False):
    """
    Args:
        data
        file: Ends with '.json'.
            Note: '.yaml' needs PyYaml to be installed.
        pretty_dump:
            True: Output json with pretty-printed format (4 spaces each level).
            False: The most compact representation.
            
    Improvements:
        Convert `set` as `list` to make it serializable.
        Convert `pathlib.PosixPath` as `str` to make it serializable.
    """
    from json import dumps as _dumps
    
    if isinstance(data, set):
        data = list(data)
    
    with wopen(file) as f:
        f.write(_dumps(data, ensure_ascii=False, default=str,
                       indent=None if pretty_dump is False else 4))
        #   ensure_ascii=False: Set to False to support Chinese characters:
        #       https://www.cnblogs.com/zdz8207/p/python_learn_note_26.html
        #   default=str: When something is not serializble, try to call its
        #       __str__() attribute, it is useful to resolve case of
        #       `pathlib.PosixPath`


# ------------------------------------------------------------------------------

def loads(file: str, offset=-1, **kwargs) -> Hint.LoadedData:
    """
    Args:
        file:
        offset: [-1|0|1|2|3|...]
            -1: If it is negative number (typically -1), means calling
                `read_file`
            0, 1, 2, 3, ...: See `read_file_by_line`
        **kwargs:
    
    Keyword Args:
        sheetx (int): Default 0. See `excel_reader.ExcelReader`
        formatting_info (bool): Default False. See `excel_reader.ExcelReader`
    """
    if file.endswith(Hint.StructFileTypes):
        return read_json(file)
    elif file.endswith(Hint.PlainFileTypes):
        if offset >= 0:
            return read_file_by_line(file, offset)
        else:
            return read_file(file)
    elif file.endswith(Hint.BinaryFileTypes):
        if file.endswith(('.xlsx', '.xls')):
            from .excel_reader import ExcelReader
            return ExcelReader(file, **kwargs)
        else:
            raise Exception('Unsupported filetype!', file)
    else:  # .js, .css, .py, etc.
        return read_file(file)


def load_list(file: str, offset=0) -> list:
    return read_file_by_line(file, offset)


def load_dict(file: str) -> Hint.StructData:
    if file.endswith(Hint.StructFileTypes):
        return read_json(file)
    else:
        raise Exception('Unsupported filetype!', file)


def dumps(data: Hint.DumpableData, file: str, **kwargs):
    if file.endswith(Hint.StructFileTypes):
        write_json(data, file, **kwargs)
    elif file.endswith(Hint.PlainFileTypes):
        write_file(data, file, **kwargs)
    elif file.endswith(Hint.BinaryFileTypes):
        raise Exception('Unsupported filetype!', file)
    else:  # .js, .css, .py, etc.
        write_file(data, file, **kwargs)


# ------------------------------------------------------------------------------

@contextmanager
def read(file: str, **kwargs):
    """ Open file as a read handle.
    
    Usage:
        with read('input.json') as r:
            print(len(r))
    """
    data = loads(file, **kwargs)
    try:
        yield data
    finally:
        del data


@contextmanager
def write(file: str, data=None, **kwargs):
    """ Create a write handle, file will be generated after the `with` block
        closed.
        
    Args:
        file: See `dumps`.
        data (list|dict|set): If the data type is not registered, an Assertion
            Error will be raised.
        kwargs: See `dumps`.
        
    Usage:
        with write('output.json', []) as w:
            for i in range(10):
                w.append(i)
        print('See "result.json:1"')
    """
    assert isinstance(data, (list, dict, set))
    try:
        yield data
    finally:
        dumps(data, file, **kwargs)
