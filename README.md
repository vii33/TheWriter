# TheWriter

Python application that excerpts the output from your sound card. So you get the text from all speech of your speakers.
I wrote this for a hearing impaired colleague of mine so that he could follow our Skype Meetings better. 

# Demo

# Features


# Installation

## Cloud Setup
You need an Azure account for billing. 

1. Create a [Azure cognitive speech ressource](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started) 
1. Go to the created ressource in the Azure Portal and note the API Key.

## Virtual Audio Cable Setup (optional)
1. Setup the Virtual Audio Cable (VAC) software, which captures your speaker sounds as microphone input
    * https://www.vb-audio.com/Cable/
    * [Youtube Configuration Manual](https://www.youtube.com/watch?v=ad30G5oBHtg&feature=emb_logo)
    * Donate if you like the software!


## Python Setup
Required packages (Python 3):
azure.cognitiveservices.speech
from datetime import datetime
from tkinter
import pprint



1. Open up main.py in text editor, edit the API Key and ressource location.
1. Start main.py (e.g. via batch file  "python main.py")

# Open Points

* Automatic detection of language. Currently (02/2020) the detected language is fixed, i.e. you cannot swtich on the fly between to languages (this would be perfect): [Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-automatic-language-detection?pivots=programming-language-python
)
* Use Logging Framework