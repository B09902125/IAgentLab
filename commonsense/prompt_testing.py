from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, set_seed
from transformers.generation.configuration_utils import GenerationConfig

def main():

    example1 = '(a bicycle, metal)\n'
    example2 = '(a book, paper)\n'
    example3 = '(a brick, clay)\n'
    example4 = '(water, H2O)\n'
    example5 = '(cloth, fiber)\n'
    
    # question = f'There is a relationship "created by" between "milk" and'
    relation_label = 'MadeOf'
    object_1 = 'soccer balls'
    
    guiding = f'The following are some pairs in the format (object1, object2), and object1 is made of object2.\n'
    examples = example1 + example2 + example3 + example4 + example5
    question = '(soccer ball,'
    
    prompt = guiding+examples+question

    model_name = 'gpt2'
    config = GenerationConfig.from_pretrained(model_name)
    config.max_new_tokens = 20
    # config.early_stopping = True
    config.temperature = 0.1
    config.num_beams = 64
    config.num_return_sequences = 1
    # set_seed(42)

    generator = pipeline(task='text-generation', model=model_name, generation_config=config)
    generated_sample = generator(prompt)
    for idx, sample in enumerate(generated_sample): 
        print(idx, sample)
    
    return
    
if __name__ == '__main__':
    main()