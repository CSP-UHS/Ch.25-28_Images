'''
-------------------------------------
Program to modify a folder of images
-------------------------------------
'''

import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw

directory = input("Image Folder Name: ")
frame_color = tuple(map(int, input("Enter a Color--> R,G,B,A:  ").split(',')))
percent_of_side = float(input("Corner Radius (Ex. .30): "))
print("Converting Images...")

new_directory = os.path.join(directory, 'modified')  # Create a new directory 'modified'
try:
    os.mkdir(new_directory)
except OSError:
    pass  # if the directory already exists, proceed



image_list = []
file_list = []

directory_list = os.listdir(directory)  # Get list of files
for entry in directory_list:
    absolute_filename = os.path.join(directory, entry)
    try:
        image = PIL.Image.open(absolute_filename)
        file_list += [entry]
        image_list += [image]
    except IOError:
        pass  # do nothing with errors trying to open non-images


for n in range(len(image_list)):  # go through the images and save modified versions
    filename, filetype = file_list[n].split('.')  # Parse the filename
    original_image = image_list[n]

    width, height = original_image.size
    radius = int(percent_of_side * min(width, height))  # radius in pixels

    #-------------------------------------------------------------------------
    # This section creates a template mask of transparent/opaque parts.
    # Any RGB colors in this section are completely irrelevant.
    # -------------------------------------------------------------------------
    template_mask = PIL.Image.new('RGBA', (width, height), (127, 0, 127, 0))
    drawing_layer = PIL.ImageDraw.Draw(template_mask)
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(radius, 0), (width - radius, 0),(width - radius, height), (radius, height)], fill=(127, 0, 127, 255))
    drawing_layer.polygon([(0, radius), (width, radius),(width, height - radius), (0, height - radius)],fill=(127, 0, 127, 255))
    # Draw four filled circles of opaqueness
    drawing_layer.ellipse((0, 0, 2 * radius, 2 * radius),fill=(0, 127, 127, 255))
    drawing_layer.ellipse((width - 2 * radius, 0, width, 2 * radius),fill=(0, 127, 127, 255))
    drawing_layer.ellipse((0, height - 2 * radius, 2 * radius, height),fill=(0, 127, 127, 255))
    drawing_layer.ellipse((width - 2 * radius, height - 2 * radius, width, height),fill=(0, 127, 127, 255))

    # Uncomment the following two lines of code to show the template mask
    # plt.imshow(template_mask)
    # plt.show(template_mask)

    # Make the new image
    new_image = PIL.Image.new('RGBA', original_image.size, (frame_color))
    new_image.paste(original_image, (0, 0), mask=template_mask)
    new_image_filename = os.path.join(new_directory,filename + '.png')  # save the altered image, adding PNG to retain transparency
    new_image.save(new_image_filename)


print()
print("Modifications Completed!")
print()

