import keyboard
import math
import time
from simple_pid import PID
import numpy as np
import json
import os
from time import time
'''
pidTurn = PID(0.008, 0.001, 0.0006, setpoint=180)
pidTurn.output_limits = (-1.0, 1.0)
pidX = PID(1, 1, 1, setpoint=0)
pidX.output_limits = (-1.0, 1.0)
pidY = PID(1, 1, 1, setpoint=0)
pidY.output_limits = (-1.0, 1.0)
'''

def TurnTo(BRot, BRotV, TRot):
    VFactor=10
    VAdd = 5
    if(abs(BRot-TRot) > 20):
        TFactor = 1
    elif(abs(BRot-TRot) >10):
        TFactor = .6
    elif(abs(BRot-TRot) >5):
        TFactor = .3
    elif(abs(BRot-TRot) >2):
        TFactor = .1
    else:
        TFactor = 0
    if(BRot-TRot > 0):
        if(abs(BRot-TRot)>BRotV*VFactor*-1+VAdd):
            return -1*TFactor
        elif(abs(BRot-TRot)<BRotV*VFactor*-1+VAdd):
            return 1*TFactor
    else:
        if(abs(BRot-TRot)>BRotV*VFactor+VAdd):
            return 1*TFactor
        elif(abs(BRot-TRot)<BRotV*VFactor+VAdd):
            return -1*TFactor
   

HAngles = [180, 170, 162, 155, 147, 140, 132, 126, 120, 115, 110, 105, 100, 95, 90, 85, 80, 75, 70, 66, 62, 58, 54, 50, 47, 44, 41, 38, 36, 34, 32]

#Set up controller input values
#Everthing above RightY is binary, 0 and 1, corresponding to a button
#Everything below and including RightY is a fload between -1 and 1
RevIn = 0
InR = 0
InRPos = 0
InL = 0
InLPos = 0
Shoot = 0
ClimbD = 0
ClimbU = 0
HoodU = 0
HoodD = 0
BumperL = 0
BumperR = 0
Stop = 0
Restart = 0
RightY = 0
Turn = 0
YMov = 0
XMov = 0
ClimbBack = 0
ClimbForward = 0

loop_time = time()

while(True):

    #Opens text documents
    
    Rbot = open('myRobot.txt', 'rt')
    Gme = open('GameElements.txt', 'rt')
    try:
        Robot = json.load(Rbot)
        Game = json.load(Gme)
    except:
        continue

    Controls = open('Controls.txt', 'w')

    #grabs positions
    GPos = Robot['myrobot'][0]['global pos']
    GRot = Robot['myrobot'][0]['global rot']
    GRotV = Robot['myrobot'][0]['rot velocity']
    HPos = [0.0 ,0.0 ,0.0]
    HAngle = Robot['myrobot'][10]['global rot']
    BallsR = []
    BallsR.append(Game['objects'][9]['global pos'])
    BallsR.append(Game['objects'][10]['global pos'])
    BallsR.append(Game['objects'][11]['global pos'])
    BallsR.append(Game['objects'][12]['global pos'])
    BallsR.append(Game['objects'][13]['global pos'])
    BallsR.append(Game['objects'][14]['global pos'])
    BallsR.append(Game['objects'][15]['global pos'])
    BallsR.append(Game['objects'][16]['global pos'])
    BallsR.append(Game['objects'][25]['global pos'])
    BallsR.append(Game['objects'][26]['global pos'])
    BallsR.append(Game['objects'][27]['global pos'])
    BallsB = []
    BallsB.append(Game['objects'][1]['global pos'])
    BallsB.append(Game['objects'][2]['global pos'])
    BallsB.append(Game['objects'][3]['global pos'])
    BallsB.append(Game['objects'][4]['global pos'])
    BallsB.append(Game['objects'][5]['global pos'])
    BallsB.append(Game['objects'][6]['global pos'])
    BallsB.append(Game['objects'][7]['global pos'])
    BallsB.append(Game['objects'][8]['global pos'])
    BallsB.append(Game['objects'][17]['global pos'])
    BallsB.append(Game['objects'][18]['global pos'])
    BallsB.append(Game['objects'][19]['global pos'])

    #Finds closest ball
    CloseL = 100
    CloseR = 100
    BallNumL = 0
    BallNumR = 0
    for i in range(len(BallsR)):
        BallNumberL = i
        BallNumberR = i
        Dis = math.hypot(GPos[0]-BallsR[i][0], GPos[2]-BallsR[i][2])
        BallRot = math.degrees(math.atan2(GPos[0]-BallsR[BallNumberL][0], GPos[2]-BallsR[BallNumberL][2]))
        if(Dis < CloseL and BallsR[i][1] < .15 and BallRot < GRot[1] or BallRot > (GRot[1]+180)%360):
            CloseL = Dis
            BallNumL = i
        if(Dis < CloseR and BallsR[i][1] < .15 and BallRot > GRot[1] or BallRot < (GRot[1]+180)%360):
            CloseR = Dis
            BallNumR = i
    RadianBallValL = math.atan2(GPos[0]-BallsR[BallNumL][0], GPos[2]-BallsR[BallNumL][2])
    BRotL = math.degrees(RadianBallValL)
    BRotL -= 180
    if BRotL < 0:
        BRotL+=360
    RadianBallValR = math.atan2(GPos[0]-BallsR[BallNumR][0], GPos[2]-BallsR[BallNumR][2])
    BRotR = math.degrees(RadianBallValR)
    BRotR -= 180
    if BRotR < 0:
        BRotR+=360
    #print(BallsR[BallNumL])

    CloseB = 100
    BallNumB = 0
    for i in range(len(BallsB)):
        BallNumberB = i
        Dis = math.hypot(GPos[0]-BallsB[i][0], GPos[2]-BallsB[i][2])
        if(Dis < CloseB):
            CloseB = Dis
            BallNumB = i
    #print(CloseB)

    #Gets good rotation to hub
    RadianBotVal = math.atan2(GPos[0], GPos[2])
    HRot = math.degrees(RadianBotVal)
    HRot+=90
    if HRot < 0:
        HRot+=360
    

    #Gets distance from hub
    Dist = math.hypot(GPos[0],GPos[2])
    Dist = round(Dist, 1)
    HIndex = int((Dist-1.3)*10)
    
    #Makes hood angle usable
    HAngle = HAngle[0]
    if(HAngle >=270):
        HAngle = (HAngle-450)*-1
    elif(HAngle <= 90):
        HAngle = (HAngle-90)*-1

    #Sets inputs based on keyboard
    if(keyboard.is_pressed('w')):
        YMov = -1
    elif(keyboard.is_pressed('s')):
        YMov = 1
    else:
        YMov = 0

    if(keyboard.is_pressed('a')):
        XMov = -1
    elif(keyboard.is_pressed('d')):
        XMov = 1
    else:
        XMov = 0

    if(keyboard.is_pressed('j')):
        Turn = -1
    elif(keyboard.is_pressed('l')):
        Turn = 1
    else:
        Turn = 0

    if(keyboard.is_pressed(',')):
        RevIn = 1
    else:
        RevIn = 0

    if(keyboard.is_pressed('.')):
        InR = 1
        if(InRPos == 0):
            InRPos = 1
        else:
            InRPos = 0
    else:
        InR = 0

    if(keyboard.is_pressed('n')):
        InL = 1
        if(InLPos == 0):
            InLPos = 1
        else:
            InLPos = 0
    else:
        InL = 0

    if(keyboard.is_pressed('k')):
        if Dist <= 4.3:
            Shoot = 1
        else:
            GoToHub = 1
            Shoot = 0
    else:
        Shoot = 0

    if(keyboard.is_pressed('z')):
        ClimbD = 1
    else:
        ClimbD = 0

    if(keyboard.is_pressed('q')):
        ClimbU = 1
    else:
        ClimbU = 0

    if(keyboard.is_pressed('e')):
        HoodD = 1
    else:
        HoodD = 0

    if(keyboard.is_pressed('r')):
        HoodU = 1
    else:
        HoodU = 0

    if(keyboard.is_pressed(']')):
        Restart = 1
        InL = 1
        InR = 1
    else:
        Restart = 0

    if(keyboard.is_pressed('f')):
        ClimbBack = 1
    else:
        ClimbBack = 0

    if(keyboard.is_pressed('h')):
        ClimbForward = 1
    else:
        ClimbForward = 0

    
    #sets hood angle automatically
    if(Dist <= 4.3):
        if abs(HAngle - HAngles[HIndex]) < 30:
            BumperL = 1
        else:
            BumperL = 0
        
        if HAngle > HAngles[HIndex]:
            HoodU = 0
            HoodD = 1
        elif HAngle < HAngles[HIndex]:
            HoodU = 1
            HoodD = 0
    else:
        if abs(HAngle - 32) < 30:
            BumperL = 1
        else:
            BumperL = 0
        if HAngle > 32:
            HoodU = 0
            HoodD = 1
        elif HAngle < 32:
            HoodU = 1
            HoodD = 0
    
    CRot = 0
    RRot = GRot[1]
    TRot = RRot
    if(keyboard.is_pressed(';')):
        TRot = HRot
        CRot = 1
    elif(keyboard.is_pressed('/')):
        TRot = BRotL
        CRot = 1
    elif(keyboard.is_pressed('p')):
        TRot = BRotR
        CRot = 1
    
    if(HRot < 90):
        TRot += 360
        if RRot < 230:
            RRot += 360
        
    if(HRot > 270):
        if(TRot < 135):
            TRot += 360
    
    if(CRot == 1):
        if CloseB < 0.14 or BallsB[BallNumB][1] > .27 and BallsB[BallNumB][1] < 1.5:
            TRot += 30
        Turn = TurnTo(RRot, GRotV[1], TRot)

    #if GoToHub == 1:
    #    pass

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time=time()
    
    #print(RRot-TRot, GRotV[1]*10)

    #Writes to the controls text document
    Controls.write('a=' + str(RevIn) + '\nb=' + str(InR) + '\nx=' + str(InL) + '\ny=' + str(Shoot) + '\ndpad_left=' + str(ClimbD) + '\ndpad_right=' + str(ClimbU) + 
    '\ndpad_up=' + str(HoodU) + '\ndpad_down=' + str(HoodD) + '\nbumper_l=' + str(BumperL) + '\nbumper_r=' + str(BumperR) + '\nstop=' + str(Stop) + '\nrestart=' + str(Restart) + 
    '\nright_y='+str(RightY) + '\nright_x=' + str(Turn) + '\nleft_y=' + str(YMov) + '\nleft_x=' + str(XMov) + '\ntrigger_l=' + str(ClimbBack) + '\ntrigger_r=' + str(ClimbForward))

    Rbot.close()
    Gme.close()
 
#cheat sheet
'''
a=0
b=0
x=0
y=0
dpad_left=0
dpad_right=0
bumper_l=0
bumper_r=0
stop=0
restart=0
right_y=0
right_x=0
left_y=0
left_x=0
trigger_l=0
trigger_r=0
'''