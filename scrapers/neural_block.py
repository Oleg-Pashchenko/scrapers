import time
from datetime import datetime

import numpy as np

from db.marketplace import MarketPlaceScraper
from db.neural import NeuralScraper
import tensorflow as tf

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
    return bool(comparison < 0.8)


def neural_block_scraper():
    source_db = NeuralScraper()
    while True:
        source_item = source_db.get_item()
        if not source_item:
            time.sleep(5)
            continue
        #items = scrape(source_item)
        #print(items)
        now = datetime.now()
        #if not items:
        #    source_db.save_to_error_mk('ozon_error', source_item, now)
        #for item in items:
        source_db.write_presentation(source_item)
