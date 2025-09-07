import os
import string
from time import sleep
import requests
import random
from bs4 import BeautifulSoup as Soup
from dotenv import dotenv_values, load_dotenv


def main():
    userAgent:string = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"

    # imgSource:string = "https://media.naked-womans.icu/uploads/2019/05/1533_1.jpg"
    
    # img = requests.get(imgSource)
    # out = open("../img.jpg","wb")
    # out.write(img.content)
    # out.close()
    if not os.path.exists("./pictures"):
        print("Создаем папку pictures")
        os.mkdir("./pictures")
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    
    page_list:list = list()
    with open("page_list.txt","r") as file:
        for line in file:
            page_list.append(line.strip())
            
    for page_src in page_list:
        page_name = page_src.split("/")[-1]
        page_name = page_name.replace(".html","")
        
        print(f"Downloading {page_name}")
        if not os.path.exists(f"./pictures/{page_name}"):
            os.mkdir(f"./pictures/{page_name}")
        content = requests.get(page_src).text
        # with open(f"./tmp/{page_name}.html","w") as file:
        #     file.write(page.text)
        #     file.flush()
        #     file.close()
        hrefList:list = list()
                
        soup:Soup = Soup(content,"lxml")
        res = soup.find_all("a","highslide")
        for el in res:
            hrefList.append(el["href"])
            
        count:int = 1;    
        totalCount = len(hrefList)
        
        for href in hrefList:
            pic_num:str = ""
            pic_num = f"{count}"
            if count<10:
                pic_num = f"00{count}"
            if count>=10 and count<100:
                pic_num = f"0{count}"
              
            if href.find("https")==-1:
                href=f"https:{href}"
                
            img = requests.get(href)
            out = open(f"./pictures/{page_name}/{pic_num}.jpg","wb")
            out.write(img.content)
            out.close()
            print(f"Saved {count} of {totalCount}")
            count=count+1
            #sleep(0.1)
        print(f"Downloading {page_name} complete")
        sleep(1)
    print("Parsing complete")
        
    
if __name__ =="__main__":
    main()