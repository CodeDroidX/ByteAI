import time
from colorama import init, Fore
init(convert=True)
start = time.time()
import json
import Levenshtein as lev
import string
import os
import zlib
import pyttsx3
import os
import fnmatch
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator
translator = Translator()
from Brains import ActionBrain as ab
log = open("Logs\Work.log", "a+")
log.seek(0)
os.system('cls' if os.name == 'nt' else 'clear')
engine = pyttsx3.init()
name =  os.environ.get( "USERNAME" )
pname = "ByteAI"
print(Fore.RED + pname+" Запускается...")
print(Fore.CYAN)
engine.setProperty('voice', "ru")
engine.setProperty('rate', 110)
engine.setProperty('123', 30)
def Log(Text):
    log.write(Text + "\n")
    log.flush()
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

def merge_brains(mainfilename, filename):
    print(Fore.YELLOW)
    print("Слияние "+ filename +" c "+mainfilename)
    with open(mainfilename, "r", encoding='utf-8') as file:
        data = json.load(file)
    with open(filename, "r", encoding='utf-8') as file:
        merge_data = json.load(file)
    data.update(merge_data)
    with open(mainfilename.format(1), 'w', encoding='utf-8') as file:
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
            filename = mainbrainname
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




def say_x(S):
    if lan != "":
        S = translator.translate(S, dest=lan).text
    if(True):
        engine.save_to_file(S, 'speech.wav')
        engine.runAndWait()
        sound = AudioSegment.from_file('speech.wav', format="wav")
        os.remove('speech.wav')

        # shift the pitch up by half an octave (speed will increase proportionally)
        octaves = 0.6

        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

        # keep the same samples but tell the computer they ought to be played at the 
        # new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
        hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

        # now we just convert it to a common sample rate (44.1k - standard audio CD) to 
        # make sure it works in regular audio players. Other than potentially losing audio quality (if
        # you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
        hipitch_sound = hipitch_sound.set_frame_rate(44100)

        #Play pitch changed sound
        play(hipitch_sound)





def learn_chat(S):
    book = open(S, 'r', encoding='utf-8')
    r = book.read()
    bookstrings = r.split("- ")
    for i in range(1,len(bookstrings),2):
        if i + 1 < len(bookstrings):
            data = [str.lower(bookstrings[i]).strip()]
            data.append(str.lower(bookstrings[i-1]).strip())
            filename = mainbrainname
            entry = {data[1]: data[0]}
            json_add(entry, filename)
opti = "Brains\\Brain.optibrain"
mainbrainname = "Brains\\Brain.speakbrain"
brains = fnmatch.filter(os.listdir("Brains\\"), "*.speakbrain")

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
    with open(opti, "r", encoding='utf-8') as file:
        datao = json.load(file)
    try:
        datao[minkey] = str(int(datao[minkey]) + 1)
    except KeyError:
        ab.GetSortBrain(mainbrainname,opti)
        with open(opti, "r", encoding='utf-8') as file:
            datao = json.load(file)
        datao[minkey] = str(int(datao[minkey]) + 1)
    with open(opti.format(1), 'w', encoding='utf-8') as file:
        json.dump(datao, file, ensure_ascii=False)
    toreturn = [data[minkey]]
    toreturn.append(mindist)
    toreturn.append(minkey)
    return(toreturn)


braincount = len(brains)
if braincount > 1:
    print(Fore.MAGENTA + "Найдено " + str(braincount) +" brains: ")
    print(brains)
    for i in brains:
        if "Brains\\"+i == mainbrainname:
            pass
        else:
            merge_brains(mainbrainname, "Brains\\"+i)
fn = 'food.txt'
learn_chat_keys(fn)
t = str(round(time.time()-start,3))
print(Fore.RED)
print(pname+" запустился за "+t+" sec)")
print(Fore.CYAN)
voices = engine.getProperty('voices')
for voice in voices:
    print("Голос: %s" % voice.name)
    print("\n")
print(Fore.GREEN)
lan = input(pname+": Выберите любой язык перевода озвучки (можете оставить поле пустым, тогда переводчик не будет работать). Например: Ja, Fr, En, Ch > ")
v = input(pname+": Выберите номер голоса озвучки. Например 1> ")

engine.setProperty("voice", voices[int(v)-1].id)
print(Fore.YELLOW)
vv = input(pname+": Голосовой ввод? y/n> ")
antiqlimit = 10
if (input(pname+": Разрешить обучение? y/n> ")=="n"):
    antiqlimit = 100
if vv == "y":
    voiceinp=True
    import speech_recognition as sr
    r = sr.Recognizer()
    def voice_input(txt):
        isvoicetext = False
        while(isvoicetext!=True):
            with sr.Microphone() as source:
                print(txt,end='')
                audio = r.listen(source)
            try:
                ret= r.recognize_google(audio, language="ru-RU")
                #ret= r.recognize_google(audio)
                print(ret)
                isvoicetext = True
                return(ret)
            except sr.UnknownValueError:
                print("Речь не распознана(")
            except sr.RequestError as e:
                print("Ошибка сервиса распознания речи; {0}".format(e))
else:
    voiceinp=False
os.system('cls' if os.name == 'nt' else 'clear')
print(Fore.RED + "Диалог "+pname+":")
ac = 0
quest = ""
while True:

    if int(ac) == -1:
        print(Fore.GREEN)
        say_x("Обучен ответ "+antiquest+" на "+lastquest)
        print("Learned "+antiquest+" for "+lastquest)
        entry = {lastquest: antiquest}
        #print(key2+"--"+key3)
        json_add(entry, mainbrainname)
    lastquest = quest
    if int(ac) >= antiqlimit:
        print(Fore.GREEN)
        print("Что бы ты ответил на> "+quest+" ?")
        say_x("Что бы ты ответил на "+quest+" ?")
        if voiceinp:
            antiquest = voice_input(pname+" Learning > ").lower()
        else:
            antiquest = input(pname+" Learning > ").lower()
        if antiquest != "отмена" and antiquest != "cancel" and antiquest != "отменить" and antiquest != "отклонить":
            entry = {quest: antiquest}
            #print(key2+"--"+key3)
            json_add(entry, mainbrainname)
    print(Fore.YELLOW)
    if voiceinp:
        quest = voice_input(name+"> ").lower()
    else:
        quest = input(name+"> ").lower()
    print()
    start = time.time()
    questsplit = quest.split("^")

    with open('Brains\\Brain.funcbrain', "r", encoding='utf-8') as file:
        data = json.load(file)
    akeys = data.keys()
    funcac = 0
    iс = 0

    for i in akeys:
        for iq in quest.split(' '):
            if i.find(iq) > -1:
                iс = iс + 1
                globaliq = iq
        if iс > 0:
            for ii in i.split(", "):
                if quest.find(ii) > -1:
                    funcac = funcac + 1
                    print(Fore.MAGENTA)
                    eval(data[i])
                    print(Fore.YELLOW)
    if funcac == 0:
        x = answer(quest,mainbrainname)
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
        Log(quest + "-" +str(a))
        t = str(round(time.time()-start,3))
        if antiqlimit == 10:
            print(Fore.CYAN + pname+"> "+str(a)+"                        Неуверенность в ответе "+str(ac)+", time="+str(t)+" sec, совпавший ключ - "+str(ak))
        else:
            print(Fore.CYAN + pname+"> "+str(a))
        say_x(str(a))




        
