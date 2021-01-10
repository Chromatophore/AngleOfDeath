
import math


x_start = 0 - 0
y_start = 0 - 0

offset_coords = []
theta = 0
radius = 6
count = 256


for index in range(count):
	theta = float(index) / math.pi
	theta = theta / 2

	factor = 1.0

	if index < 5:
		factor = float(index) / 5

	if index > (252 - 10):
		tend_zero = 252 - index
		tend_zero = float(tend_zero) / 10
		factor = tend_zero
		if factor < 0:
			factor = 0

	if index > 252:
		factor = 0

	this_radius_x = math.sin(theta / 8) * radius * factor
	this_radius_y = math.cos(theta / 16) * radius * factor
	x = x_start + this_radius_x * math.sin(theta)
	y = y_start + this_radius_y * (math.sin(2 * theta))
	coord = (round(x), round(y))
	offset_coords.append(coord)


print (": xy_count")
print (count)
print (": xy_list")
strider = ""
counter = 0
for coord in offset_coords:
	strider += (" %d %d" % (coord[0], coord[1]))
	counter += 1

	if counter == 10:
		counter = 0
		print (strider)
		strider = ""



print (": xy_mainpos")


grid_zones = [ 
		(3, 3),
		(1, 2.5),
		(3, 4),
		(5, 2.5)
		]


off_x = (128 / 2) - (3.5 * 8)
off_y = (64 / 2) - (3.5 * 8)

wait = 0
mode = 0
coord_index = 0

first_time = True


def do_a_tween(s, e, f):

	#print ("Testing...")
	#print (s)
	#print (e)
	#print (f)

	cosine_tween = (0.5 + (-0.5 * math.cos(f * math.pi)))
	#print (cosine_tween)

	x = s[0] + (e[0] - s[0]) * cosine_tween
	y = s[1] + (e[1] - s[1]) * cosine_tween

	#print ((x,y))

	return (x, y)


strider = ""

tween_static = 15
tween_frames = 64 - tween_static

main_coords = []

for j in range(257):
	wait = wait + 1

	loc = grid_zones[coord_index]

	loc_xy = (round(off_x + loc[0] * 8), round(off_y + loc[1] * 8))

	if first_time:
		tween_start = loc_xy
		first_time = False

	tween_stop = loc_xy

	output = loc_xy

	if mode == 1:
		output = do_a_tween(tween_start, tween_stop, float(wait) / tween_frames)

	strider = strider + (" %d %d" % (output[0], output[1]))

	main_coords.append((output[0], output[1]))

	if mode == 0:
		if wait == tween_static:
			wait = 0
			mode = 1
			tween_start = loc_xy
			# We want to tween to next target:
			coord_index = (coord_index + 1) % 4

	if mode == 1:
		if wait == tween_frames:
			wait = 0
			mode = 0
			#print (" %s # %d " % (strider, j))
			strider = ""


#print (" %s # %d " % (strider, j))

#print (grid_zones)


strider = ""
counter = 0

factor = 0.3

x = float(main_coords[0][0] + offset_coords[0][0])
y = float(main_coords[0][1] + offset_coords[0][1])

for j in range(256):
	goal_a = main_coords[j]
	goal_b = offset_coords[j]

	goal_x = goal_a[0] + goal_b[0]
	goal_y = goal_a[1] + goal_b[1]


	dif_x = x
	dif_y = y

	dif_x = factor * (goal_x - dif_x)
	dif_y = factor * (goal_y - dif_y)

	if dif_x > 1:
		dif_x = 1
	if dif_x < -1:
		dif_x = -1

	if dif_y > 1:
		dif_y = 1
	if dif_y < -1:
		dif_y = -1



	x += dif_x
	y += dif_y

	strider = strider + (" %d %d" % (round(x), round(y)) )

	counter = counter + 1

	if counter == 8:
		counter = 0
		print (strider)
		strider = ""

print (strider)