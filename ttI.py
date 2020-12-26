from PIL import Image, ImageDraw, ImageFont

def ttI(txtI):
	l=len(txtI)

	txtI='\n'+txtI
	img = Image.new('RGB', (470, 198), color = (73, 109, 137))

	fnt = ImageFont.truetype('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\FreeSansBoldOblique.ttf', 65)
	d = ImageDraw.Draw(img)
	d.text((10,10),txtI,font=fnt,  fill=(255, 255, 0))

	img.save('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\pil_text_font.png')
