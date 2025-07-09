#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ip-geolocation-tool",
    version="1.0.0",
    author="Nezukomi",
    author_email="nezukomi@my.id",
    description="Una herramienta avanzada para localizar direcciones IP usando múltiples fuentes públicas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nezukomii/ip-geolocation-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "iplocator=main:main",
        ],
    },
    keywords="ip geolocation location tracking network security",
    project_urls={
        "Bug Reports": "https://github.com/nezukomii/ip-geolocation-tool/issues",
        "Source": "https://github.com/nezukomii/ip-geolocation-tool",
        "Documentation": "https://github.com/nezukomii/ip-geolocation-tool/blob/main/README.md",
    },
)