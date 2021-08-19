import json
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
book = open('food.txt', 'r', encoding='utf-8')
r = book.read()
bookstrings = r.split(".")
for i in range(1,len(bookstrings),2):
    if i + 1 < len(bookstrings):
        data = [bookstrings[i]]
        data.append(bookstrings[i-1])
        key = long_substr(data)
        print(bookstrings)
        print(data)
        print(long_substr(bookstrings))
        print("Key = "+key)
        ks0 = data[0].split(key)
        ks1 = data[1].split(key)
        key0 = ks1[0].strip()
        key1 = ks0[0].strip()
        key2 = ks1[1].strip()
        key3 = ks0[1].strip()
        print(key0+"==="+key1)
        print(key2+"==="+key3)
        filename = 'Brain.json'
        entry = {key0: key1}
        json_add(entry, filename)
        entry = {key2: key3}
        json_add(entry, filename)

        
