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
'''

import re
from conference_abbreviation import conference_abbrev


def slim_bib_file(input_file, output_file, conf_slim=True, auto_fix=True, verbose=True,):
    '''
    A function to slim down the BibTeX file to ignore some unnecessary details.

    input_file: the path to the input BibTeX file
    output_file: the path to the output BibTeX file
    conf_slim: whether to slim down the conference name
    auto_fix: whether to automatically fix the conference name in journal field
    verbose: whether to print the details
    '''

    # Fields to keep
    fields_to_keep = ['title', 'author', 'booktitle', 'journal', 'publisher',
                      'volume', 'pages',  'number', 'organization', 'year']

    with open(input_file, 'r') as file:
        bib_data = file.read()

    # Find all BibTeX entries
    entries = re.findall(r'(@.*?\{.*?\n.*?\n}|\})', bib_data, re.DOTALL)
    slim_entries = []
    for entry in entries:
        lines = entry.strip().split('\n')

        # Remove unnecessary fields from each entry
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
                        
        # format the conference name
        # for booktitle, replace the original booktitle with the abbreviation
        if conf_slim and 'booktitle' in entry_dict.keys():
            original_booktitle = entry_dict['booktitle']
            year = re.findall(r'\{(\d+)\}', entry_dict['year'])[0]
            success = False
            for conf in conference_abbrev.keys():
                # check if the conference name is in the original booktitle or the abbreviation is in the original booktitle
                if conf.lower() in original_booktitle.lower() or conference_abbrev[conf].lower() in original_booktitle.lower():
                    if success:
                        print(f'Warning: Match multiple conference name !!!')
                        print(f'Warning: original_booktitle: {original_booktitle}, current conference: {conf}')
                    entry_dict['booktitle'] = f"booktitle = {{{conference_abbrev[conf]} {year}}},"
                    if verbose:
                        print(f'√ {original_booktitle} =>  booktitle = {{{conference_abbrev[conf]} {year}}},')
                    success = True
            if not success:
                print(
                    f"× Failed to find the conference name for {original_booktitle}.")
        
        # # IMPORTANT: some papers use journal instead of booktitle for conference papers, which is not standard and may have some problems for generating reference.
        # # To generate correct reference, journal field begin with @article, booktitle filed begin with @inproceedings.
        # # The below code will detect the conference in Journal format and fix it.
        if auto_fix and conf_slim and 'journal' in entry_dict.keys():
            original_booktitle = entry_dict['journal']
            year = re.findall(r'\{(\d+)\}', entry_dict['year'])[0]
            success = False
            for conf in conference_abbrev.keys():
                # check if the conference name is in the original booktitle or the abbreviation is in the original booktitle
                if conf.lower() in original_booktitle.lower() or conference_abbrev[conf].lower() in original_booktitle.lower():
                    print('>>> Detect conference name in journal field. <<<')
                    if success:
                        print(f'Warning: Match multiple conference name !!!')
                        print(f'Warning: original_booktitle: {original_booktitle}, current conference: {conf}')

                    entry_dict['booktitle'] = f"booktitle = {{{conference_abbrev[conf]} {year}}},"
                    print(f'>>> {entry_dict["journal"]} =>  booktitle = {{{conference_abbrev[conf]} {year}}},')

                    if '@article' in  entry_dict['begin']:
                        entry_dict['begin'] = entry_dict['begin'].replace('@article', '@inproceedings') 
                        print(f'>>> @article => @inproceedings')

                    success = True
                    print('>>> Fix conference name in journal field. <<<')

            if success:
                del entry_dict['journal']

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

        slim_entries.append('\n'.join(slim_entry))

    # Write slimmed-down entries to the output file
    with open(output_file, 'w') as file:
        file.write('\n\n'.join(slim_entries))

    print(
        f"Successfully slimmed down the BibTeX file. Saved to {output_file}.")


# Usage example
input_file = 'raw_bib.txt'
output_file = 'output.bib'
slim_bib_file(input_file, output_file)
