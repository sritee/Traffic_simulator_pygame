#traffic light simualator at Intersection, compatible with OpenAI gym environment type framework.
#declare an instance as env=traffic_simulator(change=0)
#Starts with green light on the vertical road. change indicates change the state of the traffic lights.
#The Reward is the total wait time at the intersection.

#traffic light simualator at Intersection, compatible with OpenAI gym environment type framework.
#declare an instance as env=traffic_simulator(change=0)
#Starts with green light on the vertical road. change indicates change the state of the traffic lights.
#The Reward is the total wait time at the intersection.

import pygame
from pygame.locals import *
import time
import random
import numpy as np

BLACK=(0,0,0)
 
#initialize display
 
class veh:
    def __init__(self,horz):
        self.horz=horz #Horz road car, or vertical road.
        self.display_size=600
        self.car_width=3
        self.car_height=30
        self.light_width=30
        self.light_height=75
        self.road_height=500
        self.road_width=126
        self.reset()
        
            
    def move(self):
        if self.horz==0:
            self.y=self.y-4
            if self.y<-1*self.car_height:
                self.reset()
                #add delay
        else:
            self.x=self.x+4
            if self.x>self.display_size:
                self.reset()
                #add delay
    def reset(self):
        #wait time of vehicle
        self.wait_time=0
        #resetting position if goes beyond the screen
        if self.horz==0:
            self.y=self.display_size+random.randint(1,1*self.road_height)
            self.x=self.display_size/2+random.randint(int(-self.road_width/2),int(self.road_width/2))
            
        else:
            self.x=random.randint(-1*self.road_height,0)
            self.y=self.display_size/2+random.randint(int(-self.road_width/2),int(self.road_width/2))
 
class traffic_simulator:
    def __init__(self):
        
        self.display_size=600
        self.car_width=3
        self.car_height=30
        self.light_width=30
        self.light_height=75
        self.road_height=500
        self.road_width=126
        self.rew=[]
        
        
        pygame.init()
        self.gameDisplay=pygame.display.set_mode((self.display_size,self.display_size))
        pygame.display.set_caption('Traffic_scenario')
        self.clock=pygame.time.Clock()
        
        
        self.background=pygame.image.load('./images/background.png')
        self.car_ver=pygame.image.load('./images/car_v_r.jpg')
        self.car_hor=pygame.image.load('./images/car_h_r.jpg')
        self.green_light=pygame.image.load('./images/go_light_r.jpg')
        self.red_light=pygame.image.load('./images/stop_light_r.jpg')
        self.road_v=pygame.image.load('./images/road_vertical.jpg')
        self.road_h=pygame.image.load('./images/road_horizontal.jpg')
        self.green_light_rot=pygame.image.load('./images/go_light_r.rotated.jpg')
        self.red_light_rot=pygame.image.load('./images/stop_light_r.rotated.jpg')
        self.lights=0
        self.change_time=time.time()
        self.cars_ver=[]
        self.num_cars_v=18 #number of vertical cars
        self.num_cars_h=50 #number of horizontal cars
        self.step_duration=0
    
 
        
        for k in range(self.num_cars_v):
            a=veh(horz=0)
            self.cars_ver.append(a)
        
        self.cars_hor=[]
        for k in range(self.num_cars_h):
            a=veh(horz=1)
            self.cars_hor.append(a)



    def draw(self,obj,x,y):
        self.gameDisplay.blit(obj, (x,y))
        

    def draw_background(self):
        self.draw(self.background,0,0)
        self.draw(self.road_v,int((self.display_size-self.road_width)/2),0)
        self.draw(self.road_h,0,int((self.display_size-self.road_width)/2))
        
        if self.lights==1:
            self.draw(self.green_light,int(0.5*(self.display_size+self.road_width)),int(0.5*(self.display_size+self.road_width)))
            self.draw(self.red_light_rot,int(0.5*(self.display_size-self.road_width))-self.light_height,int(0.5*(self.display_size-self.road_width))-self.light_width)
            
    
        else:
            self.draw(self.red_light,int(0.5*(self.display_size+self.road_width)),int(0.5*(self.display_size+self.road_width)))
            self.draw(self.green_light_rot,int(0.5*(self.display_size-self.road_width))-self.light_height,int(0.5*(self.display_size-self.road_width))-self.light_width)

    
    def step(self,change): #run simulaion for time_step seconds
        if change==1: #change the traffic light
            self.lights=not(self.lights)
            self.change_time=time.time()
        reward=0
        
        
        t_end = time.time()+1.5
        while time.time() < t_end:
        
            self.draw_background()
          
            
            for a in self.cars_ver:
                collision=0
                for tee in self.cars_ver:
                        if np.abs(tee.x-a.x)<2*a.car_width:
                            if tee.y<a.y and a.y-tee.y<1.5*a.car_height:
                                collision=1
                if not(self.lights==0 and a.y>((self.display_size/2)+self.road_width/2) and a.y<((self.display_size/2)+self.road_width/2+10) or collision==1):
                    a.move()
                else:
                    reward-=0.1
                if a.y<0:
                    #self.wait_arr.append(a.wait_time)
                    a.reset()
                
                self.draw(self.car_ver,a.x,a.y)
            for a in self.cars_hor:
                collision=0
                for tee in self.cars_hor:
                        if np.abs(tee.y-a.y)<2*a.car_width:
                            if tee.x>a.x and tee.x-a.x<1.5*a.car_height:
                                collision=1
                if not(self.lights==1 and a.x<((self.display_size/2)-self.road_width/2) and a.x>((self.display_size/2)-self.road_width/2-100) or collision==1):
                    a.move()
                else:
                    reward-=0.1
                if a.x>550:
                    #self.wait_arr.append(a.wait_time)
                    a.reset()
                self.draw(self.car_hor,a.x,a.y)
           
                
            pygame.display.update()
            
            self.gameDisplay.fill(BLACK)
           
            self.clock.tick(60)
        
        duration=time.time()-self.change_time #duration since the traffic light was last changed.
        
        return [np.array([self.lights,np.clip(duration/10,0,1)]),0.01*reward]
        

