import requests
from bs4 import BeautifulSoup
import os


class overview:
    def __init__(self, key_word, pages='1', order='recent'):
        self.key_word = key_word
        self.pages = pages
        self.order = order

    def search(self):
        if not os.path.isdir('./'+self.key_word+'_search'):
            os.mkdir(self.key_word+'_search')
        list_text = open('./'+self.key_word+'_search/'+self.key_word+'_search' +
                         '.txt', 'w', encoding='UTF-8')
        key_split = self.key_word.split()
        if not len(key_split) == 1:
            search_keyword = ''
            for kk in key_split:
                search_keyword = search_keyword+'+'+kk

        nref = 'https://nhentai.net/search/?q='+search_keyword
        if self.order == 'today':
            nref = nref+'&sort=popular-today'
        elif self.order == 'week':
            nref = nref+'&sort=popular-week'
        elif self.order == 'all time':
            nref = nref + '&sort=popular'

        if len(self.pages.split('-')) == 1:
            pp = [self.pages]
        else:
            ps = self.pages.split('-')
            pp = [str(i) for i in range(int(ps[0]), int(ps[1])+1)]

        for p in pp:
            nref1 = nref+'&page='+p

            r = requests.get(nref1)
            soup = BeautifulSoup(r.text, "html.parser")
            sel = soup.select("div.gallery a")

            for s in sel:
                nref2 = 'https://nhentai.net'+s["href"]
                r2 = requests.get(nref2)
                soup2 = BeautifulSoup(r2.text, 'html.parser')
                sel2_title = soup2.select("div h2")
                print(sel2_title[0].text)
                sel2_img = soup2.select("div a img")
                sel_sixnum = soup2.select("div h3")

                pic = requests.get(sel2_img[1]["src"])
                img2 = pic.content
                fn = s["href"].split('/')
                pic_out = open('./'+self.key_word +
                               '_search/#'+fn[2]+'.png', 'wb')
                pic_out.write(img2)
                pic_out.close()
                list_text.write(sel_sixnum[0].text +
                                ':'+sel2_title[0].text+'\ttag:')
                sel2_tags = soup2.select('div section span a')
                for s in sel2_tags:
                    ss = s['href'].split('/')
                    if ss[1] == 'tag':
                        list_text.write(ss[2]+'\t')
                list_text.write(sel2_tags[-1].text+'p\n')
                print(sel_sixnum[0].text, sel2_tags[-1].text+'p')
        list_text.close()
