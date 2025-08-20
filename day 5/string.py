def find(string,sub,start=0,end=none):
	    if end is none:
			end=len(string)
		if start<0:
	      start=0
		if end>len(string):
		   end=len(string)
		for i in range(start,end-len(sub)+1):
			  if string[i:i+len(sub)]==sub:
			    return -1
        print(find ("hello world","world"))
        print(find ("hello world","python"))
        print(find ("hello world","o"))
	
            