def is_prime(num):
	for x in range(2, num):
		if num % x == 0:
			return False
	return True

def count_primes(num):
	primes = 0
	for n in range(2, num):
		primes += is_prime(n)
	return primes
