from bitarray import bitarray
import hamming

# tests for hamming.bits_to_bytes

def bits_to_bytes_test1():
	foo = bitarray('100')
	actual = hamming.bits_to_bytes(foo)
	expected = bytearray(b'\x04')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bits_to_bytes_test2():
	bar = bitarray('1010110011111111001100011000')
	actual = hamming.bits_to_bytes(bar)
	expected = bytearray(b'\xAC\xFF\x31\x08')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bits_to_bytes_test3():
	baz = bitarray('')
	actual = hamming.bits_to_bytes(baz)
	expected = bytearray(b'')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bits_to_bytes_test4():
	# make sure extra zero byte isn't appended for byte-length data
	fubar = bitarray('10010110')
	actual = hamming.bits_to_bytes(fubar)
	expected = bytearray(b'\x96')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bits_to_bytes_tests():
	bits_to_bytes_test1()
	bits_to_bytes_test2()
	bits_to_bytes_test3()
	bits_to_bytes_test4()

# tests for hamming.bytes_to_bits

def bytes_to_bits_test1():
	foo = bytearray(b'\x11\x23\x6C')
	actual = hamming.bytes_to_bits(foo)
	expected = bitarray('000100010010001101101100')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bytes_to_bits_test2():
	bar = bytearray(b'\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21')
	actual = hamming.bytes_to_bits(bar)
	expected = bitarray('01001000011001010110110001101100011011110010110000100000010101110110111101110010011011000110010000100001')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bytes_to_bits_test3():
	# "All functions should have proper, well-defined behavior for zero or null input." - K&R
	baz = bytearray(b'')
	actual = hamming.bytes_to_bits(baz)
	expected = bitarray('')
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def bytes_to_bits_tests():
	bytes_to_bits_test1()
	bytes_to_bits_test2()
	bytes_to_bits_test3()

# tests for hamming.data_bits_covered

def data_bits_covered_test1():
	actual = [x for x in hamming.data_bits_covered(1, 14)]
	expected = [0, 1, 3, 4, 6, 8, 10, 11, 13]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test2():
	actual = [x for x in hamming.data_bits_covered(2, 7)]
	expected = [0, 2, 3, 5, 6]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test3():
	actual = [x for x in hamming.data_bits_covered(1, 33)]
	expected = [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25, 26, 28, 30, 32]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test4():
	actual = [x for x in hamming.data_bits_covered(1, 1)]
	expected = [0]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test5():
	actual = [x for x in hamming.data_bits_covered(2, 1)]
	expected = [0]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test6():
	actual = [x for x in hamming.data_bits_covered(4, 1)]
	expected = []
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test7():
	actual = [x for x in hamming.data_bits_covered(4, 15)]
	expected = [1, 2, 3, 7, 8, 9, 10, 14]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test8():
	actual = [x for x in hamming.data_bits_covered(4, 14)]
	expected = [1, 2, 3, 7, 8, 9, 10]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test9():
	actual = [x for x in hamming.data_bits_covered(8, 13)]
	expected = [4, 5, 6, 7, 8, 9, 10]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test10():
	actual = [x for x in hamming.data_bits_covered(8, 3)]
	expected = []
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test11():
	actual = [x for x in hamming.data_bits_covered(16, 11)]
	expected = []
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_test12():
	actual = [x for x in hamming.data_bits_covered(16, 24)]
	expected = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
	assert actual == expected, "TEST FAILED! Expected: {0}, Actual: {1}".format(expected, actual)

def data_bits_covered_tests():
	data_bits_covered_test1()
	data_bits_covered_test2()
	data_bits_covered_test3()
	data_bits_covered_test4()
	data_bits_covered_test5()
	data_bits_covered_test6()
	data_bits_covered_test7()
	data_bits_covered_test8()
	data_bits_covered_test9()
	data_bits_covered_test10()
	data_bits_covered_test11()
	data_bits_covered_test12()

# tests for hamming.encode

def encode_test1():
	pass

def encode_test2():
	pass

def encode_tests():
	encode_test1()
	encode_test2()

# put it all together

def run_tests():
	bits_to_bytes_tests()
	bytes_to_bits_tests()
	data_bits_covered_tests()
	encode_tests()

def main():
	run_tests()
	print("All cases passed.")

if __name__ == '__main__':
	main()