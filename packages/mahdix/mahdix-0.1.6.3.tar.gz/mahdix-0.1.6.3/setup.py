from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mahdix",
    version='0.1.6.3',
    author="Mahdi Hasan Shuvo",
    author_email="shvo.mex@gmail.com",
    url="https://www.facebook.com/bk4human",
    description="An application that informs you of the differents Moduls and vesry easy use it in short aways",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["click", "pytz"],
    entry_points={"console_scripts": ["cloudquicklabs1 = src.main:main"]},
)
