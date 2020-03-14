from tkinter import *
import theUI


if __name__ == '__main__':
    # Initialize Window
    root = Tk()
    win = theUI.Window(master=root, speech_key="KEY", 
                service_region="westeurope")

