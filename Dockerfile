FROM python:3.12-book as base

# 设置非交互模式，避免构建过程中阻塞
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 设置时区
ENV TZ=Asia/Shanghai
RUN echo "$TZ" >/etc/timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 安装所需的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev \
    libgomp1 ffmpeg libsm6 libxext6 libgl1 build-essential

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装其它工具并删除缓存
RUN apt-get install -y --no-install-recommends \
    vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
