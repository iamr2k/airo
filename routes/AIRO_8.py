print('importiing libraries For Raspberry Pi')
import csv
import RPi.GPIO as GPIO
import time
import csv
import time
import pandas as pd
from itertools import chain
import numpy as np


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

R1 = 14
R2 = 15   #Right side motor's 2 GPIO

L1 = 18
L2 = 23   #Left side motor's 2 GPIO

IR1 = 19 #left
IR2 = 13 #centre
IR3 = 26 #right

TRIG = 25 
ECHO = 24


GPIO.setup(L1, GPIO.OUT)
p = GPIO.PWM(L1, 20)
p.start(0)

GPIO.setup(L2, GPIO.OUT)
q = GPIO.PWM(L2, 20)
q.start(0)

GPIO.setup(R1, GPIO.OUT)
a = GPIO.PWM(R1, 20)
a.start(0)

GPIO.setup(R2, GPIO.OUT)
b = GPIO.PWM(R2, 20)
b.start(0)



GPIO.setup(IR1,GPIO.IN)

GPIO.setup(IR2,GPIO.IN)

GPIO.setup(IR3,GPIO.IN)

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)



# stop(): Stops both motors
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)

stop()

import pandas as pd
print("pandas loaded")

def sensor1():
    S1 = GPIO.input(IR1)
    return S1
def sensor2():
    S2 = GPIO.input(IR2)
    return S2
def sensor3():
    S3 = GPIO.input(IR3)
    return S3

  
    
    

    


    

#variables
speed = 15
frq = 1
frqsp = []*4


anom = [[0]*1000]*31
anomtype = [[0]*1000]*31
anomduration = [[0]*1000]*31


insttype = [0]
distance = [30,30]


validation = [0,0]
train = [1,[30],0,0.05]
score = [0]
error = [0]
recoverycount = [0]
train_time = [100]






GPIO.output(TRIG, False)

    
def ULTRA():
        
    global distance
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pass
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pass
        duration = time.time() - pulse_start
        d = (duration * 17150)
    distance.append(d)
    
        




    
def forward(frqsp):
    
    speed = frqsp[0]
    frq = frqsp[1]
    s = frqsp[2]
    q.ChangeDutyCycle(speed)
    q.ChangeFrequency(frq)
    p.ChangeDutyCycle(0)
                   
    b.ChangeDutyCycle(speed)
    b.ChangeFrequency(frq)
    a.ChangeDutyCycle(0)
    time.sleep(s)
    stop()
    return


def right(frqsp):
    speed1 = frqsp[0]
    speed2 = frqsp[1]
    frq = frqsp[2]
    s = frqsp[3]
    p.ChangeDutyCycle(speed2)
    p.ChangeFrequency(frq)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed1)
    b.ChangeFrequency(frq)
    time.sleep(s)
    stop()
    return

def left(frqsp):
    speed1 = frqsp[0]
    speed2 = frqsp[1]
    frq = frqsp[2]
    s = frqsp[3]
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed1)
    q.ChangeFrequency(frq)
                   
    a.ChangeDutyCycle(speed2)
    a.ChangeFrequency(frq)
    b.ChangeDutyCycle(0)
    time.sleep(s)
    stop()
    return


def recovery(frqsp):
    speed1 = frqsp[0]
    speed2 = frqsp[1]
    frq = frqsp[2]
    s = frqsp[3]
    stop()
    p.ChangeDutyCycle(speed1)
    a.ChangeDutyCycle(speed2)
    b.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    p.ChangeFrequency(frq) 
    a.ChangeFrequency(frq)
    time.sleep(s)
    stop()
    train[2] = 1
    return    
    




                     
    
def TRAIN(train):
    n = train[0]
    print("training Number ",n)
    train_start = time.time()
    flag = train[2]
    
    speedfactor = train[3]
    count = 0
    global distance
    global insttype
    global score
    global error
    global recoverycount
    global anom
    global anomtype
    global anomduration
    global train_time
 
    score.clear()
    error.clear()
    recoverycount.clear()
    speedtime = 0
    anomcount = 0
    
            
            
    
                
    while distance[-1] > 20 :
        flag = train[2]
        S1 = sensor1()
        S2 = sensor2()
        S3 = sensor3()
        if ((S1 == 1) and (S3 == 1) and (S2 == 0)):
            count +=1
            if anomtype[30][count] == 5:
                
                score.append(count)
                speedtime = speedfactor+anomduration[30][count]*0.003
                speed1 = 35+(anomduration[30][count])*0.05
                
                frq = 8
                print(speedtime,speed1)
                
            else :
                speedtime = 0.07
                error.append(count)
                speed1 = 35
                frq = 11


            
            
            frqsp= [speed1,frq,speedtime]
            c = 'f'
            
            forward(frqsp)
            insttype.append(5)
   
            if insttype[-1] != insttype[-2] :
                anom[n][count] = count
                anomtype[n][count] = insttype[-2]
                anomduration[n][count] = anom[n][count]-anom[n][count-1]
                if anomduration[n][count] < 0 :
                    anomduration[n][count] = 0
            stop()

        elif (S3 == 1) and (S1 == 0):
            count +=1

            if anomtype[30][count] == 6:

                score.append(count)
                speedtime = speedfactor+(anomduration[30][count])*0.003
                speed1 = 35+(anomduration[30][count])*0.05
                speed2 = 0+(anomduration[30][count])*0.05
                frq = 11
                
                print(speedtime,speed1,speed2)
            else :
                speedtime = 0.07
                error.append(count)
                speed1 = 35
                speed2 = 0
                frq = 11


            
            frqsp= [speed1,speed2,frq,speedtime]
            c = 'r'
            
            right(frqsp)
            insttype.append(6)

            if insttype[-1] != insttype[-2] :
                anom[n][count] = count
                anomtype[n][count] = insttype[-2]
                anomduration[n][count] = anom[n][count]-anom[n][count-1]
                if anomduration[n][count] < 0 :
                    anomduration[n][count] = 0
            stop()

        elif (S1 == 1) and (S3 == 0):
            count +=1

            if anomtype[30][count] == 4:

                score.append(count)
                speedtime = speedfactor+(anomduration[30][count])*0.003
                speed1 = 35+(anomduration[30][count])*0.05
                speed2 = 0+(anomduration[30][count])*0.05
                frq = 11
           
                print(speedtime,speed1,speed2)
            else :
                speedtime = 0.07
                error.append(count)
                speed1 = 35
                speed2 = 0
                frq = 11



            frqsp= [speed1,speed2,frq,speedtime]
            c = 'l'
            
            left(frqsp)
            insttype.append(4)
 
            if insttype[-1] != insttype[-2] :
                anom[n][count] = count
                anomtype[n][count] = insttype[-2]
                anomduration[n][count] = anom[n][count]-anom[n][count-1]
                if anomduration[n][count] < 0 :
                    anomduration[n][count] = 0
            stop()

        elif (S1 == S2 == S3):

            stop()
            error.append(count)
            recoverycount.append(count)
            flag = 0
            ULTRA()
            if min(distance) < 20 :
                stop()
                print("obsacle found....\n  at distance = ",distance[-1])
                
                print('\nscore = ',len(score),"\nerror = ",len(error))
                print("\nspeed factor",speedfactor,"\n speedtime",speedtime,"\n recoverycount",len(recoverycount))
                train_time.append(time.time() - train_start)
                print('\n time',train_time[-1])
                insttype.append(2)
                
                
            elif min(distance) > 18 :
                if c == 'r':
                    frqsp = [31,0,20,0.07]
                elif c == 'l':
                    frqsp = [0,31,20,0.07]
                else:
                    frqsp = [20,20,20,0.04]
                recovery(frqsp)
    if n > 1:
        print('new model obtained do you want to save it? (y/n')
        user = input()
        if user == 'y':
            anom[30] = anom[n]
            anomtype[30] = anomtype[n]
            anomduration[30] = anomduration[n]
            print("model updated")
        else :
            print("Model updation aborted")
            
        
            
    
    return insttype
          


def main():
    global distance
    global insttype
    global score
    global error
    global anom
    global anomtype
    global anomduration
    ULTRA()
    train = [1,[30],0,0.05]
    check = 0    
    stop()
    
    
    print('Enter option number \n\n 1.Open previously saved train \n 2.Fresh start\n 3.Run on trained path')
    user = input()
    if user == '1':
        print('enter file code to continue training')
        name = input()
        try :
            data = pd.read_csv('/home/pi/Desktop/routes/'+name+'.csv')
            file = pd.DataFrame(data)
            training_number = file.shape[1]
            check = 1
        except :
            print("file not found OR Empty file")
    elif user == '2':
        print('enter file code to create a new file')
        name = input()
        try :
            print('\ncreating file....')
            check = 1
        except :
            print("file error / same file may exist")
    elif user == '3':
        print('enter file code to open a new file')
        name = input()
        

        e = pd.read_csv('/home/pi/Desktop/routes/'+name+'.csv')
        e = e.fillna(0)
        print(e.head(20))
        size = list(e.shape)
        i = 0
        training = size[1]
        insttype = [[]]*training
        for i in range(training) :
          insttype[i] = list(e.iloc[:,i])

        training = size[1]
        
        anom_shifted = [[]]*(training)
        anomduration = [[]]*(training)
        anomtype = [[]]*(training)
        n = 0
        anom = [[]]*training 
        list1 = []  
        list2 = []
        list3 = []
        #Starting anomaly detection. store that anomalies in anom list
        while n < training:
          b = insttype[n]
          list1.clear()
          list2.clear()
          list3.clear()
          count = 1
          a = 1
          for count in range(len(insttype[n])):
            met1 = b[count]
            met2 = b[count - 1]
            if met1 != met2:
              list1.append(count)
              list2.append(met2)
              list3.append(count-a)
              a = count
              #mode = stats.mode
              #list2 = mode[0]
              count = count+1       
            anom[n] = list1[1:] #first numcer is zero
            anomtype[n] = list2[1:]
            anomduration[n] = list3[1:]
          anom = np.array(anom)
          
          n += 1
        anom = list(anom)
        print(list3)
        print('\n\n\n Now RUNNING')
        time.sleep(3)
        
        print("agent is running")
        n = training 
        count = 0
        test = []
        score = 0
        error = 0
        n = 0 #index of anom
        for i in range(len(anomtype[n])):
            condition = anomtype[n][i] 
            duration = anomduration[n][i]
            
            print('condition',condition)
            if (condition == 5):
                speed1 = 40
                speed2 = 40
                frq = 10
                speedtime = 0.05*duration
                frqsp= [speed1,frq,speedtime]
                count +=1
                forward(frqsp)
                #insttype.append('S')
                stop()
            elif (condition == 4):
                speed1 = 40
                speed2 = 0
                frq = 10
                speedtime = 0.05*duration
                frqsp= [speed1,speed2,frq,speedtime]
                c = 'r'
                count +=1
                right(frqsp)
                #insttype.append('R')
                stop()
            elif (condition == 6):
                speed1 = 40
                speed2 = 0
                frq = 10
                speedtime = 0.05*duration
                frqsp= [speed1,speed2,frq,speedtime]
                c = 'l'
                count +=1
                left(frqsp)
                #insttype.append('L')
                stop()
            S1 = sensor1()
            S2 = sensor2()
            S3 = sensor3()
            if ((S1 == 1) and (S3 == 1) and (S2 == 0)):
                test.append(5)
                if anomtype[n][i+1] == 5:
                    score += 1
                    
            elif (S3 == 1) and (S1 == 0):
                test.append(6)
                if anomtype[n][i+1] == 6:
                    score += 1
            elif (S1 == 1) and (S3 == 0):
                test.append(4)
                if anomtype[n][i+1] == 4:
                    score += 1
            else :
                error += 1
        print('running completed')
       #     if (S1 == S2 == S3):
        #        print("all sensors are in same \n checking for obstacle condition")
         #       stop()
          #      flag = 0
           #     ULTRA()
            #    if min(distance) < 20 :
             #       stop()
              #      print("obsacle found....\n  at distance = ",distance[-1])            
               #     test.append(2)
                #    score += 10
    
       #         elif min(distance) > 20 :
        #            test.append(-1)
         #           error += 1
          #          print('agent failed \n returning to home')
           #         c = test[-1]
            #        if c == '5':frqsp = [30,20,10,0.01*duration]
             #       elif c == '4':frqsp = [20,30,10,0.01*duration]
              #      else:frqsp = [30,30,10,0.01*duration]
               #     recovery(frqsp)



    else :
        print("Invalid input")
        print("error ! \n Do you want to try again ?")
        u = input()
        while u == 'y' :
            try:
                main()
            except:
                print("error ! \n Do you want to try again ?")
                u = input()

    
    S1 = sensor1()
    S2 = sensor2()
    S3 = sensor3()
    #while (S1 + S2 + S3 ) != 0 :
        #print("Allignment Error")
        #S1 = sensor1()
        #S2 = sensor2()
        #S3 = sensor3()
    n = 1
    print(distance)
    if distance[-1] > 18:
        train[1] = distance
        train[0] = n
        train[2] = 1
        train[3] = 0#0.05+(0.01*len(score))-(0.001*len(error))
        TRAIN(train)
        final = pd.DataFrame(insttype)
                
        print('training completed \n do you want to train again? (y/n')
        user = input()
        if user == 'n':
            final.to_csv('/home/pi/Desktop/routes/'+name+'.csv', index=False)
            exit(main)
        while user == 'y':
            distance.clear()
            ULTRA()
            S1 = sensor1()
            S2 = sensor2()
            S3 = sensor3()
            n = n+1
            #while (S1 + S2 + S3) != 0:
             #   print("Allignment Error")
              #  S1 = sensor1()
               # S2 = sensor2()
                #S3 = sensor3()
            
            if distance[-1]>18 :
                train[1] = [30]
                train[0] = n
                train[2] = 1
                train[3] = 0#0.05+(0.01*len(score))-(0.001*len(error))
                TRAIN(train)
                
                
                file2 = pd.DataFrame(insttype)
                insttype = [0]
                final = pd.concat([final,file2],axis=1)
                print('training completed\n do you want to train again? (y/n')
                user = input()
        
        final.to_csv('/home/pi/Desktop/routes/'+name+'.csv', index=False)
    else:
        distance.clear()
        print("error",distance,check)
    

u = 'y'
while u == 'y' :
    try:
        main()
    except:
        print("error ! \n Do you want to try again ?")
        u = input()



