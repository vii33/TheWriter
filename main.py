from tkinter import *
import theUI

# Individual Settings
SPEECH_KEY = "KEY"
SERVICE_REGION = "westeurope"

if __name__ == '__main__':
    # Initialize Window
    root = Tk()
    win = theUI.Window(master=root, speech_key=SPEECH_KEY, 
                service_region=SERVICE_REGION)

