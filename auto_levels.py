import random

all_enemy_balance = {
	0: 0,	1: 0,	2: 0,	3: 0,
	4: 0,	5: 0,	6: 0,	7: 0,
	8: 0,	9: 0,	10: 0,	11: 0,
	12: 0,	13: 0,	14: 0,	15: 0
	}

levels = {
	"level_lr_1" : [
		(0, 4),
		(1, 4)
	],
	"level_lr_2" : [
		(1, 3),
		(2, 3),
		(3, 3),
		(4, 3)
	],
	"level_lr_3" : [
		(0, 2),
		(3, 6),
		(4, 2),
		(5, 2)
	],
	"level_lr_4" : [
		(0, 3),
		(4, 4),
		(7, 4)
	],
	"level_lr_5" : [
		(2, 4),
		(3, 2),
		(5, 3)
	],
	"level_lr_6" : [
		(6, 3),
		(8, 4),
		(2, 3)
	],

	"level_dr_1" : [

	],
	"level_dr_2" : [

	],
	"level_dr_3" : [

	],
	"level_dr_4" : [

	],

}


#for x in range(5):
#for y in range(5):
#		l.append((x+1,y+1))

#random.shuffle(l)

for key in levels:
	l = levels[key]
	e = []
	for pair in l:
		e_type = pair[0]
		count = pair[1]

		all_enemy_balance[e_type] = all_enemy_balance[e_type] + count

		for x in range(count):
			e.append(e_type * 8)

	random.shuffle(e)


	o_str = ": " + key + "_enemy\n\t" + str(len(e)) + "\n\t\t"
	for v in e:
		o_str += str(v) + " "

	o_str += "\n"

	
	print(o_str)


print(all_enemy_balance)