import requests as rq
from bs4 import BeautifulSoup as bs
import sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io

# input six numbers for comics
six_num = sys.argv[:]


def get_image(img_src):
    # download image
    img = rq.get(img_src, stream=True).content
    image = Image.open(io.BytesIO(img))
    if image.mode == 'RGB' or image.mode == 'L':
        if image.width == 1280:
            return image


for sn in six_num[1:]:
    # base ref
    nref = f'https://nhentai.net/g/{sn}/'

    # get and print title of the comic
    rr = rq.get(nref)
    soup = bs(rr.text, 'html.parser')
    sel = soup.select('div h2')
    print(sel[0].text)

    # get and print the total pages of the comic
    sel_tag = soup.select('div section span a')
    print('Total pages', sel_tag[-1].text)

    # get image urls
    rr = rq.get(nref+'1/')
    soup = bs(rr.text, 'html.parser')
    sel = soup.select("div a img")
    base_src = sel[0]["src"].split('1.jpg')[0]
    img_src = [f'{base_src}{i}.jpg' for i in range(
        1, int(sel_tag[-1].text)+1)]

    # using multi-thread to download images
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(get_image, img_src)

    images = []
    for im in results:
        images.append(im)
    images[0].show()
    images[0].save(f'{sn}.pdf', 'PDF', save_all=True,
                   append_images=images[1:])
