import requests
from bs4 import BeautifulSoup
import sys
import os

#########################################################
filename = '22slash7_search'
nhentai_ref = "https://nhentai.net/parody/22-slash-7/"
#########################################################

r = requests.get(nhentai_ref)
soup = BeautifulSoup(r.text, "html.parser")
sel = soup.select("div.gallery a")

list_text = open('nhentai_'+filename+'.txt', 'w', encoding='UTF-8')
for s in sel:
    nref = 'https://nhentai.net'+s["href"]
    r2 = requests.get(nref)
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    sel2_title = soup2.select("div h2")
    print(sel2_title[0].text)
    sel2_img = soup2.select("div a img")
    sel_sixnum = soup2.select("div h3")

    pic = requests.get(sel2_img[1]["src"])
    img2 = pic.content
    fn = s["href"].split('/')
    pic_out = open('#'+fn[2]+'.png', 'wb')
    pic_out.write(img2)
    pic_out.close()
    list_text.write(sel_sixnum[0].text+':'+sel2_title[0].text+'\ttag:')
    sel2_tags = soup2.select('div section span a')
    for s in sel2_tags:
        ss = s['href'].split('/')
        if ss[1] == 'tag':
            list_text.write(ss[2]+'\t')
    list_text.write(sel2_tags[-1].text+'p\n')
    print(sel_sixnum[0].text, sel2_tags[-1].text+'p')

list_text.close()
