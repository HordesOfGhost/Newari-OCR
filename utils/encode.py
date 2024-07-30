import numpy as np

def label_to_num(label, char_dict):
    label_num = []
    for ch in label:
        label_num.append(char_dict.find(ch)) 
        #find() method returns the lowest index of the substring if it is found in given string otherwise -1
        
    return np.array(label_num)

def num_to_label(num, char_dict):
    ret = ""
    for ch in num:
        if ch == -1:  # CTC Blank
            break
        else:
            ret+=char_dict[ch]
    return ret