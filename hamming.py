"""
File:		hamming.py
Author:		Dominic Carrano (carrano.dominic@gmail.com)
Created:	December 18, 2017

Implementation of Hamming single error correction, double error detection
(SECDED) codes for bitstrings. Supports encoding of bit and bytearrays as
a bitarray, as well as error detection/correction of bitarrays to decode.

TODO: Design/implement/test encode(), decode(), and research linear-algebraic
implementation of Hamming codes for potential comparison to current lexicographic method.
"""

from bitarray import bitarray

BITS_PER_BYTE = 8

# CORE API

def encode(data):
	"""
	Takes in a bitstring of data and returns a new bitstring composed of the original
	data and Hamming even parity bits for SECDED encoding.

	data: The data bitsting to encode.
	"""
	# cache due to constant reuse
	data_length = len(data) 
	num_parity_bits = num_parity_bits_needed(data_length)

	# the Hamming SECDED encoded bitstring
	encoded = bitarray(data_length + num_parity_bits + 1) # need plus 1 for parity over entire sequence
	
	# set parity bits
	for parity_bit_index in powers_of_two(num_parity_bits):
		encoded[parity_bit_index] = calculate_parity(data, parity_bit_index)
	
	# set data bits
	data_index = 0
	for encoded_index in range(3, len(encoded)): # start at 3 instead of 1 to skip first two parity bits
		if not is_power_of_two(encoded_index):
			encoded[encoded_index] = data[data_index]
			data_index += 1

	# compute and set parity bit over the whole sequence at position zero (for even parity)
	total_parity = 0
	for i in range(1, len(encoded)):
		total_parity ^= encoded[i]
	encoded[0] = total_parity

	# voila!
	return encoded

def decode(data):
	"""
	Takes in a Hamming SECDED encoded bitstring and returns the original data bitstring,
	correcting single errors and reporting if two errors are found.

	bits: The parity-encoded bitsting to decode.
	"""
	pass


# EVERYTHING BELOW HERE IS A HELPER FUNCTION

def num_parity_bits_needed(length):
	"""
	Returns the number of parity bits needed for a bitstring of size length, not
	inclduing the parity bit over the entire sequence for double detection.
	"""
	# TODO: this is a really lazy implementation.. should probably come back and use
	# a dictionary lookup or try finding a general expression for the # parity bits
	# needed for k data bits in general, although couldn't find such a formula after
	# ~30 mins of searching.
	if type(length) != int or length <= 0:
		raise ValueError("Length must be a positive integer.")
	elif length == 1:
		return 2
	elif length <= 4:
		return 3
	elif length <= 11:
		return 4
	elif length <= 26:
		return 5
	elif length <= 57:
		return 6
	elif length <= 120:
		return 7
	elif length <= 247:
		return 8
	elif length <= 502:
		return 9
	elif length <= 1013:
		return 10
	else:
		raise ValueError("Bitstring length must be no greater than 1013 bits.")

def calculate_parity(data, parity):
	"""
	Calculates the specified Hamming parity bit (1, 2, 4, 8, etc.) for the given data.
	Computing the parity over the entire sequence is left to other functions.
	Assumes even parity to allow for easier computation of parity using XOR.
	"""
	retval = 0 		# 0 is the XOR identity
	for data_index in data_bits_covered(parity, len(data)):
		retval ^= data[data_index]
	return retval

def data_bits_covered(parity, lim):
	"""
	Yields the indices of all data bits covered by a specified parity bit in a bitstring
	of length lim. The indices are relative to just the data bitstring itself, not including
	parity bits.
	"""
	if not is_power_of_two(parity):
		raise ValueError("All hamming parity bits are indexed by powers of two.")

	# use 1-based indexing for simpler computational logic, subtract 1 in body of loop
	# to get proper zero-based result
	data_index  = 1		# the data bit we're currently at
	total_index = 3 	# index of bit if it were in the parity-encoded bitstring - 
						# the first two bits are p1 and p2, so we start at 3

	while data_index <= lim:
		curr_bit_is_data = not is_power_of_two(total_index)
		if curr_bit_is_data and (total_index % (parity << 1)) >= parity:	
			yield data_index - 1						# adjust output to be zero indexed
		data_index += curr_bit_is_data
		total_index += 1
	return None

def is_power_of_two(n):
	"""
	Returns true if the given non-negative integer n is a power of two.
	Algorithm credit: https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
	"""
	return (not (n == 0)) and ((n & (n - 1)) == 0)

def powers_of_two(n):
	"""
	Yields the first n powers of two.

	>>> for x in powers_of_two(5):
	>>> 	print(x)
	1
	2
	4
	8
	16
	"""
	power, i = 1, 0
	while i < n:
		yield power
		power = power << 1
		i += 1
	return None

def bytes_to_bits(byte_stream):
	"""
	Converts the given bytearray byte_stream to a bitarray by converting 
	each successive byte into its appropriate binary data bits and appending 
	them to the bitarray.

	>>> from bitarray import bitarray
	>>> foo = bytearray(b'\x11\x23\x6C')
	>>> bytes_to_bits(foo)
	bitarray('000100010010001101101100')
	"""
	out = bitarray()
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

	# tail case - necessary if bitstring length isn't a multiple of 8
	if len(bits) % BITS_PER_BYTE:
		byte, k = 0, 0
		for bit in bits[int(len(bits) // BITS_PER_BYTE * BITS_PER_BYTE):][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	return out
