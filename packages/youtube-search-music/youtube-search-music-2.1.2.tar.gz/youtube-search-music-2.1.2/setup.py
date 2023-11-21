import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="youtube-search-music",
    version="2.1.2",
    description="Perform YouTube music video searches using API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DWAA1660/youtube_music_search",
    author="DWAA1660",
    author_email="dwatnip123@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["youtube_search_music"],
    include_package_data=True,
    install_requires=["requests"],
)
