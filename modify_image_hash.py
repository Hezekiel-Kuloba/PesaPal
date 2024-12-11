#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse

def calculate_hash(file_path):
    """Calculate the SHA-512 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.sha512(f.read()).hexdigest()

def modify_image_and_match_hash(image_path, target_prefix, output_path):
    """
    Modify an image's pixel data to achieve a hash starting with a specific prefix.
    """
    img = Image.open(image_path)
    
    # Display original image
    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    plt.title("Original Image")
    plt.axis('off')
    plt.show()

    pixels = np.array(img)

    print(f"Original hash: {calculate_hash(image_path)}")

    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            # Modify the least significant bit (LSB) of each pixel
            pixels[x, y] ^= 1  # Flip LSB

            # Save the modified image
            modified_img = Image.fromarray(pixels)
            modified_img.save(output_path)

            # Calculate the new hash
            new_hash = calculate_hash(output_path)

            # Print the hash only if it's different from the last one
            print(f"Current hash: {new_hash}")

            # Check if the new hash matches the target prefix
            if new_hash.startswith(target_prefix):
                print(f"Success! Hash: {new_hash}")
                
                # Display the modified image after hash match
                plt.figure(figsize=(5, 5))
                plt.imshow(modified_img)
                plt.title("Modified Image")
                plt.axis('off')
                plt.show()

                return

    print("Unable to achieve the desired hash prefix.")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Modify an image to match a specific hash prefix.")
    parser.add_argument('image_path', type=str, help="Path to the input image file")
    parser.add_argument('target_prefix', type=str, help="Desired hash prefix (e.g., 'e5641')")
    parser.add_argument('output_path', type=str, help="Path to save the modified image")

    args = parser.parse_args()

    # Run the function with provided arguments
    modify_image_and_match_hash(args.image_path, args.target_prefix, args.output_path)

if __name__ == "__main__":
    main()


# In[ ]:




