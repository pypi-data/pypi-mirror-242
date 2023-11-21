import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "unknown"
with open("aifund/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')

setuptools.setup(
    name="aifund",
    version=version,
    author="tiano",
    author_email="silence_hgt@163.com",
    description="AIfund 是基于 Python 的基金量化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silenceTiano/aifund",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
