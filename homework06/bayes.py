from collections import Counter, defaultdict
from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.x_frequency = None
        self.y_frequency = None

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        total_rows = len(y)  # количество строк данных
        y_frequency = Counter()  # частота каждой метки
        for key in y:
            y_frequency[key] += 1
        for key in y_frequency.keys():
            y_frequency[key] /= total_rows

        def default():
            return {label: 0 for label in y_frequency.keys()}

        x_count = defaultdict(default)  # сколько раз каждое слово встречается в каждом классе
        y_count = defaultdict(lambda: 0)  # количество слов для каждого класса
        # через все слова во всех запросах бежим и заносим в словарь
        for text, label in zip(X, y):
            for word in text:
                x_count[word][label] += 1
                y_count[label] += 1
        x_frequency = defaultdict(default)  # вероятность принадлежности слов каждому из классов
        d = len(x_count)  # размерность вектора признаков
        for word in x_count.keys():
            for label in x_count[word].keys():
                x_frequency[word][label] = (x_count[word][label] + self.alpha) / (y_count[label] + d * self.alpha)
        self.x_frequency = x_frequency
        self.y_frequency = y_frequency

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        y = []
        for text in X:
            predictions = {}  # вероятности предложения по каждой из меток
            for label in self.y_frequency.keys():
                log_sum = 0  # сумма логарифмированных вероятностей слов
                for word in text:
                    if word in self.x_frequency.keys():
                        log_sum += log(self.x_frequency[word][label])
                predictions[label] = log(self.y_frequency[label]) + log_sum  # вероятность данного предложения с данной меткой
            y.append(max(predictions, key=predictions.get))
        return y

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y = self.predict(X_test)
        accurate = 0
        for prediction, test in zip(y, y_test):
            if prediction == test:
                accurate += 1
        return accurate / len(X_test)

