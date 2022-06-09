import keyboard
import math as m
import json
import time

RevIn = 0
TurF = 0
In = 0
Shoot = 0
ClimbD = 0
ClimbU = 0
ClimbB = 0
ClimbF = 0
HoodU = 0
HoodD = 0
SlowTurn = 0
Restart = 0
Turn = 0
YMov = 0
Precision = 4

Key = True
TRotL = 0
AutoShoot = 0

while True:
    start = time.time()
    Rbot = open('myRobot.txt', 'rt')
    Gme = open('GameElements.txt', 'rt')
    try:
        Robot = json.load(Rbot)
        Game = json.load(Gme)
    except:
        continue

    Controls = open('Controls.txt', 'w')

    #grabs positions
    RPos = Robot['myrobot'][0]['global pos']
    RVol = Robot['myrobot'][0]['velocity']
    RAngle = Robot['myrobot'][0]['global rot']
    RRotV = Robot['myrobot'][0]['rot velocity']
    Climb1Pos = Robot['myrobot'][4]['local pos'][1]
    Climb2Rot = Robot['myrobot'][5]['local rot'][2]
    HAngle = Robot['myrobot'][7]['local rot']
    TRot = Robot['myrobot'][6]['local rot'][1]

    #Gets distance from hub and velocity
    Dist = m.hypot(RPos[0],RPos[2])
    Vol = m.hypot(RVol[0], RVol[2])
    HRot = m.degrees(m.atan2(RPos[0], RPos[2])) + 90
    if HRot < 0:
        HRot+=360
    Angle = m.degrees(m.atan2(RVol[0], RVol[2])) + 90
    if Angle < 0:
        Angle += 360
    
    BRot = RAngle[1]
    BRot += 90
    if BRot < 0:
        BRot += 360
    Diff = HRot - Angle
    if Diff < 0:
        Diff += 360
    Dif = m.radians(Diff)
    YVol = m.cos(Dif)*Vol
    XVol = m.sin(Dif)*Vol

    #Makes hood angle usable and finds the best angle of the hood
    HAngle = HAngle[0]
    if(HAngle >=270):
        HAngle = (HAngle-450)*-1
    elif(HAngle <= 90):
        HAngle = (HAngle-90)*-1
    Dist += YVol * 1.25
    TAngle = -43*Dist+215

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

    #Finds closest blue ball
    CloseB = 100
    BallNumB = 0
    for i in range(len(BallsB)):
        BallNumberB = i
        Dis = m.hypot(RPos[0]-BallsB[i][0], RPos[2]-BallsB[i][2])
        if(Dis < CloseB):
            CloseB = Dis
            BallNumB = i

    if Key == True:

        #Sets inputs based on keyboard
        if(keyboard.is_pressed('w')):
            YMov = -1
        elif(keyboard.is_pressed('s')):
            YMov = 1
        else:
            YMov = 0

        if(keyboard.is_pressed('j')):
            Turn = -1
        elif(keyboard.is_pressed('l')):
            Turn = 1
        else:
            Turn = 0
        
        if(keyboard.is_pressed('k')):
            In = 1
        else:
            In = 0

        if(keyboard.is_pressed(',')):
            RevIn = 1
        else:
            RevIn = 0

        if(keyboard.is_pressed('i')):
            Shoot = 1
        else:
            Shoot = 0

        if(keyboard.is_pressed('c')):
            HoodU = 1
        else:
            HoodU = 0

        if(keyboard.is_pressed('v')):
            HoodD = 1
        else:
            HoodD = 0

        if(keyboard.is_pressed('shift')):
            SlowTurn = 1
        else:
            SlowTurn = 0
        
        if(keyboard.is_pressed('q')):
            ClimbU = 1
        else:
            ClimbU = 0
        
        if(keyboard.is_pressed('z')):
            ClimbD = 1
        else:
            ClimbD = 0

        if(keyboard.is_pressed('e')):
            ClimbB = 1
        else:
            ClimbB = 0
        
        if(keyboard.is_pressed('r')):
            ClimbF = 1
        else:
            ClimbF = 0

        if(keyboard.is_pressed(']')):
            Restart = 1
            In = 1
        else:
            Restart = 0
    
    if(keyboard.is_pressed('shift')):
        YMov = YMov * .8
        Turn = Turn * .3
        if 1.2 < Dist < 5:
            Shoot = 1
        if abs(XVol) > .5:
            if YVol > 0:
                if XVol > 0:
                    Turn = .2
                else:
                    Turn = -.2
            else:
                if  XVol < 0:
                    Turn = .2
                else:
                    Turn = -.2

    #Automatically shoots out blue balls
    if BallsB[BallNumB][1] > .3 and CloseB < .2 and BallsB[BallNumB][1] < 1:
        TurF = 1
        Shoot = 1
    else:
        TurF = 0

    #Sets hood angle automatically
    Precision = abs(HAngle - TAngle) * .06
    SlowTurn = 1
    if Precision > 4:
        Precision = 4
    
    if HAngle > TAngle:
        HoodU = 0
        HoodD = 1
    elif HAngle < TAngle:
        HoodU = 1
        HoodD = 0
    
    #Automatically shoots when standing still
    if AutoShoot == 1:
        TVol = TRot - TRotL
        if YMov == 0 and Turn == 0 and Dist < 5 and Vol < .5 and abs(TVol) < .5 and abs(RRotV[1]) < .5:
            Shoot = 1

    TRotL = TRot

    #Auto Climb
    if(keyboard.is_pressed('f')):
        if RPos[1] < .1:
            Precision = 4
            SlowTurn = 1
            if RPos[2] < -6:
                ClimbU = 0
                ClimbD = 1
            else:
                ClimbD = 0
                ClimbU = 1
            TClimb = 300
            if  Climb2Rot < TClimb:
                ClimbF = 1
                ClimbB = 0
            else:
                ClimbF = 0
                ClimbB = 1 
        elif abs(270-RAngle[1] > 2):
            ClimbD = 1
            ClimbU = 0
            ClimbB = 0
            ClimbF = 0
            SlowTurn = 0
        elif .6 > RPos[1] > .1:
            if Climb1Pos < .12 and RRotV[0] < 0:
                TClimb = 0.6
            else:
                TClimb = 0.06
            Precision = 2
            SlowTurn = 1
            
            if Climb1Pos < TClimb:
                ClimbD = 1
                ClimbU = 0
            else:
                ClimbD = 0
                ClimbU = 1
            TClimb = 210
            if  Climb2Rot < TClimb:
                ClimbF = 1
                ClimbB = 0
            else:
                ClimbF = 0
                ClimbB = 1

    #Writes to the controls text file
    Controls.write('left_y=' + str(YMov) + '\nright_x=' + str(Turn) + '\na=' + str(RevIn) + '\nb=' + str(TurF) + '\nx=' + str(In) + '\ny=' + str(Shoot) + '\ndpad_left=' + str(ClimbU)
     + '\ndpad_right=' + str(ClimbD) + '\ntrigger_l=' + str(ClimbB) + '\ntrigger_r=' + str(ClimbF) + '\ndpad_up=' + str(HoodU) + '\ndpad_down=' + str(HoodD) + '\nbumper_l=' + str(SlowTurn)
     + '\nrestart=' + str(Restart) + '\nprecision=' + str(Precision))

    #Prints for debugging
    print(XVol)

    if keyboard.is_pressed('`'):
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