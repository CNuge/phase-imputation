import os

""" this function takes a linkmfex phase file, and turns it into a .csv"""
""" bit at bottom lets this be done on a whole folder of phase files at once"""

def convert_phase(phase_file, skipheader = True):
	newfile = phase_file.split('.')[0] + "_" +phase_file.split('.')[1] + '.csv'
	phase_lines=[]
	with open(phase_file) as file:
		for line in file:
			name_and_phase = line.split()
			phase_lines.append(name_and_phase)
	if skipheader == True:
		phase_lines = phase_lines[1:]
	for line in phase_lines:
		comma_dat = [line[0]]
		for i in line[1]:
			comma_dat.append(i)
		comma_dat_str = ','.join(comma_dat)
		comma_dat_str+='\n'
		file = open(newfile, 'a')
		file.write(comma_dat_str)
		file.close()


if __name__ == '__main__':
	files = os.listdir()
	sexes=['m','f']
	to_convert = [x for x in files if x[-1] in sexes]
	for i in to_convert:
		convert_phase(i)
