#!/usr/bin/env python3

from tkinter import *
from MorseCode import *
from Sound import *
from CardReader import *
from Dialogue import *
from PIL import Image, ImageTk
import pyqrcode
import tkinter.messagebox

class GameDisplay:
    morser = MorseCode()
    sound = Sound()
    scanner = CardReader()
    dialogue = Dialogue()
    next_Location_Hint = pyqrcode.create('http://maps.ntu.edu.sg/m?q=Tutorial%20Room%20%2B%2024%20-%20LHN&fs=m')
    next_Location_Hint.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
    clue1 = 'res/clue1.wav'
    clue2 = 'res/clue2.wav'
    clue_HE = 'res/Clue - HE.mp3'
    clue_IS = 'res/Clue - IS.mp3'
    clue_NO = 'res/Clue - NO.mp3'
    clue_LONGER = 'res/Clue - LONGER.mp3'
    clue_THE = 'res/Clue - THE.mp3'
    clue_SAME = 'res/Clue - SAME.mp3'

    bgMusic = 'res/Basement Floor.mpeg'
    bgImage = 'res/Background.jpg'
    dud1 = "res/Troll Song.wav"
    dud2 = "res/Music of Memes.wav"
    dud3 = "res/Evolution_of_Dance.wav"
    dud4 = "res/My Heart Will Go On - Recorder By Candlelight by Matt Mulholland.wav"
    dud5 = "res/Rick Astley - Never Gonna Give You Up.wav"
    dud6 = "res/Charlie Schmidts Keyboard Cat! - THE ORIGINAL!.wav"
    dud7 = "res/X - Men.wav"

    code_TextBox_Intro = "Welcome to the Morse Code user interface. Fill this textBox with morse code and press " \
                         "the decode button to decode the morse code into words in the textbox below." \
                         "Input '-' for long beep, and '.' for short beep. \n" \
                            "Add a single space between each character and 2 spaces between each word\n" \
                            "DO NOT END WITH >=2 SPACES"
    string_TextBox_Intro = "Fill this box with your message in words, and press the encode button to encode to message" \
                           " to morse code. Press the play button to play the morse code you have written in the textbox" \
                           " above. Press the 'click to scan' button to scan cards placed on the reader"

    def __init__(self, master):
        self.master = master
        self.label = Label(master, bg='black')
        self.master.geometry('600x600')
        self.master.title("Revelations")
        self.label.pack(fill=BOTH, expand=True)


        #   creating necessary frames
        self.frame = Frame(self.label, bg='#212733')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.subFrame = Frame(self.frame)
        self.subFrame2 = Frame(self.frame)

        #   Adding background image/gif to the main frame
        self.image = Image.open(self.bgImage)
        self.image_copy = self.image.copy()
        self.backgroundImage = ImageTk.PhotoImage(self.image)

        self.label.config(image=self.backgroundImage)
        self.label.bind('<Configure>', self.resize_img)


        #   Creating labels
        self.encodeLabel = Label(self.frame, text="Encoded Morse Code:", bg="#212733", fg="white", font="none 12 bold")
        self.decodeLabel = Label(self.frame, text="\nDecoded String:", bg="#212733", fg="white", font="none 12 bold")
        self.exitLabel = Label(self.frame, text="\nclick to exit:", bg="#212733", fg="white", font="none 12 bold")

        #   Creating text boxes
        self.codeTextBox = Text(self.frame, width=75, height=6, wrap=WORD, background="white")
        self.stringTextBox = Text(self.frame, width=75, height=6, wrap=WORD, background="white")



        #   Creating buttons
        self.decodeBtn = Button(self.master, text="DECODE", width=6, command=self.decode)
        self.encodeBtn = Button(self.master, text="ENCODE", width=6, command=self.encode)
        self.clearBtn = Button(self.subFrame2, text="Clear", width=6, command=self.clear_text)
        self.playBtn = Button(self.master, text="Play", width=6, command=self.playCode)
        self.exitBtn = Button(self.frame, text="Exit", width=6, command=self.close_window)
        self.scanBtn = Button(self.subFrame2, text='Click to scan', command=self.create_window)

        #   Arranging the layout
        Label(self.frame, text='Morse Decoder User Interface', bg='#212733', fg='white', font='none 24 bold').pack()


        self.encodeLabel.pack()
        self.codeTextBox.pack()

        self.subFrame.pack(anchor=CENTER)
        self.encodeBtn.pack(in_=self.subFrame, side=LEFT)
        self.decodeBtn.pack(in_=self.subFrame, side=LEFT)
        self.playBtn.pack(in_=self.subFrame, side=LEFT)
        Button(self.frame, text='Intro message', command=self.intro).pack(in_=self.subFrame, side=LEFT)

        self.subFrame2.pack(anchor=CENTER)
        self.scanBtn.pack(side=LEFT)
        self.clearBtn.pack(side=LEFT)
        self.decodeLabel.pack()
        self.stringTextBox.pack()
        self.exitLabel.pack()
        self.exitBtn.pack()

        self.stringTextBox.insert(1.0, self.string_TextBox_Intro)
        self.codeTextBox.insert(1.0, self.code_TextBox_Intro)
        
        #   start off with background music on endless loop
        self.sound.playEndlessLoop(self.bgMusic)
        print("playing bg")

    def resize_img(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.image_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.background_image)

    # key down function
    def playtest(self):
        self.sound.playSound('res/clue1.mp3')

    def playCode(self):
        code = self.codeTextBox.get(1.0, 'end-1c')
        self.sound.playMorse(code)

    def decode(self):
        try:
            code = self.codeTextBox.get(1.0, 'end-1c')
            decodedString = self.morser.decrypt(code)
        except ValueError:
            decodedString = "Invalid morse code. Input '-' for long beep, and '.' for short beep. \n" \
                            "Add a single space between each character and 2 spaces between each word\n" \
                            "DO NOT END WITH >=2 SPACES"
        self.stringTextBox.delete(1.0, END)
        self.stringTextBox.insert(1.0, decodedString)

        if(decodedString == 'HE IS NO LONGER THE SAME'):
            self.dialogue.create_first_dialog()

    def encode(self):
        try:
            decodedString = self.stringTextBox.get(1.0, 'end-1c')
            code = self.morser.encrypt(decodedString)[:-1]
        except KeyError:
            code = "Invalid string. Do not include special symbols like '@#$%^&*' "
        self.codeTextBox.delete(1.0, END)
        self.codeTextBox.insert(1.0, code)

    def clear_text(self):
        self.codeTextBox.delete(1.0, END)
        self.stringTextBox.delete(1.0, END)

    def intro(self):
        self.clear_text()
        self.stringTextBox.insert(1.0, self.string_TextBox_Intro)
        self.codeTextBox.insert(1.0, self.code_TextBox_Intro)

    def create_window(self):
        clue = self.scanner.getClueNum()
        print(clue[0:15])
        if (clue[0:7] == 'Clue_HE'):
            self.sound.playSound(self.clue_HE)
            print('playing clue "HE"')
        elif (clue[0:7] == 'Clue_IS'):
            self.sound.playSound(self.clue_IS)
            print('playing clue "IS"')
        elif (clue[0:7] == 'Clue_NO'):
            self.sound.playSound(self.clue_NO)
            print('playing clue "NO"')
        elif (clue[0:11] == 'Clue_LONGER'):
            self.sound.playSound(self.clue_LONGER)
            print('playing clue "LONGER"')
        elif (clue[0:8] == 'Clue_THE'):
            self.sound.playSound(self.clue_THE)
            print('playing clue "THE"')
        elif (clue[0:9] == 'Clue_SAME'):
            self.sound.playSound(self.clue_SAME)
            print('playing clue "SAME"')
        elif (clue[0:4] == 'Dud1'):
            self.sound.playSound(self.dud1)
        elif (clue[0:4] == 'Dud2'):
            self.sound.playSound(self.dud2)
        elif (clue[0:4] == 'Dud3'):
            self.sound.playSound(self.dud3)
        elif (clue[0:4] == 'Dud4'):
            self.sound.playSound(self.dud4)
        elif (clue[0:4] == 'Dud5'):
            self.sound.playSound(self.dud5)
        elif (clue[0:4] == 'Dud6'):
            self.sound.playSound(self.dud6)
        elif (clue[0:4] == 'Dud7'):
            self.sound.playSound(self.dud7)
        elif(clue[0:8] == 'Location'):
            self.next_Location_Hint.show()
            print("Displaying the next location in QR code")

    def create_info(self):
        tkinter.messagebox.showinfo('SCANNING MODE', 'You may now place the card on the scanner')

    def close_window(self):
        self.frame.destroy()
        exit()


if __name__ == '__main__':
    root = Tk()
    windows = GameDisplay(root)
    root.mainloop()
