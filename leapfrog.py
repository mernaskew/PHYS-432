# -*- coding: utf-8 -*-
"""
This code simulates the leapfrog interaction between two vortex rings. 
Initial conditions for the vortex rings are set up, including their positions 
(x_v and y_v) and line vortex constants (k_v). The plot is initialized, and the 
initial velocity streamline is drawn based on these initial conditions.

The code iteratively updates the positions of the vortex rings (x_v and y_v) 
based on the advection velocity computed from the interaction between the vortices. 
After updating the positions, the velocity field is recalculated, and the plot 
is updated with new streamlines representing the updated velocity field.

Throughout the evolution, the plot is updated to reflect the movement of the 
vortex rings and the changes in the velocity field. The visualization helps 
observe the leapfrog interaction.

The simulation runs for a specified number of steps (Nsteps) with a time step 
(dt). The resolution of the visualization grid (ngrid) and the masking radius 
(r_mask) are also set to control the visualization quality. Adjustments to these 
parameters can be made to achieve different simulation results and visualization 
effects.

To run the simulation (on Windows), open up a terminal and run by writing 
python leapfrog.py in the directory that the file is in.

@author: Maryn Askew
@collab: Spencer Geddes
02/12/2024
"""
import numpy as np
import matplotlib.pyplot as pl

# selected time step and number of steps to observe 2 leapfrogs
dt = 5
Nsteps = 40

# Setting up initial conditions (vortex centres and circulation)
y_v = np.array([-10, 10, -10, 10])  
x_v = np.array([-28, -28, -20, -20])
k_v = np.array([-2, 2, -2, 2])   

# Setting up the plot
pl.ion()
fig, ax = pl.subplots(1,1)

# mark the initial positions of vortices
p, = ax.plot(x_v, y_v, 'k+', markersize=12) 


# draw the initial velocity streamline
#360j sets the resolution of the cartesian grid
ngrid = 30
Y, X = np.mgrid[-ngrid:ngrid:360j, -ngrid:ngrid:360j] 

# initializing x and y velocity
vel_x = np.zeros(np.shape(Y)) 
vel_y = np.zeros(np.shape(Y)) 

# masking radius for better visualization of the vortex centres
r_mask = 1

for i in range(len(x_v)): #looping over each vortex
    # computing the total velocity field
    r = np.sqrt((X - x_v[i])**2 + (Y - y_v[i])**2) 
    vel_x -= k_v[i] * (Y - y_v[i]) / r**2
    vel_y += k_v[i] * (X - x_v[i]) / r**2
    
    # masking within a certain radius for better visibility
    vel_x[r < r_mask] = np.nan
    vel_y[r < r_mask] = np.nan

# set up the boundaries of the simulation box
ax.set_xlim([-ngrid, ngrid])
ax.set_ylim([-ngrid, ngrid])

# initial plot of the streamlines
ax.streamplot(X, Y, vel_x, vel_y, density=[1.3, 1.3]) 

fig.canvas.draw()

# Evolution
count = 0
while count < Nsteps:
    # initialize advection velocities
    adv_x = np.zeros(np.shape(x_v))
    adv_y = np.zeros(np.shape(x_v))
    
    # compute and update advection velocity due to neighbouring vortices
    for i in range(len(x_v)):
        for j in range(len(x_v)):
            if i != j:  
                r = np.sqrt((x_v[i] - x_v[j])**2 + (y_v[i] - y_v[j])**2)
                adv_x[i] -= k_v[j] * (y_v[i] - y_v[j]) / r**2
                adv_y[i] += k_v[j] * (x_v[i] - x_v[j]) / r**2
    
    # updating positions of vortices
    x_v = x_v + adv_x*dt
    y_v = y_v + adv_y*dt
     
    # re-initialize the total velocity field
    Y, X = np.mgrid[-ngrid:ngrid:360j, -ngrid:ngrid:360j] 
    vel_x = np.zeros(np.shape(Y)) #this holds x-velocity
    vel_y = np.zeros(np.shape(Y)) #this holds y-velocity
    
    for i in range(len(x_v)): 
        # computing the total velocity field
        r = np.sqrt((X - x_v[i])**2 + (Y - y_v[i])**2)
        vel_x -= k_v[i] * (Y - y_v[i]) / r**2
        vel_y += k_v[i] * (X - x_v[i]) / r**2
    
        # masking within a certain radius for better visibility
        vel_x[r < r_mask] = np.nan
        vel_y[r < r_mask] = np.nan
    
    ## update plot
    # the following two lines clear out the previous streamlines
    for coll in ax.collections:
        coll.remove()

    for patch in ax.patches:
        patch.remove()

    p.set_xdata(x_v)
    p.set_ydata(y_v)

    ax.streamplot(X, Y, vel_x, vel_y, color = 'cornflowerblue', density=[1.3, 1.3]) 

    fig.canvas.draw()
    pl.pause(1e-10) 
    count += 1
    
    



