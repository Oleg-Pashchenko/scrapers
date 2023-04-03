import time
import numpy as np
from db.neural import NeuralScraper
from misc import copy_error_clear
#import tensorflow as tf

from views.content import messages


def compare_images(img1, img2):
    img1 = messages.download_image(img1, 3)
    img2 = messages.download_image(img2, 4)
    img1 = tf.keras.preprocessing.image.load_img(img1)
    img2 = tf.keras.preprocessing.image.load_img(img2)
    img1 = tf.keras.preprocessing.image.img_to_array(img1)
    img2 = tf.keras.preprocessing.image.img_to_array(img2)
    img1 = tf.image.resize(img1, (224, 224))
    img2 = tf.image.resize(img2, (224, 224))
    img1 = np.array(img1)
    img2 = np.array(img2)
    model = tf.keras.applications.MobileNetV2(
        include_top=False, weights="imagenet", input_shape=(224, 224, 3)
    )
    features1 = model.predict(img1[tf.newaxis, ...])
    features2 = model.predict(img2[tf.newaxis, ...])
    comparison = tf.reduce_mean(tf.square(features1 - features2))
    print(f"{comparison=}")
    return bool(comparison < 0.85)


def neural_block_scraper():
    source_db = NeuralScraper()
    while True:
        try:
            source_item = source_db.get_item()
            if not source_item:
                time.sleep(5)
                continue
            if copy_error_clear.has_not_block(source_item):
                source_db.write_presentation(source_item)
            else:
                source_db.write_error(source_item)
            source_db.delete_item(source_item.id)
            continue
        except:
            pass
        #if compare_images(source_item.photo, source_item.source_item.photo):
        #    source_db.write_presentation(source_item)
        #else:
        #    source_db.write_error(source_item)
