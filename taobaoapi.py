# -*- coding: utf-8 -*-
import csv
import selenium
from lxml import etree
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

from selenium.webdriver.support.wait import WebDriverWait
broswer = webdriver.Chrome()
broswer.set_window_size(720,480)
wait = WebDriverWait(broswer, 10)
def get_api(url):
    broswer.get(url)
    targetElem = broswer.find_element_by_xpath('//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/form/div[8]/div[2]/button')
    broswer.execute_script("arguments[0].scrollIntoView();", targetElem)

    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#parent_cid'))
    )
    input.send_keys('0')
    button =wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'#container > div.doc.hide-summary.show-nav > div.container > div.doc-content > div.api-document-tool > div.flex > form > div:nth-child(10) > div.next-col.next-col-16.next-form-item-control > button'))
    )

    button.click()
    parse_api(broswer)

def parse_api(broswer):

    time.sleep(4)

    #wait.until(lambda brower: brower.find_element_by_css_selector('//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]'))
    response = broswer.find_element_by_xpath('//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]')
    contents = response.find_element_by_xpath('//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]').text
    contents =json.loads(contents)
    print(contents['itemcats_get_response']['item_cats']['item_cat'])
    item = {}
    try:
        for content in contents['itemcats_get_response']['item_cats']['item_cat']:
            item['cid'] = content['cid']
            item['is_parent']= content['is_parent']
            item['name'] =content['name']
            item['parent_cid'] =content['parent_cid']
            print(item)
            save_csv('api2.csv', item)
            if item['is_parent']==True:
                    get_info(broswer,item['cid'])
                    parse_api(broswer)
                    # cid_list =set()
                    # cid_list.add(item['cid'])
                    # for cid in cid_list:
                    #     get_info(broswer,cid)


            #yield item['cid']
    except KeyError:
        pass

def get_info(broswer,keyword):

    targetElem = broswer.find_element_by_xpath(
        '//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/form/div[8]/div[2]/button')
    broswer.execute_script("arguments[0].scrollIntoView();", targetElem)
    time.sleep(2)
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#parent_cid'))
    )
    input.clear()
    input.send_keys(str(keyword))
    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '#container > div.doc.hide-summary.show-nav > div.container > div.doc-content > div.api-document-tool > div.flex > form > div:nth-child(10) > div.next-col.next-col-16.next-form-item-control > button'))
    )

    button.click()
    #return broswer
    parse_info(broswer)

def parse_info(broswer):
    # wait.until(lambda broswer: brower.find_element_by_css_selector('//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]'))
    response = broswer.find_element_by_xpath(
        '//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]')
    contents = response.find_element_by_xpath(
        '//*[@id="container"]/div[1]/div[4]/div[2]/div[2]/div[2]/div/form/div[2]/div[2]/div/div[2]').text
    contents = json.loads(contents)

    print(contents)
    item = {}
    try:
        for content in contents['itemcats_get_response']['item_cats']['item_cat']:
            item['cid'] = content['cid']
            item['name'] = content['name']
            item['parent_cid'] = content['parent_cid']
            #yield item['cid']
            print(item)
            save_csv('taobaoapi2.csv',item)
    except KeyError:
        pass



def save_csv(filename,data):
    with open(filename, 'a',newline='', errors='ignore') as f:
        writer =csv.writer(f)
        #writer.writerow(('cid','name','parent_cid'))
        writer.writerow(data.values())

if __name__ == '__main__':
    url='http://open.taobao.com/doc.htm?spm=a219a.7386653.0.0.JAHWyP&docId=1&docType=15&apiName=taobao.itemcats.get'
    get_api(url)
    for keyword in parse_api(broswer):
        time.sleep(3)
        get_info(broswer,keyword)

