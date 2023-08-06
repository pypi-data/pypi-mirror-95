import h5py
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
from skopi.util import symmpdb
from skopi.ff_waaskirf_database import *
import skopi.particle
from scipy.spatial import distance
from skopi.aggregate import build_bpca
from skopi.particleCollection import *


def max_radius(particles):
    radius_current = 0
    for particle in particles:
        radius_arr = particle.atom_pos - np.mean(particle.atom_pos, axis=0)
        for row in radius_arr:
            radius = np.sqrt(row[0]**2+row[1]**2+row[2]**2)
            if radius > radius_current:
                radius_current = radius
    radius_max = radius_current
    return radius_max


def distribute_particles(particles, beam_focus_radius, jet_radius, gamma=0): #beam_focus_radius = 10e-6 #jet_radius = 1e-4
    """
    Randomly distribute particles within the focus region. 
    Depending on the degree of attraction gamma ranging between 0 and 1, 
    the interactionn range between particles varies.
    If the distance between the particle pairs is less than the interaction range, 
    the particle pairs stick to each other, otherwise stay still.
    Remove particles that overlap each other after performing the sticking feature,
    and add particle cluster using the bpca() class so that the overall number of particles in the system remain equal to the user input.
    """ 
    state = []
    for particle in particles:
        for count in range(particles[particle]):
            state.append(particle)
    radius_max = max_radius(particles)
    N = sum(particles.values()) # total number of particles
    coords = np.zeros((N,3)) # initialize N*3 array
    # generate N*3 random positions inside the volume illuminated by the beam (cylinder)
    for i in range(N):
        coords[i,0] = beam_focus_radius*np.sqrt(np.random.uniform(0,1))*np.cos(np.random.uniform(0,2*np.pi))
        coords[i,1] = beam_focus_radius*np.sqrt(np.random.uniform(0,1))*np.sin(np.random.uniform(0,2*np.pi))
        coords[i,2] = jet_radius*np.random.uniform(-1, 1)
    # calculate N*N distance matrix
    dist_matrix = distance.cdist(coords, coords, 'euclidean')
    # collision detection check (<2 maxRadius)
    collision = dist_matrix < 2*radius_max
    checkList = [collision[i][j] for i in range(N) for j in range(N) if j > i]
    if any(item == True for item in checkList):
        distribute_particles(particles, beam_focus_radius, jet_radius)
    # calculate interaction range
    R_interaction = 2*np.sqrt(beam_focus_radius**2+jet_radius**2)*gamma
    for i in range(N-1):
        for j in range(i+1,N):
                if dist_matrix[i][j] < R_interaction:
                    dist_matrix[i][j] = 2*radius_max
                    direction = (coords[j]-coords[i])
                    direction = direction/np.linalg.norm(direction)
                    hit = coords[i]+direction*radius_max
                    coords[j] = hit+(hit-coords[i])
    dist_matrix = distance.cdist(coords, coords, 'euclidean')
    overlap = dist_matrix < 2*radius_max
    removeList = []
    for i in range(N-1):
        for j in range(i+1,N):
            if overlap[i][j] == True:
                removeList.extend([i,j])
    num_removed = len(set(removeList))
    if len(set(removeList)) != 0:
        agg = build_bpca(num_pcles=num_removed, radius=radius_max)
        for i in range(num_removed):
            coords[sorted(set(removeList))[i],0] = agg.pos[i,0]+coords[sorted(set(removeList))[0],0]
            coords[sorted(set(removeList))[i],1] = agg.pos[i,1]+coords[sorted(set(removeList))[0],1]
            coords[sorted(set(removeList))[i],2] = agg.pos[i,2]+coords[sorted(set(removeList))[0],2]
    dist_matrix = distance.cdist(coords, coords, 'euclidean')
    collision = dist_matrix < 2*radius_max
    checkList = [collision[i][j] for i in range(N) for j in range(N) if j > i]
    if any(item == True for item in checkList):
        distribute_particles(particles, beam_focus_radius, jet_radius, gamma)
    return state, coords


def position_in_3d(particles, beam_focus_radius, jet_radius):
    state, coords = distribute_particles(particles, beam_focus_radius, jet_radius)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    for i in range(len(state)):
        x = np.concatenate([x,coords[i][0]])
        y = np.concatenate([y,coords[i][1]])
        z = np.concatenate([z,coords[i][2]])
    return x, y, z


def drawSphere(xCenter, yCenter, zCenter, r):
    # draw sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    # shift and scale sphere
    x = r*x + xCenter
    y = r*y + yCenter
    z = r*z + zCenter
