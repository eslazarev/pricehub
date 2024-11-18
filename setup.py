from setuptools import setup, find_packages


package_name = "pricehub"


setup(
    name=package_name,
    version="0.0.3.11",
    packages=find_packages(),
    author="Evgenii Lazarev",
    author_email="elazarev@gmail.com",
    project_urls={
        "GitHub": "https://github.com/eslazarev",
        "LinkedIn": "https://www.linkedin.com/in/elazarev",
    },
    description="Pricehub: Unified Python Package for Collecting OHLC Prices from Binance, Bybit, and Coinbase APIs into a DataFrame",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Development Status :: 3 - Alpha",
        "Topic :: Office/Business",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Natural Language :: English",
    ],
    url="https://github.com/eslazarev/pricehub",
    install_requires=[
        "pandas",
        "pydantic>=2.0.1",
        "arrow>=1.0.0",
        "requests",
    ],
    python_requires=">=3.8",
    keywords="OHLC OHLCV prices binance bybit coinbase trading  finance quant algotrading cryptocurrency "
    "crypto futures spot broker exchange market quantitative historical candlestick back-testing dataframe",
)
