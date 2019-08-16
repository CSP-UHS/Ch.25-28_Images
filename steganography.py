"""A program that encodes and decodes hidden messages in images through LSB steganography"""
import matplotlib.pyplot as plt 
import os.path
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import textwrap




def decode_image(file_location):
    """Decodes the hidden message in an image"""
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0,0,0)
    decoded_image.save('secret.png')



def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps"""
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text



def encode_image(text_to_encode, template_image):
    """Encodes a text message into an image"""
    filename = template_image
    template_image = Image.open(template_image)
    red_template = template_image.split()[0]
    green_template = template_image.split()[1]
    blue_template = template_image.split()[2]

    x_size = template_image.size[0]
    y_size = template_image.size[1]

    #text draw
    image_text = write_text(text_to_encode, template_image.size)
    bw_encode = image_text.convert('1')

    #encode text into image
    encoded_image = Image.new("RGB", (x_size, y_size))
    pixels = encoded_image.load()
    for i in range(x_size):
        for j in range(y_size):
            red_template_pix = bin(red_template.getpixel((i,j)))
            old_pix = red_template.getpixel((i,j))
            tencode_pix = bin(bw_encode.getpixel((i,j)))

            if tencode_pix[-1] == '1':
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel((i,j)), blue_template.getpixel((i,j)))

    encoded_image.save(filename)


def Main():
    encdec=""
    done=False
    while not done:
        encdec = input("Encode(e) or Decode(d)? ")
        if encdec=="e":
            filepathway = input("Filename of image to encode: ")
            secretmessage = input("Enter secret message: ")
            print("Encoding...") 
            encode_image(secretmessage, filepathway)
            print("The image has been successfully encoded!")
            done=True
        elif encdec=="d":
            filepathway = input("Filename of image to decode: ")
            print("Decoding...") 
            decode_image(filepathway)
            print("Finished!")
            directory = os.path.dirname(os.path.abspath(__file__)) 
            secretfilename = os.path.join(directory, 'secret.png')
            img = plt.imread(secretfilename)  # Read the image data into an array
            fig, ax = plt.subplots(1, 1)
            ax.imshow(img, interpolation='none')
            ax.set_xlim(0,370)
            ax.set_ylim(40,0)
            plt.show()
            done=True
        else:
            print()
            print("Incorrect Entry. Try Again.") 
            print()
		


if __name__ == '__main__':
	Main()