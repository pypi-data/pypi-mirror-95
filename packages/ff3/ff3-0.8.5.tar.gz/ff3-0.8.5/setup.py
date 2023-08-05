import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ff3",
    version="0.8.5",
    author="Schoening Consulting, LLC",
    author_email="bschoeni+llc@gmail.com",
    description="Format Preserving Encryption (FPE) with FF3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bschoeni/fpe",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
