import os
from datetime import datetime
from uuid import uuid4

from fastapi import UploadFile


def get_uuid() -> str:
    """
    生成 str 类型的 32 位 uuid
    """
    return uuid4().hex


def makefile_by_time(file_extension: str, part_name: str = "", dir_path: str = None) -> str:
    """
    根据当前时间戳生成文件名或路径
    :param file_extension: 文件名后缀
    :param part_name: 在文件名中添加的字符
    :param dir_path: 待生成文件的父路径，为空则仅生成文件名
    :return: 文件名或文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-4]
    if part_name:
        part_name = f"{part_name[:10].strip()}-"
    file_path = f"{part_name}{timestamp}.{file_extension}"

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.abspath(os.path.join(dir_path, file_path))

    return file_path


def ensure_file_bytes(file: str | bytes | UploadFile) -> bytes:
    """
    确保得到文件的字节数据
    :param file: 文件路径
    :return: 文件字节
    """
    if isinstance(file, str):
        if not os.path.exists(file):
            raise FileNotFoundError(f"文件不存在：{file}")
        with open(file, "rb") as f:
            file_bytes = f.read()
    elif isinstance(file, bytes):
        file_bytes = file
    elif isinstance(file, UploadFile):
        file_bytes = file.read()
    else:
        raise ValueError(f"file 参数错误：{type(file)}")

    return file_bytes
