from utils.models import *
import tensorflow as tf

def clear_model(model):
    # Clear the existing model
    tf.keras.backend.clear_session()
    # You can also reinitialize the model if needed
    # e.g., model = create_model() or create_gray_model(num_of_characters)

def load_model_weights(model_dir, checkpoint, color_channel, num_of_characters):
    '''
    
        Load model

    '''
    
    # Create a new model
    if color_channel == 'gray':
        ocr_model = create_gray_model(num_of_characters)
    else:
        ocr_model = create_rgb_model(num_of_characters)  # Assuming RGB model creation function

    clear_model(ocr_model)
    
    # Load the weights into the new model
    ocr_model.load_weights(f"{model_dir}/{checkpoint}_model.keras")

    return ocr_model