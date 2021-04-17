import re
import pymorphy2

message_re = re.compile(r'<div class="text">\n(.*)') #регулярка для поиска сообщений
morph = pymorphy2.MorphAnalyzer()

def message_extracting(file_name, out_file): #вытаскивает тексты сообщений из html файлов, телеграм
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
        with open(out_file, 'w', encoding='utf-8') as f:
            for message in message_re.findall(text):
                f.write(message + '\n')

def predobrabotka(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for i in range(len(text)):
            text[i] = re.split(r"[\.,!\?\n\s]+", text[i]) #разделили сообщения на слова
            for j in range(len(text[i])):
                text[i][j] = morph.parse(text[i][j])[0].normal_form
    print(text)





