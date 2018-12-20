# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 03:49:49 2018

@author: fuwen
"""
from subprocess import call
import requests,re,time,os,js2py


BookID = 8451
FilePath = r'D:\有声小说\放开那个女巫_荣强叔叔'
IdmPath = 'C:\idman_lv\IDMan.exe'

headers =  {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36',
        }

def get_mp3_url(text):
    func = js2py.eval_js("""
        function FonHen_JieMa(u){
                var tArr = u.split("*");
                var str = '';
                for(var i=1,n=tArr.length;i<n;i++){
                    str += String.fromCharCode(tArr[i]);
                }
                return str;
            }
    """)
    return func(text).split('&')[0]

def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n'])

BookUrl = 'http://www.ting56.com/mp3/%d.html'%BookID
response = requests.get(BookUrl)
response.encoding = 'gbk'
html_doc = response.text
html_list = html_doc.split('\n')
AlreadyDown = [FileName for FileName in os.listdir(FilePath)]
for i in html_list :
    s = re.findall("href=\'(.*?)\'",i)
    if s :
        HtmlList = ['http://m.ting56.com'+ i for i in s]

for DetailUrl in HtmlList :
    DetailResponse= requests.get(DetailUrl, headers = headers)
    DetailResponse.encoding = 'gbk'
    DetailHtml = DetailResponse.text
    mp3_url = get_mp3_url(DetailHtml)
    mp3_name = re.findall('<h1 class="bookname">(.*?)在线收听</h1>', DetailHtml)[0]
    mp3_name = mp3_name + '.m4a'
    if mp3_name in AlreadyDown :
        print('%s 已下载,跳过……'%mp3_name)
        time.sleep(1)
        continue
    print('正在下载%s……'%mp3_name)
    IdmDownLoad(mp3_url, mp3_name)
    time.sleep(2)
