'''
Program fot testing with pylint
'''

# Variable names should contain > 1 letters

def do_math(number):
	'''
	Function for some number manipulation
	'''
	print(f"The number is {number}")
	print(f"Its square is {number ** 2}")
	print(f"Its square root is {number ** 0.5}")

num = 289
phrase = "Hello World!"
print(phrase)
do_math(num)
