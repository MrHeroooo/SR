#tạo file text theo yêu câu 1 dòng tên file rôi dên 1 dòng nôi dung text
import sounddevice as sd
from scipy.io.wavfile import write
import os
import nltk
#nltk.download('punkt')
from tkinter import *

to_record_text = open(r'C:\Users\Administrator.PC\Desktop\Hope\1920II\XLTN\D\Paper.txt', encoding ="utf-8").read()
text_array = nltk.sent_tokenize(to_record_text)


with open(r'C:\Users\Administrator.PC\Desktop\Hope\1920II\XLTN\D\name.txt','w', encoding="utf-8")  as file:
    count = 0
    for ele  in text_array :
    
        file.write(str(count ) + '.' + "wave\n") 
        
        file.write(ele+ '\n')
        count = count+1
    file.close()
