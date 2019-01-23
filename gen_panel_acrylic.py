'''
script for generating transparent acrylic panels for the CT800 chess computer.
created panels contains only monting and button holes which are extracted from PCB layout (KiCAD).
panel files can be manipulated and converted into desired file format by PCBnew.

the classic panel is intended for the following housing:
Axxatronic BIM1006-BLK/PG or BIM1006-GY/PG
dimensions: 130 x 215 x 72 mm, front panel: 125,5 x 209,5 mm (mounting holes: 116 x 200 mm)
https://www.voelkner.de/products/774532/Axxatronic-Pult-Gehaeuse-130-x-215-x-72-ABS-Schwarz-BIM1006-BLK-PG-1St..html

'''

keep_entries = ("kicad_pcb", "general", "page", "layers", "setup", "net ", "net_class",
#				"module CT800_PCB:ct800",
#				"module CT800_PCB:LCD04x20BL",
#				"module CT800_PCB:promotion",
#				"module CT800_PCB:D6_3FTH",			# buttons
#				"module MountingHole",
#				"module LED_THT",
#				"gr_line",							# edges
#				"gr_text"
				)


def read_file(file_path):			# read pcb file and transform into list
	file = open(file_path, "r")
	data = []
	data.append(file.readline())	# don't care about first line
	open_par = 0
	close_par = 0

	for line in file:
		if line == "\n":
			data[-1] += line
			continue

		if open_par == close_par:
			data.append(line)
		else:
			data[-1] += line

		open_par += line.count("(")
		close_par += line.count(")")

	file.close()
	return data

def write_file(file_path, data):
	file = open(file_path, "w")
	for entry in data:
		file.write(entry)
	file.write(")")
	file.close()

def slim_copy(data, keep):		# remove unused entries in copy
	copy = []
	for entry in data:
		for keep_entry in keep:
			if entry.startswith("(" + keep_entry) or entry.startswith("  (" + keep_entry):
				copy.append(entry)
				break
	return copy

def find_border(data):			# based on "gr_line" entries in "Edge.Cuts" layer
	min_x = 1000
	max_x = -1000
	min_y = 1000
	max_y = -1000

	for entry in data:
		if "layer Edge.Cuts" in entry and entry.startswith("  (gr_line"):
			tokens = entry.replace(")", " ").split()

			min_x = min(min_x, float(tokens[2]))
			max_x = max(max_x, float(tokens[2]))
			min_x = min(min_x, float(tokens[5]))
			max_x = max(max_x, float(tokens[5]))

			min_y = min(min_y, float(tokens[3]))
			max_y = max(max_y, float(tokens[3]))
			min_y = min(min_y, float(tokens[6]))
			max_y = max(max_y, float(tokens[6]))

	return (min_x, max_x, min_y, max_y)

def new_border(center, size):
	min_x = round(center[0] - size[0]/2, 3)
	max_x = round(center[0] + size[0]/2, 3)
	min_y = round(center[1] - size[1]/2, 3)
	max_y = round(center[1] + size[1]/2, 3)

	return (min_x, max_x, min_y, max_y)

def get_center(border):
	return ((border[0]+border[1]) / 2, (border[2]+border[3]) / 2)

def get_button_center(data):
	pos = []
	for entry in data:
		if entry.startswith("  (module CT800_PCB:D6_3FTH"):
			tokens = entry.replace(")", " ").split()
			pos.append((float(tokens[9]) + 2.5, float(tokens[10]) + 2.5))
	return pos

def get_hole_center(data):
	pos = []
	for entry in data:
		if entry.startswith("  (module MountingHole"):
			tokens = entry.replace(")", " ").split()
			pos.append((float(tokens[9]), float(tokens[10])))
	return pos

def append_hole(panel, x, y, r):
	panel.append(f"  (gr_circle (center {x} {y}) (end {x+r} {y}) (layer Edge.Cuts) (width 0.05))\n")
	panel.append(f"  (gr_line (start {x-r} {y}) (end {x+r} {y}) (layer F.SilkS) (width 0.15))\n")
	panel.append(f"  (gr_line (start {x} {y-r}) (end {x} {y+r}) (layer F.SilkS) (width 0.15))\n")

def gen_panel(pcb_path, panel_path, panel_size, corner_holes=(), add_buttons=True):
	mounting_hole_r = 1.6
	button_hole_r = 5.1

	pcb = read_file(pcb_path)
	panel = slim_copy(pcb, keep_entries)

	border = find_border(pcb)
	center = get_center(border)

	border = new_border(center, panel_size)

	panel.append(f"  (gr_line (start {border[0]} {border[2]}) (end {border[1]} {border[2]}) (layer Edge.Cuts) (width 0.05))\n")
	panel.append(f"  (gr_line (start {border[1]} {border[2]}) (end {border[1]} {border[3]}) (layer Edge.Cuts) (width 0.05))\n")
	panel.append(f"  (gr_line (start {border[1]} {border[3]}) (end {border[0]} {border[3]}) (layer Edge.Cuts) (width 0.05))\n")
	panel.append(f"  (gr_line (start {border[0]} {border[3]}) (end {border[0]} {border[2]}) (layer Edge.Cuts) (width 0.05))\n\n")

	if len(corner_holes) > 0:
		holes = new_border(center, corner_holes)
		holes = [[holes[0], holes[2]], [holes[0], holes[3]], [holes[1], holes[2]], [holes[1], holes[3]]]
		for hole in holes:
			append_hole(panel, hole[0], hole[1], mounting_hole_r)
			print(f"corner hole   {hole[0] - border[0] :>9.2f} {hole[1] - border[2] : >9.2f}\t\tr = {mounting_hole_r} mm")

	if add_buttons:
		buttons = get_button_center(pcb)
		for but in buttons:
			append_hole(panel, but[0], but[1], button_hole_r)
			print(f"button        {but[0] - border[0] :>9.2f} {but[1] - border[2] :>9.2f}\t\tr = {button_hole_r} mm")

	holes = get_hole_center(pcb)
	for hole in holes:
		append_hole(panel, hole[0], hole[1], mounting_hole_r)
		print(f"mounting hole {hole[0] - border[0] :>9.2f} {hole[1] - border[2] : >9.2f}\t\tr = {mounting_hole_r} mm")

	write_file(panel_path, panel)

# gen panels
pcb_path = "./CT800_PCB/CT800_PCB.kicad_pcb"	# read only
panel_path = "./CT800_PANEL/"					# directory must already exist

spartan_panel_size = (215, 125)
classic_panel_size = (209.5, 125.5)

print("spartan front panel")
gen_panel(pcb_path, panel_path + "CT800_PANEL_SPARTAN_FR.kicad_pcb", spartan_panel_size)
print("\nspartan back panel")
gen_panel(pcb_path, panel_path + "CT800_PANEL_SPARTAN_BK.kicad_pcb", spartan_panel_size, (), False)

print("\nclassic front panel")
gen_panel(pcb_path, panel_path + "CT800_PANEL_CLASSIC.kicad_pcb", classic_panel_size, (200, 116))
