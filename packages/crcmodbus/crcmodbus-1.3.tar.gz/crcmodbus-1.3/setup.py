from setuptools import setup, find_packages
filepath = 'README.md'
setup(
        name="crcmodbus",
        version="1.3",
        description="crc16",
        long_description=open(filepath, encoding='utf-8').read(),
        long_description_content_type="text/markdown",
        author="jdh99",
        author_email="jdh821@163.com",
        url="https://gitee.com/jdhxyy/crc16-python",
        packages=find_packages(),
        data_files=[filepath]
    )
