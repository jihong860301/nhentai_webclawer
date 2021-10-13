import requests as rq
from bs4 import BeautifulSoup as bs
import sys
import os
import img2pdf
from concurrent.futures import ThreadPoolExecutor

# input six numbers for comics
six_num = sys.argv[:]


def get_image(img_src):
    # download image
    img = rq.get(img_src, stream=True).content
    i = img_src.split('/')[5].split('.')[0]
    with open(f'./_{i}.png', 'wb') as pic_out:
        pic_out.write(img)


base_dir = os.getcwd()
for sn in six_num[1:]:
    os.chdir(base_dir)
    # create folder for images
    if not os.path.isdir(f'./{sn}'):
        os.mkdir(sn)
    # change dir to the created folder
    os.chdir(f'./{sn}')
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
        executor.map(get_image, img_src)

    # make pdf with A-4 size
    a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4)
    try:
        with open(f'./{sn}.pdf', 'wb') as f:
            f.write(img2pdf.convert(
                [f'./_{i}.png' for i in range(1, int(sel_tag[-1].text)+1)], layout_fun=layout_fun))
    except:
        print('Fail to make pdf!\nRemake pdf with make_pdf.py')
