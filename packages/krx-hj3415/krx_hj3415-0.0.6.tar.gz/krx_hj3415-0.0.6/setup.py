import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="krx_hj3415",
    version="0.0.6",
    author="hyungjin kim",
    author_email="hj3415@gmail.com",
    description="Get entire corp data from https://kind.krx.co.kr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://localhost",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.2.2',
        'sqlalchemy>=1.3.23',
        'selenium>=3.141.0',
        'lxml>=4.6.2',
        'webdriver_manager>=3.3.0',
    ],
)
