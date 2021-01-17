
import math

coord_name = "garden_spirit_1"

# This spirit's grid zones:
grid_zones = [ 
		(3, 3),
		(1, 2.5),
		(3, 4),
		(5, 2.5)
		]





x_start = 0 - 0
y_start = 0 - 0

offset_coords = []
theta = 0
radius = 3

offset_count = 24

for index in range(offset_count):
	# Work this out as a ratio of pi:
	theta = float(index) / (offset_count / 2)
	theta = theta * math.pi

	factor = 1.0

	this_radius_x = radius * factor #math.sin(theta / 8) * radius * factor
	this_radius_y = radius * factor #math.cos(theta / 16) * radius * factor
	x = x_start + this_radius_x * math.sin(theta)
	y = y_start + this_radius_y * (math.cos(theta))
	coord = (x, y)
	offset_coords.append(coord)


strider = ""




# Default offsets for start of grid:
off_x = (128 / 2) - (3.5 * 8)
off_y = (64 / 2) - (3.5 * 8)

# Work the true xys out
grid_true_xy = []

for x in range(len(grid_zones)):
	loc = grid_zones[x]
	grid_true_xy.append((round(off_x + loc[0] * 8), round(off_y + loc[1] * 8)))

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

tween_static = 4
tween_frames = 64 - tween_static

main_coords = []
action_line = []


def vec_sub(a, b):
	return (a[0] - b[0], a[1] - b[1])

def vec_add(a, b):
	return (b[0] + a[0], b[1] + a[1])

def vec_mag(a):
	return math.sqrt(a[0] * a[0] + a[1] * a[1])

def vec_nrm(a):
	mag = vec_mag(a)
	return (a[0] / mag, a[1] / mag)

def vec_rnd(a):
	return (round(a[0]), round(a[1]))

def vec_scl(a, f):
	return (a[0] * f, a[1] * f)

def vec_dot(a, b):
	return a[0] * b[0] + a[1] * b[1]

def vec_normal(a):
	return (-a[1], a[0])


# For every step
total_steps = len(grid_true_xy)
offset_frame = 0

output_coords = []


first_scale_count = 10

forced_frames_perlocation = 20

last_position = (0,0)
displacement_from_last = (0,0)

for current_step in range(total_steps):
	next_step = (current_step + 1) % total_steps

	current_base_xy = grid_true_xy[current_step]
	next_base_xy = grid_true_xy[next_step]

	action_line = vec_nrm(vec_sub(next_base_xy, current_base_xy))

	# We want to hang out at this XY point + our 

	c_frame = 0

	for n in range(forced_frames_perlocation):
		# Add 10 frames of doing whatever always:
		spirit_pos = vec_add(grid_true_xy[current_step], offset_coords[offset_frame])
		
		# We scale the first N frames so the spirit does emerge from the furniture
		start_scale_test = len(output_coords)
		if start_scale_test < first_scale_count:
			scale = float(start_scale_test) / first_scale_count
			spirit_pos = vec_add(grid_true_xy[current_step], vec_scl(offset_coords[offset_frame], scale ))

		offset_frame = (offset_frame + 1) % offset_count
		output_coords.append(vec_rnd(spirit_pos))

		displacement_from_last = vec_sub(spirit_pos, last_position)
		last_position = spirit_pos


	norm_disp = vec_nrm(displacement_from_last)
	dot_product = vec_dot(norm_disp, action_line)

	count_of_loop = 0
	while dot_product < 0.95:

		count_of_loop = count_of_loop + 1

		spirit_pos = vec_add(grid_true_xy[current_step], offset_coords[offset_frame])		
		offset_frame = (offset_frame + 1) % offset_count
		output_coords.append(vec_rnd(spirit_pos))
		displacement_from_last = vec_sub(spirit_pos, last_position)
		last_position = spirit_pos

		norm_disp = vec_nrm(displacement_from_last)
		dot_product = vec_dot(norm_disp, action_line)

	# We are now moving in the direction of our goal.

	# Let's create all the points we'll need from where we are on the line of action

	current_dot = vec_dot(spirit_pos, action_line)
	goal_dot = vec_dot(next_base_xy, action_line)

	dot_quest = math.ceil(goal_dot - current_dot)

	initial_dot = vec_dot(current_base_xy, action_line) - current_dot
	#print(initial_dot)

	intermediate_points = []

	# the number of points we want is a multiple of offset_count, as that way we get put back in the same place.

	for n in range(offset_count):

		ratio = float(n) / offset_count
		# This slowly displaces our root position on the line of action until we reach our goal:
		# There is an additional value for n
		displacement = vec_scl(action_line, initial_dot + dot_quest * ratio)
		result = vec_add(current_base_xy,displacement)
		intermediate_points.append(result)



	action_normal = vec_normal(action_line)

	for point in intermediate_points:
		# for every point along that line:
		off_axis = offset_coords[offset_frame]
		offset_frame = (offset_frame + 1) % offset_count

		# We have an offset, but, we must map it onto the normal of the action line

		off_axis_scale = vec_dot(off_axis, action_normal)

		off_axis = vec_scl(action_normal, off_axis_scale)

		spirit_pos = vec_add(point, off_axis)
		last_position = spirit_pos

		output_coords.append(vec_rnd(spirit_pos))


# Then scale us back to 0
for n in range(first_scale_count):

	current_base_xy = grid_true_xy[0]

	scale = 1 - (float(n) / first_scale_count)
	spirit_pos = vec_add(current_base_xy, vec_scl(offset_coords[offset_frame], scale ))

	offset_frame = (offset_frame + 1) % offset_count
	output_coords.append(vec_rnd(spirit_pos))


#print(output_coords)
#print(len(output_coords))


print (": validate")
print ("# %d" % len(output_coords))

strider = ""
counter = 0
for point in output_coords:
	strider += (" %d %d" % (round(point[0]), round(point[1])) )
	counter += 1

	if counter == 8:
		counter = 0
		print(strider)
		strider = ""

if counter != 0:
	print (strider)

print (-1)



# So we want to move towards this position

current = output_coords[0]

coord_list_a = []
coord_list_b = []

flip_flop = 0

for point in output_coords:


	approach_factor = 0.3
	# our goal is point
	# we are at current


	# Do list A:
	displacement = vec_sub(point, current)
	displacement = vec_scl(displacement, approach_factor)
	disp_mag = vec_mag(displacement)

	# If this is greater than 1 px movement:
	if disp_mag > 1:
		displacement = vec_nrm(displacement)

	current = vec_add(current, displacement)

	coord_list_a.append(vec_rnd(current))

	# Then do B:
	displacement = vec_sub(point, current)
	displacement = vec_scl(displacement, approach_factor)
	disp_mag = vec_mag(displacement)

	# If this is greater than 1 px movement:
	if disp_mag > 1:
		displacement = vec_nrm(displacement)

	current = vec_add(current, displacement)

	coord_list_b.append(vec_rnd(current))


print (": " + coord_name + "_xy_list_a")
print ("# %d" % len(coord_list_a))

strider = ""
counter = 0
for point in coord_list_a:
	strider += (" %d %d" % (round(point[0]), round(point[1])) )
	counter += 1

	if counter == 8:
		counter = 0
		print(strider)
		strider = ""

if counter != 0:
	print (strider)

print (-1)

print (": " + coord_name + "_xy_list_b")
print ("# %d" % len(coord_list_b))

strider = ""
counter = 0
for point in coord_list_b:
	strider += (" %d %d" % (round(point[0]), round(point[1])) )
	counter += 1

	if counter == 8:
		counter = 0
		print(strider)
		strider = ""

if counter != 0:
	print (strider)

print (-1)






if False:
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
			action_line.append( (tween_stop[0] - tween_start[0], tween_stop[1] - tween_start[1])  )
		else:
			action_line.append( (0,0) )
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

	validate = ""

	factor = 0.5
	off_axis_scaler = 0

	x = float(main_coords[0][0] + offset_coords[0][0])
	y = float(main_coords[0][1] + offset_coords[0][1])

	for j in range(256):
		goal_a = main_coords[j]
		goal_b = offset_coords[j]

		action_line_vector = action_line[j]

		magnitude = math.sqrt(action_line_vector[0] * action_line_vector[0] + action_line_vector[1] * action_line_vector[1])

		if magnitude == 0:
			#if off_axis_scaler != 0:
			#	print("end")
			magnitude = 0
			off_axis_scaler = 0

		else:

			# Work out the unit vector of the action line:
			unit_vector = ( action_line_vector[0] / magnitude, action_line_vector[1] / magnitude )

			#print (action_line_vector)
			#print (unit_vector)

			# Work out the normal:
			normal_vector = ( -unit_vector[1], unit_vector[0] )


			# Dot product, including goal magnitude:
			dot_product = (normal_vector[0] * goal_b[0] + normal_vector[1] * goal_b[1])

			off_axis = ( normal_vector[0] * dot_product, normal_vector[1] * dot_product)

			
			# Now compute on axis:
			dot_product = (unit_vector[0] * goal_b[0] + unit_vector[1] * goal_b[1])

			ratio = float(off_axis_scaler)
			ratio = ratio / tween_frames

			ratio = 0.5 * (1 + math.cos(math.pi * 2 * ratio))

			on_axis = ( unit_vector[0] * dot_product * ratio , unit_vector[1] * dot_product * ratio )

			goal_b = ( on_axis[0] + off_axis[0], on_axis[1] + off_axis[1] )


			off_axis_scaler = off_axis_scaler + 1

		goal_x = goal_a[0] + goal_b[0]
		goal_y = goal_a[1] + goal_b[1]


		dif_x = x
		dif_y = y

		dif_x = factor * (goal_x - dif_x)
		dif_y = factor * (goal_y - dif_y)

		# Maximum magnitude is 1:
		magnitude_action = math.sqrt(dif_y * dif_y + dif_x * dif_x)

		if magnitude_action > 1:
			dif_y = dif_y / magnitude_action
			dif_x = dif_x / magnitude_action


		x += dif_x
		y += dif_y

		strider = strider + (" %d %d" % (round(x), round(y)) )

		validate = validate + (" %d %d" % (round(goal_x), round(goal_y)) )

		counter = counter + 1

		if counter == 8:
			counter = 0
			print (strider)
			strider = ""
			validate += "\n"

	print (strider)

	print (": validate")
	print (validate)