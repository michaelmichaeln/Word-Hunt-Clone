
#Word Hunt

from cmu_graphics import *
import random,os, pathlib, pickle, copy
from PIL import Image
from profiles import Profile, saveProfiles
import Board as board


def setNewProfile(app):
    if app.nameInput not in app.existingProfiles:
        app.profile = Profile(app.nameInput)
        app.existingProfiles[app.profile.name] = Profile(app.nameInput)
        saveProfiles(app.existingProfiles)
    else:
        app.profile = app.existingProfiles[app.nameInput]
    app.nameInput = ''


#Draws Background patterns
def drawBackground(app):
    if app.backgroundType == 1:
        drawRect(0,0, app.width, app.height, fill='green')
        for i in range (40, app.height, 80):
            drawLine(0,i,app.width,i, fill =app.backgroundColor, lineWidth =40)

def startGame(app):
    app.board,app.remainingWords = board.makeLegalBoard(app.board,app.legalWords)
    app.selected = []
    app.foundWords = set()
    app.currentScore = 0
    app.timer = 80
    app.guess = []
    #Hint feature variables
    app.hintTimer = 10
    app.hintsRemaining = 3
    app.showHint =False

    setActiveScreen('game')


#-------------------------------------------------------------------------------
def onAppStart(app):
    
    app.profile = None
    app.nameInput = ''

    app.hintTimer = 6
    app.flashing = True
    app.changePressed = False
    app.foundWords = set()
    app.currentScore = 0
    app.stepsPerSecond=1
    app.hovering=None
    app.width = 800
    app.height = 800
    app.board = board.generateBoard()
    app.backgroundType = 1
    app.backgroundColor = 'lightGreen'
    app.scoresDict={3:100,4:400,5:800,6:1400,7:1800,8:2200,9:2600,10:3000}
    
    #BoardValues
    app.boardTop = app.height*9//40
    app.boardLeft = app.width//8
    app.boardSize = app.width - (2*app.boardLeft)
    app.boardRight = app.boardLeft + app.boardSize
    app.boardBottom= app.boardTop + app.boardSize
    app.squareSize = app.boardSize//4

    #Sprites
    app.homeScreen = CMUImage(Image.open("images/homeScreen2.png"))
    app.instructions = CMUImage(Image.open("images/instructions.png"))
    app.startButton = CMUImage(Image.open("images/startButton.png"))
    app.backButton = CMUImage(Image.open("images/backButton.png"))
    app.retryButton = CMUImage(Image.open("images/retryButton.png"))
    app.changeButton = CMUImage(Image.open("images/changeButton.png"))
    app.saveButton = CMUImage(Image.open("images/saveButton.png"))


    #load words dictionary: https://github.com/dwyl/english-words/blob/master/README.md

    with open('filtered_words_alpha.txt', 'r') as file:
        app.legalWords = set(file.read().split())

    #Loads existing profiles: 

    #with open('Profiles_database', 'wb') as file:
    #        pickle.dump(dict(), file)

    with open('Profiles_database', 'rb') as file:
        app.existingProfiles = pickle.load(file)




#START----------------------------------------------------------------------------------

def start_redrawAll(app):
    if app.nameInput != '':
        drawLabel(f'NAME:{app.nameInput}',app.width//2, app.height*7/16, 
                  size = 60, bold = True, align= 'center')

        drawLabel("PRESS ENTER TO SAVE", app.width//2, app.height *17/32,
                   align = 'center', size=30)
        if len(app.nameInput) == 12:
            drawLabel('Character Limit Reached (12)', app.width//2,
                      app.height*18/32, align = 'center',
                      size = 15, fill ='red')

    else:
        drawLabel("ENTER YOUR NAME",app.width//2, app.height//2,
                  size=60, align='center', bold=True )
        
        
def start_onKeyPress(app, key):
    #Build profile name
    if key == 'backspace' and app.nameInput != '':
        app.nameInput = app.nameInput[:-1]

    elif key.isalpha() and len(key) == 1 and len(app.nameInput)<12: 
        app.nameInput += key.upper()

    #Create new profile if name not used
    elif key == 'enter' and app.nameInput !='':
        setNewProfile(app)
        setActiveScreen('home')



#home SCREEN-----------------------------------------------------------------------------

def home_redrawAll(app):
    drawBackground(app)
    buttonXCenter,buttonWidth = 395,227
    buttonYCenter1,buttonYCenter2,buttonYCenter3,buttonHeight =387,514,637,87

    drawImage(app.homeScreen,0,0, width =app.width, height = app.height)
    drawRect(buttonXCenter,buttonYCenter1, buttonWidth,buttonHeight,
              align='center', fill=None, border='pink')
    drawRect(buttonXCenter,buttonYCenter2, buttonWidth,buttonHeight,
              align='center', fill=None, border='pink')
    drawRect(buttonXCenter,buttonYCenter3, buttonWidth,buttonHeight,
              align='center', fill=None, border='pink')
    #Highlights the button being hovered over
    if app.hovering == 'homeStart':
        drawRect(buttonXCenter,buttonYCenter1, buttonWidth,buttonHeight,
                  align='center', fill='red', opacity=20)
    elif app.hovering == 'homeScores':
        drawRect(buttonXCenter,buttonYCenter2, buttonWidth,buttonHeight,
                  align='center', fill='red', opacity=20)
    elif app.hovering == 'homeOptions':
        drawRect(buttonXCenter,buttonYCenter3, buttonWidth,buttonHeight,
                  align='center', fill='red', opacity=20)

def home_onMousePress(app, mouseX, mouseY):
    buttonXCenter,buttonWidth = 395,227
    buttonYCenter1,buttonYCenter2,buttonYCenter3,buttonHeight =387,514,637,87

    if (buttonXCenter-(buttonWidth//2))<= mouseX <=(buttonXCenter+(buttonWidth//2)):
        if (buttonYCenter1-(buttonHeight//2))<=mouseY<=(buttonYCenter1+(buttonHeight//2)):

            setActiveScreen('instructions')
        if (buttonYCenter2-(buttonHeight//2))<=mouseY<=(buttonYCenter2+(buttonHeight//2)):
            setActiveScreen('scores')
        if (buttonYCenter3-(buttonHeight//2))<=mouseY<=(buttonYCenter3+(buttonHeight//2)):
            saveProfiles(app.existingProfiles)
            exit()

#Assigns which button to highlight
def home_onMouseMove(app,mouseX,mouseY):
    buttonXCenter,buttonWidth = 395,227
    buttonYCenter1,buttonYCenter2,buttonYCenter3,buttonHeight =387,514,637,87
    if (buttonXCenter-(buttonWidth//2))<= mouseX <=(buttonXCenter+(buttonWidth//2)):
        if (buttonYCenter1-(buttonHeight//2))<=mouseY<=(buttonYCenter1+(buttonHeight//2)):
            app.hovering='homeStart'
        elif (buttonYCenter2-(buttonHeight//2))<=mouseY<=(buttonYCenter2+(buttonHeight//2)):
            app.hovering='homeScores'
        elif (buttonYCenter3-(buttonHeight//2))<=mouseY<=(buttonYCenter3+(buttonHeight//2)):
            app.hovering='homeOptions'
        else: app.hovering=None
    else:app.hovering=None
 

#INSTRUCTION SCREEN-----------------------------------------------------------------------------

def instructions_redrawAll(app):
    instructionWidth, instructionHeight,instructionTop,instructionLeft = (
        app.width*6//8, app.height*6//8,app.width//8,app.height//12)
    drawBackground(app)
    drawImage(app.instructions, instructionTop,instructionLeft,
              width=instructionWidth,height=instructionHeight)
    #startButton
    sbuttonXC,sbuttonYC,sbuttonWidth,sbuttonHeight = app.width//2,720,225,85
    drawImage(app.startButton, sbuttonXC,sbuttonYC, width=225,height=85, align='center')
    drawRect(sbuttonXC,sbuttonYC, sbuttonWidth,sbuttonHeight, align='center',
              fill=None, border='black',borderWidth=7)
    drawRect(sbuttonXC,sbuttonYC, sbuttonWidth,sbuttonHeight, align='center',
              fill=None, border='pink')
    
    #back button
    bButtonLeft,bButtonYC,bButtonWidth,bButtonHeight = 0,app.height//12,70,70
    drawImage(app.backButton, bButtonLeft,bButtonYC, 
              width = bButtonWidth, height =bButtonHeight, align='left')
    if app.hovering == 'back':
        drawRect(bButtonLeft,bButtonYC,bButtonWidth,bButtonHeight,
                  fill='red', opacity=20, align='left')
    elif app.hovering == 'instructionsStart':
        drawRect(sbuttonXC,sbuttonYC,sbuttonWidth,sbuttonHeight, 
                  fill='red', opacity=20, align='center')
        

def instructions_onMousePress(app,mouseX,mouseY):
    sbuttonXC,sbuttonYC,sbuttonWidth,sbuttonHeight = app.width//2,720,225,85
    bButtonLeft,bButtonYC,bButtonWidth,bButtonHeight = 0,app.height//12,70,70
    #Start Button
    if ((sbuttonXC-(sbuttonWidth//2))<= mouseX <=(sbuttonXC+(sbuttonWidth//2)) and 
    (sbuttonYC-(sbuttonHeight//2))<=mouseY<=(sbuttonYC+(sbuttonHeight//2))):
        startGame(app)
    #Back Button
    elif (bButtonLeft<=mouseX<=bButtonLeft+bButtonWidth and 
          (bButtonYC-bButtonHeight//2)<=mouseY<=bButtonYC+bButtonHeight//2):
        setActiveScreen('home')

def instructions_onMouseMove(app,mouseX,mouseY):
    sbuttonXC,sbuttonYC,sbuttonWidth,sbuttonHeight = app.width//2,720,225,85
    bButtonLeft,bButtonYC,bButtonWidth,bButtonHeight = 0,app.height//12,70,70
    if ((sbuttonXC-(sbuttonWidth//2)) <= mouseX <= (sbuttonXC+(sbuttonWidth//2)) 
        and (sbuttonYC-(sbuttonHeight//2)) <= mouseY <= (sbuttonYC+(sbuttonHeight//2))):
            app.hovering = 'instructionsStart'
    elif (bButtonLeft<=mouseX<=(bButtonLeft+bButtonWidth) 
          and (bButtonYC-(bButtonHeight//2))<=mouseY<=(bButtonYC+(bButtonHeight//2))):
        app.hovering = 'back'
    else: app.hovering = None

#SCORES------------------------------------------------------------------------------------------

def scores_redrawAll(app):
    drawBackground(app)
    drawScoresButtons(app)
    drawScoresName(app)
    #Draw changeBox/current name if not changing the name, else draw Save box

def drawScoresButtons(app):
        #back button
    drawImage(app.backButton, 0, app.height//12, 
              width = 70, height =70, align='left')
    if app.hovering == 'back':
        drawRect(0,app.height//12,70,70, fill='red', opacity=20, align='left')
    drawLeaderboard(app)
    #change button
    cbuttonWidth, cbuttonHeight, cbuttonLeft, cbuttonTop = 225*4/5,85*4/5,520,54
    if not app.changePressed:
        drawImage(app.changeButton,app.width*35/40,app.height//9, align='right',
              width = cbuttonWidth, height = cbuttonHeight) 
        if app.hovering == 'change':
            drawRect(cbuttonLeft,cbuttonTop,cbuttonWidth,cbuttonHeight,
                    fill='red', opacity=20)
    else:
        drawImage(app.saveButton,cbuttonLeft, cbuttonTop,
              width = cbuttonWidth, height = cbuttonHeight) 
        if app.hovering == 'change':
            drawRect(cbuttonLeft,cbuttonTop,cbuttonWidth,cbuttonHeight,
                    fill='red', opacity=20)   

def drawScoresName(app):
    if not app.changePressed:
        drawLabel(f'USER:{app.profile.name}', app.width/6, app.height/10, 
                  size = 40, align='left', bold =True)
    else:
        if app.flashing: inputString = f'{app.nameInput}_'
        else: inputString = f'{app.nameInput}'
        drawLabel(inputString, app.width/6, app.height/10, size = 40,
              align='left', bold =True)
def drawLeaderboard(app):
    left, top, width, height = app.width*1/10, app.height/24, app.width*8/10, app.height*22/24
    drawRect(left, top, width, height, fill = 'white',
             borderWidth = 5, border= 'black')

    #Create a list of the 5 highestScores in existing profiles
    namesL = []
    scoresD = {}
    for i in app.existingProfiles:
        score = app.existingProfiles[i].highScore
        if score in scoresD: 
            scoresD[score] += [i]
        else:
            scoresD[score] = [i]
    scoresL = sorted(scoresD,reverse=True)
    for i in (scoresL):
        namesL += sorted(scoresD[i])
    arrow =chr(8592)
    for i in range(len(namesL)):
        name = namesL[i]
        score = app.existingProfiles[name].highScore
        currentNameS, otherNameS = f'{i+1}. {name}: {score}{arrow}',f'{i+1}. {name}: {score}'
        if i <9:
            drawLabel(currentNameS if app.profile.name == namesL[i] else otherNameS,
                    app.width//2, app.height/5 +60*i,size = 50, align = 'center',
                    bold =True, fill = 'black' if app.profile.name == namesL[i] else 'gray')
        #If current profile is not in top 10 place it at bottom of the list
        elif i == 9 and app.profile.name not in namesL[:9]:
            nameS = f'{namesL.index(app.profile.name)+1}. {app.profile.name}: {app.profile.highScore}{arrow}'
            drawLabel(nameS, app.width//2, app.height/5 + 540,size = 50, align = 'center',
                    bold =True, fill = 'black')
        #If current profile is in top 10, just rank #10
        elif i ==9: 
            drawLabel(currentNameS if app.profile.name == namesL[i] else otherNameS,
                    app.width//2, app.height/5 +60*i,size = 50, align = 'center',
                    bold =True, fill = 'black' if app.profile.name == namesL[i] else 'gray')
        
        
def scores_onStep(app):
    app.flashing = not app.flashing

def scores_onKeyPress(app, key):
    #Build profile name
    if app.changePressed:
        if key == 'backspace' and app.nameInput != '':
            app.nameInput = app.nameInput[:-1]

        elif key.isalpha() and len(key) == 1 and len(app.nameInput)<12: 
            app.nameInput += key.upper()

    #Create new profile if name not used
        elif key == 'enter' and app.nameInput != '':
            setNewProfile(app)
            app.changePressed = False


def scores_onMousePress(app,mouseX,mouseY):
    cbuttonWidth, cbuttonHeight, cbuttonLeft, cbuttonTop = 225*4/5,85*4/5,520,54
    if 0<=mouseX<=70 and 31<=mouseY<=101:
        setActiveScreen('home')
    elif (cbuttonLeft<=mouseX<=cbuttonLeft+cbuttonWidth
           and cbuttonTop<=mouseY<=cbuttonTop+cbuttonHeight
           and not app.changePressed):
        app.changePressed = True
    elif (cbuttonLeft<=mouseX<=cbuttonLeft+cbuttonWidth
           and cbuttonTop<=mouseY<=cbuttonTop+cbuttonHeight):
        setNewProfile(app)
        app.changePressed = False
    

def scores_onMouseMove(app,mouseX,mouseY):
    cbuttonWidth, cbuttonHeight, cbuttonLeft, cbuttonTop = 225*4/5,85*4/5,520,54
    if 0<=mouseX<=70 and 31<=mouseY<=101:
        app.hovering = 'back'
    elif (cbuttonLeft<=mouseX<=cbuttonLeft+cbuttonWidth
           and cbuttonTop<=mouseY<=cbuttonTop+cbuttonHeight):
        app.hovering = 'change'   
    else: app.hovering = None




#GAME---------------------------------------------------------------------------------------------

def drawBoard(app):
    tan = rgb(246,209,135)
    for row in range(4):
        for col in range(4):
            #Draws the board squares and letters
            squareLeft,squareTop = (app.boardLeft+col*app.squareSize,
                                     app.boardTop+row*app.squareSize)
            if row>0:squareTop-=8
            if col>0:squareLeft-=8

            guess=''
            yellow = rgb(255,255,143)
            for row1,col1 in app.selected:
                guess += app.board[row1][col1]
            if ((guess in app.foundWords) and ((row,col) in app.selected)):
                color = yellow
            elif (guess in app.legalWords and guess not in app.foundWords
                and ((row,col) in app.selected) and 2<len(guess)<11):
                color = 'lightGreen'
            else: color = tan
        
            drawRect(squareLeft+16,squareTop+16,app.squareSize-16,
                     app.squareSize-16, 
                     fill=color)
            drawLabel(app.board[row][col],squareLeft+app.squareSize//2+8,squareTop+app.squareSize//2+8,
                      size=50, bold=True)
    #draw surrounding square,lines
    drawRect(app.boardLeft,app.boardTop,app.boardSize, app.boardSize, fill = None,
             border='black', borderWidth=16)
    for i in range(3):
        drawLine(app.boardLeft,app.boardTop+((i+1)*app.squareSize),
                 app.boardRight,app.boardTop+((i+1)*app.squareSize),
                 lineWidth=16)
        drawLine(app.boardLeft+((i+1)*app.squareSize),app.boardTop,
                 app.boardLeft+((i+1)*app.squareSize),app.boardBottom,
                 lineWidth=16)
        
def drawTimer(app):
    drawRect(app.width//2, app.height//10, 300,100, align='center', fill='white',
             border='black', borderWidth=8)
    drawLabel(f"Score:{app.currentScore}", 400,80, align='center', size=40,
              font='Helvetica', bold=True)
    drawRect(400,122,100,50, fill='white', border='black', borderWidth=8, align='center')
    minutes, seconds= app.timer//60,app.timer%60
    if seconds < 10: seconds = '0' + f'{seconds}'
    drawLabel(f'{minutes}:{seconds}',400,122, align='center',
              bold=True, size=15)
    
    
def drawSelected(app):
    def center(app,row,col):
        x = (app.boardLeft + app.squareSize*(col+0.5))
        y = app.boardTop + app.squareSize*(row+0.5)
        if row>0:y-=5
        if col>0:x-=5
        return (x,y)
    
    for row,col in app.selected:
        x1,y1 = center(app,row,col)
        drawCircle(x1,y1,10,fill='red',opacity=80)
    #Only draw lines if there are more than 1 selected square
    if len(app.selected)>1:
        for i in range(len(app.selected)-1):
            (r1,c1),(r2,c2) = (app.selected[i]),(app.selected[i+1])
            (x1,y1),(x2,y2) = (center(app,r1,c1)),(center(app,r2,c2))
            drawLine(x1,y1,x2,y2, opacity=60, 
                     fill='red',lineWidth=7)
            
def drawHint(app):
    if app.hintsRemaining <= 0:
        return
    elif not app.showHint:
        drawLabel(f'Hold h to use one of your {app.hintsRemaining} remaining hints',
                  app.width//2, app.height*4/19, size = 20, fill='yellow')
    else: 
        hint = 'zxy'
        remainingWords = sorted(app.remainingWords, key=len)
        i=0
        while len(hint) ==3:
            hint = remainingWords[i]
            i+=1

        drawLabel(f'{hint}', app.width//2, app.height*4/19,
                  size=20, fill='yellow')

def game_redrawAll(app):
    drawBackground(app)
    drawTimer(app)
    drawBoard(app)
    drawSelected(app)
    drawHint(app)
    drawLabel("press 'p' to end game", app.width//2,154, align='center', size=15)

    
    

def game_onStep(app):
    app.timer -= 1
    if app.timer <=0:
        if app.currentScore > app.profile.highScore:
            app.profile.highScore = app.currentScore
            app.existingProfiles[app.profile.name] = app.profile
            saveProfiles(app.existingProfiles)
        setActiveScreen('results')
    if app.hintTimer > 0:
        app.hintTimer -=1




def game_onMousePress(app,mouseX,mouseY):
    if app.showHint ==True:
        app.showHint = False
        app.hintsRemaining -= 1
    for row in range(4):
        for col in range(4):
            #loop through each square to check if mouse in square
            if ((row,col) not in app.selected and 
                app.boardLeft+col*app.squareSize<mouseX<app.boardLeft+(col+1)*app.squareSize and
                app.boardTop+row*app.squareSize<mouseY<app.boardTop+(row+1)*app.squareSize):
                app.selected.append((row,col))

def game_onMouseDrag(app, mouseX, mouseY):
    for row in range(4):
        for col in range(4):
            #if mouse is in a square, add that square to your selected list if square next to last square
            if ((row,col) not in app.selected and 
                app.boardLeft+col*app.squareSize+8<mouseX<app.boardLeft+(col+1)*app.squareSize-8 and
                app.boardTop+row*app.squareSize+8<mouseY<app.boardTop+(row+1)*app.squareSize-8 and
                (app.selected==[] or distance(row, col, *app.selected[-1])<2)):
                    app.selected.append((row,col))
            
                
def game_onMouseRelease(app,mouseX,mouseY):
    guess=''
    for row,col in app.selected:
        guess += app.board[row][col]
    if (guess not in app.foundWords
        and guess in app.legalWords
        and 2<len(guess)<11):
        app.foundWords.add(guess)
        app.remainingWords.remove(guess)
        app.currentScore+=app.scoresDict[len(guess)]
        app.selectedFill = 'lightGreen'
    else:
        app.selectedFill = 'red'

    app.selected = []

def game_onKeyPress(app, key):
    if key == 'p':
        if app.currentScore > app.profile.highScore:
            app.profile.highScore = app.currentScore
            app.existingProfiles[app.profile.name] = app.profile
            saveProfiles(app.existingProfiles)
        setActiveScreen('results')
    if key.lower() =='h' and app.hintsRemaining >0:
        app.showHint = True
        

def game_onKeyRelease(app,key):
    if key.lower() == 'h':
        app.showHint = False
        app.hintsRemaining -= 1

    
    app.selected=[]

#RESULTS------------------------------------------------------------------------

def results_redrawAll(app):

    retryLeft, retryRight, retryTop, retryBottom = 310, 490, 724, 799
    backLeft, backRight, backTop, backBottom = 0, 70, 31, 101
    
    drawBackground(app)
    drawLabel(f'Total:{app.currentScore}', app.width//2, app.height/10,
              size=40, bold=True)
    drawScoreBoard(app)
    drawImage(app.backButton,0, 66, align = 'left', width=70, height=70)

    if app.profile != None and  app.profile.highScore <= app.currentScore and app.flashing:
        drawLabel('New Record!', app.width//2, app.height//19, size =35,
                  align='center', fill = 'red', bold=True)

    drawImage(app.retryButton, app.width//2, app.height*99/104, 
              width = 180, height =75, align='center')
    if app.hovering == 'back':
        drawRect(0,31,70,70, fill='red', opacity=20)
    elif app.hovering == 'retry':
        drawRect(retryLeft,retryTop,retryRight-retryLeft,
                 retryBottom-retryTop, fill='red', opacity=20)
        


    
    
def drawScoreBoard(app):
    left, top, width, height = app.width*1/10, app.height/16, app.width*8/10, app.height*12/14
    drawRect(left, top, width, height, fill = 'white',
             borderWidth = 5, border= 'black')
    
    drawLabel(f'Total:{app.currentScore}', app.width//2, app.height/8,
              size=40, bold=True)
    drawLine(left,143,left+width,143, lineWidth = 5)
    if len(app.foundWords) != 0:
        foundWords = (list(app.foundWords))
        foundWords.sort()
        foundWords.sort(key =len, reverse=True)
    else:
        foundWords=[]
    

    #Draws the found words in the result screen
    for i in range(len(foundWords)):
        if len(foundWords)<21:
            drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                       app.width//2, 160 + i*29,
                       align='center', size=20, bold=True)
        elif len(foundWords)<41:
            if i<20:
                drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                            app.width//2 - width/4, 160 + i*29,
                            align='center', size=20, bold=True)
            else:
                drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                            app.width//2 + width/4, 160 + (i%20)*29,
                            align='center', size=20, bold=True)
        else:
            if i<20:
                drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                            app.width//2 - width/3, 160 + i*29,
                            align='center', size=20, bold=True)
            elif i<40:
                drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                            app.width//2, 160 + (i%20)*29,
                            align='center', size=20, bold=True)
            elif i<60:
                drawLabel(f'{foundWords[i].upper()}:{app.scoresDict[len(foundWords[i])]}',
                            app.width//2 + width/3, 160 + (i%20)*29,
                            align='center', size=20, bold=True)
                
def results_onMousePress(app,mouseX,mouseY):
    retryLeft, retryRight, retryTop, retryBottom = 310, 490, 724, 799
    backLeft, backRight, backTop, backBottom = 0, 70, 31, 101
    if retryLeft<=mouseX<=retryRight and retryTop<=mouseY<=retryBottom:
        startGame(app)
    elif backLeft<=mouseX<=backRight and backTop<=mouseY<=backBottom:
        setActiveScreen('home')

def results_onMouseMove(app,mouseX,mouseY):
    retryLeft, retryRight, retryTop, retryBottom = 310, 490, 724, 799
    backLeft, backRight, backTop, backBottom = 0, 70, 31, 101
    if retryLeft<=mouseX<=retryRight and retryTop<=mouseY<=retryBottom:
        app.hovering = 'retry'
    elif backLeft<=mouseX<=backRight and backTop<=mouseY<=backBottom:
        app.hovering = 'back'
    else: 
        app.hovering = None

def results_onStep(app):
    app.flashing = not app.flashing
    if app.hintTimer > 0:
        app.hintTimer -=1

    





def main():
    runAppWithScreens(initialScreen='start')
    app.foundWords = []

main()

