# read paper title and download link from url_download.txt
# example: paper_name, download_link
# the paper will be downloaded to the folder 'pdf'
# Note:
#     1. If the paper is already downloaded, it will be skipped.
#     2. If the download link is not valid, it will be skipped.
#     3. If the download link is from arxiv, it will be converted to pdf link.
#     4. If mirror_dict is not empty, the download link will be converted to the mirror link.



import os
import time
import random
import requests
import tqdm
import re
import sys

def download_paper(url, output_file):
    if not os.path.exists('pdf'):
        os.mkdir('pdf')
    # allow redirect
    try:
        if sys.platform == 'linux':
            print('use wget to download paper {} to {}'.format(url, output_file))
            os.system(f'wget "{url}" -O "{output_file}"')
            return 200
        r = requests.get(url, allow_redirects=True)
    except:
        # switch to wget
        # if the system is linux, use wget
            
        print('failed to download paper:', url)
        return -1

    if r.status_code == 200:
        with open(output_file, 'wb') as f:
            # show progress bar
            for chunk in tqdm.tqdm(r.iter_content(1024), total=int(r.headers['Content-Length']) // 1024):
                f.write(chunk)
                
    else:
        print('failed to download paper:', url)
    return r.status_code

url_file = 'url_download.txt'
skip_web = []
mirror_dict = {'https://arxiv.org':'http://xxx.itp.ac.cn'}
last_web = 'https://arxiv.org'
with open(url_file) as f:
    for line in f:
        line = line.strip().split(',')
        paper_name = line[0]
        download_link = line[1]

        # check the feasibility of the paper name, remove invalid characters
        paper_name = re.sub(r'[\\/*?:"<>|]', ' ', paper_name)
        
        output_file = f'pdf/{paper_name}.pdf'

        if os.path.exists(output_file):
            # check if the paper is already downloaded
            if os.path.getsize(output_file) > 0:
                print('skip:', paper_name)
                continue
            else:
                print('redownload:', paper_name)
                os.remove(output_file)

        if any([web in download_link for web in skip_web]):
            print('skip:', paper_name)
            continue

        # avoid downloading too fast
        if last_web not in download_link:
            time.sleep(random.uniform(0.5, 1.5))
        else:
            time.sleep(random.uniform(4,5))

        last_web = download_link.split('/')[2]
        
        # only keep wed until the first '.pdf'
        download_link = download_link.split('.pdf')[0] + '.pdf'
        
        # Use mirror site to download paper if possible
        for web in mirror_dict:
            if web in download_link:
                download_link = download_link.replace(web, mirror_dict[web])
                break

        print(f'downloading: {paper_name} from {download_link}')
        download_paper(download_link, output_file)
    
