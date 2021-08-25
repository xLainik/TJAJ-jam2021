import pygame, math

def center_distance(rect1, rect2):
    return math.sqrt((rect1.centerx - rect2.centerx)**2 + (rect1.centery - rect2.centery)**2)

def center_angle(rect1, rect2):
    return math.atan2(rect2.centery - rect1.centery, rect2.centerx - rect1.centerx)
