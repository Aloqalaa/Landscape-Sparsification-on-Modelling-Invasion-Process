#   Created by DANIYAH ALOQALAA on 22/08/2016.
#   Python program for implementation of the R-local simulation method

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
		self.list_time_exe_R_LOCAL_simulation = []
	
	def read_landscape(self):
# please choose the landscapes that you would like to compute the number of rounds needed for successful invasions 
		self.landscape = numpy.load('../dataset/study_landscapes/high_5x300_landscape.npy', mmap_mode='r')
		width = self.landscape.shape[0]
		height = self.landscape.shape[1]

		print "The average of all percentages = ", np.mean(self.landscape)
		print 'alpha=' ,self.alpha
		print 'The width of the landscape =',self.landscape.shape[0]
		print 'The hight of the landscape =', self.landscape.shape[1]
# The count_rounds function is used to count the number of rounds required for first, majority and all successes 
# and to compute the real time execution for each R-local simulation.

	def count_rounds(self):
		self.start_R_LOCAL_simulation_time = time.time()
		self.R = 4 # the local distance R given as input 
		first_col = self.landscape[:,0]
		last_col = self.landscape[:,int(self.landscape.shape[1])-1]
		# print 'first col = ', first_col
		# print 'last col is = ', last_col
		source = np.nonzero(self.landscape[:,0])[0] # source = non-zero patches at first column
		target = np.nonzero(self.landscape[:,int(self.landscape.shape[1])-1])[0] # target = non-zero patches at last column
		# print 'source= ', source # indexes of non-zero patches at source
		# print 'target=', target # indexes of non-zero patches at target

		self.R_LOCAL_array = np.zeros((self.landscape.shape[0], self.landscape.shape[1]))
		for i in source:
			self.R_LOCAL_array[i,0] = 1

		self.counter = 0 
		x1_R_LOCAL = 0; x2_R_LOCAL = 0; y1_R_LOCAL = 0; y2_R_LOCAL = 0
		q_i_R_LOCAL = 0 # quality of the populated patch
		
	    # majority of of non-zero target patches
		if (len(target) % 2 == 0):
			majority = len(target)/2
		else:
			majority = (len(target)/2)+1
		# print 'majority =', majority

		denominator = (2*math.pi/math.pow(self.alpha,2))-1

		self.start_wall = time.time()
		while np.any(self.R_LOCAL_array[target,self.R_LOCAL_array.shape[1]-1] == 0):# AS R_LOCAL
			self.counter+=1	
			for i in range(0,self.landscape.shape[0]): # loop for all populated patches (1) in R_LOCAL method
				for j in range(0,self.landscape.shape[1]):
					if (self.R_LOCAL_array [i,j] == 0):
						continue
					else:
						x1_R_LOCAL = i
						y1_R_LOCAL = j
						q_i_R_LOCAL = self.landscape[i,j]
						for ii in range (max(0,x1_R_LOCAL-self.R), min(x1_R_LOCAL+self.R+1, self.landscape.shape[0])): # loop for all unpopulated patches (0) in R_LOCAL method
							for jj in range(max(0,y1_R_LOCAL-self.R), min(y1_R_LOCAL+self.R+1, self.landscape.shape[1])):
								if (self.R_LOCAL_array [ii,jj] == 0 and self.landscape[ii,jj] != 0):
									x2_R_LOCAL = ii
									y2_R_LOCAL = jj
									distance = math.sqrt(math.pow(x1_R_LOCAL-x2_R_LOCAL,2)+math.pow(y1_R_LOCAL -y2_R_LOCAL ,2))
									if (0 < distance <= self.R):
										p = q_i_R_LOCAL*((math.exp(-self.alpha*(distance)))/denominator)
										p = round(p,8)
										u1 = random.random()
										u1 = round(u1,8)
										if u1 < p:
											self.R_LOCAL_array [ii,jj] = 1 # change patch from unpopulated (0) to populated (1)
											if (jj == 49):
												self.checkpoints(jj)
			
		self.averages_AS_last_col.append(self.counter)
		self.end_R_LOCAL_simulation_time = time.time()
		self.time_exe_R_LOCAL_simulation = self.end_R_LOCAL_simulation_time - self.start_R_LOCAL_simulation_time
		self.list_time_exe_R_LOCAL_simulation.append(self.time_exe_R_LOCAL_simulation)

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
		if np.count_nonzero(self.R_LOCAL_array[target1,check])== 1:
			FS = self.counter
			self.rounds_dic[check]['first'].append(FS) 
			self.end_FS_wall = time.time()
			self.time_exe_FS_wall = (self.end_FS_wall-self.start_wall)
			self.time_dic_wall[check]['first'].append(self.time_exe_FS_wall)
		
		# Majority Success
		if np.count_nonzero(self.R_LOCAL_array[target1,check])== majority1:
			MS = self.counter
			self.rounds_dic[check]['majority'].append(MS)
			self.end_MS_wall = time.time()
			self.time_exe_MS_wall = (self.end_MS_wall-self.start_wall)
			self.time_dic_wall[check]['majority'].append(self.time_exe_MS_wall)
		
		# All Successes
		if np.all(self.R_LOCAL_array[target1,check] != 0):
			AS = self.counter
			self.rounds_dic[check]['all'].append(AS)
			self.end_AS_wall = time.time()
			self.time_exe_AS_wall = (self.end_AS_wall-self.start_wall)
			self.time_dic_wall[check]['all'].append(self.time_exe_AS_wall)

# The count_times function is used to count the stabilization time for the R-local simulation  	
	def count_times(self):
		t = 0
		while t<20:
			self.count_rounds()
			t+=1

		time= 9
		stop = False
		while not stop:
			time = time +1
			stop = True
			A_time = np.mean(self.averages_AS_last_col[:time])
			for i in range (time+1,2*time+1):
				A_i = np.mean(self.averages_AS_last_col[:i])
				if abs(A_time-A_i) > (0.02 * A_time):
					stop = False
					break
				else:
					if i <len(self.averages_AS_last_col):
						pass
					else:
						self.count_rounds()
			
		print 'The stabilization time =', time
if __name__ == '__main__':
	my_gui = simulator()
	my_gui.read_landscape()
	my_gui.count_times()
	
	print 'The minimum but still non-zero qulaity in the landscape = ', np.min(my_gui.landscape[np.nonzero(my_gui.landscape)])
	print 'The maximum qulaity in the landscape =  ', my_gui.landscape.max()
	print 'The local distance R = ', my_gui.R
	FS_R_LOCAL = np.mean(my_gui.rounds_dic[49]['first'])
	MS_R_LOCAL = np.mean(my_gui.rounds_dic[49]['majority'])
	AS_R_LOCAL = np.mean(my_gui.rounds_dic[49]['all'])
	print 'The average of FS R-LOCAL= ', int(FS_R_LOCAL)
	print 'The average of MS R-LOCAL= ', int(MS_R_LOCAL)
	print 'The average of AS R-LOCAL= ', int(AS_R_LOCAL)
	print 'The average of FS exexution times = ', np.mean(my_gui.time_dic_wall[49]['first'])  
	print 'The average of MS exexution times = ', np.mean(my_gui.time_dic_wall[49]['majority'])
	print 'The average of AS exexution times = ', np.mean(my_gui.time_dic_wall[49]['all'])
	print 'The average times execution of R-LOCAL simulations = ', np.mean(my_gui.list_time_exe_R_LOCAL_simulation)	
	FS_FULL =  # it based on the number of rounds for first success obtained from Full simulation
	MS_FULL =  # it based on the number of rounds for majority success obtained from Full simulation
	AS_FULL =  # it based on the number of rounds for all successes obtained from Full simulation

	print 'The average of FS FULL=', FS_FULL
	print 'The average of MS FULL=', MS_FULL
	print 'The average of AS FULL=', AS_FULL
	ratio_FS = float(FS_FULL)/int(FS_R_LOCAL)
	ratio_MS = float(MS_FULL)/int(MS_R_LOCAL)
	ratio_AS = float(AS_FULL)/int(AS_R_LOCAL)
	print 'The FULL/R-LOCAL accuracy for first success = ', ratio_FS
	print 'The FULL/R-LOCAL accuracy for majority success = ', ratio_MS
	print 'The FULL/R-LOCAL accuracy for all successes = ', ratio_AS
