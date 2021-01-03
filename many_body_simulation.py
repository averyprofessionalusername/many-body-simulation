#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 23:25:28 2020

@author: dominicbolton

visual simulation of planets orbiting each other
"""

import numpy as np
import pygame

pygame.init()

Tracer = False

windowsize = [1300,800]

numplanet = 10
numstars = 50

class planet:
    """
    planet object has mass, radius, position and velocity. radius is determined
    by mass
    """
    def __init__(self, name,  mass, pos, vel, colour = (100,100,100)):
        self.name = name
        self.mass = mass
        self.rad = mass**(1/3)*4
        self.pos = pos
        self.vel = vel
        self.colour = colour
        

def make_planets(numplanet):
    """
    makes a list of planets with random values. numplanet is the number of 
    planets created
    """
    planets = []
    
    for i in range(numplanet):
        mass = np.random.rand(1,1)*100
        pos = np.random.rand(1,2)*np.array((1000,600)) + 100
        pos = [pos[0,0],pos[0,1]]
        vel = np.random.rand(1,2)*3 - 1.5
        vel = [vel[0,0],vel[0,1]]
        colour = np.random.rand(1,3)*255
        colour = [colour[0,0]//1, colour[0,1]//1, colour[0,2]//1]
        name = 'planet{}'.format(str(i))
        #print (colour)
        planets.append(planet(name,mass,pos,vel,colour))       
    
    return planets

def pairs(items):
    """
    takes a list of items of length m and returns a 2*m^2 array of all 
    possible pairs of items, omitting self pairs eg (i,i)
    """
    arr = [[np.array([])]]
    for i in items:
        #print (i.name)
        for j in items:
            #print (j.name)
            if i.name == j.name:
                #print (i.name, j.name)
                continue
            else:
                #print (i,j)
                #print ('appending')
                arr.append([i,j])
    #print (arr)
    return arr
    

def force_g(planets, list_planets):
    """
    calculates magnitude and direction of force on planet1 due to planet2
    """
    planet1, planet2 = planets[0], planets[1]
    distance = np.sqrt((planet1.pos[0] - planet2.pos[0])**2 + (planet1.pos[1]
                                                        - planet2.pos[1])**2)
    
    if distance <= planet1.rad + planet2.rad and planet1 in list_planets and planet2 in list_planets:
        newplanets = merge(planets, list_planets)
    else:
        newplanets = list_planets
    
    f_mag = 10*planet1.mass * planet2.mass / (distance)**2
    
    f_dir = ((planet2.pos[0] - planet1.pos[0])/distance, (planet2.pos[1] - planet1.pos[1])/distance)
    
    fx, fy = f_mag*f_dir[0], f_mag*f_dir[1]
    
    return [fx, fy], newplanets

def merge(planets, list_planets):
    """
    merges planets in planets together, conserving momentum to create a new bigger planet
    """
    planet1, planet2 = planets[0], planets[1]    
    
    planet1_momentum = [planet1.vel[0]*planet1.mass, planet1.vel[1]*planet1.mass]
    planet2_momentum = [planet2.vel[0]*planet2.mass, planet2.vel[1]*planet2.mass]
    
    newplanet_momentum = [planet1_momentum[0] + planet2_momentum[0], planet1_momentum[1] + planet2_momentum[1]]
    newplanet_momentum_mag, newplanet_momentum_dir = vect_split(newplanet_momentum)
    
    newplanet_mass = planet1.mass + planet2.mass
    newplanet_vel = [newplanet_momentum_mag * newplanet_momentum_dir[0]/newplanet_mass,
                     newplanet_momentum_mag * newplanet_momentum_dir[1]/newplanet_mass]
    newplanet_pos = vect_avg(planet1.pos, planet2.pos)
    
    newplanet_colour = vect_avg(planet1.colour, planet2.colour)
    
    newplanet_name = 'planet{}'.format(str(len(list_planets)))
    
    newplanet = planet(newplanet_name, newplanet_mass, newplanet_pos, newplanet_vel, newplanet_colour)
    
    list_planets.remove(planet1)
    list_planets.remove(planet2)
    list_planets.append(newplanet)
        
    return list_planets

def vect_split(vector):
    """
    splits a vector into its magnitude and direction
    """
    mag = np.sqrt(vector[0]**2 + vector[1]**2)
    direction = [vector[0]/mag, vector[1]/mag]
    
    return mag, direction

def vect_avg(vect1, vect2):
    """
    returns the average of 2 vectors, must be same dimension
    """
    new_vect = []
    for i in range(len(vect1)):
        new_vect.append((vect1[i] + vect2[i])/2)
        
    return new_vect

def paint_background(window, starcoords):
    """
    paints the background of space black with some stars at random coordinates
    """
    
    window.fill((0,0,0))
        
    for star in starcoords:
        pygame.draw.circle(window, (255,255,255), star, 2)
        
    return None

def starmaker(window, numstars, windowsize):
    """
    makes star coordinates using random numbers
    """
    
    coords = np.random.rand(numstars, 2)
    
    starcoords = []
    for star in coords:
        star = star*windowsize
        starcoords.append(star)
    
    return starcoords
    
        
window = pygame.display.set_mode(windowsize)
pygame.display.set_caption("manybodysim")

list_planets = make_planets(numplanet)

planet_pairs = pairs(list_planets)

starcoords = starmaker(window, numstars, windowsize)

paint_background(window, starcoords)

run = True
while run:
    pygame.time.delay(20)
    pygame.display.update()
    
    if not Tracer:
        paint_background(window, starcoords)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #print (planet_pairs)
    for pair in planet_pairs:
        #print (pair)
        for plant in list_planets:
            #print (pair)
            if pair[0] == plant:
                force, list_planets = force_g(pair, list_planets)
                planet_pairs = pairs(list_planets)
                plant.vel[0] += force[0]/plant.mass
                plant.vel[1] += force[1]/plant.mass
         
    for plant in list_planets:
        plant.pos[0] += plant.vel[0]
        plant.pos[1] += plant.vel[1]
        pygame.draw.circle(window, plant.colour, plant.pos, plant.rad)
    

pygame.quit()

    
    