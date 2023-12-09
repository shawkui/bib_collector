''' 
A program to slim down the bib file to ignore some unnecessary details.
Only keep the following fields (if any):
title
author
booktitle
pages
year
organization
journal
volume
number

Example of input:

@inproceedings{dong2020adversarial,
 author = {Yinpeng Dong and
Zhijie Deng and
Tianyu Pang and
Jun Zhu and
Hang Su},
 bibsource = {dblp computer science bibliography, https://dblp.org},
 biburl = {https://dblp.org/rec/conf/nips/DongDP0020.bib},
 booktitle = {Advances in Neural Information Processing Systems 33: Annual Conference
on Neural Information Processing Systems 2020, NeurIPS 2020, December
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

Example of output:

@inproceedings{dong2020adversarial,
title = {Adversarial Distributional Training for Robust Deep Learning},
author = {Yinpeng Dong and Zhijie Deng and Tianyu Pang and Jun Zhu and Hang Su},
booktitle = {NeurIPS 2020},
year = {2020}
}

Format of the BibTeX file:
* each entry starts with @ and its abbreviation, for example, @inproceedings{abbr,
* each entry ends with } in a new line without any other characters.


Usage:
1. Customize the input_file and output_file in the code
    python slim.py input_file output_file

2. Use default input_file and output_file:
    python slim.py

Hint: To save the log to a file, use the following command:
    python slim.py > log.txt


Caveats:
1. The code is not robust enough. If the BibTeX file is not well-formatted, the code may fail. Please check the output file and the error message in your tex editor.
2. The code is not well tested. If you find any bugs, please contact me or raise an issue.
3. The code is not optimized. If you have any suggestions, please contact me or raise an issue.
'''

import re
import sys
from conference_abbreviation import conference_abbrev
from journal_abbreviation import journal_abbrev


def slim_bib_file(input_file, output_file, auto_fix=True, verbose=True, do_abbrev_conf=False, do_abbrev_journal=False):
    '''
    A function to slim down the BibTeX file to ignore some unnecessary details.

    input_file: the path to the input BibTeX file
    output_file: the path to the output BibTeX file
    conf_slim: whether to slim down the conference name
    auto_fix: whether to automatically fix the conference name in journal field
    verbose: whether to print the details
    '''

    # Fields to keep
    fields_to_keep_conf = ['title', 'author', 'booktitle', 'journal', 'year']

    fileds_to_keep_journal = ['title', 'author', 'booktitle', 'journal', 'volume', 'pages', 'number', 'year']

    # Load conference and journal name
    conf_name = list(conference_abbrev.keys())
    conf_abbrev = list(conference_abbrev.values())
    jpur_name = list(journal_abbrev.keys())
    jour_abbrev = list(journal_abbrev.values())

    with open(input_file, 'r') as file:
        bib_data = file.read()
        
    # replace \n any space } any space \n to \n}\n
    bib_data = re.sub(r'\n\s*\}\s*\n', '\n}\n', bib_data)
    # replace any }}\n to }\n}\n
    bib_data = re.sub(r'\}\}\n', '}\n}\n', bib_data)
    
    # Find all BibTeX entries
    entries = re.findall(r'(@.*?\{.*?\n.*?\n}|\})', bib_data, re.DOTALL)
    slim_entries = []
    
    # check the number of @ and the number of entries:
    if bib_data.count('@') != len(entries):
        raise Exception(f'× Error: The number of @ is not equal to the number of detected entries. Some entries may be missing. Please check the input file: {input_file}. You can aslo comment out this line to ignore this error.')
    
    for entry_index_i, entry in enumerate(entries):
        print(f'\nProcessing entry {entry_index_i+1}/{len(entries)}, Entry name: {entry.split("{")[1].split(",")[0]}')
        abbrev_type = None
        vennue = None
        # get the infor for booktitle = {xxx} or journal = {xxx} or booktitle={xxx} or journal={xxx}
        if 'booktitle' in entry:
            vennue = re.findall(r'booktitle\s*=\s*\{(.*)', entry)[0]
        if 'journal' in entry:
            vennue = re.findall(r'journal\s*=\s*\{(.*)', entry)[0]

        if vennue is None:
            print(f'× Error: Failed to find the booktitle or journal for {entry}.')
        else:
            # Check if the entry is a conference paper or a journal paper by checking if conf_name or conf_abbrev is in the entry and if jpur_name or jour_abbrev is in the entry
            if any(conf_name_i.lower() in vennue.lower() for conf_name_i in conf_name) or any(conf_abbrev_i.lower() in vennue.lower() for conf_abbrev_i in conf_abbrev):
                abbrev_type = 'conference'
                fields_to_keep = fields_to_keep_conf 
                abbrev_dict = conference_abbrev
                do_abbrev = do_abbrev_conf
                
            if any(jpur_name_i.lower() in vennue.lower() for jpur_name_i in jpur_name) or any(jour_abbrev_i.lower() in vennue.lower() for jour_abbrev_i in jour_abbrev):
                if abbrev_type == 'conference':
                    # print all matched conference name and journal name
                    print(f'Vennue: {vennue}')
                    for conf_name_i in conf_name:
                        if conf_name_i.lower() in vennue.lower():
                            print(f'- Warning: {conf_name_i} is matched in the vennue')
                    for conf_abbrev_i in conf_abbrev:
                        if conf_abbrev_i.lower() in vennue.lower():
                            print(f'- Warning: {conf_abbrev_i} is matched in the vennue')
                    for jpur_name_i in jpur_name:
                        if jpur_name_i.lower() in vennue.lower():
                            print(f'- Warning: {jpur_name_i} is matched in the vennue')
                    for jour_abbrev_i in jour_abbrev:
                        if jour_abbrev_i.lower() in vennue.lower():
                            print(f'- Warning: {jour_abbrev_i} is matched in the vennue')
                    raise Exception(f'× Error: The entry is both a conference paper and a journal paper. Please check the input file: {input_file}. You can aslo comment out this line to ignore this error.')
                abbrev_type = 'journal'
                fields_to_keep = fileds_to_keep_journal
                abbrev_dict = journal_abbrev
                do_abbrev = do_abbrev_journal
        print('Detect entry type: ', abbrev_type)
        
        if abbrev_type is None:
            # default to use conference
            do_abbrev = do_abbrev_conf
            abbrev_dict = conference_abbrev
            fields_to_keep = fields_to_keep_conf
                   
        slim_entry = process_one_entry(entry, fields_to_keep, abbrev_dict, do_abbrev, verbose, auto_fix, abbrev_type)    
        slim_entries.append(slim_entry)

    # Write slimmed-down entries to the output file
    with open(output_file, 'w') as file:
        file.write('\n\n'.join(slim_entries))

    print(
        f"\nSuccessfully slimmed down the BibTeX file. Saved to {output_file}.")


def process_one_entry(entry, fields_to_keep, abbrev_dict, do_abbrev, verbose, auto_fix, abbrev_type):
    '''
    A function to slim down one entry.
    
    input:
        entry: one entry in the BibTeX file
        fields_to_keep: the fields to keep
        abbrev_dict: the abbreviation dictionary. If no matched conference, no abbreviation will be done.
        do_abbrev: whether to do abbreviation
        verbose: whether to print the details
        auto_fix: whether to automatically fix the conference name in journal field
        abbrev_type: the type of the entry, conference or journal. If None, default to conference.
    
    return:
        slim_entry: the slimmed-down entry    
    '''
    
    lines = entry.strip().split('\n')
        
    if lines[0].strip().split('{')[1] == '':
        raise Exception(f'× Failed to find the id of the entry: {lines[0]} for \n{entry}')

    entry_dict = {'begin': lines[0], 'end': '}'}

    multiline_field = False
    for current_line in lines:
        line = current_line.strip()

        if multiline_field:
            # only when the field is multiline and field name is in fields_to_keep, keep the line
            # slim_entry.append(line)
            new_line += ' '
            new_line += line
            if line.endswith('},'):
                multiline_field = False
                entry_dict[key] = new_line
        else:
            if '=' in line:
                key = line.split('=')[0].strip()
                if key.lower() in fields_to_keep:
                    if line.endswith('},'):
                        # normal case
                        multiline_field = False
                        entry_dict[key] = line
                    elif line.endswith('}') and current_line is lines[-2]:
                        # special case: the last field of the entry which does not end with a comma
                        multiline_field = False
                        entry_dict[key] = line
                    else:
                        # multiline field
                        multiline_field = True
                        new_line = line
                else:
                    multiline_field = False
                    
    if 'booktitle' in entry_dict.keys() :
        original_booktitle = entry_dict['booktitle']
        booktitle_type = 'booktitle'
        
    elif 'journal' in entry_dict.keys():
        original_booktitle = entry_dict['journal']
        booktitle_type = 'journal'

    else:
        # print warning and return the original entry
        print(f'× Error: Failed to find the booktitle or journal for {entry_dict["begin"]}.')
        booktitle_type = None
    
    if booktitle_type is not None:
        # Do abbreviation and autofix
        year = re.findall(r'\{(\d+)\}', entry_dict['year'])[0]
        success = False
        for conf_or_jour in abbrev_dict.keys():
            # check if the conference name is in the original booktitle or the abbreviation is in the original booktitle
            if conf_or_jour.lower() in original_booktitle.lower() or abbrev_dict[conf_or_jour].lower() in original_booktitle.lower():
                if success:
                    print(f'- Warning: Match multiple conference name !!!')
                    print(f'- Warning: original_booktitle: {original_booktitle} last matched conference: {entry_dict["booktitle"]}, current matched conference: {conf_or_jour}')

                if do_abbrev:
                    entry_dict[booktitle_type] = f"{booktitle_type} = {{{abbrev_dict[conf_or_jour]}}},"
                else:
                    entry_dict[booktitle_type] = f"{booktitle_type} = {{{conf_or_jour}}},"                

                if verbose:
                    if do_abbrev:
                        print(f'√ {original_booktitle} => matched conference: {conf_or_jour} =>  booktitle = {{{abbrev_dict[conf_or_jour]}}},')
                    else:
                        print(f'√ {original_booktitle} => matched conference: {conf_or_jour} =>  booktitle = {{{conf_or_jour}}},')

                success = True
        if not success:
            print(
                f"× Error: Failed to find the conference/journal name for {original_booktitle}.")
        
        # # IMPORTANT: To generate correct reference, inproceedings should be used for conference paper and article should be used for journal paper.
        # # The below code will detect the conference in Journal format and fix it.
        if auto_fix and abbrev_type!=booktitle_type:
            # if the entry is a conference paper
            if abbrev_type == 'conference':
                # if not begin with @inproceedings, fix it
                if entry_dict['begin'].startswith('@article'):
                    entry_dict['begin'] = entry_dict['begin'].replace('@article', '@inproceedings') 
                    print('>>> Detect conference paper in @article. Fix it.')
                if booktitle_type != 'booktitle' and entry_dict['begin'].startswith('@inproceedings'):
                    # add booktitle field and remove old one
                    entry_dict['booktitle'] = entry_dict[booktitle_type].replace(booktitle_type, 'booktitle')
                    del entry_dict[booktitle_type]
                    print('>>> Detect conference paper not in booktitle. Fix it.')

            # if the entry is a journal paper
            if abbrev_type == 'journal':
                # if not begin with @article, fix it
                if entry_dict['begin'].startswith('@inproceedings'):
                    entry_dict['begin'] = entry_dict['begin'].replace('@inproceedings', '@article') 
                    print('>>> Detect journal paper in @inproceedings. Fix it.')
                if booktitle_type != 'journal' and entry_dict['begin'].startswith('@article'):
                    # add journal field and remove old one
                    entry_dict['journal'] = entry_dict[booktitle_type].replace(booktitle_type, 'journal')
                    del entry_dict[booktitle_type]
                    print('>>> Detect journal paper not in journal. Fix it.')

    # Construct the slimmed-down entry
    slim_entry = [entry_dict['begin']]
    for key in fields_to_keep:
        if key in entry_dict:
            if entry_dict[key].endswith('}') and key != fields_to_keep[-1]:
                # Add comma to fields before last line
                entry_dict[key]+=','

            if entry_dict[key].endswith('},') and key == fields_to_keep[-1]:
                # remove comma in the last line
                entry_dict[key] = entry_dict[key][:-1]

            slim_entry.append(entry_dict[key])

    slim_entry.append(entry_dict['end'])
    return '\n'.join(slim_entry)

# check input arguments, if empty, use default
if len(sys.argv) == 1:
    input_file = 'raw_bib.txt'
    output_file = 'output.bib'
elif len(sys.argv) == 2:
    input_file = sys.argv[1]
    output_file = 'output.bib'
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

slim_bib_file(input_file, output_file)
# Show caveats
print('\n>>> The Code is not robust enough. If the BibTeX file is not well-formatted, the code may fail. Please check the output file and the error message in your tex editor.')