import pathlib

import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name="jupdoc",
    version="0.1.4",
    scripts=["jupdoc/convert.py", "jupdoc/main.py"],
    author="Ashish Papanai",
    author_email="ashishp@wadhwaniai.org",
    description="A package to convert Jupyter Notebooks to Word Documents (and other quarto supported formats) and upload them to Google Drive, with support for multiple user roles, using Quarto.",
    long_description=README,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/wadhwaniAI/jupdoc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "nbconvert",
        "nbformat",
        "PyYAML",
        "setuptools",
        "coloredlogs",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "google-auth",
        "google-api-core",
    ],
    entry_points={"console_scripts": ["jupdoc=jupdoc.__main__:main"]},
)
