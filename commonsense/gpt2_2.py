from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed
from transformers.generation.configuration_utils import GenerationConfig
import pandas as pd
from os import path
from tqdm import tqdm
import torch
import sys
from search_relation_concepts_pais import search_concept_pairs

def write_to_csv(filename, relation_type, relation_label, object_1, object_2, samples, rank_1_w, rank_2_w, rank_3_w, acc):
    data = {'relation_type':[relation_type], 'relation_label': [relation_label], 'obj_1': [object_1], 'obj_2': [object_2], 'generative_text':[samples], 'Rank1_word': [rank_1_w], 'Rank2_word': [rank_2_w], 'Rank3_word': [rank_3_w], 'accuracy': [acc]}
    df = pd.DataFrame(data=data)
    print(df)
    if not path.exists(filename):
        df.to_csv(filename, mode='w', encoding='utf_8_sig', index=False, header=['relation_type', 'relation_label', 'obj_1', 'obj_2', 'generative_text', 'Rank1_word', 'Rank2_word', 'Rank3_word', 'accuracy'])
    else:
        df.to_csv(filename, mode='a', encoding='utf_8_sig', index=False, header=False)
        
    return

def sample_analysis(prompt, object_2, generated_sample, size):
    freq_dict = dict()
    samples = list()
    for idx, sample in enumerate(generated_sample):
        sample = sample['generated_text'].replace(prompt, '').split('\n')[0].strip()
        samples.append(sample)
        try:
            freq_dict[sample] += 1
        except:
            freq_dict[sample] = 1

    sorted_list = [(key, value) for key, value in sorted(freq_dict.items(), key=(lambda item: item[1]), reverse=True)]
    
    try: 
        rank1_w = sorted_list[0][0]
    except:
        rank1_w = None
    try:
        rank2_w = sorted_list[1][0]
    except:
        rank2_w = None
    try:        
        rank3_w = sorted_list[2][0]
    except:
        rank3_w = None
    
    for key in freq_dict.keys():
        if object_2 in key:
            acc = float(freq_dict[key]) / float(size)
            break
    else:
        acc = 0.0
    
    return samples, rank1_w, rank2_w, rank3_w, acc 
    
def commomsense_test(relation_filename, test_filename, model_name, relation_type):
    config = GenerationConfig.from_pretrained(model_name)
    config.max_new_tokens = 12
    # config.early_stopping = True
    config.temperature = 0.1
    config.num_beams = 256
    config.num_return_sequences = 20
    # set_seed(42)

    example1_object_1 = 'A cake'
    example1_object_2 = 'eggs'
    example2_object_1 = 'A book'
    example2_object_2 = 'paper'
    example3_object_1 = 'Desks'
    example3_object_2 = 'wood'
    
    _, obj_pair_list = search_concept_pairs(relation_filename, relation_type)
    relation_label = 'is made of'
    obj_pair_list = obj_pair_list[138:]
    for obj_pair in tqdm(obj_pair_list):
        object_1 = obj_pair[0]
        object_1[0].upper()
        object_2 = obj_pair[1]
        
        example = f"###\nObject 1: {example1_object_1}\nrelation: {relation_label}\nObject 2: {example1_object_2}\n###\nObject 1: {example2_object_1}\nrelation: {relation_label}\nObject 2: {example2_object_2}\n###\nObject 1: {example3_object_1}\nrelation: {relation_label}\nObject 2: {example3_object_2}\n"
        question = f'###\nObject 1: {object_1}\nrelation: {relation_label}\nObject 2:'
        prompt = example+question
        
        generator = pipeline(task='text-generation', model=model_name, generation_config=config)
        generated_sample = generator(prompt)

        samples, rank1_w, rank2_w, rank3_w, acc = sample_analysis(prompt, object_2, generated_sample, config.num_return_sequences)
        write_to_csv(test_filename, relation_type, relation_label, object_1, object_2, samples, rank1_w, rank2_w, rank3_w, acc)
     
def main():
    relation_type = sys.argv[1]
    commomsense_test('relation.csv', 'MadeOf_few_shot_1.csv', 'gpt2', relation_type)
    return 
             
if __name__ == "__main__":
    main()