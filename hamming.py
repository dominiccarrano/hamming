"""
File:		hamming.py
Author:		Dominic Carrano (carrano.dominic@gmail.com)
Created:	December 18, 2017

Implementation of Hamming single error correction, double error detection
(SECDED) codes for bitstrings. Supports encoding of bit and bytearrays as
a bitarray, as well as error detection/correction of bitarrays to decode.
"""

import bitarray

BITS_PER_BYTE = 8

def encode(bits):
	"""
	Returns a new bitarray with the added parity bits for even parity.

	>>> from bitarray import bitarray
	>>> msg = bytes_to_bits(bytearray(b'\x48\x69\x21')) # "Hi!"
	>>> msg_with_parity = encode(msg)
	>>> msg
	bitarray('010010000110100100010001')
	>>> msg_with_parity
	bitarray('') ???
	"""
	pass

def decode(bits):
	pass

def data_bits_covered(parity, lim):
	"""
	Generator that yields all data bit indices covered by the given parity
	bit index in the range [1, lim]. Note that all hamming parity bits are
	placed at powers of two, so it only makes sense to generate the indices
	for such parities, e.g. parity 1, 2, 4, 8, ...

	>>> [print(x) for x in data_bits_covered(1, 6)]
	1
	3
	5
	[None, None, None]
	"""
	if not is_power_of_two(parity):
		raise ValueError("All hamming parity bits are indexed by powers of two.")

	i = parity
	while i <= lim:
		if (i % (parity << 1)) >= parity:
			yield i # TODO: Need to convert from total index (i.e. index including parity bits) to just data index and call it in the yield expression. Write helper!!
		i += 1
	return None

def is_power_of_two(n):
	"""
	Returns true if the given non-negative integer n is a power of two.
	Algorithm credit: https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
	"""
	return (not (n == 0)) and ((n & (n - 1)) == 0)

def bytes_to_bits(byte_stream):
	"""
	Converts the given bytearray byte_stream to a bitarray by converting 
	each successive byte into its appropriate BITS_PER_BYTE binary data bits 
	and appending them to the bitarray.

	>>> from bitarray import bitarray
	>>> foo = bytearray(b'\x11\x23\x6C')
	>>> bytes_to_bits(foo)
	bitarray('000100010010001101101100')
	"""
	out = bitarray.bitarray()
	for byte in byte_stream:
		data = bin(byte)[2:].zfill(BITS_PER_BYTE)
		for bit in data:
			out.append(0 if bit == '0' else 1) # note that all bits go to 1 if we just append bit, since it's a non-null string
	return out

def bits_to_bytes(bits):
	"""
	Converts the given bitarray bits to a bytearray. 

	Assumes the last len(bits) - len(bits) / 8 * 8 bits are to 
	be interpreted as the least significant bits of the last byte 
	of data, e.g. 100 would map to the byte 00000100.

	>>> from bitarray import bitarray
	>>> foo = bitarray('100')
	>>> bits_to_bytes(foo)
	bytearray(b'\x04')
	>>> bar = bitarray('1010110011111111001100011000')
	>>> bits_to_bytes(bar)
	bytearray(b'\xAC\xFF\x31\x08')
	"""
	out = bytearray()
	for i in range(0, len(bits) // BITS_PER_BYTE * BITS_PER_BYTE, BITS_PER_BYTE):
		byte, k = 0, 0
		for bit in bits[i:i + BITS_PER_BYTE][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	# tail case
	if len(bits) % BITS_PER_BYTE:
		byte, k = 0, 0
		for bit in bits[int(len(bits) // BITS_PER_BYTE * BITS_PER_BYTE):][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	return out