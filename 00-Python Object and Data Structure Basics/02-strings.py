my_str = "0123456789"
print("my_str = " + my_str)
print("my_str length = " + str(len(my_str)))

#Indexing
print("the first 5 chars of my_str = " + my_str[0:5])
print("every 2nd char of my_str = " + my_str[::2])
print("the last char of my_str (using len) = " + my_str[len(my_str) - 1])
print("the last char of my_str (using -) = " + my_str[-1])
print("every 3rd char of my_str before '6' = " + my_str[0:-4:3])
