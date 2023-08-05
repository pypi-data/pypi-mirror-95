![codecov](https://codecov.io/gh/johnpaulkiser/lamport-256/branch/main/graph/badge.svg?token=ZWIK9EVZ3N)
![tests](https://github.com/johnpaulkiser/lamport-256/workflows/tests/badge.svg)
![upload to pypi](https://github.com/johnpaulkiser/lamport-256/workflows/upload%20to%20pypi/badge.svg)

# lamport-256
Simple single use Lamport signature scheme in python

_Great for building toy blockchains and the like._

**DO NOT use in a security conscious production environment!** 


## Usage:
### Library

To install run 
```bash
> pip install lamport-256
```

Import
```python
import lamport_256
```

Generate a private/public key pair
```python
key_pair = lamport_256.generate_keys()
private_key = key_pair.priv
public_key = key_pair.pub
```

> _from here on out the library functions will appear as if they were imported directly e.g. `from lamport_256 import sign_message`_

Sign a message
```python
signature = sign_message(private_key, 'Hello, World')
```

Verify a message
```python
if not verify_signature(public_key, 'Hello, World', signature):
    raise Exception('Invalid signature')
```

Dump keys to files
```python
# together
export_key_pair(key_pair, 'pub.key', 'priv.key') #filenames can be named anything you'd like

# or individually:
export_key(key_pair.priv, 'priv.key')
```

Read keys from file
```python
# together
key_pair = parse_key_pair('location/of/pub.key', 'location/of/priv.key')

# or individually:
pub = parse_key('pub.key')
```

_____
### CLI

Although you can simply run `python location/to/lamport_256.py generate_keys`, it's best to create an alias to run the python script.
```bash
# In your .bashrc or equivalent
alias lamp='python location/of/lamport_256.py'
```

Now you can run the script more concisely
```bash
lamp generate_keys
```

To specify where to save keys use the appropriate options
```bash
lamp generate_keys --priv location/to/save/key --pub location/to/save/key
```

Sign a message
```bash
lamp sign --priv location/of/private/key --msg 'Hello, world' > signature.txt

# or pass the message in as a file
lamp sign --priv location/of/private/key --msg location/of/message > signature.txt
```

Verify a signature
```bash
lamp verify --pub location/of/public/key --msg 'message' --sig location/of/signature 

# you can pass the message as a file here as well
lamp verify --pub location/of/public/key --msg location/of/message --sig location/of/signature 
```
