import argparse
import urllib
import os
import urllib.request
from ithread import IThread 
from bs4 import BeautifulSoup
import requests

# https://www.meizitu.com/a/xinggan.html
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    request = urllib.request.Request(url=url, headers=headers)
    return urllib.request.urlopen(request)

def get_soup(html):
    if None == html:
        return
    return BeautifulSoup(html.read(), 'html.parser')

def get_img_dirs(soup):
    if None == soup: return

    lis = soup.find(id='maincontent').find_all(name='li') # findAll(name='a') # attrs={'class':'lazy'}
    if None != lis:
        img_dirs = {};
        for li in lis:
            link = li.find(name='a')
            if None == link: continue
            img = link.find(name='img')
            if None == img: continue
            k = img.attrs['alt']
            t = link.attrs['href']
            img_dirs[k] = t;
        return img_dirs

def download_imgs(info):
    if None == info:
        return

    t = info[0]
    l = info[1]
    if None == t or None == l:
        return
    print("创建相册：" + t +" " + l)
    try:
        os.mkdir(t)
    except Exception as e:
        print("文件夹："+t+"，已经存在")

    print("开始获取相册《" + t + "》内，图片的数量...")

    dir_html = get_html(l)
    dir_soup = get_soup(dir_html)
    img_page_url = get_dir_img_page_url(l, dir_soup)

    # 得到当前相册的封面
    main_image = dir_soup.findAll(name='div', attrs={'id':'picture'})
    if None != main_image:
        for image_parent in main_image:
            imgs = image_parent.findAll(name='img')
            if None != imgs:
                img_url = str(imgs[0].attrs['src'])
                filename = img_url.split('/')[-1]
                print("开始下载:" + img_url + ", 保存为："+filename)
                save_file(t, filename, img_url)

    # 获取相册下的图片
    for photo_web_url in img_page_url:
        download_img_from_page(t, photo_web_url)



def download_img_from_page(t, page_url):
    dir_html = get_html(page_url)
    dir_soup = get_soup(dir_html)

    print(dir_soup)
    print()

    # 得到当前页面的图片
    main_image = dir_soup.findAll(name='div', attrs={'class':'main-image'})
    if None != main_image:
        for image_parent in main_image:
            imgs = image_parent.findAll(name='img')
            if None != imgs:
                img_url = str(imgs[0].attrs['src'])
                filename = img_url.split('/')[-1]
                print("开始下载:" + img_url + ", 保存为："+filename)
                save_file(t, filename, img_url)



def save_file(d, filename, img_url):
    print(img_url+"=========")
    img = requests.get(img_url)
    name = str(d+"/"+filename)
    with open(name, "wb") as code:
        code.write(img.content)

def get_dir_img_page_url(l, dir_soup):
    """
    获取相册里面的图片数量
    :param l: 相册链接
    :param dir_soup:
    :return: 相册图片数量
    """
    # print(l, dir_soup)
    # print()
    divs = dir_soup.find_all(name='div', attrs={'id':'picture'})
    navi = divs[0]

    links = navi.findAll(name='img')
    if None == links:
        return
    a = []
    url_list = []
    for link in links:
        h = str(link['src'])
        url_list.append(h)
    return url_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("echo")
    # parser.add_argument("url")
    # url = int(args.url)
    args = parser.parse_args()
    url = str(args.echo)
    print("开始解析：" + url)

    html = get_html(url)
    soup = get_soup(html)
    img_dirs = get_img_dirs(soup)
    if None == img_dirs:
        print("无法获取该网页下的相册内容...")
    else:
        for d in img_dirs:
            my_thread = IThread(download_imgs, (d, img_dirs.get(d)))
            my_thread.start()
            my_thread.join()