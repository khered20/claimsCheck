# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:21:00 2022

@author: SmaRt
"""

import urljoin
import urllib.request
import json
import urllib
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

import pandas as pd

from urllib import request

import sys
import os

import re

# use your key here (Fact Check Tools API | Google Developers)
key=''

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-src', '-source', help='Specify the data source (reviewPublisherSiteFilter)',
                    nargs='?', default='None', const='You should specify the source (reviewPublisherSiteFilter) such as: -src fullfact.org')
parser.add_argument('-b_mup', '-markup', help='Specify the markup tag that has the full article',
                    nargs='?', default='None', const='You should specify the markup tag for the body that has the full article such as in fullfact.org: -b_mup div')
parser.add_argument('-b_class', '-class', help='Specify the class that has the full article',
                    nargs='?', default='None', const='You should specify the class of the body that has the full article such as in fullfact.org: -b_class cms-content')
parser.add_argument('-pth', '-path', help='Specify the folder name for the data will be saved in, default: -pth claims',
                    nargs='?', default='claims', const='You should specify the folder name for the data will be saved in')
parser.add_argument('-it', '-iteration', help='Specify how many iteration will will be repeated until close (the Total sets in all files)',
                    nargs='?', default='50', const='You should specify the iteration number, default: -it 50')
parser.add_argument('-ps', '-pageSize', help='Specify the pagesize for each rquest',
                    nargs='?', default='10', const='You can specify the pageSize for each rquest, default: -ps 10')
parser.add_argument('-st', '-setTotal', help='Specify how many sets will be saved in one file (total samples in each file will be in around ps×st)',
                    nargs='?', default='10', const='You can specify the setTotal which will be saved in one file, default: -st 10')
parser.add_argument('-npt', '-nextPageToken', help='Specify nextPageToken',
                    nargs='?', default='', const='You can specify nextPageToken, ex -npt CAo')

args = parser.parse_args()

if args.src == 'None' and args.pth == 'claims' and args.it == '50' and args.ps == '10' and args.st == '10' and args.npt == '':
    print('~getFData.py -src (mandantory) Specify the data source (reviewPublisherSiteFilter). You can show the saved list by using -src list')
    print('~-src (optional) Specify the data source (reviewPublisherSiteFilter)')
    print('~-b_mup (optional) pecify the markup tag that has the full article')
    print('~-b_class (optional) Specify the class that has the full article')
    print('If both mup and class are not used, the system will use tag from the saved sources')
    print('~-it (optional) You can specify how many iteration will will be repeated until it finishes (the Total sets in all files)')
    print('~ps (optional) You can specify the pageSize for each rquest, default: -ps 10')
    print('~st (optional) You can specify the setTotal which will be saved in one file, default: -st 10')
    print('~npt (optional) You can specify nextPageToken, ex -npt CAo')
    print('~getFData.py -src fullfact.org -pth datafolder -it 1500 -ps 300 -st 50')
    
    

    quit()

reviewPublisherSiteFilter=args.src

iteration=int(args.it)
pageSize=int(args.ps)
setTotal=int(args.st)
nextPageToken=args.npt

claimsPath=args.pth+'/'
ensure_dir(claimsPath)

tag_body= args.b_mup
class_body=args.b_class


#imgLink='https://fullfact.org'
#################################
# #### Test localy
# iteration=1500
# pageSize=300
# setTotal=50
# nextPageToken=''
# claimsPath='snopes/'
# ensure_dir(claimsPath)
# reviewPublisherSiteFilter='snopes.com'
# imgLink=reviewPublisherSiteFilter
# filename = 'claims'
# tag_body='None'
# class_body='None'
################################


imgLink=reviewPublisherSiteFilter

if tag_body == 'None' or class_body=='None':
    if reviewPublisherSiteFilter == 'list':
        print('1- reviewPublisherSiteFilter=fullfact.org >> full article tag_body=div and class_body=cms-content')
        print('2- reviewPublisherSiteFilter=bbc.co.uk >> full article tag_body=div and class_body=ssrcss-rgov1k-MainColumn e1sbfw0p0')
        print('3- reviewPublisherSiteFilter=politifact.com >> full article tag_body=div and class_body=t-row__center')
        print('4- reviewPublisherSiteFilter=snopes.com >> full article tag_body=div and class_body=single-body card-body rich-text')
        print('5- reviewPublisherSiteFilter=nytimes.com >> full article tag_body=section and class_body=meteredContent css-1r7ky0e')
        print('6- reviewPublisherSiteFilter=washingtonpost.com >> full article tag_body=div and class_body=article-body')
        print('7- reviewPublisherSiteFilter=climatefeedback.org >> full article tag_body=div and class_body=entry-content')
        print('8- reviewPublisherSiteFilter=factcheck.afp.com >> full article tag_body=div and class_body=article-entry clearfix')
        print('ex: getFData.py -src fullfact.org -it 1500 -ps 300 -st 50')
        quit()
    elif reviewPublisherSiteFilter=='fullfact.org':
        tag_body='div'
        class_body='cms-content'
    elif reviewPublisherSiteFilter=='bbc.co.uk':
        tag_body='div'
        #class_body='ssrcss-rgov1k-MainColumn'
        class_body='ssrcss-rgov1k-MainColumn e1sbfw0p0'
    elif reviewPublisherSiteFilter=='politifact.com':
        tag_body='div'
        class_body='t-row__center'
    elif reviewPublisherSiteFilter=='snopes.com':
        tag_body='div'
        class_body='single-body card-body rich-text'
    elif reviewPublisherSiteFilter=='nytimes.com':
        tag_body='section'
        class_body='meteredContent css-1r7ky0e'
    elif reviewPublisherSiteFilter=='washingtonpost.com':
        tag_body='div'
        class_body='article-body'
    elif reviewPublisherSiteFilter=='climatefeedback.org':
        tag_body='div'
        class_body='entry-content'
    elif reviewPublisherSiteFilter=='factcheck.afp.com':
        tag_body='div'
        class_body='article-entry clearfix'
    else:
        print('Sorry the full article will not be extracted as we dont know the body article tag for '+reviewPublisherSiteFilter)



filename = reviewPublisherSiteFilter.split(".")[0]

x = {
  "link": [],
  "img": []
}

i=0
j=0
sampfile=0
while i <iteration:
    insialUrl= 'https://factchecktools.googleapis.com/v1alpha1/claims:search?key='+key+'&reviewPublisherSiteFilter='+reviewPublisherSiteFilter+'&pageSize='+str(pageSize)+'&pageToken='
    url = insialUrl+nextPageToken
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    site_json=json.loads(soup.text)
    for d in site_json['claims']:
        #print(d)
        sampfile=sampfile+1
        text=d.get('text')
        claimant=d.get('claimant')
        claimDate=d.get('claimDate')
        claimReview=d.get('claimReview')[0]
        publisher=claimReview.get('publisher')
        name=publisher.get('name')
        site=publisher.get('site')
        url=claimReview.get('url')
        title=claimReview.get('title')
        reviewDate=claimReview.get('reviewDate')
        textualRating=claimReview.get('textualRating')
        languageCode=claimReview.get('languageCode')
        article=''
        text_article=''
        
        try:
            html = request.urlopen(url).read()
            soup = BeautifulSoup(html,'html.parser')
            #site_json=json.loads(soup.text)
            article = soup.find(tag_body, class_=class_body)
            htmlarticle=article
            text_article=article.text
            #text_article=re.sub('\s+',' ',text_article)
            x = {
              "link": [],
              "img": []
            }
            for link in htmlarticle.find_all(['a','img']):
                #print(link)
                if link.has_attr('href') and len(link['href']) < 500:
                    if 'http' not in link['href']:
                        x['link'].append(imgLink+link['href'])
                    else:
                        x['link'].append(link['href'])
                    #print(link['href'])
                elif len(link['href']) > 500:
                    article='TOO LONG LINK'
                if link.has_attr('src')  and len(link['src']) < 500:
                    if 'http' not in link['src']:
                        x['img'].append(imgLink+link['src'])
                    else:
                        x['img'].append(link['src'])
                    #print(imgLink+link['src'])
            
            print(i)
        except Exception:
            print('Exception exist')
            pass
        
        #duration=str(timedelta(seconds=duration))
        if article is not None:
            if len(article)> 70000:
                article='TOO LONG'
            #else:
                #article='deleted'
        else:
            article='None'
            
            
        raw_data = {
                    'id': [sampfile],
                    'text': [text],
                    'claimant': [claimant],
                    'claimDate': [claimDate],
                    'cR_p_name': [name],
                    'cR_p_site': [site],
                    'cR_url': [url],
                    'cR_title': [title],
                    'cR_reviewDate': [reviewDate],
                    'cR_textualRating': [textualRating],
                    'lCode': [languageCode],
                    'links_article': [json.dumps(x)],
                    'text_article': [text_article],
                    'html_article': [article]
                    }
        df = pd.DataFrame(raw_data,columns = ['id','text','claimant','claimDate',
          'cR_p_name','cR_p_site','cR_url','cR_title','cR_reviewDate','cR_textualRating','lCode','links_article','text_article','html_article'])
        
        evalpath= claimsPath+filename+'.csv'
        from os import path
        isexist = path.exists(evalpath)
        if(isexist):
            evaldata = pd.read_csv (r''+evalpath,encoding='utf-8')
            evaldata=evaldata.append(df)
        else: 
            evaldata = df
            
        evaldata.to_csv(evalpath,index=False )
        
        x = {
          "link": [],
          "img": []
        }
        article=''
        text_article=''
        
    nextPageToken =site_json['nextPageToken']
    
    ###########
    
        
    
    i=i+1
    
    raw_data = {
                'set': [str(i)],
                'samples': [len(site_json['claims'])],
                'nextPageToken': [nextPageToken],
                'file': ['claim'+str(j+1)]
                
                }
    df = pd.DataFrame(raw_data,columns = ['set','samples','nextPageToken','file'])
    
    evalpath= claimsPath+filename+'Sets.csv'
    from os import path
    isexist = path.exists(evalpath)
    if(isexist):
        evaldata = pd.read_csv (r''+evalpath,encoding='latin1')
        evaldata=evaldata.append(df)
    else: 
        evaldata = df
        
    evaldata.to_csv(evalpath,index=False )
    
    
    if i % setTotal == 0:
        
        j=j+1
        os.rename(claimsPath+filename+'.csv', claimsPath+filename+str(j)+'.csv')

        raw_data = {
                    'file': ['claim'+str(j)],
                    'setTotal': [str(setTotal)],
                    'samplesTotal': [str(sampfile)],
                    'LastNextPageToken': [nextPageToken]
                    
                    }
        df = pd.DataFrame(raw_data,columns = ['file','setTotal','samplesTotal','LastNextPageToken'])
        
        evalpath= claimsPath+filename+'Files.csv'
        from os import path
        isexist = path.exists(evalpath)
        if(isexist):
            evaldata = pd.read_csv (r''+evalpath,encoding='latin1')
            evaldata=evaldata.append(df)
        else: 
            evaldata = df
            
        evaldata.to_csv(evalpath,index=False )
        
        sampfile=0
        
        

#printing for entrezgene, do the same for name and symbol
#print([d.get('text') for d in site_json['claims'] if d.get('text')])