# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
# from tensorflow.keras.utils import img_to_array, load_img
# import numpy as np

# # Load the model
# model = load_model('model_weights_vgg.keras')

# def preprocess_image(image_path):
#     # Resize the image to the model's expected dimensions
#     image = load_img(image_path, target_size=(124, 62))  # Update dimensions here
#     image = img_to_array(image)
#     image = np.expand_dims(image, axis=0)  # Add batch dimension
#     return preprocess_input(image)

# def predict_image(image_path, model):
#     processed_image = preprocess_image(image_path)
#     predictions = model.predict(processed_image)
#     return predictions

# # Test the model
# image_path = 'OAS1_0028_MR1_mpr-1_100_aug_1.jpg'  # Path to your image
# results = predict_image(image_path, model)

# # Display the results
# print(results)



# import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications.vgg16 import preprocess_input
# from tensorflow.keras.utils import img_to_array, load_img
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# class BrainMRIClassifier:
#     def __init__(self, model_path):
#         self.model = load_model(model_path)
#         self.classes = ['Non-Demented', 'Very Mild Demented', 'Mild Demented', 'Demented']
        
#     def preprocess_image(self, image_path):
#         """Preprocess the input image for model prediction"""
#         image = load_img(image_path, target_size=(124, 62))
#         image = img_to_array(image)
#         image = np.expand_dims(image, axis=0)
#         return preprocess_input(image)
    
#     def predict_image(self, image_path):
#         """Make predictions on the input image"""
#         processed_image = self.preprocess_image(image_path)
#         predictions = self.model.predict(processed_image)
#         return predictions[0]
    
#     def display_results(self, predictions):
#         """Display comprehensive results including probabilities and visualizations"""
#         # Get the predicted class and confidence
#         predicted_class_idx = np.argmax(predictions)
#         predicted_class = self.classes[predicted_class_idx]
#         confidence = predictions[predicted_class_idx] * 100
        
#         # Print text results
#         print("\n=== Classification Results ===")
#         print(f"Predicted Class: {predicted_class}")
#         print(f"Confidence: {confidence:.2f}%\n")
        
#         print("Detailed Probabilities:")
#         for class_name, prob in zip(self.classes, predictions):
#             print(f"{class_name}: {prob*100:.2f}%")
            
#         # Create visualization of results
#         self.plot_results(predictions)
        
#     def plot_results(self, predictions):
#         """Create bar plot of prediction probabilities"""
#         plt.figure(figsize=(10, 6))
#         sns.barplot(x=predictions * 100, y=self.classes)
#         plt.xlabel('Probability (%)')
#         plt.title('Dementia Classification Probabilities')
#         plt.tight_layout()
#         plt.show()
        
#     def generate_report(self, predictions):
#         """Generate a detailed classification report"""
#         report = {
#             'predicted_class': self.classes[np.argmax(predictions)],
#             'confidence': float(np.max(predictions) * 100),
#             'class_probabilities': {
#                 class_name: float(prob * 100)
#                 for class_name, prob in zip(self.classes, predictions)
#             }
#         }
#         return report

# def main():
#     # Initialize the classifier
#     model_path = 'model_weights_vgg.keras'  # Update with your model path
#     image_path = 'images\Mild Dementia\OAS1_0028_MR1_mpr-1_100.jpg'  # Update with your image path
    
#     try:
#         # Create classifier instance
#         classifier = BrainMRIClassifier(model_path)
        
#         # Make predictions
#         predictions = classifier.predict_image(image_path)
        
#         # Display results
#         classifier.display_results(predictions)
        
#         # Generate and print detailed report
#         report = classifier.generate_report(predictions)
#         print("\n=== Detailed Report ===")
#         print(f"Predicted Class: {report['predicted_class']}")
#         print(f"Confidence: {report['confidence']:.2f}%")
#         print("\nProbabilities by Class:")
#         for class_name, prob in report['class_probabilities'].items():
#             print(f"{class_name}: {prob:.2f}%")
            
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()


# aimodel.py

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.utils import img_to_array, load_img
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.preprocessing.image import array_to_img

class BrainMRIClassifier:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        # self.classes = ['Non-Demented', 'Very Mild Demented', 'Mild Demented', 'Demented']
        self.classes = ['Mild Dementia', 'Moderate Dementia', 'Non Demented', 'Very mild Dementia']
        
        
    def preprocess_image(self, image_input):
        """Preprocess the input image for model prediction.
        Accepts a file path or a NumPy array."""
        if isinstance(image_input, str):  # If it's a file path
            image = load_img(image_input, target_size=(124, 62))
        elif isinstance(image_input, np.ndarray):  # If it's a NumPy array
            image = array_to_img(image_input)
            image = image.resize((124, 62))  # Resize to match the model's input size
        else:
            raise ValueError("Input must be a file path or a NumPy array.")
        
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return preprocess_input(image)
    
    def predict_image(self, image_path):
        """Make predictions on the input image"""
        processed_image = self.preprocess_image(image_path)
        predictions = self.model.predict(processed_image)
        return predictions
    
    def display_results(self, predictions):
        """Display comprehensive results including probabilities and visualizations"""
        # Print raw prediction values
        print("\n=== Raw Prediction Values ===")
        print(predictions)
        
        predictions = predictions[0]  # Get the first prediction array
        
        # Get the predicted class and confidence
        predicted_class_idx = np.argmax(predictions)
        predicted_class = self.classes[predicted_class_idx]
        confidence = predictions[predicted_class_idx] * 100
        
        # Print text results
        print("\n=== Classification Results ===")
        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence: {confidence:.2f}%\n")
        
        print("Detailed Probabilities:")
        for class_name, prob in zip(self.classes, predictions):
            print(f"{class_name}: {prob*100:.2f}%")
            
        # Create visualization of results
        # self.plot_results(predictions)
        
    def plot_results(self, predictions):
        """Create bar plot of prediction probabilities"""
        plt.figure(figsize=(10, 6))
        sns.barplot(x=predictions * 100, y=self.classes)
        plt.xlabel('Probability (%)')
        plt.title('Dementia Classification Probabilities')
        plt.tight_layout()
        plt.show()
        
    def generate_report(self, predictions):
        """Generate a detailed classification report"""
        predictions = predictions[0]  # Get the first prediction array
        report = {
            'raw_predictions': predictions.tolist(),
            'predicted_class': self.classes[np.argmax(predictions)],
            'confidence': float(np.max(predictions) * 100),
            'class_probabilities': {
                class_name: float(prob * 100)
                for class_name, prob in zip(self.classes, predictions)
            }
        }
        return report

def main():
    # Initialize the classifier
    model_path = 'model_weights_vgg.keras'  # Update with your model path
    image_path = r'images\Very Mild Dementia\OAS1_0003_MR1_mpr-1_104.jpg'  # Update with your image path
    
    try:
        # Create classifier instance
        classifier = BrainMRIClassifier(model_path)
        
        # Make predictions
        predictions = classifier.predict_image(image_path)
        
        # Display results
        classifier.display_results(predictions)
        
        # Generate and print detailed report
        report = classifier.generate_report(predictions)
        print("\n=== Detailed Report ===")
        print("Raw Predictions:", report['raw_predictions'])
        print(f"\nPredicted Class: {report['predicted_class']}")
        print(f"Confidence: {report['confidence']:.2f}%")
        print("\nProbabilities by Class:")
        for class_name, prob in report['class_probabilities'].items():
            print(f"{class_name}: {prob:.2f}%")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()