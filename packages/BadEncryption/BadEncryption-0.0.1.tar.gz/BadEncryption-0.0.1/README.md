# Bad-Encryption
Python package to use encryption, bad encryption.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BadEncryption.

```bash
pip install BadEncryption
```

## Usage

```python
import BadEncryption

BadEncryption.vbh('hello') # returns -1267296259
BadEncryption.rotate('hello', 13) # returns 'uryyb'
```