import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gewu",  # 用自己的名替换其中的YOUR_USERNAME_
    version="1.1.0",  # 包版本号，便于维护版本,保证每次发布都是版本都是唯一的
    author="denglihua",  # 作者，可以写自己的姓名
    author_email="1173324325@qq.com",  # 作者联系方式，可写自己的邮箱地址
    description="在线模式下，格物板与pc机之间的通信",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://www.haoqixingstem.com/#/",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts" : ['gewu=gewu.manage:run']
    }, #安装成功后，在命令行输入mwjApiTest 就相当于执行了mwjApiTest.manage.py中的run了
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # 对python的最低版本要求
)
