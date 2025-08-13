'''




96 to 100 Excellent
Also check for invalid score . no negative marking
'''


average_score=int(input('Enter your average score to print result:'))
if average_score<0 and average_score>100:
    print('Invalid score')
elif average_score>=0 and average_score<=59:
    print('Result is fail')
elif average_score>=60 and average_score<=84:
    print('Result is second class')
elif average_score>=85 and average_score<=95:
    print('Result is first class')
else:
    print('Result is Excellent')
