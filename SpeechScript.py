import speech_recognition as sr
from random import *
import UserWrittenModules.MultiprocessingFunctions as multi
check_words = ["hello radar","hello Radhika","hi radar","hello Radha","hey Radhika","hey radar","heda","Irada","Prada"]
initial_response = ["hello man!,whats going on","hey!,what do want to know from me","namaskar, how can i help you","hoi,how can i be a help to you?"]
print("[INFO] |COMMUNICATION FEATURE IS ENABLED FOR 'WANG REDA'.")
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recognisedtext = str(r.recognize_google(audio))
        if recognisedtext not in check_words:
            print("[INFO] |REDA DO NOT RESPONDS AS SHE THINKS YOU SAID : "+recognisedtext)
        if recognisedtext in check_words:
            print("[REDA WAKES UP]")
            multi.MakeAwareness(initial_response[randint(0, 3)])
            print("[IF YOU DONT SPEAK >> REDA SLEEPS]")
            count = 0
            while True:
                R = sr.Recognizer()
                with sr.Microphone() as source:
                    R.adjust_for_ambient_noise(source)
                    audio = R.listen(source)
                try:
                    recognisedtext = str(R.recognize_google(audio))
                    print("[YOUR RESPONSE] >> " + recognisedtext)
                    dialogflowresult = multi.DialogflowSocket(recognisedtext)
                    print("[REDA'S  REPLY] >> " + dialogflowresult)
                    multi.TextToSpeech(dialogflowresult)
                    count = 0
                except sr.UnknownValueError:
                    count+=1
                    if count > 2:
                        print("[REDA SLEEPS]")
                        break
                except sr.RequestError as e:
                    print("Could not process because of the reason : {0}".format(e))
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print("Could not process because of the reason : {0}".format(e))
