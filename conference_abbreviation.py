raw_abbrev = {
    'Advances in Neural Information Processing Systems': 'NeurIPS', 
    'Association for the Advancement of Artificial Intelligence': 'AAAI', 
    'Asian Conference on Machine Learning': 'ACML',
    'Conference on Computer Vision and Pattern Recognition': 'CVPR',
    'Conference on Empirical Methods in Natural Language Processing': 'EMNLP',
    'Conference on Neural Information Processing Systems Datasets and Benchmarks Track': 'NeurIPS Datasets and Benchmarks Track',
    'European Conference on Computer Vision': 'ECCV', 
    'European Signal Processing Conference': 'EUSIPCO',
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
    'International Conference on Robotics and Automation': 'ICRA', 
    'International Conference on Intelligent Robots and Systems': 'IROS', 
    'International Conference on Acoustics, Speech and Signal Processing': 'ICASSP',
    'International Conference on Data Mining': 'ICDM',
    'International Conference on Image Processing': 'ICIP',
    'International Conference on Multimedia and Expo': 'ICME',
    'international joint conference on neural networks' : 'IJCNN',    
    'International symposium on Information theory': 'ISIT',
    'Pattern Recognition and Computer Vision': 'PRCV',
    'Robotics: Science and Systems': 'RSS', 
    'Research in Attacks, Intrusions, and Defenses': 'RAID',
    'Uncertainty in Artificial Intelligence': 'UAI',
}    

# sort conference_abbrev by keys to ensure the order is consistent.
# To avoid wrong override in multiple matching case, ensure shorter is former. For example, IJCAI is former than IJCAI-ECAI, ICCV is former than ICCVIP.
conference_name = list(raw_abbrev.keys())
conference_name.sort()
conference_abbrev={}
for name in conference_name:
    conference_abbrev[name] = raw_abbrev[name]

if __name__ == "__main__":
    print(conference_abbrev)
