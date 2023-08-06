import setuptools
setuptools.setup(
    name='hyMethod',#库名
    version='0.0.2',#版本号，建议一开始取0.0.1
    author='Junshuo Tan',#你的名字，名在前，姓在后，例：张一一 Yiyi Zhang
    author_email='3357135715@qq.com',#你的邮箱（任何邮箱都行，只要不是假的）
    description='学而思火焰方法库',#库介绍
    long_descripition_content_type="text/markdown",
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ,
    ],
)
