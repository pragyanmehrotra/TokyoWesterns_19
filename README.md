# Challenge - Simple Logic

### Description

Simple cipher is always strong. (The challenge files are in the challenge folder, The output file has been edit a bit so that it can be easily parsed.)

### Looking at the encrypt function

```ruby
def encrypt(msg, key)
    enc = msg
    mask = (1 << BITS) - 1
    ROUNDS.times do
        enc = (enc + key) & mask
        enc = enc ^ key
    end
    enc
end
```

It accepts 2 args a msg and a key both as Integers and performs some basic operations on it repeatedly adds and then xors the msg with the key 765 times to be precise (doesn't matter tho). Also, the mask is nothing but just 127 ones similar to modulo pow(2,128) well that doesn't concern us much as we are given a corresponding decrypt function.

### Approach

One key thing to note is that the operations on the MSB does not affect the LSB so we can simply exploit the encrypt function and get the key bit by bit although a BFS approach is neccessary because multiple solutions maybe possible at each level hence we keep on eliminating those keys as it starts to unsatisfy any of the pair given.


### Solution

The solution was not that hard to code but coming up with this observation took some time. It was a fun challenge :D . The solution script

```python
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
```