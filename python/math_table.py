import sys
number=int(sys.argv[1])
print(f'User given number is(number)')

for i in range(1,21):
    print('%d *% d= %d' % (number,i,number*i))

    '''
    15*1=15
    15*2=30

    '''