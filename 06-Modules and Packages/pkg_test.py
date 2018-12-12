from mymath import prime
from mymath.geometry import cube

a = 19
b = 1042
c = 100

print(f"It's {prime.is_prime(a)} that {a} is a prime number")
print(f"It's {prime.is_prime(b)} that {b} is a prime number")

print(f"There are {prime.count_primes(c)} prime numbers in range up to {c}")

cube_side = 5

print(f"If side length of the cube equals to {cube_side} cm, then its sutface \
square is {cube.cube_surface_sqr(cube_side)} (sq. cm) and its volume is \
{cube.cube_volume(cube_side)} (cub. cm)")
