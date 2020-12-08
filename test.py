"""
    test.py
"""



while True:
    line = input('> ')
    if line[0] == '+':
        print('do not')
        continue
    if line == 'done':
        break
    print(line)
print('Done!')