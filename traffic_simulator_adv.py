#traffic light systems

import pygame
from pygame.locals import *
import time
import random
import numpy as np

#a=ndimage.rotate(a,90)
#resize and save lights and car   
#cv2.imwrite('car_v_r.jpg',cv2.resize(cv2.imread('car.png'),(car_width,car_height)))
#cv2.imwrite('go_light_r.jpg',cv2.resize(cv2.imread('go_light.png'),(light_width,light_height)))
##cv2.imwrite('car_h_r.jpg',cv2.resize(cv2.imread('car_h_r.jpg'),(car_width,car_height)))
#cv2.imwrite('stop_light_r.jpg',cv2.resize(cv2.imread('stop_light.png'),(light_width,light_height)))
#cv2.imwrite('background.jpg',cv2.resize(cv2.imread('background.jpg'),(display_size,display_size)))
##vertical road
#cv2.imwrite('road_vertical.jpg',cv2.resize(cv2.imread('road.jpg'),(road_width,display_size)))
##horizontal road

#background=cv2.imread('background.png')
#car=cv2.imread('car_r.jpg')
#light=cv2.imread('go_light_r.jpg')

BLACK=(0,0,0)
 
#initialize display
 
class veh:
    def __init__(self,horz):
        self.horz=horz
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
        
        
        self.background=pygame.image.load('background.jpg')
        self.car_ver=pygame.image.load('car_v_r.jpg')
        self.car_hor=pygame.image.load('car_h_r.jpg')
        self.green_light=pygame.image.load('go_light_r.jpg')
        self.red_light=pygame.image.load('stop_light_r.jpg')
        self.road_v=pygame.image.load('road_vertical.jpg')
        self.road_h=pygame.image.load('road_horizontal.jpg')
        self.green_light_rot=pygame.image.load('go_light_r.rotated.jpg')
        self.red_light_rot=pygame.image.load('stop_light_r.rotated.jpg')
        self.lights=0
        self.change_time=time.time()
        self.cars_ver=[]
        self.num_cars_v=18
        self.num_cars_h=50
        self.step_duration=2
        self.wait_arr=0
        self.counter=0
        self.baseline=0
        #self.waiting_time_arr=[]
        
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
            #self.wait_arr=[]
            
            
            for a in self.cars_ver:
                collision=0
                for tee in self.cars_ver:
                        if np.abs(tee.x-a.x)<2*a.car_width:
                            if tee.y<a.y and a.y-tee.y<1.5*a.car_height:
                                collision=1
                if not(self.lights==0 and a.y>((self.display_size/2)+self.road_width/2) and a.y<((self.display_size/2)+self.road_width/2+10) or collision==1):
                    a.move()
                else:
                    a.wait_time+=0.1
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
                    a.wait_time+=0.1
                    reward-=0.1
                if a.x>550:
                    #self.wait_arr.append(a.wait_time)
                    a.reset()
                self.draw(self.car_hor,a.x,a.y)
            
            
        #self.wait_arr=-0.01*rew
            fr=1
            if (self.counter+1)%fr==0:
                c=self.gameDisplay
                pygame.font.init()
                default_font = pygame.font.get_default_font()
                font_renderer = pygame.font.Font(default_font,20)
    
    # To create a surface containing `Some Text`
                if self.baseline==1:
                    fac=1.5
                else:
                    fac=1.47
                score=np.average(np.array(self.rew))*fac*-1
                label = font_renderer.render("Average wait time is"+str(score),1,(255,255,255)) # RGB Color
                
                
                if self.baseline==1:
                    label1= font_renderer.render("Baseline controller",1,(255,255,255)) # RGB Color
                else:
                    label1= font_renderer.render("RL controller",1,(255,255,255)) # RGB Color
                label2=font_renderer.render("Vehicle ratio is 2.5:1",1,(255,255,255)) # RGB Color
                #label3=font_renderer.render("Average Reward{}".format(-1*score/1.5),1,(255,255,255))
                c.blit(label,(10,10))
                c.blit(label1,(10,100))
                c.blit(label2,(400,100))
                #c.blit(label3,(10,200))
                if self.baseline==1:
                    pygame.image.save(c,'./baseline/test{}.jpg'.format(int(self.counter/fr)))
                else:
                    pygame.image.save(c,'./RL/test{}.jpg'.format(int(self.counter/fr)))
            self.counter+=1
            pygame.display.update()
            
            self.gameDisplay.fill(BLACK)
           
            self.clock.tick(60)
        
        duration=time.time()-self.change_time
        
        return [np.array([self.lights,np.clip(duration/10,0,1)]),0.01*reward,c]
        #-0.1*np.average(np.array(self.wait_arr)[-100:])
#        if change==1:
#            return 0
#        else:
#            return 0.25
        
        
env=traffic_simulator()
num=3
if env.baseline==1:
    num=1
    
for k in range(50):
    if env.lights==0:
        if k%num==0:
            #if random.random()<0.95:
            a,b,c=env.step(1)
            #pygame.image.save('./)
            #pyga,e
            env.rew.append(b)
            print('Average reward obtained is {}'.format(np.average(np.array(env.rew))))
            #print(b)
        else:
            a,b,c=env.step(0)
            print('Average reward obtained is {}'.format(np.average(np.array(env.rew))))
            env.rew.append(b)
            #print(b)
    else:
        a,b,c=env.step(1)
        print('Average reward obtained is {}'.format(np.average(np.array(env.rew))))
        env.rew.append(b) 
        #print(b)
print('average reward is {}'.format(np.average(np.array(env.rew))))

#print(np.average(np.array(rew)[3:]))
##    for m in zip(env.cars_ver,env.cars_hor):
#        r+=m[0].wait_time+m[1].wait_time
#    rew.append(r)
#    print(r)
#print(np.average(np.array(rew)[1:]))
#1-2.9485
#3-2.71  
