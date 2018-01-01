"""
File:		tests.py
Author:		Dominic Carrano (carrano.dominic@gmail.com)
Created:	December 19, 2017

Suite of unit tests for functions in hammming.py.
Each test returns a tuple of (# tests failed, textual info about the failure).
"""
from bitarray import bitarray
from sys import stderr, stdout
import hamming

N_TESTS = 25 # total number of unit tests

# tests for hamming.bits_to_bytes

def bits_to_bytes_test1():
	foo = bitarray('100')
	actual = hamming.bits_to_bytes(foo)
	expected = bytearray(b'\x04')
	return (0, "") if actual == expected else (1, "bits_to_bytes_test1 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bits_to_bytes_test2():
	bar = bitarray('1010110011111111001100011000')
	actual = hamming.bits_to_bytes(bar)
	expected = bytearray(b'\xAC\xFF\x31\x08')
	return (0, "") if actual == expected else (1, "bits_to_bytes_test2 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bits_to_bytes_test3():
	baz = bitarray('')
	actual = hamming.bits_to_bytes(baz)
	expected = bytearray(b'')
	return (0, "") if actual == expected else (1, "bits_to_bytes_test3 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bits_to_bytes_test4():
	# make sure extra zero byte isn't appended for byte-length data
	fubar = bitarray('10010110')
	actual = hamming.bits_to_bytes(fubar)
	expected = bytearray(b'\x96')
	return (0, "") if actual == expected else (1, "bits_to_bytes_test4 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bits_to_bytes_tests():
	a = bits_to_bytes_test1()
	b = bits_to_bytes_test2()
	c = bits_to_bytes_test3()
	d = bits_to_bytes_test4()
	return (a[0] + b[0] + c[0] + d[0], a[1] + b[1] + c[1] + d[1])

# tests for hamming.bytes_to_bits

def bytes_to_bits_test1():
	foo = bytearray(b'\x11\x23\x6C')
	actual = hamming.bytes_to_bits(foo)
	expected = bitarray('000100010010001101101100')
	return (0, "") if actual == expected else (1, "bytes_to_bits_test1 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bytes_to_bits_test2():
	bar = bytearray(b'\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21')
	actual = hamming.bytes_to_bits(bar)
	expected = bitarray('01001000011001010110110001101100011011110010110000100000010101110110111101110010011011000110010000100001')
	return (0, "") if actual == expected else (1, "bytes_to_bits_test2 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bytes_to_bits_test3():
	# "All functions should have proper, well-defined behavior for zero or null input." - K&R
	baz = bytearray(b'')
	actual = hamming.bytes_to_bits(baz)
	expected = bitarray('')
	return (0, "") if actual == expected else (1, "bytes_to_bits_test3 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def bytes_to_bits_tests():
	a = bytes_to_bits_test1()
	b = bytes_to_bits_test2()
	c = bytes_to_bits_test3()
	return (a[0] + b[0] + c[0], a[1] + b[1] + c[1])

# tests for hamming.data_bits_covered

def data_bits_covered_test1():
	actual = [x for x in hamming.data_bits_covered(1, 14)]
	expected = [0, 1, 3, 4, 6, 8, 10, 11, 13]
	return (0, "") if actual == expected else (1, "data_bits_covered_test1 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test2():
	actual = [x for x in hamming.data_bits_covered(2, 7)]
	expected = [0, 2, 3, 5, 6]
	return (0, "") if actual == expected else (1, "data_bits_covered_test2 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test3():
	actual = [x for x in hamming.data_bits_covered(1, 33)]
	expected = [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25, 26, 28, 30, 32]
	return (0, "") if actual == expected else (1, "data_bits_covered_test3 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test4():
	actual = [x for x in hamming.data_bits_covered(1, 1)]
	expected = [0]
	return (0, "") if actual == expected else (1, "data_bits_covered_test4 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test5():
	actual = [x for x in hamming.data_bits_covered(2, 1)]
	expected = [0]
	return (0, "") if actual == expected else (1, "data_bits_covered_test5 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test6():
	actual = [x for x in hamming.data_bits_covered(4, 1)]
	expected = []
	return (0, "") if actual == expected else (1, "data_bits_covered_test6 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test7():
	actual = [x for x in hamming.data_bits_covered(4, 15)]
	expected = [1, 2, 3, 7, 8, 9, 10, 14]
	return (0, "") if actual == expected else (1, "data_bits_covered_test7 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test8():
	actual = [x for x in hamming.data_bits_covered(4, 14)]
	expected = [1, 2, 3, 7, 8, 9, 10]
	return (0, "") if actual == expected else (1, "data_bits_covered_test8 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test9():
	actual = [x for x in hamming.data_bits_covered(8, 13)]
	expected = [4, 5, 6, 7, 8, 9, 10]
	return (0, "") if actual == expected else (1, "data_bits_covered_test9 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test10():
	actual = [x for x in hamming.data_bits_covered(8, 3)]
	expected = []
	return (0, "") if actual == expected else (1, "data_bits_covered_test10 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test11():
	actual = [x for x in hamming.data_bits_covered(16, 11)]
	expected = []
	return (0, "") if actual == expected else (1, "data_bits_covered_test11 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_test12():
	actual = [x for x in hamming.data_bits_covered(16, 24)]
	expected = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	return (0, "") if actual == expected else (1, "data_bits_covered_test12 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def data_bits_covered_tests():
	a = data_bits_covered_test1()
	b = data_bits_covered_test2()
	c = data_bits_covered_test3()
	d = data_bits_covered_test4()
	e = data_bits_covered_test5()
	f = data_bits_covered_test6()
	g = data_bits_covered_test7()
	h = data_bits_covered_test8()
	i = data_bits_covered_test9()
	j = data_bits_covered_test10()
	k = data_bits_covered_test11()
	l = data_bits_covered_test12()
	return (a[0] + b[0] + c[0] + d[0] + e[0] + f[0] + g[0] + h[0] + i[0] + j[0] + k[0] + l[0], \
		a[1] + b[1] + c[1] + d[1] + e[1] + f[1] + g[1] + h[1] + i[1] + j[1] + k[1] + l[1])

# tests for hamming.encode

def encode_test1():
	data     = bitarray('0011')
	actual   = hamming.encode(data)
	expected = bitarray('11000011')	# p1 = 1, p2 = 0, p4 = 0, overall = 1
	return (0, "") if actual == expected else (1, "encode_test1 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def encode_test2():
	data     = bitarray('01100100110')
	actual   = hamming.encode(data)
	expected = bitarray('1010011010100110') # p1 = 0, p2 = 1, p4 = 0, p8 = 1, overall = 1
	return (0, "") if actual == expected else (1, "encode_test2 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def encode_test3():
	data     = bitarray('0011')
	actual   = hamming.encode(data)
	expected = bitarray('11000011') # p1 = 1, p2 = 0, p4 = 0, overall = 1
	return (0, "") if actual == expected else (1, "encode_test3 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def encode_tests():
	a = encode_test1()
	b = encode_test2()
	c = encode_test3()
	return (a[0] + b[0] + c[0], a[1] + b[1] + c[1])

# tests for hamming.decode

def decode_test1():
	encoded  = bitarray('00110111') # bit 5 in error
	actual   = hamming.decode(encoded)
	expected = bitarray('1011') 
	return (0, "") if actual == expected else (1, "decode_test1 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def decode_test2():
	encoded  = bitarray('11001000') # bit 5 in error
	actual   = hamming.decode(encoded)
	expected = bitarray('0100') 
	return (0, "") if actual == expected else (1, "decode_test2 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def decode_test3():
	encoded  = bitarray('1010011010000110') # bit 10 in error
	actual   = hamming.decode(encoded)
	expected = bitarray('01100100110') 
	return (0, "") if actual == expected else (1, "decode_test3 FAILED! Expected: {0}, Actual: {1}\n".format(expected, actual))

def decode_tests():
	a = decode_test1()
	b = decode_test2()
	c = decode_test3()
	return (a[0] + b[0] + c[0], a[1] + b[1] + c[1])

# put it all together

def run_tests():
	a = bits_to_bytes_tests()
	b = bytes_to_bits_tests()
	c = data_bits_covered_tests()
	d = decode_tests()
	e = encode_tests()
	return (a[0] + b[0] + c[0] + d[0] + e[0], a[1] + b[1] + c[1] + d[1] + e[1])

def main():
	total_failed, error_output = run_tests()
	if total_failed:
		stderr.write(error_output)
		stderr.write("{0} of {1} test cases passed. {2} tests failed.\n".format(N_TESTS - total_failed, N_TESTS, total_failed))
		exit(1)
	stdout.write("All {0} test cases passed!\n".format(N_TESTS))
	return None

if __name__ == '__main__':
	main()