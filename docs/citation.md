# Citation

If you use PriceHub in academic work, technical reports, or any published analysis, please cite it. Citation helps demonstrate research uptake and justifies continued maintenance.

## How to Cite

The canonical citation metadata lives in [`CITATION.cff`](https://github.com/eslazarev/pricehub/blob/main/CITATION.cff) at the root of the repository. GitHub renders a "Cite this repository" button in the right sidebar based on this file.

### BibTeX

```bibtex
@software{lazarev_pricehub,
  author       = {Lazarev, Evgenii},
  title        = {{PriceHub: Unified Python Package for Collecting OHLC
                   Prices from Cryptocurrency Exchange APIs}},
  url          = {https://github.com/eslazarev/pricehub},
  license      = {MIT},
  orcid        = {0009-0000-1398-7842}
}
```

Once a DOI is minted via Zenodo, add the `doi` and `version` fields:

```bibtex
@software{lazarev_pricehub_vX_Y_Z,
  author       = {Lazarev, Evgenii},
  title        = {{PriceHub: Unified Python Package for Collecting OHLC
                   Prices from Cryptocurrency Exchange APIs}},
  version      = {X.Y.Z},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX},
  license      = {MIT}
}
```

## Citing a Specific Version

For reproducibility, cite the **version DOI** of the exact PriceHub release you used (not the concept DOI, which always resolves to the latest). The version DOI is shown on the Zenodo record page for each release.

## ORCID

The author's ORCID iD is [0009-0000-1398-7842](https://orcid.org/0009-0000-1398-7842). Zenodo automatically associates DOIs with this profile when ORCID is linked in account settings.

## Acknowledgments in Papers

A suggested phrasing for a methods or data section:

> Historical OHLC data were retrieved via PriceHub (Lazarev, version X.Y.Z, DOI: 10.5281/zenodo.XXXXXXX), a unified Python interface to the public APIs of Binance, Bybit, Coinbase, OKX, Kraken, and KuCoin.
