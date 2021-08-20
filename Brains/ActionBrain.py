import webbrowser
import os
def OpenApp(q,k):
    quest = q.split(k, 1)
    os.system("start "+quest[1].strip())
def Shutd():
    os.system('shutdown /s')
def Shutdoff():
    os.system('shutdown /a')
def OpenExit():
    exit()
def OpenInternet(q,k):
    quest = q.split(k, 1)
    if len(quest[1].strip().split(".")) == 1:
        q = quest[1].strip()+".com"
    else:
        q = quest[1].strip()
    webbrowser.open('https://'+q, new=1)