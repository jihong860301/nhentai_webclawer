import requests as rq
from bs4 import BeautifulSoup as bs
import os
import img2pdf
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io


class nhentai_download:
    def __init__(self, six_num='000000', dldir=None, threads=16):
        self.six_num = six_num
        if not dldir:
            self.dldir = os.getcwd()
        self.threads = threads

        # download base info
        if not six_num == '000000':
            self.url = f'https://nhentai.net/g/{self.six_num}/'
            rr = rq.get(self.url)
            soup = bs(rr.text, 'html.parser')
            sel_tag = soup.select('div section span a')
            sel = soup.select('div h2')
            self.title = sel[0].text
            self.total_pages = sel_tag[-1].text
        else:
            self.url = 'https://nhentai.net/'
            self.title = ''
            self.total_pages = ''

    def download(self):
        # download dir
        os.chdir(self.dldir)
        # create folder for images
        if not os.path.isdir(f'./{self.six_num}'):
            os.mkdir(self.six_num)
        # change dir to the created folder
        os.chdir(f'./{self.six_num}')

        # get and print title of the comic
        rr = rq.get(self.url)
        soup = bs(rr.text, 'html.parser')
        sel = soup.select('div h2')
        print(sel[0].text)

        # get and print the total pages of the comic
        sel_tag = soup.select('div section span a')
        print('Total pages', sel_tag[-1].text)

        # get image urls
        rr = rq.get(self.url+'1/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        base_src = sel[0]["src"].split('1.jpg')[0]
        img_src = [f'{base_src}{i}.jpg' for i in range(
            1, int(sel_tag[-1].text)+1)]

        # using multi-thread to download images
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(get_image, img_src)

    def set_sixnum(self, six_num):
        self.six_num = six_num
        self.url = f'https://nhentai.net/g/{six_num}/'
        rr = rq.get(self.url)
        soup = bs(rr.text, 'html.parser')
        sel_tag = soup.select('div section span a')
        sel = soup.select('div h2')
        self.title = sel[0].text
        self.total_pages = sel_tag[-1].text

    def get_sixnum(self):
        return self.six_num

    def get_url(self):
        print(self.url)

    def set_threads(self, threads):
        self.threads = threads

    def set_dldir(self, dldir):
        self.dldir = dldir

    def info(self):
        print('Title: '+self.title)
        print('Pages: '+self.total_pages+'p')

    def show_cover(self):
        rr = rq.get(self.url+'1/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        img_src = sel[0]["src"]
        img = rq.get(img_src, stream=True).content

        image = Image.open(io.BytesIO(img))
        image.show()

    def make_pdf(self):
        a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
        layout_fun = img2pdf.get_layout_fun(a4)
        try:
            with open(f'./{self.six_num}.pdf', 'wb') as f:
                f.write(img2pdf.convert(
                    [f'./_{i}.png' for i in range(1, int(self.total_pages)+1)], layout_fun=layout_fun))
        except:
            print('Fail to make pdf!\nRemake pdf with make_pdf.py')


def get_image(img_src):
    # download image
    img = rq.get(img_src, stream=True).content
    i = img_src.split('/')[5].split('.')[0]
    with open(f'./_{i}.png', 'wb') as pic_out:
        pic_out.write(img)
