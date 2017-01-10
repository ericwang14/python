import numpy as np

ip_dictionary = []

def init_ip_dictionary() :
	with open('ipv4_list.txt', 'r+') as reader:
		ip_lines = reader.readlines()

		for ip_line in ip_lines:
			ip_dictionary.extend(build_ips(get_ip(ip_line)))
	print len(ip_dictionary)

def get_ip(ip_line):
	ips = ip_line.replace(' China', '')
	ips = ips.split('-')
	records = []
	for ip in ips:
		records.append(ip.strip().split('.'))

	return np.asarray(records).transpose()

def build_ips(ip_range):
	ips = []
	for i in range(int(ip_range[1][0]), int(ip_range[1][1]) + 1):
		for y in range(int(ip_range[2][0]), int(ip_range[2][1]) + 1):
			for z in range(int(ip_range[3][0]), int(ip_range[3][1]) + 1):
				ips.append(ip_range[0][0] + '.' + str(i) + '.' + str(y) + '.' + str(z))

	
	return ips




if __name__ == '__main__':
	init_ip_dictionary()