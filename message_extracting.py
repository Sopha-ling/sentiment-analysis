import re
import pymorphy2
import csv
from statistics import mean

message_re = re.compile(r'<div class="text">\n(.*)') #регулярка для поиска сообщений
replace_re = re.compile(r'(<br>|&quot;)')

morph = pymorphy2.MorphAnalyzer()

def message_extracting(file_name, out_file): #вытаскивает тексты сообщений из html файлов, телеграм
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
        with open(out_file, 'w', encoding='utf-8') as f:
            for message in message_re.findall(text):
                f.write(message + '\n')
    return out_file

def predobrabotka(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for i in range(len(text)):
            text[i] = re.split(r"[\.,!\?\n\s]+", text[i]) #разделили сообщения на слова
            for j in range(len(text[i])):
                if replace_re.search(text[i][j]):
                    text[i][j] = replace_re.sub(text[i][j], ' ')
                text[i][j] = morph.parse(text[i][j])[0].normal_form
        return text

html_file = input('Введите имя файла: ')
lemmatised_messages = predobrabotka(message_extracting(html_file, 'outer.txt')) #список сообщений

with open('emo_dict.csv', encoding='utf-8') as f:
    data = list(csv.DictReader(f, delimiter=';'))
    for m in range(len(lemmatised_messages)): #идём по сообщениям
        for w in range(len(lemmatised_messages[m])):#идём по словам в сообщении
            for i in data:  # идём по словарю
                if lemmatised_messages[m][w] == i['term']:
                    freq = 1
                    with open('freqrnc2011.csv', encoding='utf-8') as t:
                        data_1 = list(csv.DictReader(f, delimiter='\t'))
                        for j in data_1:
                            print(j)
                            if lemmatised_messages[m][w] == j['Lemma']:
                                freq = j['Freq(ipm)']
                                print(lemmatised_messages[m][w], freq)
                    lemmatised_messages[m][w] = float(i['value']) / freq
            if type(lemmatised_messages[m][w]) == str:
                lemmatised_messages[m][w] = 0.0

if input('Учитывать слова с нулевым коэффициентом тональности? Пожалуйста, ответьте "да" или "нет" ') == "да":
    for m in range(len(lemmatised_messages)):
        lemmatised_messages[m] = mean(lemmatised_messages[m])
else:
    for m in range(len(lemmatised_messages)):
        for w in range(len(lemmatised_messages[m])):
            while 0.0 in lemmatised_messages[m]:
                lemmatised_messages[m].remove(0.0)
    print(lemmatised_messages)
    if input('Учитывать нейтральные слова? Пожалуйста, ответьте "да" или "нет" ') == "да":
        for m in range(len(lemmatised_messages)):
            lemmatised_messages[m] = mean(lemmatised_messages[m])





