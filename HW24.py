import ebooklib
from ebooklib import epub
import json
import requests
import sys,os
from bs4 import BeautifulSoup
import zipfile
from ggtranslate import ggtranslate
import shutil
import glob

#測試用的電子書檔
bookname="Absolute_Value.epub"

bookUNzip = zipfile.ZipFile(bookname)
bookUNzip.extractall("temp")
bookUNzip.close

book = epub.read_epub(bookname)

for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        print('NAME : ', item.get_name())
        f=item.get_content()
        soup = BeautifulSoup(f, "html5lib")
        txt_dict={}
        p_count=0
        for t in soup.find_all('p'):
            t_text=str(t)
            if t_text.strip() != '' :
                p_count=p_count+1
                print(p_count)              
                
                #翻譯
                translator = ggtranslate.ggtranslate()             
                tran_txt=translator.translate(t_text, 'zh-tw')
                print(tran_txt)
                
                #產生字典檔
                txt_dict[t_text]=t_text+"<br>"+tran_txt
        #print(txt_dict)

        if p_count > 0:
            check_mame=[]
            check_mame=item.get_name()
            x_count=len(check_mame)
            
            #只要取出書檔html或xhtml檔名，不要子路徑
            for x in check_mame:
                if x=='/':
                    doc_name=check_mame[len(check_mame)-x_count:len(check_mame)]
                    break
                else:
                    x_count=x_count-1
                    
            for main_dir, sub_dir, allfile in os.walk("temp"):
                if doc_name in allfile:
                    nowfile_path=str(main_dir + "\\" + doc_name)
                    print (nowfile_path)
                    file_obj=open(nowfile_path, "r" , encoding = 'utf-8')   
                    content = file_obj.read()
                    file_obj.close()
                    
                    for x in txt_dict:
                        #翻譯後的內容替換上去
                        content = content.replace(x,txt_dict[x])
                    
                    file_obj=open(nowfile_path, "w" , encoding = 'utf-8')   
                    file_obj.write(content)
                    file_obj.close()
                

bookNew=zipfile.ZipFile('new_'+bookname,'w')
#os.chdir("temp")
for root, folders, files in os.walk("temp"):
    for sfile in files:
        aFile = os.path.join(root, sfile)
        bookNew.write(aFile)
bookNew.close()

shutil.rmtree("temp")    
print("完成")