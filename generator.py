#!/usr/bin/env

import requests
import json
from PIL import Image
from urllib.request import Request, urlopen
from uuid import uuid4
from random import randint
import random

#GLOBALS
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#Function that creates the collage
def createCollage(img, size, bgc=(255,255,255)):
    s=sorted(size,reverse=True)
    nWidth=s[0][0]+s[1][0]
    s=sorted(size,key=lambda x:x[1],reverse=True)
    nHeight=s[0][1]+s[0][1]

    print('GENERATING COLLAGE...\n')
    collage=Image.new('RGB',(nWidth,nHeight),color=bgc)

    for ind,i in enumerate(img):
        max_dim=max([nWidth,nHeight])
        offset_param=int(max_dim/3)
        offset=randint(-offset_param,offset_param)
        # Old offset. Fits all images within canvas
        # offset=randint(-50,50)
        x=y=max_dim
        #Fit in canvas
        while (x+i.size[0])>collage.size[0] or (y+i.size[1])>collage.size[1]:
            x=randint(0,nWidth)
            y=randint(0,nHeight)
        collage.paste(i,(offset+x,offset+y))

    return collage

# Exposed endpoint to start the creation of collage
def generate_coll(query, count, colour=None):
    img = []
    size = []

    # Request data to fetch images
    r = requests.get("https://customsearch.googleapis.com/customsearch/v1",
        params={
            'key': 'AIzaSyAlSxpfMPROMhfmx92tZZgnh_YwuOVd7gU ',
            'cx': 'b7693fbe7cebc855c',
            'q': query,
            'searchType': 'IMAGE',
            'num': 10
        },
        headers=headers
    )

    # Number of images in collage
    for _ in range(count):
        response = r.json().get('items')
        choice = random.choice(response)
        url = choice.get('link')

        imgreq = Request(url,headers=headers)
        img.append(Image.open(urlopen(imgreq)))
        size.append((choice['image']['width'],choice['image']['height']))

        print(f"TEXT : {query} , URL : {url}")
        # print(f"{choice}")

    # clg = createCollage(img,size,(randint(0,255),randint(0,255),randint(0,255)))
    clg = createCollage(img,size,colour)
    # clg.show()
    filename = f"{uuid4().hex}.jpg"
    clg.save(f'./static/outputs/{filename}')

    return filename
