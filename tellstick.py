
import re
import arctech, everflourish, fineoffset, pt2262

METHOD_OFF = 0
METHOD_ON  = 1
METHOD_DIM = 2
METHOD_LEARN = 3

def message(string):
	lst = []
	pos = 0

	while pos < len(string):
		if string[pos] == "s":
			break
		elif string[pos] == "i":
			pos += 1
			integer = string[pos:].split("s", 1)[0]
			lst.append( int(integer, 16) )
			pos += len(integer)
		elif string[pos] == "l":
			pos += 1
			(l,i) = message(string[pos:])
			lst.append(l)
			pos += i
		elif string[pos] == "h":
			pos += 1
			dic = {}
			(l, i) = message(string[pos:])
			for j in range(0, len(l),2):
				dic.update({l[j] : l[j+1]})
			lst.append(dic)
			pos += i
		else:
			split = string[pos:].split(':', 1)
			length = int(split[0], 16)
			pos += len(split[0]) + 1
			lst.append(string[pos:pos+length])
			pos += length




#	while pos < len(string):
		# if elements[i][0] == 'i':
			# msg.append( int(elements[i][1:], 16) )


	return (lst, pos)

def parse(msg):
	obj = message(msg)[0]
	if obj[0] == "RawData":
		try:
			protocol = obj[1]['protocol']
			if protocol == "arctech":
				return arctech.parse(obj[1])
			elif protocol == "everflourish":
				return everflourish.parse(obj[1])
			elif protocol == "fineoffset":
				return fineoffset.parse(obj[1])
			elif protocol == "pt2262":
				return pt2262.parse(obj[1])
 			else:
				raise Exception("Unknown protocol")
				return false
		except Exception, e:
			raise Exception("Could not parse message object: %s" % e)
	return False
