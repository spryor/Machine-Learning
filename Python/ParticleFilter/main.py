#Author: Stephen Pryor
#Date: September 27, 12
"""
A Particle Filter Testing Program

Usage:
To run the program with a default setting of 2 objects and 300 particles
>main.py
To run the program with a default setting of <n> objects and 300 particles
OR
>main.py <n>
  - where <n> is the number of objects you want in your scene
To run the program with a default setting of <n> objects and 300 particles
OR
>main.py <n> <p>
  - where <n> is the number of objects you want in your scene
  - where <p> is the number of particles you want in your scene
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
import pylab
from particleFilter_util import *
from particleFilter import particle_filter
import random
import sys


numIterations = 200
numParticles = 400
numObjects = 2

if len(sys.argv) > 1:
  numObjects = int(sys.argv[1])
  if len(sys.argv) > 2:
    numParticles = int(sys.argv[2])

max_x = 1000
max_y = max_x
robot = [50, 200]
objects = []
for i in range(0, numObjects):
  objects.append((random.randrange(0, max_x), random.randrange(0, max_y)))
particles = []
for i in range(0, numParticles):
  particles.append((random.randrange(0, max_x), random.randrange(0, max_y)))
objects_x, objects_y = getX_Y(objects)
plt.figure()
plt.ion()
#run the particle filter
for i in range(numIterations):
  #kidnap the robot after 90 iterations
  if i == 90:
    robot = [50, 200]
  robot[0] = robot[0] + 8
  robot[1] = robot[1] + 5
  observations = []
  for object in objects:
    observations.append(euclidean_distance(robot, object)+random.randrange(1, 3)*random.random()) #add some noise to our observations
  particles = particle_filter(particles, observations, objects, max_x)
  particle_x, particle_y = getX_Y(particles)
  plt.xlim([0,max_x])
  plt.ylim([0,max_y])
  plt.plot(particle_x, particle_y, 'bo', alpha=0.6)
  plt.plot(objects_x, objects_y, 'rs')
  robot_x, robot_y = robot[0], robot[1]
  plt.plot(robot_x, robot_y, 'ms')
  plt.title(i)
  plt.draw()
  plt.clf()

#display the final results
plt.xlim([0,max_x])
plt.ylim([0,max_y])
particle_x, particle_y = getX_Y(particles)
plt.plot(particle_x, particle_y, 'bo', alpha=0.6)
plt.plot(objects_x, objects_y, 'rs')
robot_x, robot_y = robot[0], robot[1]
plt.plot(robot_x, robot_y, 'ms')
plt.ioff()
plt.title("Final Position")
plt.show()