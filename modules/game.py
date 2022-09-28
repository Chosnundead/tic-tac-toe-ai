import re

# Создание класса игры
class Game:

    # Массив поля игры
    _table = [[str(i + 3 * j) for i in range(1, 4)] for j in range(3)]
    # Символ для игрока, что будет ходить следущим
    _nextStep = "X"
    # Номер хода
    numberOfTurn = 1

    # Конструктор класса
    def __init__(self) -> None:
        pass

    # Метод для отбражения таблицы
    def _showTable(self):
        print("===========")
        for arr in self._table:
            print("|", end="")
            for item in arr:
                print(f"|{item}|", end="")
            print("|\n===========")

    # Метод для проверки на выйгрыш\пройгрыш\ничью
    def check(self):
        string = ""
        # row check
        for i in range(3):
            for j in range(3):
                string += self._table[i][j]
            if string == "OOO":
                return "O"
            elif string == "XXX":
                return "X"
            else:
                string = ""
        # column check
        for i in range(3):
            for j in range(3):
                string += self._table[j][i]
            if string == "OOO":
                return "O"
            elif string == "XXX":
                return "X"
            else:
                string = ""
        # diagonal check
        if (
            "{}{}{}".format(self._table[0][0], self._table[1][1], self._table[2][2])
            == "XXX"
        ):
            return "X"
        elif (
            "{}{}{}".format(self._table[0][0], self._table[1][1], self._table[2][2])
            == "OOO"
        ):
            return "O"
        elif (
            "{}{}{}".format(self._table[0][2], self._table[1][1], self._table[2][0])
            == "XXX"
        ):
            return "X"
        elif (
            "{}{}{}".format(self._table[0][2], self._table[1][1], self._table[2][0])
            == "OOO"
        ):
            return "O"
        else:
            stringOfTable = ""
            for arr in self._table:
                for item in arr:
                    stringOfTable += item
            if re.search(r"\d+", stringOfTable) == None:
                return "Draw"
            else:
                return "None"

    # Метод для проверки на продолжение игры
    def isContinue(self):
        return True if self.check() == "None" else False

    # Метод для хода(вставки в таблицу)
    # Возвращем состоялся ли ход
    # Не работает если использовать последовательно\вместе с self.step()
    def stepBy(self, where, who):
        for arr in range(len(self._table)):
            for item in range(len(self._table[arr])):
                if str(where) == self._table[arr][item]:
                    self._table[arr][item] = who
                    self.numberOfTurn += 1
                    return True
        return False

    # Метод для хода(вставки в таблицу) без обозначение того кто ходит
    # Возвращем состоялся ли ход
    def step(self, where):
        for arr in range(len(self._table)):
            for item in range(len(self._table[arr])):
                if str(where) == self._table[arr][item]:
                    self._table[arr][item] = self._nextStep
                    if self._nextStep == "X":
                        self._nextStep = "O"
                    else:
                        self._nextStep = "X"
                    self.numberOfTurn += 1
                    return True
        return False

    # Метод очистки доски
    def clear(self):
        self._table = [[str(i + 3 * j) for i in range(1, 4)] for j in range(3)]
        self._nextStep = "X"
        self.numberOfTurn = 1
        pass

    # Входные данные для нейросети
    def getInfo(self):
        result = []
        for arr in self._table:
            for item in arr:
                if item == "X":
                    result.append(0.0)
                elif item == "O":
                    result.append(0.5)
                else:
                    result.append(1.0)
        return result
