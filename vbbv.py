import speech_recognition as sr
import easyimap as e
import pyttsx3
import smtplib
from getpass4 import getpass
from email.message import EmailMessage


r = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


def speak(x):
    print(x)
    engine.say(x)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        a = "speak now"
        speak(a)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            s = "sorry could not recognize what you said"
            speak(s)


def receiverID():
    global rec
    rec = listen()
    if "slash at the rate" in rec:
        rec = rec.replace('slash at the rate', '@')
        rec = rec.replace(' ', '')
    speak("the emailID of the receiver is:")
    speak(rec)
    speak("do you want to re-enter your email id? If so say YES, else say NO")
    check = listen()
    if check == "no":
        print(rec)
        return rec
    else:
        speak("speak the receiverID again after the speak now command")
        receiverID()

def subject():
    global smsg
    smsg = listen()
    speak("the subject of your email is:")
    speak(smsg)
    speak("do you want to re-enter your subject? If so say YES, else say NO")
    check = listen()
    if check == "no":
        return smsg
    else:
        speak("speak the subject of your email again after the speak now command")
        subject()

def body():
    global bmsg
    bmsg = listen()
    speak("the body of your email is:")
    speak(bmsg)
    speak("do you want to re-enter the body of your email? If so say YES, else say NO")
    check = listen()
    if check == "no":
        return bmsg
    else:
        speak("speak the body of your email again after the speak now command")
        body()


def sendmail():
    email = EmailMessage()
    email['subject'] = smsg
    email['from'] = unm
    email['To'] = rec
    email.set_content(bmsg)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(unm, pwd)
    server.send_message(email)
    server.quit()

    b = "The email has been sent"
    speak(b)


def readmail():
    server = e.connect("imap.gmail.com", unm, pwd)
    server.listids()

    c = "please say the serial Number of the email you want to read starting from latest"
    speak(c)

    a = listen()

    b = int(a) - 1

    email = server.mail(server.listids()[b])

    speak("The email is from: ")
    speak(email.from_addr)
    speak("The subject of the email is")
    speak(email.title)
    speak(email.attachments)
    if not email.attachments:
        speak("there are no attachments to this email")
    speak("email date is ")
    speak(email.date)
    speak("The body of the email is:")
    speak(email.body)


m = "Welcome to voice controlled email services"
speak(m)


speak('enter your email address')
unm = input("Pleas enter your email ID:")
speak("enter your password")
pwd = getpass("please enter your password:")

while 1:
    x = "what do you want to do?"
    speak(x)

    x = "Speak SEND, to send email. Speak READ, to Read inbox. Speak EXIT, to Exit. "
    speak(x)

    ch = listen()

    if ch == 'send':
        speak("you have chosen to send an email")

        speak("Would you like to use voice controls for entering receiver's email ID? If so say YES, else say NO")
        t = listen()
        if t == "yes":

            speak("please speak the email address of the receiver")
            receiverID()

            speak("please speak the subject of your email")
            subject()

            speak("Please speak the body of your email")
            body()

            sendmail()
        else:
            speak("please enter receavers email address")
            rec = input("Please enter receiver's emailID:")
            speak("please speak the subject of your email")
            subject()

            speak("Please speak the body of your email")
            body()

            sendmail()

    elif ch == 'read':
        x = "you have chosen to read an email"
        speak(x)
        readmail()

    elif ch == 'exit':
        x = "You have chosen to exit, have a good day"
        speak(x)
        exit() 
    else:
        x = "Invalid choice, you said:"
        speak(x)
        speak(ch)
