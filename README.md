## Bib Collector
#### A simple python program to collect BibTeX info from Google Scholar and slim the bib files.

1. Install selenium
>> pip install selenium==4.9.1 
2. Install Chrome/Chromium and Chrome driver
    * Install Chrome or Chromium
    * Check your Chrome/Chromium version, e.g., enter ”chrome://version/“ in the address line
    * Install the corresponding driver from http://chromedriver.storage.googleapis.com/index.html to your_customized_driver_path

3. Modify settings in collect.py:

    >> input_file = 'paper_list.txt'
    
    >> output_file = 'links.txt'
    
    >> output_bib_file = 'bib.txt'
    
    >> chromedriver_path = "your_customized_driver_path"

4. Run in terminal
    * Add the paper titles to input_file line by line.
    * Run the following code:
    >> python collect.py

5. Exception
   * After some running, the program may be interrupted by Google. Run the following line to continue to collect from line xxx
   >> python collect.py xxx

6. Demo:
    ![Alt text](demo/demo.gif)


7. Further Improvements:
    * You can also slim your bib files such as removing unnecessary fields, and formatting the conference abbreviation by running the script **slim.py** .
       * Before slim: 
           ```
           @inproceedings{dong2020adversarial,
           author = {Yinpeng Dong and
           Zhijie Deng and
           Tianyu Pang and
           Jun Zhu and
           Hang Su},
           bibsource = {dblp computer science bibliography, https://dblp.org},
           biburl = {https://dblp.org/rec/conf/nips/DongDP0020.bib},
           booktitle = {Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December
           6-12, 2020, virtual},
           editor = {Hugo Larochelle and
           Marc'Aurelio Ranzato and
           Raia Hadsell and
           Maria{-}Florina Balcan and
           Hsuan{-}Tien Lin},
           timestamp = {Tue, 19 Jan 2021 00:00:00 +0100},
           title = {Adversarial Distributional Training for Robust Deep Learning},
           url = {https://proceedings.neurips.cc/paper/2020/hash/5de8a36008b04a6167761fa19b61aa6c-Abstract.html},
           year = {2020}
           }
           ```
       * After slim:
           ```
           @inproceedings{dong2020adversarial,
           title = {Adversarial Distributional Training for Robust Deep Learning},
           author = {Yinpeng Dong and Zhijie Deng and Tianyu Pang and Jun Zhu and Hang Su},
           booktitle = {NeurIPS 2020},
           year = {2020}
           }
           ```
   * The link to the papers is stored and you can download the papers in PDF format by running 
       >> python download_papers.py

* Other recommend resources
    * Rebiber: A tool for normalizing bibtex with official info: https://github.com/yuchenlin/rebiber
