import tensorflow as tf
from PIL import Image
import os
# import matplotlib.pyplot as plt


def preprocess(imageRawDir,imageSize,imageDir = "./output"):
    """
    images preprocess

    Arguments:
    imageRawDir -str- directory of primary images.
    imageDir -str- directory of processed images.
    imageSize -tuple- output image size (20,20)

    Return: none.

    example:
      ##test code
        rawDir = "./rawdata"
        outputDir = "./data"
        size = (20,20)
        preprocess(rawDir,size, outputDir)
    """
    os.mkdir(imageDir)

    eachDirs = os.listdir(imageRawDir)

    for oneDir in eachDirs:

        imageNames = os.listdir(imageRawDir+"/"+ oneDir)
        label = imageDir.split("/")[-2] # directory format："./data/cat/"
        savePath = os.mkdir(imageDir+"/"+oneDir)
        for index, imageName in enumerate(imageNames):
            image = Image.open(os.path.join(imageRawDir+"/"+ oneDir,imageName))
            image = image.resize(imageSize)
            savePath = os.path.join(imageDir+"/"+oneDir, str(label+"_"+str(index))+".jpg")
            image.save(savePath)
    print("Successfully preprocess")


# preprocess("./test",(400,400))


def _int64_feature(value):
    """
    generate int64 feature.
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))




def _bytes_feature(value):
    """
    generate byte feature.
    """
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))




def createRecord(dataName,imageDir="output"):
    """
    create TFRecord data.

    Arguments:
    imageDir -str- image directory.
    classNames -list- like this:classNames = ["cat", "dog", "horse"]
    Return: none.

    ##test code:
        createRecord("output",["cat", "dog", "horse"])
    """
    classNames = os.listdir(imageDir)
    writer = tf.python_io.TFRecordWriter(os.path.join(imageDir, dataName+".tfrecords"))

    
    for classIndex, className in enumerate(classNames):
        print("class name = ",className)
        currentClassDir = os.path.join(imageDir,className)
        print("current dir = ",currentClassDir)
        for index, imageName in enumerate(os.listdir(currentClassDir)):
            image = Image.open(os.path.join(currentClassDir,imageName))
            image_raw = image.tobytes() # convert image to binary format
            print(index, imageName)

            example = tf.train.Example(features = tf.train.Features(feature = {
            "label": _int64_feature(classIndex),
            "image_raw": _bytes_feature(image_raw),
            }))
            writer.write(example.SerializeToString())
    writer.close()
    print("Successfully build tfrecord file")


# createRecord('data')



def autoCreater(imageRawDir,imageSize,dataName="trainData"):

    preprocess(imageRawDir,imageSize)
    createRecord(dataName)

    print("Successfully build tfrecord data")



def readRecord(recordName,imageSize):
    """
    read TFRecord data (images).

    Arguments:
    recordName -- the TFRecord file to be read.
    imageSize -- the image size :[400,400,3]
    return: data saved in recordName (image and label).
    """
    filenameQueue = tf.train.string_input_producer([recordName])
    reader = tf.TFRecordReader()
    _, serializedExample = reader.read(filenameQueue)
    features = tf.parse_single_example(serializedExample, features={
        "label": tf.FixedLenFeature([], tf.int64),
        "image_raw": tf.FixedLenFeature([], tf.string)
    })

    label = features["label"]
    image = features["image_raw"]
    image = tf.decode_raw(image, tf.uint8)
    image = tf.reshape(image,imageSize)
    label = tf.cast(label, tf.int32)
    return image, label












# image, label =  readRecord("./output/data.tfrecords",[400,400,3])


# print(image,label)

# imageBatch, labelBatch = tf.train.shuffle_batch([image, label], batch_size=1, capacity=10, min_after_dequeue=5)


# ##test code
# init = tf.global_variables_initializer()
# sess = tf.Session()
# sess.run(init)
# thread = tf.train.start_queue_runners(sess=sess)
# for i in range(5):
#     #print image_batch.shape, label.shape
#     images, labels = sess.run([imageBatch, labelBatch])
#     print("batch shape = ", images.shape,"labels = ", labels)





# plt.imshow(images[0])

# plt.show()

