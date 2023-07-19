#some problem occurred
import pygame
import os
import random
import math
#initialize
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#import image
list_of_terrain = []
grassland_image = pygame.image.load(os.path.join("images", "grassland.png")).convert_alpha()
plain_image = pygame.image.load(os.path.join("images", "plain.png")).convert_alpha()
mountain_image = pygame.image.load(os.path.join("images", "mountain.png")).convert_alpha()
coast_image = pygame.image.load(os.path.join("images", "coast.png")).convert_alpha()
desert_image = pygame.image.load(os.path.join("images", "desert.png")).convert_alpha()
ocean_image = pygame.image.load(os.path.join("images", "ocean.png")).convert_alpha()
tundra_image = pygame.image.load(os.path.join("images", "tundra.png")).convert_alpha()
tundra_forest_image = pygame.image.load(os.path.join("images", "tundra_forest.png")).convert_alpha()
snow_image = pygame.image.load(os.path.join("images", "snow.png")).convert_alpha()
#variable about image
x = grassland_image.get_width()
y = grassland_image.get_height()
grassland_image = pygame.transform.scale(grassland_image,(x*2,y*2)) #1
plain_image = pygame.transform.scale(plain_image,(x*2,y*2)) #2
mountain_image = pygame.transform.scale(mountain_image,(x*2,y*2)) #3
coast_image = pygame.transform.scale(coast_image, (x*2,y*2)) #4
desert_image = pygame.transform.scale(desert_image, (x*2,y*2)) #5
ocean_image = pygame.transform.scale(ocean_image, (x*2,y*2)) #6
tundra_image = pygame.transform.scale(tundra_image, (x*2,y*2)) #7
tundra_forest_image = pygame.transform.scale(tundra_forest_image, (x*2,y*2)) #8
snow_image = pygame.transform.scale(snow_image, (x*2,y*2)) #8z
x = grassland_image.get_width()
y = grassland_image.get_height()
print(x,y)
dict_of_terrain = {grassland_image:'1', plain_image:'2', mountain_image:'3', coast_image:'4', desert_image:'5', ocean_image:'6', tundra_image:'7', tundra_forest_image:'8', snow_image:'9'}
list_of_terrain = []
for picture in list(dict_of_terrain.keys()):
    for a in range(20):
        list_of_terrain.append(picture)
copy_of_list_of_terrain = list_of_terrain[:]
print(len(list_of_terrain),len(copy_of_list_of_terrain))

#other variable
FPS = 60
clock = pygame.time.Clock()
running = True
dragging = False
scale = 1
background_coordinate = [0,0]
storing_surface = pygame.Surface((800,600))

#some definitions
#draw the background and insert into a file
class background_drawing():
    def __init__(self,coordinate,list_of_terrain,copy_of_list_of_terrain,x,y):
        self.copy_of_list_of_terrain = copy_of_list_of_terrain
        self.list_of_terrain = list_of_terrain
        self.coordinate = coordinate
        self.copy_of_x = coordinate[0]
        self.copy_of_y = coordinate[1]
        self.x = x
        self.y= y
        self.index_dict = {}
        self.number = 1
        self.choice = random.choice(self.list_of_terrain)
        print(len(self.copy_of_list_of_terrain))
    def drawing(self):
        w = 1200
        h = 900
        self.copy_of_x = self.coordinate[0]
        self.copy_of_y = self.coordinate[1]
        global surface
        surface = pygame.Surface(((w+self.list_of_terrain[0].get_width()*3/4), (h+self.list_of_terrain[0].get_height())))
        surface.fill((0,255,0))
        flag = True
        #setting the frame
        while self.coordinate[1]-self.copy_of_y <= h:
            while self.coordinate[0]-self.copy_of_x <= w:
                #note that the outer layer should be ocean
                if abs(self.coordinate[0]-self.copy_of_x) <= 320 or abs(self.coordinate[1]-self.copy_of_y) <= 280 or abs(self.coordinate[0]-w) <= 320 or abs(self.coordinate[1]-h) <= 280:
                    surface.blit(ocean_image, (self.coordinate))
                    self.index_dict[tuple(self.coordinate)] = (6, self.number)
                else:
                    self.choice = random.choice(self.list_of_terrain)
                    surface.blit(self.choice, self.coordinate)
                    self.list_of_terrain = self.copy_of_list_of_terrain[:]
                    self.index_dict[tuple(self.coordinate)] = (dict_of_terrain[self.choice], self.number)
                self.coordinate[0] += self.x*3/2
            self.coordinate[1] += self.y/2
            self.coordinate[0] = self.copy_of_x
            if flag:
                self.coordinate[0] += self.x*3/4
                flag = False
            else:
                flag = True
            self.number += 0.5
        save_directory = os.path.join("images")
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        save_path = os.path.join(save_directory, "map.png")
        pygame.image.save(surface, save_path)
#insert the image into the file
instance = background_drawing(background_coordinate,list_of_terrain,copy_of_list_of_terrain,x,y)
instance.drawing()
background_coordinate = [0,0]
maps = pygame.image.load(os.path.join("images", "map.png")).convert_alpha()
copy_of_maps = pygame.image.load(os.path.join("images", "map.png")).convert_alpha()
screen.blit(maps,background_coordinate)
x1 = maps.get_width()
y1 = maps.get_height()

#game loop
while running:
    #clock.tick(FPS)
    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            last_mouse_coordinate = event.pos
            calibrate_coordinate = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if scale <= 2:
                maps = pygame.transform.scale(copy_of_maps, (x1, y1))
                scale += 0.1
                scale = round(scale,2)
                maps = pygame.transform.scale(copy_of_maps, (maps.get_width()*scale, maps.get_height()*scale))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if scale >= 0.5:
                maps = pygame.transform.scale(copy_of_maps, (x1, y1))
                scale -= 0.1
                scale = round(scale,2)
                maps = pygame.transform.scale(copy_of_maps, (maps.get_width()*scale, maps.get_height()*scale))
  
    #loop       
    if dragging:
        now_mouse_coordinate = pygame.mouse.get_pos()
        last_mouse_coordinate = calibrate_coordinate
        calibrate_coordinate = pygame.mouse.get_pos()
        delta_x = now_mouse_coordinate[0] - last_mouse_coordinate[0]
        delta_y = now_mouse_coordinate[1] - last_mouse_coordinate[1]
        background_coordinate = [background_coordinate[0]+delta_x,background_coordinate[1]+delta_y]
    #render
    screen.fill((0,0,0))    
    screen.blit(maps,background_coordinate)
    pygame.display.update()
pygame.QUIT
