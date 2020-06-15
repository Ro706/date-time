from time import time, ctime
 
prev_time = ""
while True:
    the_time = ctime(time())
    if prev_time != the_time:
        print "The time is:", ctime(time())
        prev_time = the_time
