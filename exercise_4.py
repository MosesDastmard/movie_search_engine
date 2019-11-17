import time
from itertools import combinations

sequence = input('First algorithm implementation. Please insert a string: ')

start_time = time.time()

count = set()
done = False
for i in range(len(sequence), 1, -1):
    if (time.time() - start_time) > 10:
        break
    subsequences = list(combinations(sequence, i))
    for k in range(len(subsequences)):
        if subsequences[k] == subsequences[k][::-1]:
            count.add(len(subsequences[k]))
            done = True
            break
    if done: break

try:
    print('The longest palindromic subsequence has length: ' + str(max(count)))
except ValueError:
    print('There is no palindromic sequence or the elapsed time was higher than 10 seconds.')
    

elapsed_time = time.time() - start_time

print('The algorithm took approximately ' + str(round(elapsed_time, 2)) + ' seconds.')

def palindrome(sequence, i, j): 
    if (i == j): 
        return 1
    if (sequence[i] == sequence[j] and i + 1 == j): 
        return 2
    if (sequence[i] == sequence[j]): 
        return palindrome(sequence, i + 1, j - 1) + 2
    return max(palindrome(sequence, i, j - 1), palindrome(sequence, i + 1, j)) 

sequence = input('Second algorithm implementation. Please insert a string: ')
   
start_time = time.time()

length = len(sequence) 

if int(length) < 27:
    print("The longest palindromic subsequence has length: ", palindrome(sequence, 0, length - 1)) 
else:
    print('It would take too much time.')

elapsed_time = time.time() - start_time

print('The algorithm took approximately ' + str(round(elapsed_time, 2)) + ' seconds.')

sequence = input('Third algorithm implementation. Please insert a string: ') 

start_time = time.time()

table = [[1 for x in range(len(sequence))] for x in range(len(sequence))] 

for i in range(len(sequence)): 
    table[i][i] = 1

for substring_length in range(2, len(sequence) + 1): 
    for i in range(len(sequence)-substring_length + 1): 
        j = i + substring_length-1
        if sequence[i] == sequence[j] and substring_length == 2: 
            table[i][j] = 2
        elif sequence[i] == sequence[j]: 
            table[i][j] = table[i + 1][j-1] + 2
        else: 
            table[i][j] = max(table[i][j-1], table[i + 1][j])

print("The longest palindromic subsequence has length: " + str(table[0][len(sequence)-1])) 

elapsed_time = time.time() - start_time

print('The algorithm took approximately ' + str(round(elapsed_time, 2)) + ' seconds.')