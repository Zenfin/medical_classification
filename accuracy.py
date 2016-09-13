from tabulate import tabulate


class Tester(object):
    def __init__(self, y_hat, outcomes, algo_name=""):
        self.algo_name = algo_name
        self.test_samples = len(y_hat)
        self.train_samples = 0
        self.y_hat = y_hat
        self.outcomes = outcomes
        self.guesses = {outcome: {"guessed": 0, "guessed right": 0, "actual": 0}
                        for outcome in self.outcomes}

    def predict(self, y_training, y_test):
        self.train_samples = len(y_training)
        accuracy = 0
        for i, answer in enumerate(y_test):
            guess = int(self.y_hat[i])
            self.guesses[guess]['guessed'] += 1
            self.guesses[answer]['actual'] += 1
            if int(answer) == guess:
                self.guesses[guess]["guessed right"] += 1
                accuracy += 1
        self.accuracy = accuracy / float(len(y_test)) * 100

    def print_results(self):
        table = [[self.algo_name, "", "", "", "", "", "", ""]]
        table += [["---", "---", "---", "---", "---", "---", "---", "---"]]
        table += [["Outcome", "Guessed", "Guessed Right", "Actual", "Diff", "Right Diff", "Diff %", "Right Diff %"]]
        table += [["---", "---", "---", "---", "---", "---", "---", "---"]]
        rows = [
            [name,
             self.guesses[outcome]["guessed"],
             self.guesses[outcome]["guessed right"],
             self.guesses[outcome]["actual"],
             self.guesses[outcome]["guessed"] - self.guesses[outcome]['actual'],
             self.guesses[outcome]["guessed right"] - self.guesses[outcome]['actual'],
             "{}%".format(round(float(self.guesses[outcome]["guessed"] - self.guesses[outcome]['actual']) / (self.guesses[outcome]['actual'] or 1) * 100)),
             "{}%".format(round(float(self.guesses[outcome]["guessed right"] - self.guesses[outcome]['actual']) / (self.guesses[outcome]['actual'] or 1) * 100))]
            for outcome, name in self.outcomes.items()]
        table += rows
        table += [["---", "---", "---", "---", "---", "---", "---", "---"]]
        table += [["Test Samples:", self.test_samples, "", "", "", "", "", ""]]
        table += [["Training Samples:", self.train_samples, "", "", "", "", "", ""]]
        table += [["Total Samples:", self.total_samples, "", "", "", "", "", ""]]
        table += [["Accuracy:", "{}%".format(round(self.accuracy)), "", "", "", "", "", ""]]
        print tabulate(table)

    @property
    def total_samples(self):
        return self.train_samples + self.test_samples
