import tensorflow as tf
import numpy as np
print("실행")
# 데이터 불러오기
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
print("데이터 가지고옴")
# 넘파이 데이터를 텐서 데이터로 변환
x_train, x_test = x_train/255, x_test/255
print(x_train.shape, x_test.shape)

x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

print(x_train.shape, x_test.shape)

# Layer 쌓기
model = tf.keras.models.Sequential([         
  tf.keras.layers.Conv2D(32, kernel_size=(3,3), activation="relu", input_shape=(28,28,1)),
  tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
  tf.keras.layers.Conv2D(64, kernel_size=(3,3), activation="relu"),
  tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Dense(10, activation='softmax')
])

# 모델 컴파일하기
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# CPU 학습

print("GPU를 사용한 학습")
with tf.device("/device:GPU:0"):
    model.fit(x_train, y_train, batch_size=32, epochs=3)
