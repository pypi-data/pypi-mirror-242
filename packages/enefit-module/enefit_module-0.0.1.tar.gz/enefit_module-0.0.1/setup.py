import setuptools
 
with open("README.md", "r", encoding='UTF8') as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="enefit_module",
    version="0.0.1",
    author="WTMO",
    author_email="wtmo_dev@naver.com",
    description="Package of enefit_module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)