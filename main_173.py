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

Key = True
TRotL = 0

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
    HAngle = Robot['myrobot'][7]['global rot']
    TRot = Robot['myrobot'][6]['global rot'][1]

    #Gets distance from hub and velocity
    Dist = m.hypot(RPos[0],RPos[2])
    Vol = m.hypot(RVol[0], RVol[2])
    HRot = m.degrees(m.atan2(RPos[0], RPos[2]))

    #Makes hood angle usable and finds the best angle of the hood
    HAngle = HAngle[0]
    if(HAngle >=270):
        HAngle = (HAngle-450)*-1
    elif(HAngle <= 90):
        HAngle = (HAngle-90)*-1

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

        if(keyboard.is_pressed('x')):
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
    
    #Automatically shoots out blue balls
    if BallsB[BallNumB][1] > .3 and CloseB < .2 and BallsB[BallNumB][1] < 1:
        TurF = 1
    else:
        TurF = 0

    #Sets hood angle automatically
    if abs(HAngle - TAngle) < 10:
        SlowTurn = 1
    else:
        SlowTurn = 0

    if abs(HAngle - TAngle) < 3:
        HoodU = 0
        HoodD = 0
    elif HAngle > TAngle:
        HoodU = 0
        HoodD = 1
    elif HAngle < TAngle:
        HoodU = 1
        HoodD = 0
    
    #Automatically shoots when standing still
    TVol = TRot - TRotL
    if YMov == 0 and Turn == 0 and Dist < 5 and Vol < 1 and abs(TVol) < .5:
        Shoot = 1

    TRotL = TRot

    #Writes to the controls text file
    Controls.write('left_y=' + str(YMov) + '\nright_x=' + str(Turn) + '\na=' + str(RevIn) + '\nb=' + str(TurF) + '\nx=' + str(In) + '\ny=' + str(Shoot) + '\ndpad_left=' + str(ClimbU)
     + '\ndpad_right=' + str(ClimbD) + '\ntrigger_l=' + str(ClimbB) + '\ntrigger_r=' + str(ClimbF) + '\ndpad_up=' + str(HoodU) + '\ndpad_down=' + str(HoodD) + '\nbumper_l=' + str(SlowTurn)
     + '\nrestart=' + str(Restart))

    #Prints for debugging
    print(round(TVol, 2))

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