import pygame
from pygame.locals import *
import random

pygame.init()
# create window 
width = 500
height = 500
screen_size = (width,height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('car game')

#colors
gray = (100,100,100)
green = (70,200,50)
red = (200,0,0)
white = (255,255,255)
yellow = (255,230,0)

#road nd sizes 
road_width = 300
marker_width = 10
marker_height = 50

#lane coordinates 
left_lane = 150
centre_lane = 250
right_lane = 350
lanes = [left_lane,centre_lane,right_lane]

#game setiings
gameover = False
speed = 2
score = 0 

#road and edge markers 
road = (100,0,300,height)
left_edge_marker = (95,0,marker_width,height)
right_edge_marker = (395,0,marker_width,height)


lane_marker_move_y = 0

def welcome_screen():
    pass

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image,x,y):
        pygame.sprite.Sprite.__init__(self)


        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))


        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

class PlayerVehicle(Vehicle):
    def __init__(self,x,y):
        image = pygame.image.load('images/car.png')
        super().__init__(image,x,y)
        
player_x= 250
player_y= 400

player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x,player_y)
player_group.add(player)




image_filenames = ['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
vehicle_images = []
for imfiles in image_filenames:
    image = pygame.image.load('images/' + imfiles)
    vehicle_images.append(image)

vehicle_Group = pygame.sprite.Group()



#crash 
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()



#game loop 
clock = pygame.time.Clock()
#fps = frames per second
fps = 120
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == quit:
            running = False 


        if event.type == KEYDOWN:

            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            for vehicles in vehicle_Group:
                if pygame.sprite.collide_rect(player,vehicle):

                    gameover = True

                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1] / 2)]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1] / 2)]                        

#draw the grass 
    screen.fill(green)

    #creating road of color gray  
    pygame.draw.rect(screen,gray,road)

    #adding colors on road sides
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    #making lane markers to move 
    lane_marker_move_y += speed*2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    #adding lane whitte lines
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y,marker_width,marker_height))
        pygame.draw.rect(screen, white, (centre_lane + 45, y + lane_marker_move_y,marker_width,marker_height))

    
    player_group.draw(screen)

    #adding upto 2 vehicles at a time in a scenerio 
    if len(vehicle_Group) < 2:
        
        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_Group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_Group.add(vehicle)

        #making vehicles move 
    for vehicle in vehicle_Group:
        vehicle.rect.y += speed


        if vehicle.rect.top >= height:
            vehicle.kill()

            score +=1

        #speeding up vehicles once 5 vehicles passes 
        if score > 0 and score >= 5:
            speed = 3

        #speeding up vehicles once 10 vehicles passes 
        if score > 5 and score >= 10:
           speed = 4

    vehicle_Group.draw(screen)

    #display game score 
    font = pygame.font.Font(pygame.font.get_default_font(),20)
    text = font.render('Score: ' + str(score),True, red)
    text_rect = text.get_rect()
    text_rect.center = (450,40)
    screen.blit(text,text_rect)



#checking if coloosion is from top 
    if pygame.sprite.spritecollide(player, vehicle_Group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0],player.rect.top]

    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(),16)
        text = font.render('Game Over \n Play Again? Enter y/n', True, white)
        # text.rect = text.get_rect(50,50)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    running =  True
                    speed = 2
                    score = 0
                    vehicle_Group.empty()
                    player.rect.center = [player_x,player_y]
                elif event.key == K_n:
                    gameover = False 
                    running = False
                    pygame.quit()