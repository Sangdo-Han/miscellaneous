import tensorflow as tf

# sample model 
model = tf.keras.applications.MobileNetV3Small(include_top=False)
model.summary()
