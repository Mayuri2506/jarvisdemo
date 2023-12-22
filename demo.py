import sys
import time
import pyautogui
import pyjokes
import pyttsx3
import speech_recognition as sr
import pyaudio
import PyPDF2
import datetime
import os
import cv2
import webbrowser
from requests import get
import wikipedia
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from email.mime.base import MIMEBase
import email
import geocoder

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# voice to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")

    except Exception as e:
        speak("Say that again please")
        return "none"
    return query


# to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Luna. Please tell me how can i help you")


# to fetch current location
def get_current_location():
    # Get the user's current location based on IP address
    location = geocoder.ip('me')
    return location


# take screenshot
def take_screenshot_and_save():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Define the file name using the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"screenshot_{timestamp}.png"

    # Save the screenshot to the desktop
    desktop_path = "C:\\Users\\Mayuri\\Pictures\\Screenshots"  # Change this path if your desktop is in a different location
    file_path = f"{desktop_path}/{file_name}"

    screenshot.save(file_path)
    speak(f"Screenshot saved to: {file_path}")


def find_file(file_name):
    for drive in range(ord('A'), ord('Z') + 1):
        drive_letter = chr(drive) + ":"
        try:
            for root, dirs, files in os.walk(drive_letter):
                if file_name in files:
                    return os.path.join(root, file_name)
        except PermissionError:
            # Handle PermissionError, as some drives may be inaccessible
            pass

    return None


def open_pdf(pdf_file_path):
    if pdf_file_path is not None:
        # Open the PDF file using the default PDF viewer
        webbrowser.open(pdf_file_path)
        print(f"Opening PDF file: {pdf_file_path}")
    else:
        print("Error: PDF file not found in the system.")


# to send email
def sendEmail():
    sender_email = "manjarekarmayu25@gmail.com"
    app_password = "ezqb pkfk cuar aayh"

    # Get recipient email address from user input
    speak("Pleas enter the recipient email address")
    recipient_email = input("Enter the recipient's email address: ")

    # Create the email message
    speak("What is the subject of email")
    subject = takecommand().lower()
    speak("What is the body of email")
    body = takecommand().lower()
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server (in this case, Gmail's SMTP server)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to your email account using the App Password
    server.login(sender_email, app_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, message.as_string())

    # Quit the server
    server.quit()


# to send file via email
def send_fileemail(receiver_email, file_name):
    sender_email = "manjarekarmayu25@gmail.com"  # Replace with your email
    app_key = "ezqb pkfk cuar aayh"  # Replace with your app-specific key

    file_path = find_file(file_name)

    if file_path is None:
        print(f"File '{file_name}' not found.")
        return

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "File Sharing"

    # Attach the body to the email
    message.attach(MIMEText("Please find the attached file.", "plain"))

    # Attach the file to the email
    attachment = open(file_path, "rb")
    base = MIMEBase("application", "octet-stream")
    base.set_payload((attachment).read())
    email.encoders.encode_base64(base)
    base.add_header("Content-Disposition", f"attachment; filename={file_name}")
    message.attach(base)

    # Connect to the SMTP server
    smtp_server = "smtp.gmail.com"  # Update this based on your email provider
    smtp_port = 587  # Update this based on your email provider

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()

        # Log in to your email account using app-specific key
        server.login(sender_email, app_key)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully.")


# to fetch news using newsapi
def news():
    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=3cd88dd06b794c5b8338fdff94a0f0f2"
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is:{head[i]}")


def start():
    wish()
    while True:
        if 1:
            query = takecommand().lower()
            # logic building for task
            if "open notepad" and "notepad" in query:
                npath = "C:\\Windows\\notepad.exe"
                os.startfile(npath)

            elif "what's the time" in query:
                tt = time.strftime('%I:%M %p')
                speak(f"The time is {tt}")

            elif "what is my current location" in query:
                speak("please wait,let me check")
                currenloc = get_current_location()
                speak(f"your location is {currenloc.city} city in {currenloc.country} ")

            elif "take a screenshot" in query:
                take_screenshot_and_save()

            elif "opem command prompt" in query:
                os.system("start cmd")
            elif "open camera" in query:
                cam = cv2.VideoCapture(0)
                while True:
                    ret, img = cam.read()
                    cv2.imshow('webcam', img)
                    if cv2.waitKey(5000) & 0xFF == ord('q'):
                        break
                    if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                        break
                cam.release()
                cv2.destroyAllWindows()

            elif "open pdf file" in query:
                # Input the PDF file name
                speak("please enter the file name you want to open with .pdf extension")
                user_input_file_name = input("Enter the PDF file name to open (with extension (.pdf)): ")

                # Search for and open the specified PDF file
                pdf_file_path = find_file(user_input_file_name)
                speak(f"opened the pdf file {user_input_file_name}")
                # Open the PDF file if found
                open_pdf(pdf_file_path)
            elif "open spotify" in query:
                spotify_url = "https://open.spotify.com/"
                webbrowser.open(spotify_url)
            elif "ip address" in query:
                ip = get("https://api.ipify.org").text
                speak(f"Your IP address is {ip}")
            elif "wikipedia" in query:
                speak("What should i search on wikipedia")
                queryy = takecommand().lower()
                results = wikipedia.summary(queryy, sentences=2)
                speak("according to wikipedia...")
                speak(results)
                print(results)
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
            elif "open google" in query:
                webbrowser.open("www.google.com")
            elif "send a whatsapp message" in query:
                speak("Tell me the contact number to send message:")
                contact = int(input("Enter the contact number (with country code):"))
                speak("what is the content of message")
                msgcont = takecommand().lower()
                kit.sendwhatmsg_instantly(contact, msgcont, 15, 3)
                speak("Message has been sent successfully!!")
            elif "play song on youtube" in query:

                speak("What should i play on youtube")
                playcont = takecommand().lower()
                kit.playonyt(playcont)
            elif "send email" in query:
                try:
                    sendEmail()
                    speak("Email has been sent")
                except Exception as e:
                    print(e)
                    speak("Sorry!I am unable to send email")

            elif "send file via email" in query:
                speak("please enter the recipient's email address")
                receiver_email = input("Enter the recipient's email address: ")
                speak("please enter the file name with extension")
                file_name = input("Enter the file name with extension: ")
                send_fileemail(receiver_email, file_name)
                speak("file has been sent via email")

            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "tell me news" in query:
                speak("Please wait ,fetching the latest news")
                news()

            elif "switch Window" in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in query:
                os.system("shutdown /h")
            elif "no thanks" in query:
                speak("Thanks for using me")
                sys.exit()

            speak("Do You have any other work")

if __name__ == "__main__":
    start()
