import webbrowser
import os
import json
import Levenshtein as lev

def in_dict(key, dict):
    return key in dict
def json_add(entry, filename):
    with open(filename, "r", encoding='utf-8') as file:
        jdata = json.load(file)
    jdata.update(entry)
    with open(filename.format(1), 'w', encoding='utf-8') as file:
        json.dump(jdata, file, ensure_ascii=False)
        file.flush()

def OpenApp(q,k):
    quest = q.split(k, 1)
    print("Runned "+quest[1].strip())
    os.system("start "+quest[1].strip())

def Shutd():
    print("PC off request ")
    os.system('shutdown /s')

def Shutdoff():
    print("PC off canceled ")
    os.system('shutdown /a')

def OpenExit():
    print("Exit ")
    exit()

def GetSortBrain(filename,opti):
    ii = 0

    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    with open(opti, "r", encoding='utf-8') as file:
        dataop = json.load(file)
    for i in data.keys():
        if (in_dict(i, dataop) != True):
            print("Add - "+i)
            entry = {i: "0"}
            json_add(entry, opti)
    with open(opti, "r", encoding='utf-8') as file:
        dataop = json.load(file)
    dataiter = dataop.keys()
    for i in list(dataiter):
        if (in_dict(i, data) != True):
            print("Del - "+i)
            del dataop[i]
    with open(opti.format(1), 'w', encoding='utf-8') as file:
        json.dump(dataop, file, ensure_ascii=False)

    with open(opti, "r", encoding='utf-8') as file:
        dataop = json.load(file)

    sortop = sorted(dataop.items(), key=lambda x: int(x[1]), reverse=True)
    import collections
    sorted_dict = collections.OrderedDict(sortop)
    sortop = sorted_dict
    with open(opti.format(1), 'w', encoding='utf-8') as file:
        json.dump(sortop, file, ensure_ascii=False)
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    with open(opti, "r", encoding='utf-8') as file:
        dataop = json.load(file)
    with open(filename.format(1), 'w', encoding='utf-8') as file:
        print("Brain rebuild...")
        json.dump({}, file, ensure_ascii=False)
    for i in dataop.keys():
        entry = {i: data[i]}
        json_add(entry, filename)
    print("Brain rebuilded!")
            
    
def Teach(q,k,mainbrainname,lastquest):
    #mainbrainname = mainbrainname.split("\\")[1]
    if (q.split(k, 1)[0].strip() == ""):
        lastquest = q.split(k, 1)[0].strip()
    antiquest = q.split(k, 1)[1].strip()
    entry = {lastquest: antiquest}
    json_add(entry, mainbrainname)
    print("Learned "+antiquest+" for "+lastquest)

def OpenInternet(q,k):
    quest = q.split(k, 1)
    if len(quest[1].strip().split(".")) == 1:
        q = quest[1].strip()+".com"
    else:
        q = quest[1].strip()
    print("Web "+q)
    webbrowser.open('https://'+q, new=1)