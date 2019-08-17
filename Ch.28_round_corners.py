import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def round_corners(original_image, percent_of_side):

    width, height = original_image.size
    radius = int(percent_of_side * min(width, height)) # radius in pixels

    #create a mask
    
    #start with transparent mask
    rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(rounded_mask)

    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.polygon([(radius,0),(width-radius,0),
                            (width-radius,height),(radius,height)],
                            fill=(127,0,127,255))
    drawing_layer.polygon([(0,radius),(width,radius),
                            (width,height-radius),(0,height-radius)],
                            fill=(127,0,127,255))

    #Draw four filled circles of opaqueness
    drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                            fill=(0,127,127,255)) #top left
    drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                            fill=(0,127,127,255)) #top right
    drawing_layer.ellipse((0,height-2*radius,  2*radius,height), 
                            fill=(0,127,127,255)) #bottom left
    drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                            fill=(0,127,127,255)) #bottom right
     
    # Uncomment the following two lines of code to show the mask
    # plt.imshow(rounded_mask)
    # plt.show(rounded_mask)

    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
    result.paste(original_image, (0,0), mask=rounded_mask)
    return result



def get_images(directory):

    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = []
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors trying to open non-images
    return image_list, file_list


def round(directory):

    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified

    new_directory = os.path.join(directory, 'modified') # Create a new directory 'modified'
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  

    image_list, file_list = get_images(directory)  #load all the images

    for n in range(len(image_list)): #go through the images and save modified versions
        filename, filetype = file_list[n].split('.') # Parse the filename
        new_image = round_corners(image_list[n],.30) # Round the corners with radius = 30% of short side
        new_image_filename = os.path.join(new_directory, filename + '.png') #save the altered image, adding PNG to retain transparency
        new_image.save(new_image_filename)

def main():
    folder = input("Image Folder Name: ")
    print("Converting Images...")
    round(folder)


if __name__ == "__main__":
    main()
