import os

print "PA COUNT: " + str(len([x for x in os.listdir(".") if '.py' in x]))
print "TEST COUNT: " + str(len([x for x in os.listdir("tests") if '.txt' in x]))

for filename in [x for x in os.listdir(".") if '.py' in x]:
    if 'assignment1_p1.py' == filename or 'test.py' == filename:
        continue
    for test in [x for x in os.listdir("tests") if '.txt' in x]:
        print (filename + " " +  test)
        os.system("time python " + filename + "< tests/" + test)
        print ""
    

