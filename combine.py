import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import os
import cv2
from PIL import Image
dir = "C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\"
out_file = "C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\joined_images.jpg"
# emo=1
image_width=450
image_height=570
	

def merge_images(dir, file):
	image = Image.open(os.path.join(dir, file))
	base = Image.open(out_file)

	(width1, height1) = image.size
	(width2, height2) = base.size

	result_height = max(height1, height2)
	result_width = width1 + width2

	out = Image.new('RGB', (result_width, result_height))
	out.paste(im=base, box=(0, 0))
	out.paste(im=image, box=(width2, 0))

	out.save(out_file,"JPEG")
	return out

def merge_imagesv(dir, file):
	image = Image.open(os.path.join(dir, file))
	base = Image.open(out_file)

	(width1, height1) = image.size
	(width2, height2) = base.size

	result_height = height2
	result_width = max(width1,width2)

	out = Image.new('RGB', (result_width, result_height))
	out.paste(im=base, box=(0, 0))
	out.paste(im=image, box=(1000, 570))
	out.save(out_file,"JPEG")
	return out

def createTarget():
	result = Image.new('RGB', (1, 1))
	result.save(out_file,"JPEG")

def create(emo):
	path='hi'
	if emo == 'Happy' or emo == 'happy':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\happy.png'
	elif emo == 'Sad' or emo == 'sad':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\sad.png'
	elif emo == 'Surprised' or emo == 'surprised':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\surprised.png'
	elif emo == 'Fearful' or emo == 'fearful':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\fear.png'
	elif emo == 'Angry' or emo == 'angry':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\angry.png'
	elif emo == 'Disgusted' or emo == 'disgusted':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\disgust.png'
	elif emo == 'Neutral' or emo == 'neutral':
		path = 'C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\emojis\\neutral.png'

	# print(path)
	createTarget()	
	image=cv2.imread(path)
	image=cv2.resize(image,(image_width,image_height),0,0,cv2.INTER_LINEAR)
	cv2.imwrite(path, image)
	merge_images(dir, "Cartoon version.jpg") 
	merge_images(dir, path)  
	merge_imagesv(dir, "pil_text_font.png")

#if __name__=='__main__':
#	create('3')	
	  
