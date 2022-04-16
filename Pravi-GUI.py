'''
Pravi - A Fully Automated System to Conduct Viva Exams
GUI
Developed by:

Satyajeet Kumar

## Pravi - A Fully Automated System to Conduct online viva exams

'''
## Importing required libraries
import speech_recognition as sr
import time
import pyttsx3
import random as r
import sys

## GUI Imports
from tkinter import *
import time

## Setting Root - Tkinter GUI
root = Tk()
root.geometry("600x500+400+100")
root.configure(background='green')
root.title('Pravi')
#root.resizable(True, True)


## Setting up voice engine for text to speech conversion
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty("rate", 130)

## Function to convert a text string to audio -- Pravi Speaks
def pravi_speaks(audio_string):
    Pravi_Text.config(text=str(audio_string))
    Pravi_Text.update()
    #print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()

## Function to take speech input of user and return a text string -- Pravi Listens
def pravi_listens(ask = False):
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        if ask:
            print(ask)
        Pravi_Text.config(text=Pravi_Text['text'] + "\n\nPlease answer after 2 seconds...")
        Pravi_Text.update()
        r.adjust_for_ambient_noise(source)
        #print("Please Speak After 2 Seconds...")
        audio = r.listen(source)
        voice_data = ''
        try: 
            Pravi_Text.config(text=Pravi_Text['text'] + "\n\nGetting it...")
            Pravi_Text.update()   
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            pravi_speaks('Sorry, I could not get that')
            return "could not hear that"
        except sr.RequestError:
            pravi_speaks('Sorry, my speech service is down, try again later.')
            return "speech servie down"
        print("Your answer: " + voice_data)
        return voice_data

## Fucntion to evaluate user's numerical answers and return marks -- Pravi Evaluates
def pravi_evaluates_num(ans, user_ans, n):
    marks = 0
    for i in range(n):
        if user_ans[i] == ans[i] :
            marks = marks+1
            
    return marks

## Function to evaluate user's string answers and return marks
def pravi_evaluates_string(ans, user_ans, n):
    marks = 0
    ##n = 3
    for i in range(n):
        if user_ans[i] == ans[i] :
            marks = marks+1
            
    return marks

## Function to give instructions
def give_instructions(name, n):
    instructions = "Okay " + name + ", So I'm here to ask you a few questions. I will be asking you " + str(2*n) + " questions, " + str(n) + " science questions, and " + str(n) + " math questions. You'll be given enough time to answer them, please answer loudly and clearly, if I don't understand your answer, I'll ask you again. In the end, you will get to know how many questions you get right. We will start, now. All the best!"
    pravi_speaks(instructions)
    
## Fuction to greet the user
def pravi_greets(n):
    pravi_speaks("Hey there, I am Pravi.")
    while(1):
        pravi_speaks("What's your name?")
        user_name = pravi_listens()
        if(user_name != "could not hear that" and user_name != "speech servie down" ): 
            break
    
    pravi_speaks("Hello "+ str(user_name) +". Nice to meet you!")
    time.sleep(0.5)
    give_instructions(str(user_name), n)


    
## Function to randomize a dictionary and return it
def randomize(dict):
    key_list = list(dict)
    r.shuffle(key_list)
    rand_dict = {}
    for key in key_list:
        rand_dict[key] = dict[key]
    return rand_dict

## Function to verify if Pravi heard what the user said
def verify_from_user(user_input):
    pravi_speaks("Was your answer "+ str(user_input) +"?")
    verified = str(pravi_listens())
    if( "yes" in verified or "yeah" in verified or "yup" in verified or 
       "yep" in verified or verified == "right" or "ya" in verified ):
        return 1
    elif ("no" in verified or"nah" in verified or "nope" in verified or 
       "naah" in verified or "noo" in verified or "na" in verified):
        return -1
    else:
        return 0
        

## Function to read two text files containing questions and answers, save them to a dictionary and return randomized dictionary
def get_qus_ans(qus_file, ans_file):
    qus_ans={}
    i=0
    ans_list = []
    ## Appending answers to ans_list
    with open(ans_file) as ans:
        for ans_line in ans:
            ans_list.append(ans_line.rstrip('\n'))
                            
    with open(qus_file) as f:
        for qus_line in f:
            qus_ans[qus_line.rstrip('\n')] = ans_list[i]
            i=i+1
    rand_qus_ans = randomize(qus_ans)
    return rand_qus_ans


## Function to conduct viva exam
def take_viva(ques, ans, n, sub):
    user_ans = []
    print("\n")
    ##n = 3
    for i in range(n):
        
        while(1):
            pravi_speaks(ques[i])
            user_input = pravi_listens()
            if(user_input != "could not hear that" and user_input != "speech servie down" ):
                break
        correctly_heard= verify_from_user(str(user_input))
        while(correctly_heard != 1):
            time.sleep(1)
            pravi_speaks("Oh no! I'll ask the question again, please answer loudly and clearly this time.")
            pravi_speaks(ques[i])
            user_input = pravi_listens()
            correctly_heard= verify_from_user(str(user_input))
            
        if(correctly_heard == 1):
            time.sleep(1)
            pravi_speaks("Great!")
            if(i!=(n-1)):
                pravi_speaks("Now, the next question!")
            user_ans.append((user_input.upper()))
                   
    if(sub=="math"):
        marks = pravi_evaluates_num(ans, user_ans, n)
    if(sub=="sci"):   
        marks = pravi_evaluates_string(ans, user_ans, n)
    return marks

    
## Function to start viva
def start_viva():
    n = 2
    pravi_greets(n)
    time.sleep(1)
    qus_ans_sci = get_qus_ans('src/qus_sci.txt','src/ans_sci.txt' ) ## Loading questions and their answers from text files
    ques_sci = []
    ans_sci  = []
    for i in qus_ans_sci:
        ques_sci.append(i) 
        ans_sci.append((qus_ans_sci[i].upper()))
    marks_sci = take_viva(ques_sci, ans_sci, n, sub="sci")
    time.sleep(1)
    pravi_speaks("Okay, so science questions are over. Now I'll ask you some math questions.")
    qus_ans_math = get_qus_ans('src/qus_math.txt','src/ans_math.txt' ) ## Loading questions and their answers from text files
    ques_math = []
    ans_math  = []
    for i in qus_ans_math:
        ques_math.append(i) 
        ans_math.append(qus_ans_math[i])
    marks_math = take_viva(ques_math, ans_math, n, sub = "math")
    pravi_speaks("You have got " + str(marks_sci+marks_math) + " correct out of " + str(2*n)+"!")


## Function to stop Pravi
def stop_pravi():
    sys.exit()

## Pravi Text Frame
Pravi_Frame = LabelFrame(root, text='  Pravi is speaking ...  ')
Pravi_Frame.pack(padx=5, pady=5)

Pravi_Text = Message(Pravi_Frame, text="", width='500', font=(
    "Helevetica", 10, "bold"), bg=root['bg'], fg="white")
Pravi_Text.pack(padx=5, pady=5)

## Stop Pravi
Button(root, text='Stop Pravi', command=stop_pravi,
    bg='red', fg='white').pack(pady=5)
## Start Viva again
Button(root, text='Start viva again', command=start_viva,
    bg='red', fg='white').pack(pady=5)

## Status Bar 
Status_Bar = Label(root, text='Pravi Working...',
                   relief=SUNKEN, anchor=W, bg=root['bg'])
Status_Bar.pack(side=BOTTOM, fill=X)

if __name__ == "__main__":
    start_viva()

root.mainloop()
