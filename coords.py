import random

l = []

for x in range(5):
	for y in range(5):
		l.append((x+1,y+1))

random.shuffle(l)

print(l)