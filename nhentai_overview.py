import requests
from bs4 import BeautifulSoup

#########################################################
filename = 'loli_search'
nhentai_ref = "https://nhentai.net/search/?q=loli"
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
    print(sel2_img[1]["src"])

    pic = requests.get(sel2_img[1]["src"])
    img2 = pic.content
    fn = s["href"].split('/')
    pic_out = open(fn[2]+'.png', 'wb')
    pic_out.write(img2)
    pic_out.close()
    list_text.write(fn[2]+':'+sel2_title[0].text+'\n')

list_text.close()
