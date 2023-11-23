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
    def __init__(self, x, y, m_curr=0, c_curr=0, iteration=100, rate=0.01):
        self.x = x
        self.y = y
        #predicted_y using initial slope and intercept
        self.predicted_y = (m_curr * x) + c_curr
        self.m_curr = m_curr
        self.c_curr = c_curr
        self.iteration = iteration
        self.rate = rate

    def cost_function(self):
        N = len(self.y)
        #mean squared error
        return sum((self.y - self.predicted_y) ** 2) / N

    def calculation(self):
        N = float(len(self.y))
        gradient_descent = []
        #perform gradient descent iterations
        for i in range(self.iteration):
            #predicted y values using current slope and intercept
            self.predicted_y = (self.m_curr * self.x) + self.c_curr
            cost = self.cost_function()
            #gradients for slope (m_grad) and intercept (c_grad)
            m_gradient = -(2 / N) * np.sum(self.x * (self.y - self.predicted_y))
            c_gradient = -(2 / N) * np.sum(self.y - self.predicted_y)
            #update the slope and intercept using gradient and learning rate
            self.m_curr -= self.rate * m_gradient
            self.c_curr -= self.rate * c_gradient
            gradient_descent.append({"m_curr": round(self.m_curr, 4), "c_curr": round(self.c_curr, 4), "cost": round(cost, 4)})
        return gradient_descent

class LinearRegression:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_mean = np.mean(x)
        self.y_mean = np.mean(y)
        self.x_value = x - self.x_mean
        self.y_value = y - self.y_mean
        self.x_value_square = self.x_value**2
        self.x_value_square_total = np.sum(self.x_value_square)
        self.x_y_value_square = self.x_value * self.y_value
        self.x_y_value_square_total = np.sum(self.x_y_value_square)
        self.b1 = self.x_y_value_square_total / self.x_value_square_total
        self.bo = self.y_mean - (self.b1 * self.x_mean)
        self.n = len(x)
        self.learning_rate = 0.01
        self.train_mse_history = []

    def predict(self, x):
        return self.bo + self.b1 * x

    def mean_squared_error(self):
        y_pred = self.predict(self.x)
        return np.sum((y_pred - self.y)**2) / self.n

    def root_mean_squared_error(self):
        return np.sqrt(self.mean_squared_error())

    def r_squared(self):
        y_mean_line = np.full_like(self.y, self.y_mean)
        total_sum_squares = np.sum((self.y - y_mean_line)**2)
        residual_sum_squares = np.sum((self.y - self.predict(self.x))**2)
        return 1 - (residual_sum_squares / total_sum_squares)

    def intercept(self):
        return self.bo

    def coefficient(self):
        return self.b1

    def model_evaluation(self):
        data = [
            {"Parameter": "Intercept", "Value": round(self.bo, 4)},
            {"Parameter": "Slope", "Value": round(self.b1, 4)},
            {"Parameter": "R-squared", "Value": round(self.r_squared(), 4)},
            {"Parameter": "Mean Squared Error", "Value": round(self.mean_squared_error(), 4)},
            {"Parameter": "Root Mean Squared Error", "Value": round(self.root_mean_squared_error(), 4)}
        ]
        tab(data)

    def gradient_descent(self, epochs, learning_rate):
        gd = GradientDescent(self.x, self.y, iteration=epochs, rate=learning_rate)
        gradient_descent_result = gd.calculation()

        #gradient descent results
        gradient_descent_data = [
            {"Iteration": i + 1, "m_curr": round(row['m_curr'], 4), "c_curr": round(row['c_curr'], 4), "Cost": round(row['cost'], 4)}
            for i, row in enumerate(gradient_descent_result)
        ]
        tab(gradient_descent_data)

        #update self.train_mse_history
        self.train_mse_history = [row['cost'] for row in gradient_descent_result]

    def plot_learning_curve(self):
        plt.plot(range(1, len(self.train_mse_history) + 1), self.train_mse_history, label='Train')
        plt.title('Learning Curve (MSE vs Iterations)')
        plt.xlabel('Iterations')
        plt.ylabel('Mean Squared Error')
        plt.legend()
        plt.show()
