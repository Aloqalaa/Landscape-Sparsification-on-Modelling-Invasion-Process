#   Created by DANIYAH ALOQALAA on 22/08/2016.
#   Python program for implementation of the full simulation method

import numpy
import numpy as np
import math
import random
import time
#*************************************************************
class simulator():
	def __init__(self):
		self.alpha = 0.25 # the dispersal distance initialized to 0.25
		self.landscape = np.array([])
		self.rounds_dic= {}
		self.time_dic_wall={} 
		self.averages_AS_last_col = []
		self.list_time_exe_full_simulation = []

	def read_landscape(self):
# please choose the landscapes that you would like to compute the number of rounds needed for successful invasions 
		self.landscape = numpy.load('../dataset/study_landscapes/high_5x300_landscape.npy', mmap_mode='r')
		self.landscape = self.landscape [:10,:10]
		width = self.landscape.shape[0]
		height = self.landscape.shape[1]

		print 'The average of all percentages = ', np.mean(self.landscape)
		print 'alpha =' ,self.alpha
		print 'The width of the landscape =',self.landscape.shape[0]
		print 'The hight of the landscape =', self.landscape.shape[1]
# The count_rounds function is used to count the number of rounds required for first, majority and all successes 
# and to compute the real time execution for each R-local simulation. 

	def count_rounds(self):
		self.start_full_simulation_time = time.time()
		R = self.landscape.shape[0] + self.landscape.shape[1]
		first_col = self.landscape[:,0]
		last_col = self.landscape[:,int(self.landscape.shape[1])-1]
		# print 'first col = ', first_col
		# print 'last col is = ', last_col
		source = np.nonzero(self.landscape[:,0])[0] # source = non-zero patches at first column
		target = np.nonzero(self.landscape[:,int(self.landscape.shape[1])-1])[0] # target = non-zero patches at last column
		# print 'source= ', source # indexes of non-zero patches at source
		# print 'target=', target # indexes of non-zero patches at target

		self.full_array = np.zeros((self.landscape.shape[0], self.landscape.shape[1]))
		for i in source:
			self.full_array[i,0] = 1

		self.counter = 0 
		x1_full = 0; x2_full = 0; y1_full = 0; y2_full = 0
		q_i_full = 0 # quality of the populated patch
		
	    # majority of of non-zero target patches
		if (len(target) % 2 == 0):
			majority = len(target)/2
		else:
			majority = (len(target)/2)+1
		# print 'majority =', majority

		denominator = (2*math.pi/math.pow(self.alpha,2))-1

		self.start_wall = time.time()
		while np.any(self.full_array[target,self.full_array.shape[1]-1] == 0):# AS full
			self.counter+=1	
			for i in range(0,self.landscape.shape[0]): # loop for all populated patches (1) in full process
				for j in range(0,self.landscape.shape[1]):
					if (self.full_array [i,j] == 0):
						continue
					else:
						x1_full = i
						y1_full = j
						q_i_full = self.landscape[i,j]
						for ii in range(0,self.landscape.shape[0]): # loop for all unpopulated patches (0) in full process
							for jj in range(0,self.landscape.shape[1]):
								if (self.full_array [ii,jj] == 0 and self.landscape[ii,jj] != 0):
									x2_full = ii
									y2_full = jj
									distance = math.sqrt(math.pow(x1_full-x2_full,2)+math.pow(y1_full -y2_full ,2))
									if (0 < distance <= R):
										p = q_i_full*((math.exp(-self.alpha*(distance)))/denominator)
										p = round(p,8)
										u1 = random.random()
										u1 = round(u1,8)
										if u1 < p:
											self.full_array [ii,jj] = 1 # change from unpopulated (0) to populated (1)
											if (jj == 2):
												self.checkpoints(jj)
			
		self.averages_AS_last_col.append(self.counter)
		self.end_full_simulation_time = time.time()
		self.time_exe_full_simulation = self.end_full_simulation_time - self.start_full_simulation_time
		self.list_time_exe_full_simulation.append(self.time_exe_full_simulation)

# The checkpoints function is used to Check the invasion type first or majority or all
	def checkpoints(self, check):
		target1 = np.nonzero(self.landscape[:,check])[0]
		self.rounds_dic.setdefault(check,{'first':[],'majority':[],'all':[]})
		self.time_dic_wall.setdefault(check,{'first':[],'majority':[],'all':[]})
		
		if (len(target1) % 2 == 0):
			majority1 = len(target1)/2
		else:
			majority1 = (len(target1)/2)+1
		
		# First Success
		if np.count_nonzero(self.full_array[target1,check])== 1:
			FS = self.counter
			self.rounds_dic[check]['first'].append(FS) 
			self.end_FS_wall = time.time()
			self.time_exe_FS_wall = (self.end_FS_wall-self.start_wall)
			self.time_dic_wall[check]['first'].append(self.time_exe_FS_wall)
		
		# Majority Success
		if np.count_nonzero(self.full_array[target1,check])== majority1:
			MS = self.counter
			self.rounds_dic[check]['majority'].append(MS)
			self.end_MS_wall = time.time()
			self.time_exe_MS_wall = (self.end_MS_wall-self.start_wall)
			self.time_dic_wall[check]['majority'].append(self.time_exe_MS_wall)
		
		# All Successes
		if np.all(self.full_array[target1,check] != 0):
			AS = self.counter
			self.rounds_dic[check]['all'].append(AS)
			self.end_AS_wall = time.time()
			self.time_exe_AS_wall = (self.end_AS_wall-self.start_wall)
			self.time_dic_wall[check]['all'].append(self.time_exe_AS_wall)
			
# The count_times function is used to count the stabilization time for the full simulation  	
	def count_times(self):
		t = 0
		while t<20:
			self.count_rounds()
			t+=1

		time= 9
		stop = False
		while not stop:
			time = time +1
			print 'time =', time
			stop = True
			A_time = np.mean(self.averages_AS_last_col[:time])
			print 'A_time =', A_time
			for i in range (time+1,2*time+1):
				A_i = np.mean(self.averages_AS_last_col[:i])
				print 'A_i =', A_i
				print 'abs(A_time-A_i) =', abs(A_time-A_i)
				print '(0.02 * A_time) =', (0.02 * A_time)
				if abs(A_time-A_i) > (0.02 * A_time):
					print "abs(A_time-A_i) > (0.02 * A_time) is satisfied please ------ break"
					stop = False
					break
				else:
					print '--------------'
					print 'when i=', i
					print '--------------'
					if i <len(self.averages_AS_last_col):
						pass
					else:
						print "we need to call count_rounds function"
						self.count_rounds()			
		print 'The stabilization time =', time
if __name__ == '__main__':
	my_gui = simulator()
	my_gui.read_landscape()
	my_gui.count_times()
	
	print 'The minimum but still non-zero qulaity in the landscape = ', np.min(my_gui.landscape[np.nonzero(my_gui.landscape)])
	print 'The maximum qulaity in the landscape = ', my_gui.landscape.max()
	print 'The average of FS FULL= ', np.mean(my_gui.rounds_dic[2]['first'])  
	print 'The average of MS FULL= ', np.mean(my_gui.rounds_dic[2]['majority'])
	print 'The average of AS FULL= ', np.mean(my_gui.rounds_dic[2]['all'])
	print 'The average of FS exexution times = ', np.mean(my_gui.time_dic_wall[2]['first'])  
	print 'The average of MS exexution times = ', np.mean(my_gui.time_dic_wall[2]['majority'])
	print 'The average of AS exexution times = ', np.mean(my_gui.time_dic_wall[2]['all'])
	print 'The average times execution of full simulations = ', np.mean(my_gui.list_time_exe_full_simulation)

