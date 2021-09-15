from genericpath import samefile
import requests as rq
from bs4 import BeautifulSoup as bs
import sys
import os

##########################################
six_num = sys.argv[:]
##########################################
for sn in six_num[1:]:
    if not os.path.isdir('./'+sn):
        os.mkdir(sn)
    nref = 'https://nhentai.net/g/'+sn+'/'

    rr = rq.get(nref)
    soup = bs(rr.text, 'html.parser')
    sel = soup.select('div h2')
    print(sel[0].text)

    rr = rq.get(nref+'1/')
    soup = bs(rr.text, 'html.parser')
    sel = soup.select('div section button span')

    print('total pages', sel[-1].text)

    ii = int(sel[-1].text)
    for i in range(ii):
        rr = rq.get(nref+str(i+1)+'/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        img_src = sel[0]["src"]
        img_get = rq.get(img_src)
        img = img_get.content
        pic_out = open('./'+sn+'/_'+str(i+1)+'.png', 'wb')
        pic_out.write(img)
        pic_out.close()
        print('Page '+str(i+1)+' done!')
