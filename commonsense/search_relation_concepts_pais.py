import pandas as pd
import sys

def search_concept_pairs(filename, relation_type):
    relation_type = relation_type
    dataset = pd.read_csv(filename)
    data = dataset.loc[(dataset['relation_type']==relation_type)]
    relation_label = data['relation_label'].iloc[0].strip()
    print(data)
    print("======================")
    text_list = data['concept_pairs'].iloc[0].strip('[').strip(']').strip('(').strip(')').split('), (')
    for idx, text in enumerate(text_list):
        text = text.split(', ')
        text_list[idx] = [text[0].strip('\''), text[1].strip('\'')]
        print(f'{text_list[idx]}')
    
    return relation_label, text_list

def main():
    search_concept_pairs('relation.csv', sys.argv[1])    
    return

if __name__ == '__main__':
    main()