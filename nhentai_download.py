from genericpath import samefile
import requests as rq
from bs4 import BeautifulSoup as bs
import sys

##########################################
six_num = sys.argv[:]
##########################################
nref = 'https://nhentai.net/g/'+six_num+'/'

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
    pic_out = open('_'+str(i+1)+'.png', 'wb')
    pic_out.write(img)
    pic_out.close()
    print('Page '+str(i)+' done!')
