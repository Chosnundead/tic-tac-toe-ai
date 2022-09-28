# Импорт необходимых библиотек
import random as rd
import numpy as np
import matplotlib.pyplot as plt

from deap import base, algorithms, creator, tools
from modules.game import Game
from modules.neural_net import NeuralNet

# Нейросеть
neuralNet = NeuralNet()
# Окружение
game = Game()

# game._table = [["O", "X", "O"], ["O", "X", "X"], ["1", "X", "O"]]
# print(game.isContinue())
# print(game.check())
# raise Exception
# pred = neuralNet.model.predict(np.expand_dims(game.getInfo(), axis=0))
# pred = np.argmax(pred, axis=1)[0] + 1
# print(pred)
# raise Exception
# print(neuralNet.model.predict(np.expand_dims(game.getInfo(), axis=0)))

# Глобальные значения
LEN_OF_GENOM = len(neuralNet.getWeights())
LEN_OF_POPULATIONS = 100
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = max(int(MAX_GENERATIONS / 4), 2)
P_CROSSOVER = 0.9
P_MUTATION = 0.1
LOW = -2.0
UP = 2.0
ETA = 42

# Создание зала славы
hof = tools.HallOfFame(HALL_OF_FAME_SIZE)
testInd = neuralNet.getWeights()

# Объявление базовых классов для пакета deap
# Класс для максимизации награждения
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# Класс нашего индивида, что наследуется от класса list
creator.create("Individual", list, fitness=creator.FitnessMax)

# Создание базовых функций для пакета deap и их регистрация в нашем тулбоксе
toolbox = base.Toolbox()
# Функция создания случайного значения в пределах наших LOW и UP для весов
toolbox.register("randomWeight", rd.uniform, LOW, UP)
# Функция создания индивида
toolbox.register(
    "individualCreator",
    tools.initRepeat,
    creator.Individual,
    toolbox.randomWeight,
    LEN_OF_GENOM,
)
# Функция создания популяции
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

# Создание популяции
population = toolbox.populationCreator(n=LEN_OF_POPULATIONS)

# Объявление функции для расчёта награждения у нашего индивида
def getScore(ind):
    global neuralNet, game, hof, testInd
    game.clear()
    best = testInd
    if len(hof.items) > 0:
        randomInt = rd.randint(0, (len(hof.items) - 1))
        best = hof.items[randomInt]
        if len(hof.items) >= HALL_OF_FAME_SIZE:
            hof.remove(rd.randint(0, max((len(hof.items) - 1), 1)))

    resultReward = 0
    counter = 0
    while game.isContinue():
        if counter % 2 == 0:
            neuralNet.setWeights(ind)
        else:
            neuralNet.setWeights(best)
        pred = neuralNet.model.predict(
            np.expand_dims(game.getInfo(), axis=0), verbose=0
        )
        pred = np.argmax(pred, axis=1)[0] + 1
        isCompleteTurn = game.step(pred)
        if not isCompleteTurn:
            if counter % 2 == 0:
                resultReward -= 250
            for i in range(1, 10):
                isBreak = game.step(i)
                if isBreak:
                    break
        resultReward -= 1
        counter += 1

    if game.check() == "X":
        resultReward += 100
    if game.check() == "O":
        resultReward -= 100

    return (resultReward,)


# Создание базовых функций для пакета deap и их регистрация в нашем тулбоксе
# Функция для возврашения score нашего индивида
toolbox.register("evaluate", getScore)
# Функция для выборки индивидов из поколений
toolbox.register("select", tools.selTournament, tournsize=3)
# Функция для наследственности(кроссовера) из двух роителей в новое поколение
toolbox.register("mate", tools.cxSimulatedBinary, eta=ETA)
# Функция для мутирования особей
toolbox.register(
    "mutate",
    tools.mutPolynomialBounded,
    low=LOW,
    up=UP,
    eta=ETA,
    indpb=1.0 / LEN_OF_GENOM,
)

# Создание статистики поколений
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", np.max)
stats.register("avg", np.mean)

# Запуск нашего обучения
population, logbook = algorithms.eaSimple(
    population,
    toolbox,
    cxpb=P_CROSSOVER,
    mutpb=P_MUTATION,
    ngen=MAX_GENERATIONS,
    halloffame=hof,
    stats=stats,
    verbose=True,
)

# Выборка значений нашей статистики
maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")


# Отрисовка графика
plt.plot(maxFitnessValues, color="red")
plt.plot(meanFitnessValues, color="green")
plt.xlabel("Поколение")
plt.ylabel("Макс(красный)/средняя(зелёная) приспособленность")
plt.title("Зависимость максимальной и средней приспособленности от поколения")
plt.show()

# Получение и отрисовка лучшего индивида из зала славы поколений
best = hof.items[0]
print(f"Лучший парень: {best}.")
