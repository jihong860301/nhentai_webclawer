import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor


class overview:
    def __init__(self, keyword='Default', pages='1', order='recent'):
        self.keyword = keyword  # keyword
        # pages: string ,can be one number or two number connect with '-', like'1-5'
        self.pages = pages
        # order of searching result, 'recent', 'today', 'week', 'all time'
        self.order = order

        # process keyword
        key_split = self.keyword.split()
        if not len(key_split) == 1:
            search_keyword = ''
            for kk in key_split:
                search_keyword = search_keyword+'+'+kk
        else:
            search_keyword = self.keyword
        nref = 'https://nhentai.net/search/?q='+search_keyword

        # process order for url
        if self.order == 'today':
            nref = nref+'&sort=popular-today'
        elif self.order == 'week':
            nref = nref+'&sort=popular-week'
        elif self.order == 'all time':
            nref = nref + '&sort=popular'

        if search_keyword == 'Default':
            nref = 'https://nhentai.net/'

        # base url for searching result
        self.url = nref

    def search(self):
        # create folder and change path to the folder
        if not os.path.isdir(f'./{self.keyword}_search'):
            os.mkdir(self.keyword+'_search')
        os.chdir(f'./{self.keyword}_search')
        # open a .txt file for comic list
        list_text = open(
            f'./{self.keyword}_search.txt', 'w', encoding='UTF-8')

        # process pages for url
        if len(self.pages.split('-')) == 1:
            pp = [self.pages]
        else:
            ps = self.pages.split('-')
            pp = [str(i) for i in range(int(ps[0]), int(ps[1])+1)]

        for p in pp:
            nref1 = self.url+'&page='+p

            # get whole searching page info
            r = requests.get(nref1)
            soup = BeautifulSoup(r.text, "html.parser")
            sel = soup.select("div.gallery a")

            for s in sel:
                # go into every comic to get info and download cover
                nref2 = 'https://nhentai.net'+s["href"]
                r2 = requests.get(nref2)
                soup2 = BeautifulSoup(r2.text, 'html.parser')
                sel2_title = soup2.select("div h2")
                print(sel2_title[0].text)
                # download cover
                sel2_img = soup2.select("div a img")
                sel_sixnum = soup2.select("div h3")
                pic = requests.get(sel2_img[1]["src"])
                img2 = pic.content
                fn = s["href"].split('/')
                pic_out = open(f'./#{fn[2]}.png', 'wb')
                pic_out.write(img2)
                pic_out.close()
                # write info into text, include title, tags and total pages
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

    def set_keyword(self, keyword):
        self.keyword = keyword  # set keyword

    def set_pages(self, pages):
        self.pages = pages  # set pages

    def set_order(self, order):
        self.order = order  # set order
