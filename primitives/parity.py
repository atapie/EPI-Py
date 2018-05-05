import random
import time

# Assuming input is a unsigned 64-bit integer
MAX_VALUE = 2 ** 64 - 1

def parity( input ):
	assert input >= 0 and input <= MAX_VALUE
	res = 0
	while input:
		res ^= 1
		input &= input - 1
	
	return res
	
def parityLogN( input ):
	assert input >= 0 and input <= MAX_VALUE
	input ^= input >> 32
	input ^= input >> 16
	input ^= input >> 8
	input ^= input >> 4
	input ^= input >> 2
	input ^= input >> 1
	return input & 1

cache = {}
for i in range( 0x10000 ):
	cache[ i ] = parityLogN( i )

def parityWithCache( input ):
	assert input >= 0 and input <= MAX_VALUE
	return cache[ input >> 56 ] ^ \
				 cache[ ( input >> 48 ) & 0xff ] ^ \
				 cache[ ( input >> 40 ) & 0xff ] ^ \
				 cache[ ( input >> 32 ) & 0xff ] ^ \
				 cache[ ( input >> 24 ) & 0xff ] ^ \
				 cache[ ( input >> 16 ) & 0xff ] ^ \
				 cache[ ( input >> 8 ) & 0xff ] ^ \
				 cache[ input & 0xff ]
	
def parityWithCache2( input ):
	assert input >= 0 and input <= MAX_VALUE
	return cache[ input >> 48 ] ^ \
				 cache[ ( input >> 32 ) & 0xffff ] ^ \
				 cache[ ( input >> 16 ) & 0xffff ] ^ \
				 cache[ input & 0xffff ]
				 
if __name__ == '__main__':
	samples = [ random.randint( 0, MAX_VALUE ) for _ in range( 100000 ) ]

	for parityFunc in [ parity, parityLogN, parityWithCache, parityWithCache2 ]:
		# Sanity check
		assert parityFunc( 0 ) == 0
		assert parityFunc( 1 ) == 1
		assert parityFunc( 0b1100 ) == 0
		assert parityFunc( 0b1111100 ) == 1
		assert parityFunc( 0b1010010 ) == 1
		assert parityFunc( 0b1011010 ) == 0
		assert parityFunc( 0xffff ) == 0
		
		for invalidInput in [ -1, 2 ** 64 ]:
			try:
				parityFunc( invalidInput )
			except AssertionError:
				pass
			else:
				assert False, 'Should assert on invalid input'
		
		start = time.time()
		for input in samples:
			parityFunc( input )
			
		end = time.time()
		print( parityFunc.__name__, 'execution time for', len(samples), 'inputs is', end - start )

	# Sanity check
	for input in samples:
		assert parity( input ) == parityLogN( input )
		assert parity( input ) == parityWithCache( input )
		assert parity( input ) == parityWithCache2( input )
