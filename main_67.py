import keyboard
import math as m
import time
from simple_pid import PID
import json
import pygame



pidTurn = PID(0.022, 0.0, 0.004, setpoint=0)
pidTurn.output_limits = (-1.0, 1.0)
pidTurn.sample_time = .01
pidX = PID(1, 1, 1, setpoint=0)
pidX.output_limits = (-1.0, 1.0)
pidY = PID(1, 1, 1, setpoint=0)
pidY.output_limits = (-1.0, 1.0)

'''
def TurnTo(BRot, BRotV, TRot):
    VFactor=10.1
    VAdd = 1
    if(abs(BRot-TRot) > 15):
        TFactor = 1
    elif(abs(BRot-TRot) >7):
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
'''
'''
def TurnTo(BRot, BRotV, TRot):
    VFactor = 20
    VAdd = 0
    if(BRot - TRot > 0):
        if(abs(BRot-TRot) > BRotV*VFactor*-1+VAdd and abs(BRot-TRot) > 5):
            return -1
        else:
            return 0
    else:
        if(abs(BRot-TRot) > BRotV*VFactor+VAdd and abs(BRot-TRot) > 5):
            return 1
        else:
            return 0
'''
def TurnTo(BRot, BRotV, TRot):
    pidTurn.setpoint = TRot
    return pidTurn(BRot)

def turn(StartX, StartY, Angle1):
    Hypot = m.hypot(StartX, StartY)
    Angle2 = m.degrees(m.atan2(StartX, StartY))
    AngleR = m.radians(Angle1 - Angle2)
    EndY = m.sin(AngleR) * Hypot
    #print(m.degrees(AngleR))
    EndX = m.cos(AngleR) * Hypot
    #print(EndY)
    Tup = [EndX, EndY]
    #print(Tup)
    return Tup

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
TRot = 0.0
Precision = 0

loop_time = time.time()

pygame.init()

joysticks = []

# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print ("Detected joystick "),joysticks[-1].get_name(),"'"

while(True):
    start = time.time()

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
    GVol = Robot['myrobot'][0]['velocity']
    GRot = Robot['myrobot'][0]['global rot']
    GRotV = Robot['myrobot'][0]['rot velocity']
    HAngle = Robot['myrobot'][10]['local rot']
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
        Dis = m.hypot(GPos[0]-BallsR[i][0], GPos[2]-BallsR[i][2])
        BallRot = m.degrees(m.atan2(GPos[0]-BallsR[BallNumberL][0], GPos[2]-BallsR[BallNumberL][2]))
        if(Dis < CloseL and BallsR[i][1] < .15 and BallRot < GRot[1] or BallRot > (GRot[1]+180)%360):
            CloseL = Dis
            BallNumL = i
        if(Dis < CloseR and BallsR[i][1] < .15 and BallRot > GRot[1] or BallRot < (GRot[1]+180)%360):
            CloseR = Dis
            BallNumR = i
    RadianBallValL = m.atan2(GPos[0]-BallsR[BallNumL][0], GPos[2]-BallsR[BallNumL][2])
    BRotL = m.degrees(RadianBallValL)
    BRotL -= 180
    if BRotL < 0:
        BRotL+=360
    RadianBallValR = m.atan2(GPos[0]-BallsR[BallNumR][0], GPos[2]-BallsR[BallNumR][2])
    BRotR = m.degrees(RadianBallValR)
    BRotR -= 180
    if BRotR < 0:
        BRotR+=360
    #print(BallsR[BallNumL])

    CloseB = 100
    BallNumB = 0
    for i in range(len(BallsB)):
        BallNumberB = i
        Dis = m.hypot(GPos[0]-BallsB[i][0], GPos[2]-BallsB[i][2])
        if(Dis < CloseB):
            CloseB = Dis
            BallNumB = i
    #print(CloseB)
    
    #Gets good rotation to hub
    RadianBotVal = m.atan2(GPos[0], GPos[2])
    HRot = m.degrees(RadianBotVal)
    HRot+=90
    if HRot < 0:
        HRot+=360
    
    #Finds robot velocity and angle
    Vol = m.hypot(GVol[0], GVol[2])
    Angle = m.degrees(m.atan2(GVol[0], GVol[2])) + 90
    if Angle < 0:
        Angle += 360
    
    BRot = GRot[1]
    BRot += 90
    if BRot < 0:
        BRot += 360
    Diff = HRot - Angle
    if Diff < 0:
        Diff += 360
    Dif = m.radians(Diff)
    YVol = m.cos(Dif)*Vol
    XVol = m.sin(Dif)*Vol

    

    #Gets distance from hub
    Dist = m.hypot(GPos[0],GPos[2])
    Dist = round(Dist, 1)
    Dist += YVol * 1.25
    
    #Makes hood angle usable
    HAngle = HAngle[0]
    if(HAngle >=270):
        HAngle = (HAngle-450)*-1
    elif(HAngle <= 90):
        HAngle = (HAngle-90)*-1

    Turn = 0
    XMov = 0
    YMov = 0

    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 3:
                ButY = True
            if event.button == 2:
                ButX = True
            if event.button == 1:
                ButB = True
            if event.button == 0:
                ButA = True
            if event.button == 4:
                BL = True
            if event.button == 5:
                BR = True
            if event.button == 6:
                ButR = True
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 3:
                ButY = False
            if event.button == 2:
                ButX = False
            if event.button == 1:
                ButB = False
            if event.button == 0:
                ButA = False
            if event.button == 4:
                BL = False
            if event.button == 5:
                BR = False
            if event.button == 6:
                ButR = False
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                XMov = event.value
                if(abs(event.value) < 0.1):
                    XMov = 0
            if event.axis == 1:
                YMov = event.value
                if(abs(event.value) < 0.1):
                    YMov = 0
            if event.axis == 2:
                Turn = event.value * .7
                if(abs(event.value) < 0.1):
                    Turn = 0
            if event.axis == 4:
                if(event.value > 0.2):
                    TrigL = True
                else:
                    TrigL = False
            if event.axis == 5:
                if(event.value > 0.2):
                    TRigR = True
                else:
                    TRigR = False

    #Sets inputs based on keyboard
    if YMov == 0:
        if(keyboard.is_pressed('w')):
            YMov = -1
        elif(keyboard.is_pressed('s')):
            YMov = 1
        else:
            YMov = 0

    if XMov == 0:
        if(keyboard.is_pressed('a')):
            XMov = -1
        elif(keyboard.is_pressed('d')):
            XMov = 1
        else:
            XMov = 0

    if Turn == 0:
        if(keyboard.is_pressed('j')):
            Turn = -.7
        elif(keyboard.is_pressed('l')):
            Turn = .7
        else:
            Turn = 0

    if(keyboard.is_pressed(',') or ButY):
        RevIn = 1
    else:
        RevIn = 0

    if(keyboard.is_pressed('.') or ButB):
        InR = 1
        if(InRPos == 0):
            InRPos = 1
        else:
            InRPos = 0
    else:
        InR = 0

    if(keyboard.is_pressed('n')) or ButX:
        InL = 1
        if(InLPos == 0):
            InLPos = 1
        else:
            InLPos = 0
    else:
        InL = 0

    if(keyboard.is_pressed('k') or BR):
        Shoot = 1
        '''
        if Dist <= 4.3:
            Shoot = 1
        else:
            GoToHub = 1
            Shoot = 0
        '''
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

    if(keyboard.is_pressed(']') or ButR):
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

    
            
            

    RRot = GRot[1]
    CRot = 0

    if(keyboard.is_pressed('shift') or BL):
        if Dist < 4:
            YMov = YMov * .4
        elif Dist < 6:
            YMov = YMov * .6
        else:
            YMov = YMov * .8
        if Dist > 3.5 and abs(YMov) < .1:
            YMov -= .5
        Turn = Turn * .3
        XMov = XMov * .5
        XDis = XVol * 1.25
        CRot = XDis/Dist
        if CRot > 1 or CRot < -1:
            CRot = .9   
        CRot = m.asin(CRot)
        CRot = m.degrees(CRot)
        TRot = HRot-CRot
        CRot = 1
        if 1.2 < Dist < 4.4 and abs(TRot - RRot) < 5:
            Shoot = 1
        if XMov != 0 or YMov != 0:
            Movs = turn(XMov, YMov, HRot - RRot + 90)
            #print(HRot)
            XMov = Movs[0]
            YMov = Movs[1]
    # and abs(TRot - RRot) > 5
    print(Dist)

    if(keyboard.is_pressed(';' or ButA)):
        TRot = HRot
        CRot = 1
    
    TRot = TRot % 360

    if(TRot < 90):
        TRot += 360
        if RRot < 230:
            RRot += 360
        
    if(TRot > 270):
        if(RRot < 135):
            RRot += 360
    
    Fender = 0
    if(CRot == 1):
        if CloseB < 0.14 or BallsB[BallNumB][1] > .27 and BallsB[BallNumB][1] < 1.5:
            Fender = 1
        else:
            Fender = 0
        Turn = TurnTo(RRot, GRotV[1], TRot + 2)

    #sets hood angle automatically
    HIndex = int((Dist-1.3)*10)
    if HIndex < 0:
        HIndex = 0
    elif HIndex > 30:
        HIndex = 30
    if Fender == 1:
        TAngle = 180
    else:
        TAngle = HAngles[HIndex]
    Precision = abs(HAngle - TAngle) * .06
    BumperL = 1
    if Precision > 4:
        Precision = 4
    
    if HAngle > TAngle:
        HoodU = 0
        HoodD = 1
    elif HAngle < TAngle:
        HoodU = 1
        HoodD = 0

    #print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time=time.time()
    #print(abs(TRot - RRot))

    #Writes to the controls text document
    Controls.write('a=' + str(RevIn) + '\nb=' + str(InR) + '\nx=' + str(InL) + '\ny=' + str(Shoot) + '\ndpad_left=' + str(ClimbD) + '\ndpad_right=' + str(ClimbU) + 
    '\ndpad_up=' + str(HoodU) + '\ndpad_down=' + str(HoodD) + '\nbumper_l=' + str(BumperL) + '\nbumper_r=' + str(BumperR) + '\nstop=' + str(Stop) + '\nrestart=' + str(Restart) + 
    '\nright_y='+str(RightY) + '\nright_x=' + str(Turn) + '\nleft_y=' + str(YMov) + '\nleft_x=' + str(XMov) + '\ntrigger_l=' + str(ClimbBack) + '\ntrigger_r=' + str(ClimbForward)
     + '\nprecision=' + str(Precision))

    Rbot.close()
    Gme.close()

    if keyboard.is_pressed('esc'):
        break

    #Keeps fps at 60
    time.sleep(max(1./60 - (time.time() - start), 0))
 
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