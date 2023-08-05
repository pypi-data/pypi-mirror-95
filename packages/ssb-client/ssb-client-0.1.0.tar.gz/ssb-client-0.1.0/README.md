# Secure Scuttlebutt (SSB) Client in Python

**WORK IN PROGRESS**

This is a fork of the unmaintained [pyssb repo](https://github.com/pferreir/pyssb).

Things that are currently implemented:

 * Basic Message feed logic
 * Secret Handshake
 * packet-stream protocol

Usage (requires [Poetry](https://python-poetry.org/)):

```
poetry install
PYTHONPATH=. poetry run python3 examples/test_client.py
```
