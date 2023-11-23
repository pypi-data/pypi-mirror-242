import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML

def tab(data):
    if isinstance(data, list) and all(isinstance(d, dict) for d in data):
        columns = list(data[0].keys())
        rows = [list(row.values()) for row in data]
    elif isinstance(data, list) and all(isinstance(d, list) for d in data):
        columns = data[0]
        rows = data[1:]
    else:
        raise ValueError("Input data should be a list of dictionaries or a list of lists.")

    table_html = "<table>"
    table_html += "<tr>"
    for col in columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr>"

    for row in rows:
        table_html += "<tr>"
        for col in row:
            table_html += f"<td>{col}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    display(HTML(table_html))

class GradientDescent:
    def __init__(self, x, y, coefficients=None, iteration=100, rate=0.01):
        self.x = x
        self.y = y
        self.predicted_y = np.dot(x, coefficients) if coefficients is not None else np.zeros(len(y))
        self.coefficients = coefficients if coefficients is not None else np.zeros(x.shape[1])
        self.iteration = iteration
        self.rate = rate

    def cost_function(self):
        N = len(self.y)
        return np.sum((self.y - self.predicted_y) ** 2) / N

    def calculation(self):
        N = float(len(self.y))
        gradient_descent = []

        for i in range(self.iteration):
            self.predicted_y = np.dot(self.x, self.coefficients)
            cost = self.cost_function()
            gradient = -(2/N) * np.dot(self.x.T, (self.y - self.predicted_y))
            self.coefficients -= self.rate * gradient
            gradient_descent.append({"coefficients": np.copy(self.coefficients), "cost": cost})

        return gradient_descent

class MultipleLinear:
    def __init__(self, X, y):
        self.X = np.column_stack((np.ones(len(X)), X))
        self.y = y
        self.coefficients = np.zeros(self.X.shape[1])
        self.n = len(X)
        self.learning_rate = 0.01
        self.train_mse_history = []

    def predict(self, X):
        return np.dot(X, self.coefficients)

    def mean_squared_error(self, y_pred):
        return np.sum((y_pred - self.y)**2) / self.n

    def root_mean_squared_error(self, y_pred):
        return np.sqrt(self.mean_squared_error(y_pred))

    def r_squared(self, y_pred):
        y_mean_line = np.full_like(self.y, np.mean(self.y))
        total_sum_squares = np.sum((self.y - y_mean_line)**2)
        residual_sum_squares = np.sum((self.y - y_pred)**2)
        return 1 - (residual_sum_squares / total_sum_squares)

    def model_evaluation(self):
        y_pred = self.predict(self.X)
        data = [
            {"Parameter": "Intercept", "Value": round(self.coefficients[0], 4)},
            {"Parameter": "Coefficients", "Value": [round(b, 4) for b in self.coefficients[1:]]},
            {"Parameter": "R-squared", "Value": round(self.r_squared(y_pred), 4)},
            {"Parameter": "Mean Squared Error", "Value": round(self.mean_squared_error(y_pred), 4)},
            {"Parameter": "Root Mean Squared Error", "Value": round(self.root_mean_squared_error(y_pred), 4)}
        ]
        tab(data)

    def gradient_descent(self, epochs, learning_rate):
        gd = GradientDescent(self.X, self.y, coefficients=self.coefficients, iteration=epochs, rate=learning_rate)
        gradient_descent_result = gd.calculation()
        #gradient descent results
        gradient_descent_data = [
            {"Iteration": i + 1, "Coefficients": [round(b, 4) for b in row['coefficients']], "Cost": round(row['cost'], 4)}
            for i, row in enumerate(gradient_descent_result)
        ]
        tab(gradient_descent_data)
        #update self.train_mse_history
        self.train_mse_history = [row['cost'] for row in gradient_descent_result]

    def plot_learning_curve(self):
        plt.plot(range(1, len(self.train_mse_history) + 1), self.train_mse_history)
        plt.grid(True, ls='--', alpha=0.5)
        plt.title('Learning Curve (MSE vs Iterations)')
        plt.xlabel('Iterations')
        plt.ylabel('Mean Squared Error')
        plt.show()