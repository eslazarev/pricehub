from setuptools import setup, find_packages


package_name = "pricehub"


setup(
    name=package_name,
    version="0.0.3",
    packages=find_packages(),
    author="Evgenii Lazarev",
    author_email="elazarev@gmail.com",
    project_urls={
        "GitHub": "https://github.com/eslazarev/pricehub",
        "LinkedIn": "https://www.linkedin.com/in/elazarev",
    },
    description="Open-High-Low-Close (OHLC) prices data from brokers: binance (spot, futures), bybit (spot, )",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/eslazarev/pricehub",
    install_requires=[
        "pandas",
        "pydantic>=2.0.1",
        "arrow>=1.0.0",
        "requests",
    ],
)
