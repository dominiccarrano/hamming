"""
File:		hamming.py
Author:		Dominic Carrano (carrano.dominic@gmail.com)
Created:	December 18, 2017

Implementation of Hamming single error correction, double error detection
(SECDED) codes for bitstrings, which are represented as Python bitarrays.

For more, see: 
https://en.wikipedia.org/wiki/Hamming_code
https://en.wikipedia.org/wiki/Hamming_code#Hamming_codes_with_additional_parity_(SECDED)
"""

from bitarray import bitarray
from math import floor, ceil, log2

BITS_PER_BYTE = 8

# CORE API

def encode(data):
	"""
	Takes in a bitstring of data and returns a new bitstring composed of the original
	data and Hamming even parity bits for SECDED encoding.

	Parameters
	data: The data bitsting to encode.
	"""
	# cache due to constant reuse
	data_length     = len(data) 
	num_parity_bits = num_parity_bits_needed(data_length)
	encoded_length  = data_length + num_parity_bits + 1 # need plus 1 for parity bit over entire sequence

	# the Hamming SECDED encoded bitstring
	encoded = bitarray(encoded_length) 
	
	# set parity bits
	for parity_bit_index in powers_of_two(num_parity_bits):
		encoded[parity_bit_index] = calculate_parity(data, parity_bit_index)
	
	# set data bits
	data_index = 0
	for encoded_index in range(3, len(encoded)): # start at 3 instead of 1 to skip first two parity bits
		if not is_power_of_two(encoded_index):
			encoded[encoded_index] = data[data_index]
			data_index += 1

	# compute and set overall parity for the entire encoded data, not including the overall parity bit itself
	encoded[0] = calculate_parity(encoded[1:], 0)

	# all done!
	return encoded

def decode(encoded):
	"""
	Takes in a Hamming SECDED encoded bitstring and returns the original data bitstring,
	correcting single errors (with no reporting) and reporting if two errors are found.

	Parameters
	encoded: The parity-encoded bitsting to decode.

	Throws
	ValueError: if two errors are detected.
	"""
	encoded_length  = len(encoded)
	num_parity_bits = int(log2(encoded_length))
	index_of_error  = 0 # the bit in error

	# the original data bits, which may be corrupted
	decoded = extract_data(encoded)

	# check overall parity
	overall_expected = calculate_parity(encoded[1:], 0)
	overall_actual   = encoded[0]
	overall_correct  = overall_expected == overall_actual

	# check individual parities
	for parity_bit_index in powers_of_two(num_parity_bits):
		expected = calculate_parity(decoded, parity_bit_index)
		actual   = encoded[parity_bit_index]
		if not expected == actual:
			index_of_error += parity_bit_index

	# report results
	if index_of_error and overall_correct:          # two errors found
		raise ValueError("Two errors detected.")
	elif index_of_error and not overall_correct:    # one error found - flip the bit in error and we're good
		encoded[index_of_error] = not encoded[index_of_error]

	decoded = extract_data(encoded)                 # extract new, corrected data and return it
	return decoded

# HELPER FUNCTIONS

def num_parity_bits_needed(length):
	"""
	Returns the number of parity bits needed for a bitstring of size length, NOT
	inclduing the parity bit over the entire sequence for double detection.
	"""
	n = next_power_of_two(length)
	lower_bin = floor(log2(n))
	upper_bin = lower_bin + 1
	data_bit_boundary = n - lower_bin - 1					
	return lower_bin if length <= data_bit_boundary else upper_bin

def calculate_parity(data, parity):
	"""
	Calculates the specified Hamming parity bit (1, 2, 4, 8, etc.) for the given data.
	Assumes even parity to allow for easier computation of parity using XOR.

	If 0 is passed in to parity, then the overall parity is computed - that is, parity over
	the entire sequence.
	"""
	retval = 0 # 0 is the XOR identity

	if parity == 0: # special case - compute the overall parity
		for bit in data:
			retval ^= bit
	else:
		for data_index in data_bits_covered(parity, len(data)):
			retval ^= data[data_index]
	return retval

def data_bits_covered(parity, lim):
	"""
	Yields the indices of all data bits covered by a specified parity bit in a bitstring
	of length lim. The indices are relative to DATA BITSTRING ITSELF, NOT including
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

def extract_data(encoded):
	"""
	Assuming encoded is a Hamming SECDED encoded bitstring, returns the substring that is the data bits.
	"""
	data = bitarray()
	for i in range(3, len(encoded)):
		if not is_power_of_two(i):
			data.append(encoded[i])
	return data

def next_power_of_two(x):
	"""
	Given an integer x, returns the next power of two after x.

	>>> next_power_of_two(768)
	1024
	>>> next_power_of_two(4)
	8
	>>> next_power_of_two(3)
	4
	"""
	if (not (type(x) == int)) or (x <= 0):
		raise ValueError("Argument must be a positive integer.")
	elif is_power_of_two(x):
		return x << 1
	return 2 ** ceil(log2(x))

def is_power_of_two(n):
	"""
	Returns true if the given non-negative integer n is a power of two.
	Algorithm credit: https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2
	"""
	return (not (n == 0)) and ((n & (n - 1)) == 0)

def powers_of_two(n):
	"""
	Yields the first n powers of two.

	>>> [x for x in powers_of_two(5)]
	[1, 2, 4, 8, 16]
	"""
	power, i = 1, 0
	while i < n:
		yield power
		power <<= 1
		i += 1
	return None

def bytes_to_bits(byte_stream):
	"""
	Converts the given bytearray to a bitarray by converting  each successive byte into its 
	appropriate binary data bits and appending them to the bitarray.
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

	Assumes the last len(bits) - len(bits) / 8 * 8 bits are to  be interpreted as the least 
	significant bits of the last byte of data, e.g. 0b100 would map to the byte 0b00000100.
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
