from glob import glob

def get_dict(model_dir):
    '''

        Get character dict and number of characters. Required for encoding and building model.
        
    '''

    file = glob(f"{model_dir}/*.txt")[0]
    with open(file,"r", encoding='utf-8') as f:
        char_dict = f.readline()
    char_dict = char_dict + " "
    return len(char_dict) + 1, char_dict #  for CTC flag (-1)