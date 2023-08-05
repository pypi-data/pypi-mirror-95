import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jqpd", 
    version="0.0.1",
    author="Imran Khan",
    author_email="iakhan@utexas.edu",
    description="implementation of jqpd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas', 'numpy', 'scipy'],
    keywords=['python', 'jqpd'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)