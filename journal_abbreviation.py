raw_abbrev = {
    'Journal of Machine Learning Research': 'JMLR',
    'Transactions on Pattern Analysis and Machine Intelligence': 'TPAMI',
    'Transactions on Image Processing': 'TIP',
    'Transactions on Knowledge and Data Engineering': 'TKDE',
    'Transactions on Information Forensics and Security': 'TIFS',
    'Transactions on Multimedia': 'TMM',
    'Transactions on Signal Processing': 'TSP',
    'Transactions on Wireless Communications': 'TWC',
    'Transactions on Communications': 'TCOMM',
    'Transactions on Networking': 'TON',
    'Transactions on Mobile Computing': 'TMC',
    'Transactions on Parallel and Distributed Systems': 'TPDS',
    'Transactions on Software Engineering': 'TSE',
    'Transactions on Visualization and Computer Graphics': 'TVCG',
    'Transactions on Dependable and Secure Computing': 'TDSC',
    'Transactions on Autonomous and Adaptive Systems': 'TAAS',
    'Transactions on Computational Social Systems': 'TCSS',
    'Transactions on Cyber-Physical Systems': 'TCPS',
    'Transactions on Services Computing': 'TSC',
    'Transactions on Big Data': 'TBD',
    'Transactions on Emerging Topics in Computing': 'TETC',
    'Transactions on Haptics': 'TOH',
    'IEEE Access': 'IEEE Access',
    'arXiv e-prints': 'arXiv',
    'Neural computation': 'Neural Computation',
    'IEEE Signal Processing Magazine': 'IEEE Signal Processing Magazine',
    'International Journal of Computer Vision': 'IJCV',
    'International Journal of Computer Vision and Image Processing': 'IJCVIP',
    'Neuroimage': 'NeuroImage',
    'IEEE Internet of Things Journal': 'IEEE Internet of Things Journal',
    'Electronics': 'Electronics',
    'Optics Letters': 'Optics Letters',
}    

# sort journal_abbrev by keys to ensure the order is consistent.
# To avoid wrong override in multiple matching case, ensure shorter is former. For example, IJCAI is former than IJCAI-ECAI, ICCV is former than ICCVIP.
journal_name = list(raw_abbrev.keys())
journal_name.sort()

# check if the latter is a substring of the former
for i in range(len(journal_name)):
    for j in range(i+1, len(journal_name)):
        if journal_name[j] in journal_name[i] and journal_name[j] != journal_name[i]:
            raise Exception(f'× {journal_name[j]} is a substring of {journal_name[i]}. This will cause wrong override.')
        if raw_abbrev[journal_name[j]] in raw_abbrev[journal_name[i]] and raw_abbrev[journal_name[j]] != raw_abbrev[journal_name[i]]:
            raise Exception(f'× {raw_abbrev[journal_name[j]]} is a substring of {raw_abbrev[journal_name[i]]}. This will cause wrong override.')
journal_abbrev={}
for name in journal_name:
    journal_abbrev[name] = raw_abbrev[name]

if __name__ == "__main__":
    print(journal_abbrev)
