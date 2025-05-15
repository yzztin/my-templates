import os
import time
from typing import Literal
from datetime import datetime
from uuid import uuid4
from pathlib import Path

from starlette.datastructures import UploadFile


def get_uuid() -> str:
    """
    生成 str 类型的 32 位 uuid
    """
    return uuid4().hex

def get_timestamp(time_unit: Literal["s", "ms"] = "ms") -> int:
    """
    生成 int 类型的时间戳，默认为毫秒级
    :param time_unit: 时间戳单位，s 为秒，ms 为毫秒
    """
    return int(time.time() * 1000) if time_unit == "ms" else int(time.time())

def get_filename_and_extension(file_path: str) -> tuple[str, str]:
    """
    获取文件名和扩展名，如 test.txt -> (test, .txt)
    """
    return Path(file_path).stem, Path(file_path).suffix.lower()


def makefile_by_time(file_extension: str, part_name: str = "", dir_path: str | None = None) -> str:
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
    file_path = f"{part_name}{timestamp}.{file_extension.lstrip('.')}"

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.abspath(os.path.join(dir_path, file_path))

    return file_path


async def ensure_file_bytes(file: str | bytes | UploadFile) -> bytes:
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
        file_bytes = await file.read()
    else:
        raise ValueError(f"file 参数错误：{type(file)}")

    return file_bytes
