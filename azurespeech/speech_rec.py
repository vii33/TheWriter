import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
#import time    # used for pretty cmdline output
#from _thread import start_new_thread
#from os import system   #used for pretty cmdline output


# Manual: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/67bd7c502d5a859fd981227ce1cf60f51cd5e112/samples/python/console/speech_sample.py#L196

#AUTO DETECTION OF LANG (not avail for python currently)
# in sharp doesnt work very well on live changing languages (02/2020)
#https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-automatic-language-detection?pivots=programming-language-csharp


def text_splitter(data: str, split_num: int, result: list):
    tmp = data.split(maxsplit=split_num)
    #print("tmp: {}".format(tmp))
    
    if len(tmp) > split_num:
        # Store triplets
        result.append(tmp[0:split_num])
        # recursion
        #print("kkk")
        text_splitter(tmp[split_num], split_num, result) # potential bug if more elements then splitnum
        #print("recursion.end1 -")
        return result
    else:
        #less then splitnum elements: append rest
        #print("lll")
        result.append(tmp)
        #print("recursion.end2 -")
        return result

def text_printer (dataarray: str):
    system('cls') 
    for i in range(len(dataarray)):
        print(" ".join(dataarray[i]))

def pretty_print(evt_text: str):
    result = []
    result = text_splitter(evt_text, 5, result)
    #print("result: {}".format(result))
    text_printer(result)




class  Speech_Rec:
    def __init__(self, speech_key: str, service_region: str, 
            recognition_language: str, callbackUI):
        
        self.speech_recognizer = None
        self.callback_UI = callbackUI
        self.conversation = {}

        # Setup Azure Speech Recognizer
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language=recognition_language
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        
        # Connect callbacks to the events fired by the speech recognizer
        self.speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.speech_recognizer.recognizing.connect(self.cb_recogonizing) # every utterance, even when recogn. is not finished
    
        self.speech_recognizer.recognized.connect(self.cb_recognized)
        self.speech_recognizer.canceled.connect(self.cb_cancelled)

        # stop continuous recognition on either session stopped or canceled events
        self.speech_recognizer.session_stopped.connect(self.stop_cb)
        self.speech_recognizer.canceled.connect(self.stop_cb)


    def cb_recognized(self, evt):
        """callback for finshed recoginzed sentences. mostly gets called after a speaking pause"""
        print("R: {}".format(evt.result.text))
        
        key = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.conversation[key] = evt.result.text
        self.callback_UI.mytext_final.set(evt.result.text)
            
    def cb_recogonizing(self, evt):
        """callback for recoginzed sentences. Gets updated frequently but words change sometimes (due to /
        sentence context info"""
        print("T: {}".format(evt.result.text))
        #pretty_print(evt.result.text)
                
        self.callback_UI.mytext_live.set(evt.result.text)
        

    def cb_cancelled(self, evt):
        """Callback when continous recogntion is cancelled"""
        cancellation_details = evt.result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    done = False
    def stop_cb(self, evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        #nonlocal done   # from the MS example. doesn't work
        done = True


    def start_recognizing(self):
        """Class Method to start the real recognition process"""
        self.speech_recognizer.start_continuous_recognition_async()
        
    def stop_recognizing(self):
        """Class Method to stop the real recognition process"""
        self.speech_recognizer.stop_continuous_recognition_async()

