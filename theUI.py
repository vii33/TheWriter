from tkinter import *
import azurespeech.speech_rec as speech
#import time
from datetime import datetime
import pprint

#Transparency Tips:
#app.wait_visibility(app)
#app.wm_attributes('-alpha',0.3)
#Canvas(app, width=100, height=100, bd=1, highlightthickness=1)

class Window(Frame):
    def __init__(self, master, speech_key:str, service_region: str):
        print("ui init")
        
        # Prop init
        self.speech_recoginzer = None
        self.speech_key = speech_key
        self.service_region = service_region
        self.conversation = {}

        # UI stuff
        super().__init__(master)
        self.master = master
        self.master.title('The Writer')
        #master.geometry("700x350")
        self.master.configure(bg="#333333")
        global Tkinterinstance
        Tkinterinstance = master

        self.create_widgets()
        self.mainloop()




    def create_widgets(self):  
        self.mytext_live = StringVar()
        self.mytext_live.set("inital")

        self.mytext_final = StringVar()
        self.mytext_final.set("inital")
   
        self.label_final = Label(self.master, textvariable=self.mytext_final, 
            font=("bold", 14), 
            pady=4, 
            padx=1,
            width=40,
            height=4,
            justify=LEFT,
            anchor=NW,
            bg="#1E1E1E",
            fg="white",
            wraplength=400)

        self.label_live = Label(self.master, textvariable=self.mytext_live, 
            font=("bold", 14), 
            pady=4, 
            padx=1,
            width=40,
            height=4,
            justify=LEFT,
            anchor=NW,
            bg="#252526",
            fg="white",
            wraplength=400)

        self.label_blind = Label(self.master, width=10, bg="#333333")

        self.button_en = Button(self.master, text="EN", command=self.startEn,
                width=5,
                bg="#333333",
                relief=GROOVE,
                fg="white"
                )
        self.button_de = Button(self.master, text="DE", command=self.startDe,
                width=5,
                bg="#333333",
                relief=GROOVE,
                fg="white",
                )
        self.button_clipboard = Button(self.master, text="Clip", command=self.ClipBoardSummary,
                width=5,
                bg="#333333",
                relief=GROOVE,
                fg="white",
                )
        self.button_save = Button(self.master, text="Save", command=self.save,
                width=22,
                bg="#333333",
                relief=GROOVE,
                fg="white"
                )

        self.button_en.grid(row=0, column=0, sticky=W, padx=3, pady=5)
        self.button_de.grid(row=0, column=1, sticky=W)
        self.button_clipboard.grid(row=0, column=2)
        self.label_blind.grid(row=0, column=2)
        self.button_save.grid(row=0, column=3, sticky=E, padx=3, pady=5)
        self.label_final.grid(row=1, column=0, columnspan=4, padx=3, pady=0)
        self.label_live.grid(row=2, column=0, columnspan=4, padx=3, pady=3)
        
        

    def startEn(self):
        if self.speech_recoginzer is not None:
            self.speech_recoginzer.stop_recognizing()
        
        self.startRecognizing("en-US")


    def startDe(self):
        if self.speech_recoginzer is not None:
            self.speech_recoginzer.stop_recognizing()
        
        self.startRecognizing("de-DE") 
        #self.button_de.configure(highlightbackground="blue")

    def ClipBoardSummary(self):
        Tkinterinstance.clipboard_clear()
        Tkinterinstance.clipboard_append(self.speech_recoginzer.conversation)

    def startRecognizing(self, recognition_language: str):
        print("starting {}".format(recognition_language))
        self.speech_recoginzer = speech.Speech_Rec(self.speech_key, 
                self.service_region, recognition_language, self)
        self.speech_recoginzer.start_recognizing()


    def save(self):
        if self.speech_recoginzer is not None:
            fn = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            f = open(fn +".txt","w")
            #f.write( str(self.speech_recoginzer.conversation) )
            pprint.pprint(self.speech_recoginzer.conversation, stream=f, indent=1, width=160, depth=None)
            f.close()

            


if __name__ == '__main__':
    root = Tk()
    win = Window(master=root, speech_key="speech_key", service_region="service_region")
    win.mytext_live.set("this is an example text for display")
    win.mainloop()

