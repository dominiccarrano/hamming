# hamming
Implementation of Hamming codes for detecting up to 2 errors and correcting up to 1 error in a data bitstring. These are known as "SECDED" (Single Error Correction, Double Error Detection) codes and are extremely popular in computer memory for handling random errors. For example, RAID-2 uses Hamming codes for its parity.

This implementation is geared toward generality, i.e. allowing the user to encode/decode bitstrings of arbitrary length, and requires they be passed in as Python bitarray objects. An alternative implemenation might focus on implementing a specific block-size Hamming code (e.g. the popular Hamming(7, 4) code) or take the linear algebra approach to such an implementation but here we focus on a more general version.

**Files**

**hamming.py**: The implementation. The two functions encode() and decode() form the main API; the rest are helper functions.

**tests.py**:   A set of unit tests written while implementing hamming.py to verify its functionality.

Users only need import the encode and decode functions from the hamming module to use it. The code has been verified to pass all 40+ tests in tests.py, so it would be a good idea to run them on one's machine first as well.

A brief example:
```python
>>> from hamming import encode, decode
>>> from bitarray import bitarray
>>> data = bitarray('101010')
>>> data_with_parity = encode(data)
>>> data_with_parity[3] = not data_with_parity
>>> decode(data_with_parity)
bitarray('101010')
```
