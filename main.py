import sys, getopt
from tkinter import *
import theUI


def main(argv):

    SPEECH_KEY = "KEY"
    SERVICE_REGION = "westeurope"

    try:
        opts, args = getopt.getopt(argv,"k:r:")
    except getopt.GetoptError:
        print ('main.py -k <AZURE_SPEECH_KEY> -r <AZURE_SERVICE_REGION>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -k <AZURE_SPEECH_KEY> -r <AZURE_SERVICE_REGION>')
            sys.exit()
        elif opt in ("-k", "--k"):
            SPEECH_KEY = arg
        elif opt in ("-r", "--r"):
            SERVICE_REGION = arg
        else:
            assert False, "unhandled option"

    # Initialize Window
    root = Tk()
    win = theUI.Window(master=root, speech_key=SPEECH_KEY, 
                service_region=SERVICE_REGION)


if __name__ == "__main__":
   main(sys.argv[1:])