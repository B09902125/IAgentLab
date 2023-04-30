import pandas as pd
import sys

def search_case(filename, relation_type, obj_1, obj_2):
    dataset = pd.read_csv(filename)
    data = dataset.loc[(dataset['relation_type']==relation_type) & (dataset['obj_1']==obj_1) & (dataset['obj_2']==obj_2)]
    print(data)
    text_list = data['generative_text'][0].strip('[').strip(']').split(', ')
    for text in text_list:
        print(text)
    return

def length_of_undo(filename, relation_type):
    dataset = pd.read_csv(filename)
    data = dataset.loc[(dataset['relation_type']==relation_type)]
    print(len(data))

def main():
    # search_case('test.csv', sys.argv[1], sys.argv[2], sys.argv[3])
    length_of_undo('test.csv', 'CreatedBy')
    return 

if __name__ == '__main__':
    main()
