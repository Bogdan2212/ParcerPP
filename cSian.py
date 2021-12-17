import asyncio

import requests as req
from bs4 import BeautifulSoup
import time
from user_agent import generate_user_agent
import lxml
import regex
from send_telegram import send_telegram
from send_mail import send_mail
headers={
    "user-agent" : generate_user_agent()
}


async def cian_parcer(silka,id,mail,hours):
    print(1)
    hours = hours * 60
    timer = 0
    try:
        URL = silka
        ans = req.get(URL, headers=headers)
        page = BeautifulSoup(ans.text, "lxml")
        countold=page.find("h5", class_="_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6").text
        stroka=regex.findall("\d+", countold)
        ss=""
        for i in stroka:
            ss+=i
        ss=int(ss)
        countold=ss
        while True:
            timer += 5
            if timer == hours:
                break
            URL = silka
            ans = req.get(URL, headers=headers)
            page = BeautifulSoup(ans.text, "lxml")
            countnew = page.find("h5", class_="_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_20px--tUURJ _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6").text
            stroka = regex.findall("\d+", countnew)
            ss = ""
            for i in stroka:
                ss += i
            ss = int(ss)
            countnew = ss
            k=0
            if countold<countnew:
                items = page.find_all("article", class_="_93444fe79c--container--2pFUD _93444fe79c--cont--1Ddh2")
                for item in items:
                    k+=1
                    try:
                        name = item.find("div", class_="_93444fe79c--container--JdWD4").text
                        place = item.find("div", class_="_93444fe79c--container--2h0AF").text
                        link =str(item.find("a", class_="_93444fe79c--link--39cNw").get("href"))
                        price = item.find("div", class_="_93444fe79c--container--2Kouc _93444fe79c--link--2-ANY")

                        price = str(price)


                        n = price.find('data-mark="MainPrice"><span class=""')
                        zz = ""
                        for i in range(n + 37, n + 60):
                            zz += price[i]
                            if price[i] == "₽":
                                break
                        s = f"Название: {name}\n\nМестоположение: {place}\n\nСсылка: {link}\n\nЦена: {zz}\n\n"
                        await send_telegram(s,id)
                        #await send_mail(mail,s)

                    except Exception:
                        raise Exception
                    finally:
                        if k>=(countnew-countold):
                            break
            countold=countnew
            time.sleep(50)

    except Exception:
        raise Exception
