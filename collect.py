from selenium import webdriver
import time 
from selenium.webdriver.common.by import By

import random
import sys 

# modified from https://zhuanlan.zhihu.com/p/448630104
def extract_href(input_file, output_file, output_bib_file, chrome_driver, begin_index = 0):
    '''
    input_file: a txt file containing the paper titles
    output_file: a txt file containing the links to the bibtex files
    output_bib_file: a txt file containing the raw bibtex files
    chrome_driver: the path to the chrome driver
    begin_index: the index of the first paper. Used when the program is interrupted.
    '''
    scholars = open(input_file)
    file_out = open(output_file,'a+')
    file_bib_out = open(output_bib_file, 'a+')
    file_url_download = open('url_download.txt','a+')
    scholars = scholars.readlines()
    browser = webdriver.Chrome(executable_path=chrome_driver)
    url = "https://scholar.google.com"
    browser.get(url)
    links = []
    bibs = []
    failed = []
    current_line = begin_index

    for tt in scholars[begin_index:]:
        tt = tt.strip().split('\t')
        print(tt[0])
        tt = tt[-1]
        browser.get(url)
        time.sleep(random.uniform(0.5,1.5))

        browser.find_element(by=By.XPATH, value = '//*[@name="q"]').send_keys(tt)
        for tt in scholars[begin_index:]:
        tt = tt.strip().split('\t')
        print(tt[0])
        tt = tt[-1]
        browser.get(url)
        time.sleep(random.uniform(0.5,1.5))
        print('begin')
        browser.find_element(by=By.XPATH, value = '//*[@name="q"]').send_keys(tt)
        try:
            browser.find_element(by=By.XPATH,value = '//*[@name="btnG"]').click()
            # get citation number of format 'Cited by 1234'. Only the number is kept and only the first result is considered.
            if "学术搜索" in browser.title:
                citation_str = browser.find_element(by=By.XPATH,value = '//*[contains(text(),"被引用次数")]')
            else:
                citation_str = browser.find_element(by=By.XPATH,value = '//*[contains(text(),"Cited by")]')
            print(citation_str.text)
            # fetch the number of citations
            citation_number = int(re.findall(r'\d+', citation_str.text)[0])
            
            download_link = browser.find_element(by=By.XPATH,value = '//*[@data-clk]').get_attribute('href')
            browser.find_element(by=By.XPATH,value = '//*[@class="gs_or_cit gs_or_btn gs_nph"]').click()
            time.sleep(random.uniform(0.5,1.5))
    
            link = browser.find_element(by=By.XPATH,value = '//*[@class="gs_citi"]').get_attribute('href')
            
            print(link)
            print(download_link)
            if link not in links:
                links.append(link)
                file_out.write(link+'\n')
            
            browser.get(link)
            text = browser.find_element(by=By.XPATH,value = '/html/body/pre')  
            text = text.text + '\n'
            file_bib_out.writelines(text)
            file_url_download.write(f"{tt},{download_link},{citation_number}\n")
            bibs.append(text)
        except:
            print('[*****************************]')
            failed.append(tt)
            continue
        print('>> current line:', current_line)
        current_line+=1

    print(links)
    print(bibs)
    file_out.close()
    file_bib_out.close()

input_file = 'paper_list.txt'
output_file = 'links.txt'
output_bib_file = 'raw_bib.txt'
chromedriver_path = "your_customer_driver_path"

if len(sys.argv)>1:
    print(sys.argv)
    extract_href(input_file, output_file, output_bib_file, chromedriver_path, begin_index=int(sys.argv[1]))    
else:
    extract_href(input_file, output_file, output_bib_file, chromedriver_path)
