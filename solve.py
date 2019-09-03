ROUNDS = 765
BITS = 128

def encrypt(msg, key):
	enc = msg
	
	mask = (1 << BITS) - 1
	for i in range(ROUNDS):
		enc = (enc + key) & mask
		enc = enc^key
	return enc

def decrypt(msg, key):
    enc = msg
    mask = (1 << BITS) - 1
    for i in range(ROUNDS):
        enc = enc ^ key
        enc = (enc - key) & mask
    return enc

f = open('challenge/output','r').readlines()
the_flag = int(f[0],16)
pairs = []
for i in range(1,len(f)):
	pairs.append([bin(int(f[i].split()[0],16))[2:].rjust(128).replace(' ','0'),bin(int(f[i].split()[1],16))[2:].rjust(128).replace(' ','0')])

q = ['0','1']

while len(q) != 0:
	key = q.pop(0)
	flag = 1

	##check if we have found the correct key which decrypts all the pairs
	for i in range(len(pairs)):
		if decrypt(int(pairs[i][1],2),int(key,2)) != int(pairs[i][0],2):
			flag = 0
			break
	if flag == 1:
		print key
		break
	flag = 1

	##checking if the next MSB can be 0
	for j in range(len(pairs)):
		if bin(decrypt(int(pairs[j][1],2),int('0' + key,2)))[2:].rjust(128).replace(' ','0')[-(len(key)+1):] != pairs[j][0][-(len(key)+1):]:
			flag = 0
			break
	if flag == 1:
		q.append('0' + key)
	flag =1

	##checking if the next MSB can be 1
	for j in range(len(pairs)):
		if bin(decrypt(int(pairs[j][1],2),int('1' + key,2)))[2:].rjust(128).replace(' ','0')[-(len(key)+1):] != pairs[j][0][-(len(key)+1):]:
			flag = 0
			break
	if flag == 1:
		q.append('1' + key)

print "TWCTF{" +  str(hex(decrypt(the_flag,int(key,2)))[2:-1]) + "}"