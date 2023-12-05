raw_abbrev = {
    'Advances in Neural Information Processing Systems': 'NeurIPS', 
    'Annual Computer Security Applications Conference': 'ACSAC',
    'Association for the Advancement of Artificial Intelligence': 'AAAI', 
    'Asian Conference on Machine Learning': 'ACML',
    'Conference on Computer and Communications Security': 'CCS',
    'Conference on Computer Vision and Pattern Recognition': 'CVPR',
    'Conference on Empirical Methods in Natural Language Processing': 'EMNLP',
    'Conference on Neural Information Processing Systems': 'NeurIPS',
    'Conference on Neural Information Processing Systems Datasets and Benchmarks Track': 'NeurIPS Datasets and Benchmarks Track',
    'ACM International Conference on Multimedia': 'ACM Multimedia', 
    'European Conference on Computer Vision': 'ECCV', 
    'European Signal Processing Conference': 'EUSIPCO',
    'European Symposium on Research in Computer Security': 'ESORICS',
    'Findings of the Association for Computational Linguistics': 'ACL',
    'NIPS': 'NIPS', # alias
    'Network and Distributed System Security Symposium': 'NDSS Symposium',
    'International Conference on Machine Learning': 'ICML', 
    'International Conference on Multimedia and Expo': 'ICME',
    'International Conference on Learning Representations': 'ICLR', 
    'International Conference on Computer Vision': 'ICCV', 
    'International Conference on Computer Vision and Graphics': 'ICCVG',
    'International Conference on Computer Vision and Image Processing': 'ICCVIP',
    'International Conference on Computer Vision Theory and Applications': 'VISAPP',
    'International Joint Conference on Artificial Intelligence': 'IJCAI', 
    'International Conference on Pattern Recognition': 'ICPR',
    'International Conference on Robotics and Automation': 'ICRA', 
    'International Conference on Intelligent Robots and Systems': 'IROS', 
    'International Conference on Acoustics, Speech and Signal Processing': 'ICASSP',
    'International Conference on Data Mining': 'ICDM',
    'International Conference on Image Processing': 'ICIP',
    'International Conference on Multimedia and Expo': 'ICME',
    'International Conference on Parallel and Distributed Systems': 'ICPADS',
    'international joint conference on neural networks' : 'IJCNN',    
    'International Symposium on Computer Architecture': 'ISCA',
    'International symposium on Information theory': 'ISIT',
    'IEEE Conference on Computer Communications': 'INFOCOM',
    'International Conference of the Biometrics Special Interest Group': 'BIOSIG',
    'International conference on artificial intelligence and statistics': 'AISTATS',
    'ACM SIGKDD Conference on Knowledge Discovery and Data Mining': 'KDD',
    'Machine Learning and Knowledge Discovery in Databases: European Conference': 'ECML-PKDD',
    'Pattern Recognition and Computer Vision': 'PRCV',
    'Pacific-Asia conference on knowledge discovery and data mining': 'PAKDD',
    'Robotics: Science and Systems': 'RSS', 
    'Research in Attacks, Intrusions, and Defenses': 'RAID',
    'Winter Conference on Applications of Computer Vision': 'WACV',
    r'Annual International Conference of the {IEEE} Engineering in Medicine \& Biology Society': 'EMBC',
    'ACM International Conference on Information and Knowledge Management': 'CIKM',
    'International Conference on Computer Aided Verification': 'CAV',
    'Symposium on Security and Privacy': 'S\&P',
    'Security and Privacy Workshops': 'SPW',
    'Uncertainty in Artificial Intelligence': 'UAI',
    'USENIX Security Symposium': 'USENIX Security',
    r'{USENIX} Security Symposium': 'USENIX Security',
}    

# sort conference_abbrev by keys to ensure the order is consistent.
# To avoid wrong override in multiple matching case, ensure shorter is former. For example, IJCAI is former than IJCAI-ECAI, ICCV is former than ICCVIP.
conference_name = list(raw_abbrev.keys())
conference_name.sort()

# check if the latter is a substring of the former
for i in range(len(conference_name)):
    for j in range(i+1, len(conference_name)):
        if conference_name[j] in conference_name[i] and conference_name[j] != conference_name[i]:
            raise Exception(f'× {conference_name[j]} is a substring of {conference_name[i]}. This will cause wrong override.')
        if raw_abbrev[conference_name[j]] in raw_abbrev[conference_name[i]] and raw_abbrev[conference_name[j]] != raw_abbrev[conference_name[i]]:
            raise Exception(f'× {raw_abbrev[conference_name[j]]} is a substring of {raw_abbrev[conference_name[i]]}. This will cause wrong override.')
conference_abbrev={}
for name in conference_name:
    conference_abbrev[name] = raw_abbrev[name]

if __name__ == "__main__":
    print(conference_abbrev)
