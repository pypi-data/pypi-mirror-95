# 乐白机器人 Python SDK

## 使用说明

```
pip install lebai
```

[API文档](http://lebai.py.kingfree.moe)

提供基于 `async/await` 的异步 API。

安装依赖（Python 3.7+）：
```bash
pip install grpcio asyncio protobuf
```

示例：

```python
import asyncio

from lebai import LebaiRobot, CartesianPose, JointPose

async def run():
    rb = LebaiRobot("192.168.3.218")

    await rb.start_sys()

    await rb.movej(JointPose(0, -0.5, math.pi/6, 0, 0, 0), 0, 0, 1, 0)

    p2 = CartesianPose(0.1, 0.2, 0, 0, 0, 0, base=base)
    await rb.movel(p2, 0, 0, 2, 0)

    print(await rb.get_actual_tcp_pose())

    await rb.stop_sys()

if __name__ == '__main__':
    asyncio.run(run())
```

### 安装 Python 和 pip

例如在 Ubuntu 下：
```bash
sudo apt install python3 python3-pip
```

查看 Python 版本：
```bash
python --version
```

如果 Python 版本小于 3.7：
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-distutils
```

如果 Python 环境配置有问题：
```bash
sudo ln -sf /usr/bin/python3.9 /usr/bin/python3
sudo ln -sf /usr/bin/python3 /usr/bin/python
sudo ln -sf /usr/bin/pip3 /usr/bin/pip
python -m pip install --upgrade pip setuptools wheel
```

## 开发人员指南

- [https://pip.pypa.io/en/stable/installing/]()
- [https://packaging.python.org/tutorials/managing-dependencies/]

### 安装项目依赖

安装依赖：
```
pip install -r requirements.txt
```

- [https://grpc.io/docs/languages/python/quickstart/]()
- [https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html]()


## 运行

```bash
GRPC_TRACE=all GRPC_VERBOSITY=debug ./main.py
```

## 构建和发布

```bash
python -m pip install --user pipenv
python3 -m pip install --user --upgrade setuptools wheel twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*

python3 -m twine upload --repository pypi dist/*
```

## 从 PyPI 安装

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps lebai

pip install lebai
```
