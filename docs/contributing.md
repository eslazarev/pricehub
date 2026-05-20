# Contributing

Contributions are welcome — from bug reports to new broker integrations. This page covers the development workflow.

## Reporting Bugs and Requesting Features

Open an issue on [GitHub Issues](https://github.com/eslazarev/pricehub/issues). For bug reports, please include:

- PriceHub version (`pip show pricehub`)
- Python version
- A minimal reproducer (broker, symbol, interval, dates)
- The full exception traceback if applicable

For feature requests, describe the use case rather than the implementation — that lets us evaluate alternatives.

## Development Setup

```bash
git clone https://github.com/eslazarev/pricehub.git
cd pricehub
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e .
pip install mypy black pylint pytest pytest-cov pytest-mock
```

## Running Checks Locally

The CI pipeline runs four checks; reproduce them locally before opening a PR.

```bash
# Type checking
mypy --install-types --non-interactive --explicit-package-bases .

# Linting
pylint pricehub

# Formatting (max line length 120)
black --line-length 120 pricehub tests

# Tests with coverage
pytest --cov=pricehub
```

## Adding a New Broker

1. Add a module under `pricehub/brokers/` modeled on the existing implementations (Binance, Bybit, etc.).
2. Register the broker identifier in the `SupportedBroker` literal.
3. Add unit tests in `tests/` mirroring the structure of existing broker tests, using `pytest-mock` to stub HTTP responses.
4. Update `docs/api.md` with the new broker string and `docs/usage.md` with at least one example.
5. Add the broker to the support matrix in `docs/index.md` and `README.md`.

## Pull Request Checklist

- [ ] Tests added or updated; `pytest` passes locally
- [ ] `mypy`, `pylint`, `black` all pass
- [ ] Documentation updated for any user-facing changes
- [ ] PR description explains the *why* of the change, not only the *what*

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to abide by its terms.

## License

By contributing to PriceHub you agree that your contributions will be licensed under the [MIT License](https://github.com/eslazarev/pricehub/blob/main/LICENSE), matching the project's license.
