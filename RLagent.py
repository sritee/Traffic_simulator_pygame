#generally takes ~10 or so minutes to converge to an optimal policy, depending on the simulator setup
#Q-learning agent with Fourier basis for value function approximation.
#States include current state of traffic light, time since last traffic light change. Add queue length for adaptive aget.
import numpy as np
from a_traffic_simulator import traffic_simulator
import random

env =traffic_simulator()
num_actions=2
num_episodes=300
fourier_order=2 #change order as desired.
basealpha=0.001#change required base alpha
observations_dim=2 #the observations in the environment
w=np.random.uniform(0,0.01,[pow(fourier_order+1,observations_dim),num_actions])  #weight matrix, with number of columns equal number of actions
gamma=1 #discount factor
zeta=0.95 #bootstrapping parameter, note that lambda is keyword in python
epsilon=0.2 #set exploration parameter as desired

def createalphas(basealpha,fourier_order,observations_dim):  #different alpha for different order terms of fourier
    temp=tuple([np.arange(fourier_order+1)]*observations_dim)
    b=np.array(np.meshgrid(*temp)).T.reshape(-1,observations_dim)
    c=np.linalg.norm(b,axis=1)
    d=basealpha/(c+1e-10)
    d[0]=basealpha
    d = np.expand_dims(d, axis=1)
    alphavec=np.tile(d,num_actions)
    alphavec=np.reshape(alphavec,(-1,num_actions))
    return alphavec
    
def normalize(state):
    
    normstate=np.empty(np.shape(state))
    val=np.zeros([observations_dim])
    val1=np.ones([observations_dim])
    
    for i in range(np.shape(state)[0]):
        normstate[i]=translate(state[i],val[i],val1[i],0,1)
    return normstate
    
def computeFourierBasis(state,fourier_order,observations_dim):
    normstate=normalize(state)
    temp=tuple([np.arange(fourier_order+1)]*observations_dim)
    b=np.array(np.meshgrid(*temp)).T.reshape(-1,observations_dim)
    return np.cos(np.pi*np.dot(b,normstate))        

def computevalue(w,action,state): #compute value of taking some state in some state
    return np.dot(w[:,action],computeFourierBasis(state,fourier_order,observations_dim))
    
def updateweights(w,e,alphavec,delta):
    
    w= w+ delta*alphavec*e;
    return w
    
def epsilon_greedy(state,epsilon,w): #pass a state where agent is eps-greedy, weight matrix w
    
    temp=np.zeros([1,num_actions])
    for k in range(num_actions):
        temp[0,k]=computevalue(w,k,state)
    c=np.argmax(temp) 
    
    if np.random.rand(1)< epsilon:
        c=random.randint(0,1) #epsilon greedy
    return c
    
def translate(value, leftMin, leftMax, rightMin, rightMax):
   
    leftrange = leftMax - leftMin
    rightrange = rightMax - rightMin
    #Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / leftrange
     #Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightrange)
    
alphavec=createalphas(basealpha,fourier_order,observations_dim)
e=np.zeros(np.shape(w))
curaction=epsilon_greedy(np.array([0,0]),epsilon,w)  #epsilon greedy 
monitor_action=[]
curstate=np.array([1,0])
num_steps=0
for m in range(3):
    env.step(0)
while True:
    #print(normalize(curstate))
    e[:,curaction]=e[:,curaction]+ computeFourierBasis(curstate,fourier_order,observations_dim); #accumulating traces
    #nextstate,reward, done, info = env.step(curaction) 
    nextstate,reward=env.step(curaction)
    reward=np.clip(reward,-1,0)
    done=0
    delta = reward - computevalue(w,curaction,curstate);   #The TD Error
    print('delta is {}'.format(delta))
                      

    if done:
        print("Episode finished")
        w=updateweights(w,e,alphavec,delta)
        break
    
    nextaction=epsilon_greedy(nextstate,epsilon,w)
    #print(nextaction)
    delta=delta+ gamma*computevalue(w,nextaction,nextstate)
    w=updateweights(w,e,alphavec,delta) #update the weight vector
    e=e*gamma*zeta             #trace decay parameter zeta
    curstate=nextstate
    curaction=nextaction
    #print('action take is {}'.format(curaction))
    #print('curstate is {} and nextstate is {}'.format(curstate,nextstate))
    if num_steps>50:
        epsilon=epsilon*0.95
    if len(monitor_action)>7:
        monitor_action.pop(0)
    monitor_action.append(curaction)
    if num_steps%1==0:
        #print('average action is {} with epsilon {}'.format(np.average(np.array(monitor_action)),epsilon))
        print('action{} in state{} with reward {}'.format(curaction,curstate,reward))
    num_steps+=1
    if num_steps%25==0:
        env=traffic_simulator()
        for k in range(3):
            env.step(change=0)
        e=np.zeros(np.shape(w))
        curaction=epsilon_greedy(np.array([0,0]),epsilon,w) 
        curstate=np.array([1,0])
    
    #if num_steps%30==0:
        #env=traffic_simulator()
    

                       
        
            
