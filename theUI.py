from tkinter import *
import azurespeech.speech_wrapper as speech  #custom wrapper
from datetime import datetime
import pprint
import keyboard

#Transparency Tips:
#app.wait_visibility(app)
#app.wm_attributes('-alpha',0.3)
#Canvas(app, width=100, height=100, bd=1, highlightthickness=1)

# Colors
color_bg_dark = "#1E1E1E"
color_bg_light = "#252526"
color_header = "#2D2D2D"
color_buttons = "#3A3A3A"

class Window(Frame):
    def __init__(self, master, speech_key:str, service_region: str, mic_id: str = None):
        print("UI init")
        
        # Prop init
        self.speech_recoginzer = None
        self.speech_key = speech_key
        self.service_region = service_region
        self.conversation = {}
        self.silent_mode_active = False
        self.dict_mode_active = False
        self.mic_id = mic_id
        self.__text_result = ""
        self.__text_live = ""  

        # UI stuff
        super().__init__(master)
        self.master = master
        self.master.title('The Writer')
        #master.geometry("700x350")
        self.master.configure(bg=color_header)

        self.create_widgets()
        self.mainloop()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing())

  
    def on_closing(self):
        print("Closing...")
        self.speech_recoginzer.stop_recognizing()

    def create_widgets(self):  
        self.mytext_live = StringVar()
        self.mytext_live.set("...")

        self.mytext_result = StringVar()
        self.mytext_result.set("...")
   
        self.label_final = Label(self.master, textvariable=self.mytext_result, 
            font=("bold", 14), 
            pady=5, # inside text padding
            padx=1,
            width=40,
            height=4,
            justify=LEFT,
            anchor=NW,
            bg=color_bg_light,
            fg="white",
            wraplength=400)

        self.label_live = Label(self.master, textvariable=self.mytext_live, 
            font=("bold", 14), 
            pady=5,   
            padx=1,
            width=40,
            height=4,
            justify=LEFT,
            anchor=NW,
            bg=color_bg_dark,
            fg="white",
            wraplength=400)

        self.label_blind = Label(self.master, width=16, bg=color_header)

        self.button_en = Button(self.master, text="EN", command=self.btn_start_EN,
                font=("normal", 10),
                width=6,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )
        self.button_de = Button(self.master, text="DE", command=self.btn_start_DE,
                font=("normal", 10),
                width=6,
                bg=color_buttons,
                relief=GROOVE,
                fg="white",
                )
        self.button_silent_mode = Button(self.master, text="Silent", command=self.btn_silent_mode,
                font=("normal", 8),
                #width=6,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )
        self.button_clear_record = Button(self.master, text="C", command=self.btn_clear_record,
                font=("normal", 8),
                #width=6,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )
        self.button_dictation_mode = Button(self.master, text="Dict", command=self.btn_dictation_mode,
                font=("normal", 8),
                #width=6,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )
        self.button_save_clipboard = Button(self.master, text="Save CB", command=self.save_cb,
                font=("normal", 10),
                #width=10,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )
        self.button_save_file = Button(self.master, text="Save file", command=self.save_file,
                font=("normal", 10),
                #width=10,
                bg=color_buttons,
                relief=GROOVE,
                fg="white"
                )

        btnYpadding = 12
        self.button_en.grid(row=0, column=0, sticky=W, padx=(8, 3), pady=btnYpadding)
        self.button_de.grid(row=0, column=1, sticky=W, padx=0, pady=btnYpadding)
        self.button_dictation_mode.grid(row=0, column=2, sticky=W, padx=(3,0), pady=btnYpadding)
        self.button_silent_mode.grid(row=0, column=3, sticky=W, padx=0, pady=btnYpadding)
        self.button_clear_record.grid(row=0, column=4, sticky=W, padx=3, pady=btnYpadding)
        self.label_blind.grid(row=0, column=5, padx=0, pady=btnYpadding)
        self.button_save_clipboard.grid(row=0, column=6, sticky=E, padx=0, pady=btnYpadding)
        self.button_save_file.grid(row=0, column=7, sticky=E, padx=(3, 8), pady=btnYpadding)
        self.label_final.grid(row=1, column=0, columnspan=8, padx=3, pady=0)
        self.label_live.grid(row=2, column=0, columnspan=8, padx=3, pady=3)
        

    def btn_start_EN(self):
        if self.speech_recoginzer is not None:
            self.speech_recoginzer.stop_recognizing()
            self.speech_recoginzer = None
            self.reset_buttons()
            return
        
        self.startRecognizing("en-US", self.dict_mode_active)
        self.mytext_result.set("Detection started")
        self.button_en.config(background = color_bg_dark)
        self.button_en.config(text="(X)")


    def btn_start_DE(self):
        if self.speech_recoginzer is not None:
            self.speech_recoginzer.stop_recognizing()
            self.speech_recoginzer = None
            self.reset_buttons()
            return

        self.startRecognizing("de-DE", self.dict_mode_active) 
        self.mytext_result.set("Detection started")
        self.button_de.config(background = color_bg_dark)
        self.button_de.config(text="(X)")

    def reset_buttons(self):
        self.button_en.config(background = color_buttons)
        self.button_en.config(text="EN")
        self.button_de.config(background = color_buttons)
        self.button_de.config(text="DE")

    def startRecognizing(self, recognition_language: str, dict_mode_active: str = False):
        print("starting {}".format(recognition_language))
        self.speech_recoginzer = speech.Speech_Wrapper(self.speech_key, 
                self.service_region, recognition_language, self.mic_id, dict_mode_active, self)
        self.speech_recoginzer.start_recognizing()

    def btn_silent_mode(self):
        if self.silent_mode_active == False:
            self.button_silent_mode.config(background = color_bg_dark)
            self.label_final.config(fg = color_bg_light)
            self.label_live.config(fg = color_bg_dark)
            self.silent_mode_active = True
        else:
            self.button_silent_mode.config(background = color_buttons)
            self.label_final.config(fg = "white")
            self.label_live.config(fg = "white")
            self.silent_mode_active = False

    def btn_dictation_mode(self):
        if self.dict_mode_active == False:
            self.button_dictation_mode.config(background = color_bg_dark)
            self.dict_mode_active = True
        else:
            self.button_dictation_mode.config(background = color_buttons)
            self.dict_mode_active = False

    def btn_clear_record(self):
        self.speech_recoginzer.conversation = {}
        self.mytext_result.set("")
        self.mytext_live.set("")

    def save_cb(self):
        if self.speech_recoginzer is not None:
            pp = pprint.PrettyPrinter(indent=1, width=90)
            text = pp.pformat(self.speech_recoginzer.conversation)

            self.master.clipboard_clear()
            self.master.clipboard_append(text)
            self.master.update()      # needed to stay on the clipboard after the window is closed
            
            print("Text copied to clipboard")
            self.mytext_result.set("Text copied")

    def save_file(self):
        if self.speech_recoginzer is not None:
            fn = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            f = open(fn +".txt","w")
            pprint.pprint(self.speech_recoginzer.conversation, stream=f, indent=1, width=120, depth=None)
            f.close()
            
            print("Text written to HDD")
            self.mytext_result.set("Text written to HDD")

    def getResultText(self):
        return self.__text_result

    def setResultText(self, x):
        self.__text_result = x
        if (self.dict_mode_active == True):        
            keyboard.write(" ")
            keyboard.write(x)
        self.mytext_result.set(x)

    def getLiveText(self):
        return self.__text_live

    def setLiveText(self, x):
        self.__text_live = x
        self.mytext_live.set(x)

    result_text = property(getResultText, setResultText)   
    live_text = property(getLiveText, setLiveText)   

if __name__ == '__main__':
    root = Tk()
    win = Window(master=root, speech_key="a459d5678a5447e2a46e66a4ae719037", service_region="westeurope")
    win.mytext_live.set("this is an example text for display")
    win.mainloop()

