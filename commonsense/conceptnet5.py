import requests
import pandas as pd
from os import path
import sys

def write_to_csv(filename, relation_type, relation_label, pair_list):
    df = pd.DataFrame({'relation_type': [relation_type], 'relation_label': [relation_label], 'concept_pairs': [pair_list], 'size': [len(pair_list)]})
    if not path.exists(filename):
        df.to_csv(filename, mode='w', encoding='utf_8_sig', index=False, header=['relation_type', 'relation_label', 'concept_pairs', 'size'])
    else:
        df.to_csv(filename, mode='a', encoding='utf_8_sig', index=False, header=False)
    return 

def concept_pairs_scraping():
    relation_type = sys.argv[1]
    relation_label = None
    limit = 20
    total_limit = 1000
    lang = 'en'
    web_domain = 'http://api.conceptnet.io'
    first_page = f'/query?start=/c/{lang}&end=/c/{lang}&rel=/r/{relation_type}&sources=/s/contributor/omcs&limit={limit}'
    next_page = first_page
    concept_pairs = list()
    pair_num = 0
    
    while pair_num < total_limit and next_page != None:
        relation_dict = requests.get(web_domain + next_page).json()
        edges_list = relation_dict['edges']
        try:
            next_page = relation_dict['view']['nextPage']
        except:
            next_page = None
        for sample in edges_list:
            concept_pairs.append((sample['start']['label'], sample['end']['label']))
            pair_num += 1
            if relation_label == None:
                relation_label = sample['rel']['label']

    print(f'relation name is "{relation_type}"')
    print(f'number of edges samples: {len(edges_list)}')
    print('===================================================')
    for pair in concept_pairs: print(pair)
    write_to_csv('relation.csv', relation_type, relation_label, concept_pairs)

def concept_surfaceText_scraping():
    relation_type = sys.argv[1]
    relation_label = None
    limit = 20
    total_limit = 1000
    lang = 'en'
    web_domain = 'http://api.conceptnet.io'
    first_page = f'/query?start=/c/{lang}&end=/c/{lang}&rel=/r/{relation_type}&sources=/s/contributor/omcs&limit={limit}'
    next_page = first_page
    surfaceText_list = list()
    n_surfaceText = 0
    
    while next_page != None:
        relation_dict = requests.get(web_domain + next_page).json()
        edges_list = relation_dict['edges']
        try:
            next_page = relation_dict['view']['nextPage']
        except:
            next_page = None
        for sample in edges_list:
            surfaceText_list.append()
            pair_num += 1
            if relation_label == None:
                relation_label = sample['rel']['label']

    print(f'relation name is "{relation_type}"')
    print(f'number of edges samples: {len(edges_list)}')
    print('===================================================')
    for pair in concept_pairs: print(pair)
    write_to_csv('relation.csv', relation_type, relation_label, concept_pairs)

def main():
    concept_pairs_scraping()    
    return

if __name__ == '__main__':
    main()
