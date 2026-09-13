#Kaeleana Ramirez
#GEOG 676 - Lab 2
#Practicing loops w/ lists

#Part 1: Multiply every value in the list
multiplication_numbers = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
multiplication_answer = 1
for current_number in multiplication_numbers:
    multiplication_answer = multiplication_answer * current_number
print("My answer for Part 1 is:", multiplication_answer)

#Part 2: Add every value in the list
addition_numbers = [-1, 23, 483, 8573, -13847,-381569, 1652337, 718522177]
addition_answer = 0
for current_number in addition_numbers:
    addition_answer = addition_answer + current_number
print("My answer for Part 2 is:", addition_answer)

#Part3: Add only the even values
mixed_numbers = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21]
even_number_answer = 0
for current_number in mixed_numbers:
    if current_number % 2 == 0:
        even_number_answer = even_number_answer + current_number
print("Myanswer for Part 3 is:", even_number_answer)