from lxml import etree
from PIL import Image 
import os
import shutil

def getRegion(xmlFile):
	"""
	xmlFile --str-- file dir

		xmlFile = "./test/class1/data_0.xml"

	return region tuple
	"""

	xml = etree.parse(xmlFile)
	region = (int(xml.xpath("//bndbox/xmin/text()")[0]),\
		int(xml.xpath("//bndbox/ymin/text()")[0]),\
		int(xml.xpath("//bndbox/xmax/text()")[0]),\
		int(xml.xpath("//bndbox/ymax/text()")[0]))

	return region




def imageCut(imgFile,cutRegion):

	"""
	imgFile --str-- open image file
	cutRegion --tuple -- a cut region

	example:
	  imageCut("./img/test.jpg",(10,10,200,200))
	"""

	img = Image.open(imgFile,"r")
	crop = img.crop(cutRegion)
	
	return crop 




def cutAll(imgDir,xmlDir,resize,imgSaveDir="./output"):
	"""
	imgDir --str-- image file dir
	xmlDir --str-- xml file dir
	example:
		xmlDir="./xml"
		imgDir="./img"
		resize =(200,200)
		imgSaveDir="output"
	"""

	if os.path.exists("./output"):
		shutil.rmtree("./output")
		os.mkdir(imgSaveDir)
	else:
		os.mkdir(imgSaveDir)

	imgsDirs = os.listdir(imgDir)

	for oneDir in imgsDirs:
		imgNames = os.listdir(imgDir+"/"+ oneDir)
		# xmlNames = os.listdir(xmlDir+"/"+ oneDir)
		os.mkdir(imgSaveDir+"/"+oneDir)

		for imgName in imgNames:

			name = imgName.split(".")
			region = getRegion(xmlDir+"/"+oneDir+"/"+name[0]+".xml")
			crop = imageCut(imgDir+"/"+oneDir+"/"+imgName,region)
			
			resImg = crop.resize(resize)

			resImg.save(imgSaveDir+"/"+oneDir+"/"+ name[0]+".jpg")

			print("sucessfully cut "+oneDir+"/" +name[0])







