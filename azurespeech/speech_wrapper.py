import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

class  Speech_Wrapper:
    def __init__(self, speech_key: str, service_region: str, 
            recognition_language: str, mic_id: str, dict_mode_active: bool, callbackClass):
        
        self.speech_recognizer = None
        self.callbackClass = callbackClass
        self.conversation = {}

        # Setup Azure Speech Recognizer
        if mic_id is not None:
            audio_config = speechsdk.AudioConfig(device_name = mic_id)
        else:
            audio_config = None

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = recognition_language
        if (dict_mode_active == True):
            speech_config.enable_dictation()
            print("Dictiation Mode enabled.")
        
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        # Connect callbacks to the events fired by the speech recognizer
        self.speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.speech_recognizer.recognizing.connect(self.cb_recogonizing) # every utterance, even when recogn. is not finished
    
        self.speech_recognizer.recognized.connect(self.cb_recognized)
        self.speech_recognizer.canceled.connect(self.cb_cancelled)

        # stop continuous recognition on either session stopped or canceled events
        self.speech_recognizer.session_stopped.connect(self.stop_cb)
        self.speech_recognizer.canceled.connect(self.stop_cb)

        # Improve recognition accuracy with custom lists 
        self.update_grammar_list(self.speech_recognizer)
    
    def update_grammar_list(self, speech_recognizer):
        """
        Improves recognition accuracy with custom lists. Currently does not work correctly (Azure Bug)
        """
        phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(speech_recognizer)
        phrase_list_grammar.addPhrase("Hermo")


    def cb_recognized(self, evt):
        """callback for finshed recoginzed sentences. mostly gets called after a speaking pause"""
        #print("R: {}".format(evt.result.text))
        
        key = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.conversation[key] = evt.result.text
        #self.callback_UI.mytext_final.set(evt.result.text) ###
        self.callbackClass.result_text = evt.result.text
            
    def cb_recogonizing(self, evt):
        """callback for recoginzed sentences. Gets updated frequently but words change sometimes (due to /
        sentence context info"""
        #print("T: {}".format(evt.result.text))
                
        # self.callback_UI.mytext_live.set(evt.result.text) ###
        self.callbackClass.live_text = evt.result.text

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
        done = True


    def start_recognizing(self):
        """Class Method to start the real recognition process"""
        self.speech_recognizer.start_continuous_recognition_async()
        
    def stop_recognizing(self):
        """Class Method to stop the real recognition process"""
        self.speech_recognizer.stop_continuous_recognition_async()

