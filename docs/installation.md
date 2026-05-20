# Installation

## Requirements

- Python 3.8 or newer
- Operating system: Linux, macOS, or Windows

## Install from PyPI

```bash
pip install pricehub
```

This installs the latest stable release along with required dependencies (`pandas`, `pydantic`, `arrow`, `requests`).

## Optional Dependencies

For exporting to Parquet:

```bash
pip install pyarrow      # recommended
# or
pip install fastparquet
```

For plotting examples shown later in the documentation:

```bash
pip install matplotlib plotly
```

## Install from Source

If you want the development version or plan to contribute:

```bash
git clone https://github.com/eslazarev/pricehub.git
cd pricehub
pip install -e .
```

## Verify Installation

```python
from pricehub import get_ohlc

df = get_ohlc("binance_spot", "BTCUSDT", "1d", "2024-10-01", "2024-10-03")
print(df.head())
```

If you see a DataFrame with OHLC columns, you're ready to go.
