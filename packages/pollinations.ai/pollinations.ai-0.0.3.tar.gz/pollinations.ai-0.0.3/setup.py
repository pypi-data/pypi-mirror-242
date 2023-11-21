from setuptools import setup, find_packages
from pathlib import Path

path_absolute = Path(__file__).parent.absolute()

setup(
    name="pollinations.ai",
    version="0.0.3",
    description="pollinations.ai package api wrapper",
    long_description=Path(f"{path_absolute}/README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://pollinations.ai/",
    author="tlkr.",
    author_email="toolkitr.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pollinations=pollinations.__init__:main",
        ]
    },
    python_requires=">=3.7",    
    keyphrases=['pollinations', 'pollinations.ai', 'pollinations-ai', 'pollinations_ai'],
)