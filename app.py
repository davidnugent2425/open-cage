# from flask import Flask, request, jsonify
# import requests
# import os

# app = Flask(__name__)

# BAD_REQUEST_MSG="Not a proper request method or data"
# INTERNAL_ERROR_MSG="Error from within the Cage! Check the logs for more info."

# # SIMPLE HELLO WORLD ENDPOINT. ADD A BODY AND IT WILL BE RETURNED IN THE RESPONSE.
# @app.route('/hello', methods=['GET', 'POST'])
# def hello():
#     enclave_message = "Hello! I'm writing to you from within an enclave"
#     if request.method=="POST":
#         try:
#             data = request.get_json()
#             data['response'] = enclave_message
#             return jsonify(data)
#         except Exception as e:
#             app.logger.error(str(e))
#             return INTERNAL_ERROR_MSG
#     elif request.method=="GET":
#         return enclave_message
#     else:
#         return BAD_REQUEST_MSG

# Save the overlay image to a file or display it
# overlay_image.show()

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8008)

import torch
import requests
from PIL import Image
from torchvision import transforms
import io

# Define the URL of the sample image
url = "https://github.com/mateuszbuda/brain-segmentation-pytorch/raw/master/assets/TCGA_CS_4944.png"

# Download the sample image and load it into a PIL image object
print('downloading sample image')
response = requests.get(url)
pil_image = Image.open(io.BytesIO(response.content)).convert('RGB')

# Define the transforms to apply to the image
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Apply the transforms to the image
input_tensor = transform(pil_image)

print('downloading pre-trained model')
# Load the pre-trained model
model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet',
                       in_channels=3, out_channels=1, init_features=32, pretrained=True)

# Set the model to evaluation mode
model.eval()

print('running inference')
# Make a prediction using the input tensor
with torch.no_grad():
    output_tensor = model(input_tensor.unsqueeze(0))

# Convert the output tensor to a PIL image
output_array = output_tensor.cpu().squeeze().numpy()
output_array = (output_array * 255).astype('uint8')
output_image = Image.fromarray(output_array)

# Resize the output image to the size of the input image
output_image = output_image.resize(pil_image.size)

# Create a blank PIL image of the same size as the input image
mask_image = Image.new(mode='L', size=pil_image.size, color=0)

# Paste the output image onto the mask image
mask_image.paste(output_image, box=(0, 0))

# Create a copy of the input image and convert it to RGBA
overlay_image = pil_image.copy().convert('RGBA')

# Paste the mask image onto the overlay image
overlay_image.paste((255, 255, 255, 0), box=(0, 0), mask=mask_image)

print('inference finished')