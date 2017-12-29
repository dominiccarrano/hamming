# hamming
Implementation of Hamming codes for detecting up to 2 errors and correcting up to 1 error. These are known as "SECDED" (Single Error Correction, Double Error Detection) codes and are extremely popular in computer memmory for handling random errors. For example, RAID 2 uses Hamming codes for its parity.

Files
hamming.py: The implementation. The two functions encode() and decode() form the main API; the rest are helper functions.
tests.py:   A set of unit tests written while implementing hamming.py to verify its functionality.

This implementation is geared toward generality, i.e. allowing the user to encode/decode bitstrings of (nearly) arbitrary length, and requires they be passed in as Python bitarray objects. An alternative implemenation might focus on 
