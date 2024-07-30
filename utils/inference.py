import numpy as np
from utils.encode import *
import tensorflow as tf

def predict(ocr_model, image_arr, char_dict):
    
    print(image_arr.shape)
    preds = ocr_model.predict(image_arr, verbose=False)

    # Define input_length for CTC decoding
    input_length = np.ones(preds.shape[0]) * preds.shape[1]  # Same length for all sequences

    # Convert numpy arrays to TensorFlow tensors
    preds_tensor = tf.convert_to_tensor(preds, dtype=tf.float32)
    input_length_tensor = tf.convert_to_tensor(input_length, dtype=tf.int32)
   

    # Perform CTC decoding
    decoded, _ = tf.keras.backend.ctc_decode(preds_tensor, input_length=input_length_tensor, greedy=True)

    # Extract the decoded values
    decoded_np = decoded[0].numpy()  # Convert tensor to numpy array
    
    # Assuming num_to_label is a function that maps label indices to strings
    prediction = [num_to_label(decoded_np[i], char_dict) for i in range(preds.shape[0])]
    pred_str = "".join(prediction)

    return pred_str