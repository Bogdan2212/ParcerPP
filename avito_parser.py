import requests as req
from bs4 import BeautifulSoup
import time
from user_agent import generate_user_agent
import lxml
from send_telegram import send_telegram
from send_mail import send_mail
import asyncio
headers = {
    "user-agent": generate_user_agent()
}


async def avito_parcer(silka,id,mail,hours):
    hours = hours * 60
    timer = 0
    URL = silka
    ans = req.get(URL, headers=headers)
    page = BeautifulSoup(ans.text, "lxml")
    countold = page.find("span", class_="page-title-count-oYIga").text

    countold = int(countold.replace("\xa0", ""))

    while True:
        timer += 5
        if timer >= hours:
            break
        URL = silka
        ans = req.get(URL, headers=headers)
        name='Нет названия'
        price='Нет цены'
        page = BeautifulSoup(ans.text, "lxml")
        countnew = page.find("span", class_="page-title-count-oYIga").text
        countnew = int(countnew.replace("\xa0", ""))
        k = 0

        if countold < countnew:
            items = page.find_all("div", class_="iva-item-content-UnQQ4")
            for item in items:
                k += 1
                try:
                    name = item.find("h3",
                                     class_="title-root-j7cja iva-item-title-_qCwt title-listRedesign-XHq38 title-root_maxHeight-SXHes text-text-LurtD text-size-s-BxGpL text-bold-SinUO").text
                    price = item.find("span", class_="price-text-E1Y7h text-text-LurtD text-size-s-BxGpL").text
                    link = "https://www.avito.ru" + str(item.find("a", class_="iva-item-sliderLink-bJ9Pv").get("href"))
                    place = item.find("div", class_="geo-georeferences-Yd_m5 text-text-LurtD text-size-s-BxGpL").text
                    s = f"Название: {name}\n\nСсылка: {link}\n\nЦена: {price}\n\nМесторасположение: {place}\n\n"
                    await send_telegram(s, id)
                    #await send_mail(mail, s)
                except Exception:
                    link = "https://www.avito.ru" + str(item.find("a", class_="iva-item-sliderLink-bJ9Pv").get("href"))
                    s=f"{name}\n\n{price}\n\n{link}"
                    await send_telegram(s, id)
                    raise Exception
                finally:
                    if k >= (countnew - countold):
                        break
        countold = countnew
        time.sleep(300)


