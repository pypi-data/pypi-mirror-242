from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()

setup(
    name="aiodgram",
    version="0.1.0",
    author="Darkangel",
    author_email="fvovva@gmail.com",
    description="This library from easy work with aiogram",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["aiogram>=2.23.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="telegram aiogram",
    python_requires=">=3.6",

)