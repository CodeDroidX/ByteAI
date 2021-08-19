import json
import Levenshtein as lev
import string
import os
import zlib
name =  os.environ.get( "USERNAME" )
pname = "ByteAI"
from colorama import init, Fore
init(convert=True)
import time
print(Fore.RED + pname+" Запускается...")
start = time.time()
def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr
def json_add(entry, filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    data.update(entry)
    with open(filename.format(1), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
def learn_chat_keys(S):
    book = open(S, 'r', encoding='utf-8')
    r = book.read()
    bookstrings = r.split(".")
    for i in range(1,len(bookstrings),2):
        if i + 1 < len(bookstrings):
            data = [str.lower(bookstrings[i].translate(str.maketrans('', '', string.punctuation))).strip()]
            data.append(str.lower(bookstrings[i-1].translate(str.maketrans('', '', string.punctuation))).strip())
            #data = [bookstrings[i]]
            #data.append(bookstrings[i-1])
            key = long_substr(data)
            #print(bookstrings)
            #print(data)
            #print(long_substr(bookstrings))
            #print("Key = "+key)
            ks0 = data[0].split(key)
            ks1 = data[1].split(key)
            key0 = ks1[0].strip()
            key1 = ks0[0].strip()
            key2 = ks1[1].strip()
            key3 = ks0[1].strip()
            filename = 'Brain.json'
            if(key0 == "" and key3 == ""):
                entry = {key2: key1}
                #print(key2+"--"+key1)
                json_add(entry, filename)
            elif(key1 == "" and key2 == ""):
                entry = {key0: key3}
                #print(key0+"--"+key3)
                json_add(entry, filename)
            else:
                entry = {key0: key1}
                #print(key0+"--"+key1)
                json_add(entry, filename)
                entry = {key2: key3}
                #print(key2+"--"+key3)
                json_add(entry, filename)
def learn_chat(S):
    book = open(S, 'r', encoding='utf-8')
    r = book.read()
    bookstrings = r.split("- ")
    for i in range(1,len(bookstrings),2):
        if i + 1 < len(bookstrings):
            data = [str.lower(bookstrings[i]).strip()]
            data.append(str.lower(bookstrings[i-1]).strip())
            filename = 'Brain.json'
            entry = {data[1]: data[0]}
            json_add(entry, filename)
def answer(S, filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    akeys = data.keys()
    mindist = 100
    minkey = ""
    for ii in akeys:
        dist = lev.distance(ii,S)
        if mindist > dist:
            minkey = ii
            mindist = dist
    toreturn = [data[minkey]]
    toreturn.append(mindist)
    toreturn.append(minkey)
    return(toreturn)
fn = 'food.txt'
learn_chat_keys(fn)
t = str(round(time.time()-start,3))
print(Fore.GREEN + pname+" запустился за "+t+" sec)")
ac = 0
while True:
    if int(ac) == -1:
        print(Fore.GREEN)
        print("Learned "+antiquest+" for "+lastquest)
        entry = {lastquest: antiquest}
        #print(key2+"--"+key3)
        json_add(entry, 'Brain.json')
    lastquest = quest
    if int(ac) >= 10:
        print(Fore.GREEN)
        print("Что бы ты ответил на> "+quest+" ?")
        antiquest = input(pname+" Learning > ")
        entry = {quest: antiquest}
        #print(key2+"--"+key3)
        json_add(entry, 'Brain.json')
    print(Fore.YELLOW)
    quest = input(name+"> ")
    print()
    start = time.time()
    questsplit = quest.split("^")

    x = answer(quest,'Brain.json')
    a = x[0]
    if a == "":
        a = "Не понял тебя("
    else:
        a = str.capitalize(a+".")
    ac = str(x[1])
    if len(questsplit) > 1:
        ac = -1
        antiquest = questsplit[0]
        quest = questsplit[1]
    else:
        quest = questsplit[0]
    ak = str(zlib.crc32(x[2].encode('utf-8')))[:5]
    #ac = ac/len(ak)
    #ac = ac*100
    #ac = str(100 - int(ac))
    t = str(time.time()-start)
    print(Fore.CYAN + pname+"> "+str(a)+"                        Неуверенность в ответе "+str(ac)+", time="+str(t)+" sec, совпавший ключ - "+str(ak))


        
