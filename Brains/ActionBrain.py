import webbrowser
import os
import json
def json_add(entry, filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    data.update(entry)
    with open(filename.format(1), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

def OpenApp(q,k):
    quest = q.split(k, 1)
    os.system("start "+quest[1].strip())

def Shutd():
    os.system('shutdown /s')

def Shutdoff():
    os.system('shutdown /a')

def OpenExit():
    exit()

def Teach(q,k,mainbrainname,lastquest):
    #mainbrainname = mainbrainname.split("\\")[1]
    antiquest = q.split(k, 1)[1].strip()
    entry = {lastquest: antiquest}
    json_add(entry, mainbrainname)
    print("Learned "+lastquest+" for "+antiquest)

def OpenInternet(q,k):
    quest = q.split(k, 1)
    if len(quest[1].strip().split(".")) == 1:
        q = quest[1].strip()+".com"
    else:
        q = quest[1].strip()
    webbrowser.open('https://'+q, new=1)