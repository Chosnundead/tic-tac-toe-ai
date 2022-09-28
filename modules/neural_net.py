import os

# Сточка для отключения предупреждений
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import keras as ks
import numpy as np
from keras.layers import Flatten, Dense

# Создание класса нейронки
class NeuralNet:

    # Модель нейронки
    model = ks.Sequential(
        [
            Flatten(input_shape=(9,)),
            Dense(8, activation="relu"),
            Dense(9, activation="relu"),
            Dense(9, activation="softmax"),
        ]
    )

    def __init__(self) -> None:
        pass

    # Выведение инфы
    def _info(self):
        print(self.model.summary())
        pass

    # Получение весов
    def getWeights(self):
        result = []
        numberOfLayer = 0
        for layer in self.model.layers:
            if numberOfLayer >= 1:
                arr = layer.get_weights()[0].flatten()
                for item in arr:
                    result.append(item)
            numberOfLayer += 1
        return result

    # Присвоение весов нейронке
    def setWeights(self, arr):
        numberOfLayer = 0
        for layer in self.model.layers:
            if numberOfLayer == 0:
                layer.set_weights([])
            elif numberOfLayer == 1:
                layer.set_weights(
                    [
                        np.array(
                            [[*[arr[j + i * 8] for j in range(8)]] for i in range(9)],
                            dtype=np.float32,
                        ),
                        np.array(
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32
                        ),
                    ]
                )
                arr = arr[(8 * 9) :]
            elif numberOfLayer == 2:
                layer.set_weights(
                    [
                        np.array(
                            [[*[arr[j + i * 9] for j in range(9)]] for i in range(8)],
                            dtype=np.float32,
                        ),
                        np.array(
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            dtype=np.float32,
                        ),
                    ]
                )
                arr = arr[(8 * 9) :]
            elif numberOfLayer == 3:
                layer.set_weights(
                    [
                        np.array(
                            [[*[arr[j + i * 9] for j in range(9)]] for i in range(9)],
                            dtype=np.float32,
                        ),
                        np.array(
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            dtype=np.float32,
                        ),
                    ]
                )
            numberOfLayer += 1
        pass
