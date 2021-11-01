import requests as rq
from bs4 import BeautifulSoup as bs
import os
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
            self.author = ''
            self.title = ''
            self.otherinfo = ''
            self.total_pages = ''

    def dlimages(self):
        if not self.dldir:
            self.dldir = os.getcwd()
        # download dir
        os.chdir(self.dldir)
        # create folder for images
        if not os.path.isdir(f'./{self.six_num}'):
            os.mkdir(self.six_num)
        # change dir to the created folder
        os.chdir(f'./{self.six_num}')

        # get image urls
        rr = rq.get(self.url+'1/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        base_src = sel[0]["src"].split('1.jpg')[0]
        img_src = [f'{base_src}{i}.jpg' for i in range(
            1, int(self.total_pages)+1)]

        # using multi-thread to download images
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = executor.map(get_image, img_src)

        pp = 1
        for rr in results:
            rr.save(f'_{pp}.png', 'PNG')
            pp += 1
        os.chdir(self.dldir)

    def dlpdf(self):
        if not self.dldir:
            self.dldir = os.getcwd()
        rr = rq.get(self.url+'1/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        base_src = sel[0]["src"].split('1.jpg')[0]
        img_src = [f'{base_src}{i}.jpg' for i in range(
            1, int(self.total_pages)+1)]

        # using multi-thread to download images
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = executor.map(get_image, img_src)

        images = []
        for rr in results:
            images.append(rr)
        images[0].save(f'{self.dldir}\{self.six_num}.pdf',
                       'PDF', save_all=True, append_images=images[1:])

    def set_sixnum(self, six_num):
        self.six_num = six_num
        self.url = f'https://nhentai.net/g/{six_num}/'
        rr = rq.get(self.url)
        soup = bs(rr.text, 'html.parser')
        sel_tag = soup.select('div section span a')
        sel = soup.select('div h2')
        self.total_pages = sel_tag[-1].text
        sel = soup.select('div h2.title span.before')
        self.author = sel[0].text
        sel = soup.select('div h2.title span.pretty')
        self.title = sel[0].text
        sel = soup.select('div h2.title span.after')
        self.otherinfo = sel[0].text

    def set_threads(self, threads):
        if isinstance(threads, int):
            self.threads = threads
        elif isinstance(threads, str):
            try:
                self.threads = int(threads)
            except:
                pass
        else:
            pass

    def set_dldir(self, dldir):
        self.dldir = dldir

    def get_sixnum(self):
        return self.six_num

    def get_url(self):
        return self.url

    def info(self):
        return {'author': self.author,
                'title': self.title,
                'other': self.otherinfo,
                'pages': self.total_pages}

    def show_cover(self):
        rr = rq.get(self.url+'1/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        img_src = sel[0]["src"]
        img = rq.get(img_src, stream=True).content

        image = Image.open(io.BytesIO(img))
        return image


def get_image(img_src):
    # download image
    img = rq.get(img_src, stream=True).content
    image = Image.open(io.BytesIO(img))
    if image.mode == 'RGB' or image.mode == 'L':
        return image


if __name__ == '__main__':
    ndl = nhentai_download()
    ndl.set_sixnum('369008')
