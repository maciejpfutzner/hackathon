"""
Module for creating the racing tracks each of which is an instance of class Track.
Allows to create a flat block, series of slopes or a continuous track with
parametrised roughness. Class method build the track as a series of box2d polygons.

TODO:
    Write class docstrings!
    Make the spawnpoint just above the first track segment
    Provide a finish point to run_simulation
"""

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody, vec2)
import random
from datetime import datetime
import math

class Track:
    def __init__(self, length, roughness=0, seed=None):
        self.length = length
        self.roughness = roughness
        self.seed = seed
        self.generated = False
        self.generate()

    def generate(self):
        if self.seed:
            random.seed(seed)
        else:
            random.seed(datetime.now())

        if self.roughness == 0:
            self.gen_flat()
        elif self.roughness == 1:
            self.gen_slopes()
        else:
            self.gen_rough(self.roughness-1)

    def build(self, world):
        if not self.generated:
            return None

        start = 0
        self.bodies = []
        for i in xrange(self.n_segments):
            body = world.CreateStaticBody(
                    position=self.seg_positions[i],
                    angle=self.seg_angles[i],
                    shapes=polygonShape(
                        box=(self.seg_lengths[i]/2., .5)))
            start += self.seg_lengths[i]
            self.bodies.append(body)

        return self.length


    def gen_flat(self):
        self.n_segments = 1
        self.seg_lengths = [self.length]
        self.seg_angles = [0]
        self.seg_positions = [(0,3)]
        self.spawn = (5, 10)
        self.generated = True

    def gen_slopes(self):
        seg_len = 30
        nn = self.length/seg_len
        self.n_segments = nn
        self.seg_lengths = [seg_len for x in xrange(nn)]
        self.seg_angles = [0.15 for x in xrange(nn)]
        self.seg_positions = [(0.9*seg_len*x,3) for x in xrange(nn)]
        self.spawn = (5, 10)
        self.generated = True

    def gen_rough(self, roughness):
        SEG_LENGTH = 15
        nn = self.length/SEG_LENGTH
        self.n_segments = nn
        self.seg_lengths = [0]*nn
        self.seg_angles = [0]*nn
        self.seg_positions = [0]*nn
        prev_pos = vec2(0, 20) # starting coordinates
        for i in xrange(nn):
            self.seg_lengths[i] = SEG_LENGTH
            angle = random.uniform(-0.1, 0.1)*roughness
            self.seg_angles[i] = angle
            length = SEG_LENGTH * math.cos(angle)
            height = SEG_LENGTH * math.sin(angle)
            self.seg_positions[i] = prev_pos + (.5*length, .5*height)
            prev_pos += (length, height)
        self.spawn = (SEG_LENGTH, 30)
        self.generated = True

    def get_spawn_pos(self):
        if not self.generated:
            print 'Error, track not generated for some reason'
            return None
        return self.spawn

