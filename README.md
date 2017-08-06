# Landscape-Sparsification-on-Modelling-Invasion-Process

These codes implement the full and R-local simulation methods. For details of these methods or to cite these codes please use the following reference.

@inproceedings{AHW2017,

Author = {Daniyah A. Aloqalaa and Jenny A. Hodgson and Prudence W.H. Wong},

Booktitle = {Proceedings of the 16th International Symposium on Experimental Algorithms},

Title = {The Impact of Landscape Sparsification on Modelling and Analysis of the Invasion Process},

year = {2017},

note = {to appear}

}
# Required Modules and Libraries
The following packages are required.

- numpy library for loading numpy file, creating 2-dimensional array ..etc.  

- math library for mathematical function (abs, sort, round, exp ..etc). This library is installed be default when installing Python.

- random library for generating random number between 0 and 1. This library is installed be default when installing Python.

- time library for compute the execution time of simulation. This library is installed be default when installing Python.
# Instruction to run full_simulation.py and R_local_simulation.py codes

-To compare full and R-local results on the same landscapes, the user need to run full simulation first, then R-local simulation. 

-To implement the full_simulation.py or R_local_simulation.py program, data numpy file is required which stores a 2-dimensional array and represents the selected landscapes.For instance, the author chooses “high_5x300_landscape.npy” numpy file from the dataset=> study_landscapes folder. The user can choose another landscapes from the dataset folder.

-The user need to specify the value of the dispersal distance which is defined as parameter alpha in line 12 in both programs (it is given 0.25)

# More especial Instruction to run R_local_simulation.py program 

-Before running R_local_simulation.py, the user need to give the local distance which is defined as parameter R in line 34 in the code.
 
-The user need to give the total number of rounds needed for first, majority and all successes which are obtained from the full simulation by assigning these number of rounds to variables FS_FULL, MS_FULL, AS_FULL in lines 171, 172 and 173 in R_local_simulation.py code. 


# Licensing and Re-distribution
See the LICENCE file. You may use/re-distribute the codes if you do all of the following.

1. Request in writing via e-mail to me

2. agree to distribute the LICENCE file along with your code

3. cite the paper and these codes in your publication.
