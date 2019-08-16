
import matplotlib.pyplot as plt
import PIL.ImageDraw
import PIL.ImageFont

sith_img = PIL.Image.open('sith_lord.jpg')
fig, axes = plt.subplots(1, 3)
axes[0].imshow(sith_img, interpolation='none')
axes[0].axis('off')
axes[0].set_title("Sith Lord")

# Display student in second axes and set window to the right eye
axes[1].imshow(sith_img, interpolation='none')
axes[1].axis('off')
axes[1].set_title("Left Eye")
axes[1].set_xlim(265, 310)
axes[1].set_ylim(145, 110)

axes[2].imshow(sith_img, interpolation='none')
axes[2].axis('off')
axes[2].set_title("Right Eye")
axes[2].set_xlim(458, 503)
axes[2].set_ylim(142, 105)
plt.show()


evil_eye = PIL.Image.open('evil_eye.png')
left_evil_eye = evil_eye.resize((30, 25))
right_evil_eye = evil_eye.resize((30, 25))
fig2, axes2 = plt.subplots(1, 3)
axes2[0].imshow(evil_eye)
axes2[0].axis('off')
axes2[0].set_title("Original Evil Eye")
axes2[1].imshow(left_evil_eye)
axes2[1].axis('off')
axes2[1].set_title("Evil Left Eye")
axes2[2].imshow(right_evil_eye)
axes2[2].axis('off')
axes2[2].set_title("Evil Right Eye")
plt.show()

# Paste earth into right eye and display
# Uses alpha from mask
sith_img.paste(left_evil_eye, (277,115), mask=left_evil_eye) 
sith_img.paste(right_evil_eye, (468,115), mask=right_evil_eye) 

# Display
draw = PIL.ImageDraw.Draw(sith_img)
draw.polygon( [(25,490),(720,490),(720,570),(25,570)], fill='#000000', outline='orange')
font=PIL.ImageFont.truetype('FaceYourFears.ttf',70)
draw.text( (25,500), 'The Eyes of the Sith', font=font, fill='orange')

fig3, axes3 = plt.subplots(1, 1)
axes3.imshow(sith_img, interpolation='none')
axes3.axis('off')
plt.show()