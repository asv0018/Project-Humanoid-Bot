import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition as sr
import pyttsx3

#  NIRAN you should change the below credentials in order to use your dialogflow account!. please do the necessorry
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'Assets/humanoid-bot-qxmcwn-c1ebdc7db876.json' # it is there in this folder inside the currrent working directory
DIALOGFLOW_PROJECT_ID = 'humanoid-bot-qxmcwn'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
text_to_be_analyzed = ""


def SpeechToText():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[I AM LISTENING...]")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        recognisedtext = str(r.recognize_google(audio))
        print("[YOU SAID] " + recognisedtext)
        dialogflowresult = DialogflowSocket(recognisedtext)
        print("[I REPLIED] " + dialogflowresult)
        TextToSpeech(dialogflowresult)
    except sr.UnknownValueError:
        print("NO SPEECH HEARD!")
    except sr.RequestError as e:
        print("Could not process because of the reason : {0}".format(e))

def TextToSpeech(text):
    engine = pyttsx3.init()  # object creation
    engine.setProperty('rate', 210)  # setting up new voice rate
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def DialogflowSocket(queryText):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=queryText, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    #print("Query text:", response.query_result.query_text)
    #print("Detected intent:", response.query_result.intent.display_name)
    #print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    #print("Fulfillment text:", response.query_result.fulfillment_text)
    return str(response.query_result.fulfillment_text)


