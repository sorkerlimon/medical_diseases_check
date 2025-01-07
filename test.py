import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function for Grayscale Conversion
def grayscale_conversion(image):
    grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_img

# Function for Smoothing/Blurring
def smoothing_blurring(image, kernel_size=(5, 5)):
    blurred_img = cv2.GaussianBlur(image, kernel_size, 0)
    return blurred_img

# Function for Edge Detection
def edge_detection(image, low_threshold=50, high_threshold=150):
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges

# Function for Thresholding
def thresholding(image, threshold_value=127, max_value=255):
    _, thresholded_img = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY)
    return thresholded_img

# Example of using the functions
def process_mri_image(image_path):
    # Load the MRI image
    img = cv2.imread(image_path)
    
    # Grayscale conversion
    grayscale_img = grayscale_conversion(img)
    
    # Smoothing/Blurring
    blurred_img = smoothing_blurring(grayscale_img)
    
    # Edge detection
    edges = edge_detection(grayscale_img)
    
    # Thresholding
    thresholded_img = thresholding(grayscale_img)
    
    # Display the results
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.title("Grayscale Conversion")
    plt.imshow(grayscale_img, cmap='gray')
    
    plt.subplot(2, 2, 2)
    plt.title("Smoothing/Blurring")
    plt.imshow(blurred_img, cmap='gray')
    
    plt.subplot(2, 2, 3)
    plt.title("Edge Detection")
    plt.imshow(edges, cmap='gray')
    
    plt.subplot(2, 2, 4)
    plt.title("Thresholding")
    plt.imshow(thresholded_img, cmap='gray')
    
    plt.tight_layout()
    plt.show()

# Provide the MRI image path here
image_path = r'images\MRI_of_Human_Brain.jpg'
process_mri_image(image_path)
