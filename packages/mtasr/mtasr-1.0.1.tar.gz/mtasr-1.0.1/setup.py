import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtasr",
    version="1.0.1",
    author="mthreads",
    author_email="yi.liu@mthreads.com",
    description="MT ASR interface for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yiliu-mt/mtasr_examples",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'loguru',
    ],
    python_requires='>=3.6',
)
