# The Writer
A Python application that excerpts the output from your sound card. So you get on scree text from all speech related stuff of your speakers.
I wrote this application for a hearing impaired colleague of mine so that he could follow our Skype Meetings better. 

## Demo

## Features


## Installation
You need an Azure account for billing. 

1. Create a [Azure cognitive speech ressource](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started) 
1. Go to the created ressource in the Azure Portal and note the API Key.
1. You need to have Python 3 installed [(manual)](https://phoenixnap.com/kb/how-to-install-python-3-windows)
1. Do a `pip install azure-cognitiveservices-speech`
1. Setup the Virtual Audio Cable (VAC) software, which captures your speaker sounds as microphone input
    * https://www.vb-audio.com/Cable/
    * [Youtube Configuration Manual](https://www.youtube.com/watch?v=ad30G5oBHtg&feature=emb_logo)
    * Donate if you like the software!
1. Open up main.py in text editor, edit the API Key and ressource location.
1. Start main.py (e.g. via batch file  "python main.py")
