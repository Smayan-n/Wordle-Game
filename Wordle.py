#created using PyQt5
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random, sys

class Window(QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        #fonts 
        self.font1 = QFont("Aerial", 50)
        self.font2 = QFont("Aerial", 15)

        #creating the timer and connecting it to the updateTimer method
        timer = QTimer(self)
        timer.timeout.connect(self.updateTimer) #calls updateTimer method every second
        #updates every second
        timer.start(1000)

        #creating timer label and related variables
        self.timerRun = False
        self.time = 0
        self.time_label = QLabel("Time Elapsed: 0", self)
        self.time_label.setGeometry(780, -10, 500, 100)
        self.time_label.setFont(self.font2)
        self.time_label.setStyleSheet("color: white")

        #var to store state of game (in progress or gameComplete)
        self.gameComplete = False
        
        #setting some rgb colors to use
        self.COLOR_GREY = "rgb(58, 58, 60)"
        self.COLOR_GREEN = "rgb(83, 141, 78)"
        self.COLOR_YELLOW = "rgb(181, 159, 59)"
       
        #array that stores keys from a to z so event.key (look below) can easily identify key from corresponding decimal value
        self.keys = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z"]

        #first call to init game
        self.importWords()
        self.initGame()

    def updateTimer(self):
        
        #if flag is true
        if self.timerRun:
            #increment time
            self.time += 1
            #update time label
            self.time_label.setText("Time Elapsed: " + str(self.time))
    
    def resetTimer(self):
        self.timerRun = False
        self.time = 0
        self.time_label.setText("Time Elapsed: 0")

    #function imports stores words from .txt files in arrays (dictionary and word_set)
    def importWords(self):
        
        #getting a random word from wordle_words.txt file
        self.word_set = []

        wordsDir = "data/wordle_words.txt"
        with open(wordsDir, "r") as f:
            #getting list of all words
            for line in f.readlines():
                word = line.strip().upper() #stripping word to remove \n char
                self.word_set.append(word)


        #making a dictionary list that wil be used to check the words entered.
        self.dictionary = []

        dictDir = "data/wordle_dictionary.txt"
        with open(dictDir, "r") as f:
            #getting list of all words
            for line in f.readlines():
                word = line.strip().upper() #stripping word to remove \n char
                self.dictionary.append(word)


    #function to init variables 
    def initGame(self):

        #2D array that stores the 5x6 grid for letters. Each space for a letter is a QLabel self
        self.mainWordDisplay = [[QLabel("_", self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)],
                        [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)],
                        [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)],
                        [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)],
                        [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)],
                        [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
                        ]


        #variables for accesing the labels in mainWordDisplay (accesed mainly by input handler)
        self.row = 0
        self.column = -1


        #a random word is choosen from a list of all the words in wordle_words.txt
        self.actualWord = random.choice(self.word_set)
        #print(self.actualWord)


        #calls method to init UI
        self.initUI()


    #initialization of window and ui
    def initUI(self):

        #widget is accesed by self keyword
        self.setWindowTitle("Wordle!")

        #sets size of window. The ability to be resized is restricted
        self.setFixedSize(1280, 1580)

        #setting bg color of window
        self.setStyleSheet("background: rgb(18, 18, 19)") 


        #nested for loop to initialize all the QLabels inside array
        #x and y represent the position of the labels
        x = 30
        y = 90

        for list in self.mainWordDisplay:
            
            for label in list:
                
                #sets font
                label.setFont(self.font1)
                #alligns text in label to center
                label.setAlignment(QtCore.Qt.AlignCenter)

                #determines placement and size of label
                label.setGeometry(x, y, 220, 220)
                x += 250

                #setting border around label
                self.setLetterAppearence(label, "border: 10px solid rgb(45, 45, 46); color: white")
                               

            #resetting x after each row of labels are initialized
            x = 30
            #incrementing y after every row is initialized
            y += 250

        #making a reset button:
        resetBtn = QPushButton("New Word", self)
        resetBtn.setGeometry(32, 10, 218, 60)
        resetBtn.setStyleSheet("background-color: rgb(235, 116, 47)")
        resetBtn.clicked.connect(self.resetGame)

        #save image button
        #saveImgBtn = QPushButton("Save Wordle", self)
        #saveImgBtn.setGeometry(284, 10, 218, 60)
        #saveImgBtn.setStyleSheet("background-color: rgb(235, 116, 47)")
        #saveImgBtn.clicked.connect(self.saveWordImage)

    #method that gets keyboard presses (automatically called)
    #event.key returns decimal value of keyboard key pressesd
    def keyPressEvent(self, event):

        self.timerRun = True

        #gets decimal value of key press
        key = event.key()

        keyPressed = ""
        
        #if key pressed not letter or backspace or enter, it's not considered

        if key == 16777219:
            keyPressed = "backspace"
        elif key == 16777220:
            keyPressed = "enter"
        elif(key >= 65 and key <= 90):
            keyPressed = self.keys[key - 65]
        
        #if key pressed is not between decimal values of a and z
        else:
            keyPressed = ""


        #calls method that handles input with key pressed as parameter
        self.inputHandler(keyPressed)

    #handles keyboard inputs
    def inputHandler(self, key):

        #if game is gameComplete, use cannot type anything 
        if(not self.gameComplete):

            #1D array of the current row of letters (passed into many other funcs as an arg) - used to access letters on currenct row
            letters = self.mainWordDisplay[self.row]


            #if key pressed is enter, the rest of the code is not run
            if(key == "enter"):


                #calling the method that handles the main logic(matching words etc.) if word is valid
                if(self.isValid(letters)):

                    self.wordHandler(letters)

                    #if word is valid, the row and column are adjusted (input goes to next row, and column value is reset):
                    self.row += 1
                    self.column = -1
                    return


                return

            #if key is blank, it is of no use, so it's ignored
            if(key != ""):

    
                #if key pressed is backspace, a letter is removed from label:
                if(key == "backspace"):

                    #if there was a showWarning before, pressing backspace will reset it
                    self.showWarning(letters, False)

                    #clears current letter
                    self.mainWordDisplay[self.row][self.column].clear()

                    #decrement value of col to highlight previous letter
                    if self.column >= 0:
                        self.column -= 1
                    

                else:
                    #if there was a showWarning before, pressing any other key will reset it for that row
                    self.showWarning(letters, False)

                    
                    #if one row is full, player is not allowed to enter more letters. no more code runs to prevent any erros
                    if(self.column == 4):
                        return
                    

                    #incrementing col of arr each time letter is entered.
                    self.column+=1
                    
                    #setting key presses to label in mainWordDisplay
                    self.mainWordDisplay[self.row][self.column].setText(key)
        

    #seperate function to check for errors in word entered(too short, not in set, etc) - is it valid?
    def isValid(self, letters):

        #if word entered(word in one row) does not contain 5 letters, a Warning is displayed
        #the border color is changed to red
        word = ""
        for letter in letters:
            if(letter.text() == ""):
                #calls showWarning method
                self.showWarning(letters, True)

                #exit method - not valid
                return False
            
            word += letter.text()

     
        #also checks if word is dictionary(self.dictionary)
        #if it's not, a showWarning is shows
        if(word not in self.dictionary):
            self.showWarning(letters, True)

            #also show a popup
            self.showOutputDialog("Word not found in dictionary", "Invalid Word")

            return False

        #else, return true
        return True


    def wordHandler(self, letters):

        #splitting actual word into individual letters (list comprehention)
        actualLetters = [char for char in self.actualWord]
            
        #checking the individal letters of word

        #array to store colors representing wrong / right / misplaced letters
        colorOverview = ["", "", "", "", ""]

            
        #using enumerate to get index for actualLetters as well
        #first loop identifies the correct letters
        for i, letter in enumerate(letters, 0):
                
            if(letter.text() == actualLetters[i]):
                colorOverview[i] = self.COLOR_GREEN
                #removing the correct letter from list
                actualLetters[i] = ""

        
        #second loop identifies misplaced and wrong letters
        for i, letter in enumerate(letters, 0):

            #if letter is in the word and the letter is not in the right place
            if(letter.text() in actualLetters and colorOverview[i] == ""):
                colorOverview[i] = self.COLOR_YELLOW
                #removing the misplaced letter from list
                actualLetters[actualLetters.index(letter.text())] = ""
                
            #finally, the letter is wrong only if it is not misplaced or correct
            elif(colorOverview[i] == ""):
                colorOverview[i] = self.COLOR_GREY
                        
                
                
        #calling method to display colorOverview of right / wrong letters
        self.displayOverview(letters, colorOverview)
        self.checkMatch(letters)


    #method to check if word matched actual word
    def checkMatch(self, letters):

        #checks to see if word is correct:
        word = ""
        for letter in letters:
            word += letter.text()
        
        if word == self.actualWord:
            #pauses timer
            self.timerRun = False

            #shows player that he got the word right
            self.showOutputDialog(f"Congrats! You got the word {self.actualWord} in {self.time} seconds" ,                                                                                                "You Win!")
            self.gameComplete = True

        #else if player could not get word, he looses
        elif(self.row == 5):
            #pauses timer
            self.timerRun = False

            self.showOutputDialog("Better luck next time The word was: " + self.actualWord, "Game Over")
            self.gameComplete = True
          
    #method to display the colors representing right and wrong letters in a row
    def displayOverview(self, letters, colorOverview):
        
        
        #using enumerate to get index value as well (used to access colors in colorOverview)
        for i, letter in enumerate(letters, 0):

            style = "background-color: " + colorOverview[i] + "; color: white"
            self.setLetterAppearence(letter, style)
            

    #method that sets color of row border depending on condition
    def showWarning(self, letters, condition):

        #if condition is true, its an showWarning. If condition os false, the showWarning needs to be reset
        style = "border: 10px solid rgb(45, 45, 46); color: white"
        if condition:
            style = "border: 5px solid rgb(237, 64, 70); color: white"

        for letter in letters:
            self.setLetterAppearence(letter, style)


    #sepearte method to set the appeearance of the letters(color, border etc)
    def setLetterAppearence(self, letter, style):
        letter.setStyleSheet(style)
    
    #method to create QDialoges and output win / loose messages
    def showOutputDialog(self, text, title):

        #creates a dialog object
        dialog = QDialog()
        dialog.setFixedSize(600, 350)

        #creates a label
        label = QLabel(text, dialog)
        label.setFont(self.font2)
        label.setWordWrap(True)
        label.setAlignment(QtCore.Qt.AlignCenter)
        

        #button inside the dialogbox to dismiss it
        btn = QPushButton("OK", dialog)
        btn.setFont(self.font2)
        btn.move(300, 125)

        btn.clicked.connect(lambda: dialog.close())

        #creates a layout for displaying the button and text(label)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch()
        vbox.addWidget(btn)

        dialog.setLayout(vbox)

        dialog.setWindowTitle(title)
        dialog.exec_()

    #resets game and generates new word
    def resetGame(self):

        for row in self.mainWordDisplay:
            for label in row:
                #clearing all letters and formatting
                label.clear()

                self.setLetterAppearence(label, "border: 10px solid rgb(45, 45, 46); color: white")
            
        
        self.mainWordDisplay[0][0].setText("_")

        #resetting row and column vals
        self.row = 0
        self.column = -1

        #a new random word is choosen
        self.actualWord = random.choice(self.word_set)
        #print(self.actualWord)

        #reset timer
        self.resetTimer()

        #game gameComplete is false again
        self.gameComplete = False

    #not used
    def saveWordImage(self):

        return
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId(), 0, 70)
        screenshot.save("img.jpg", "jpg")        


def start():

    #driver code to create a new QMainWindow object
    app = QApplication(sys.argv)

    #creating the window
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
   start()