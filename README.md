# hamming
Implementation of Hamming codes for detecting up to 2 errors and correcting up to 1 error in a data bitstring. These are known as "SECDED" (Single Error Correction, Double Error Detection) codes and are extremely popular in computer memory for handling random errors. For example, RAID-2 uses Hamming codes for its parity.

This implementation is geared toward generality, i.e. allowing the user to encode/decode bitstrings of up to 1013 bits in length, and requires they be passed in as Python bitarray objects. An alternative implemenation might focus on implementing a specific block-size Hamming code (e.g. the popular Hamming(7, 4) code) or take the linear algebra approach to such an implementation but here we focus on a more general version.


**Files**

**hamming.py**: The implementation. The two functions encode() and decode() form the main API; the rest are helper functions.

**tests.py**:   A set of unit tests written while implementing hamming.py to verify its functionality.
