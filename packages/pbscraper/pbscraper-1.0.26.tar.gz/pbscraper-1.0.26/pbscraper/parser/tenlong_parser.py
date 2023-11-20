from .base_parser import BaseParser
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import logging
from ..common.utility import utility
from requests.adapters import HTTPAdapter
requests.adapters.DEFAULT_RETRIES = 0
import html
import json

class TenlongParser(BaseParser):
    def __init__(self):
        self._ecid = 15
        self._ecpid = None
    def get_ec_popidx(self):
        return 90
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.tenlong\.com\.tw\/products\/(\d+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            is_book = True
        return is_book

    def scrape_page_to_strprd(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='https://www.tenlong.com.tw')
        res = reqss.get(url, headers=headers, timeout=60)'''
        if res.status_code == 404:
            print('-- 商品已下架? 404找不到商品頁') 
            return None
        if res.status_code != 200:
            raise ValueError(f'-- status_code is {res.status_code}')
        pure_html = res.text
        res.connection.close()
        # ---- 準備剖析html ----
        popIdx = self.get_ec_popidx()
        prd = {}
        soup = BeautifulSoup(pure_html,features="lxml")
        is_onshelf = self._extract_is_onshelf(soup)
        if is_onshelf == 1: 
            # ---- step1 商品頁可取得的資訊 ----
            prd['Name'] = self._extract_name(soup)
            prd['Url'] = self._extract_url(soup)
            prd['ImgUrl'] = self._extract_imgurl(soup)
            prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
            prd['VideoUrl'] = None
            prd['VideoUrlList'] = None
            prd['OriPrice'] = self._extract_oriprice(soup)
            prd['Price'] = self._extract_price(soup)
            prd['Author'] = self._extract_author(soup)
            prd['ISBN'] = self._extract_isbn_by_url(url)
            prd['ECID'] = self._ecid
            prd['ECPID'] = self._extract_ecpid_by_url(url)
            prd['ECCatlog'] = self._extract_eccatlog(soup) 
            prd['isOnShelf'] = is_onshelf
            
            prd['isEnable'] = True # esc index v2是用boolean
            prd['Desc'] = self._extract_desc(soup)
            prd['ModifyTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['CreateTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['PopIdx'] = popIdx
            prd['CatID'] = None
            prd['Translator'] = self._extract_translator(soup)
            prd['PublishDate'] = self._extract_pub_date(soup)
            
            prd['Publisher'] = self._extract_publisher(soup) # esc index v2改名為publishcompany->publisher
            prd['Painter'] = self._extract_painter(soup)
            prd['OriginName'] = self._extract_origin_name(soup)
            prd['Summary'] = self._extract_summary(soup)
            prd['ISBN10'] = self._extract_isbn10(soup)
            prd['ISBNADD'] = self._extract_isbnadd(soup)
            prd['BookType'] = self._extract_booktype(soup, prd)
            prd['Text1'] = None
            prd['Text2'] = None
            prd['Text3'] = None
            prd['Keyword1'] = None
            prd['Keyword2'] = None
            prd['Keyword3'] = None
            
            # ---- step2 特殊處理的資訊 ----
            # 沒有原價的商品:https://www.kingstone.com.tw/basics/basics.asp?kmcode=2019920474639&lid=book_class_sec_se&actid=WISE
            if prd['OriPrice'] is None:
                prd['OriPrice'] = prd['Price']
            
            return prd

        else:
            print('-- 商品已下架? 找不到購物車鈕') 
            return None #回傳None則在main_parser下架商品

    # ======== 私有 萃取各值的方法 ========
    def _extract_is_onshelf(self, soup):
        val = 1
        return val
    
    def _extract_name(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['name']
                break
        if not val:
            elem = soup.select_one('div.content h1.item-title')
            if elem:
                val = elem.text.strip()
        return val
    
    def _extract_url(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['url']
                break
        if not val:
            val = soup.find("link", rel="canonical")['href']
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['image']#.replace('/original/', '/medium/')
                break
        if not val:
            elem = soup.select_one('div.img-wrapper picture img')
            if elem:
                val = elem['src']
        return val
    
    def _extract_imgurl_list(self, soup):
        val = None
        elems = soup.select('div.preview-wrapper ul li a picture img')
        imgs = [elem['src'] for elem in elems]
        val = ','.join([img for img in imgs])
        return val

    def _extract_ecpid_by_url(self, url):
        val = None
        match = re.search('www\.tenlong\.com\.tw\/products\/(\d+)?', url.lower())
        if match:
            val = match.group(1) if match.group(1) else None
        return val

    def _extract_eccatlog(self, soup):
        val = None
        cats = []
        elems = soup.find_all(text=re.compile(r'相關分類:'))
        for elem in elems:
            if elem.parent.parent.name == 'li':
                ar_a = elem.parent.parent.select('span.info-content a')
                cats = [a.text.strip() for a in ar_a]
                val = '>'.join(cats)
                break
        return val

    def _extract_author(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['author']
                break
        if not val:
            elem = soup.select_one('div.item-info div.item-header h3.item-author')
            if elem:
                ary_au = elem.text.split('、')
                val = ary_au[0].strip().replace(' 著', '')
        return val

    def _extract_isbn_by_url(self, url):
        val = None
        match = re.search('www\.tenlong\.com\.tw\/products\/(\d+)?', url.lower())
        if match:
            val = match.group(1) if match.group(1) else None
        return val

    def _extract_desc(self, soup):
        val = None
        elem = soup.select_one('div.item-desc')
        if elem:
            val = html.escape(elem.decode_contents())[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        elem = soup.select_one('div.item-info div.item-header h3.item-author')
        if elem:
            ary_au = elem.text.split('、')
            for au in ary_au:
                if '譯' in au:
                    val = au.strip().replace(' 譯', '')
                    break
        return val

    def _extract_pub_date(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['datePublished']
                break
        if not val:
            elems = soup.find_all(text=re.compile(r'出版日期:'))
            for elem in elems:
                if elem.parent.parent.name == 'li':
                    a = elem.parent.parent.select_one('span.info-content')
                    val = a.text
                    break
        if val:
            val = val.replace('-', '/')
        return val

    def _extract_publisher(self, soup):
        val = None
        elems = soup.find_all(text=re.compile(r'出版商:'))
        for elem in elems:
            if elem.parent.parent.name == 'li':
                a = elem.parent.parent.select_one('span.info-content a')
                val = a.text.strip()
                break
    
        if not val:
            elems = soup.findAll('script', type='application/ld+json')
            for el in elems:
                dict_data = json.loads(el.string, strict=False)[0]
                if dict_data['@type'] == "Book":
                    val = dict_data['publisher']
                    break
                
        return val

    def _extract_oriprice(self, soup):
        val = None
        orip = soup.find(text=re.compile(r'定價:'))
        if orip:
            p = orip.parent.parent.select_one('span.info-content')
            val = p.text.replace('$', '').replace(',', '').strip()
        return val

    def _extract_price(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['offers']['price']
                break
        if not val:
            vipp = soup.find(text=re.compile(r'貴賓 價:'))
            if vipp:
                ps = vipp.parent.parent.select_one('span.info-content')
                val = ps.select('span.pricing')[-1].text
            else:
                elems = soup.find_all(text=re.compile(r'售價:'))
                for elem in elems:
                    if elem.parent.parent.name == 'li':
                        ps = elem.parent.parent.select('span.pricing')
                        val = ps[-1].text
                        break
        if val:
            val = val.replace('$', '').replace(',', '')
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        return val
    def _extract_origin_name(self, soup):
        val = None
        return val  
    def _extract_summary(self, soup):
        val = None
        return val
    def _extract_isbn10(self, soup):
        val = None
        elems = soup.findAll('script', type='application/ld+json')
        for el in elems:
            dict_data = json.loads(el.string, strict=False)[0]
            if dict_data['@type'] == "Book":
                val = dict_data['isbn']
                break
        return val
    def _extract_isbnadd(self, soup):
        val = None
        return val
    
    def _extract_booktype(self, soup, prd):
        book_type = 'book'
        return book_type
    