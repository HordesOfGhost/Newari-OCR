from glob import glob

def get_dict(model_dir):
    
    file = glob(f"{model_dir}/*.txt")[0]
    with open(file,"r", encoding='utf-8') as f:
        char_dict = f.readline()
    return len(char_dict) + 2 # one for whitespace and another is for CTC flag (-1)