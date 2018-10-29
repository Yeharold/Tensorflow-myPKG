from setuptools import setup, find_packages

setup(
    name="cutImg",
    version="2.0",
    license="MIT Licence",

    author="YeHarold",
    packages=find_packages(),
    include_package_data=True,
    platforms="linux",
    install_requires=['pillow',"lxml"],

)