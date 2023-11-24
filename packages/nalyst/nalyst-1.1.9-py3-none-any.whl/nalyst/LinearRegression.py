from typing import List
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


class LinearRegression:
    """
    Class for building and analyzing a linear regression model.
    Attributes:
        x (List[float]): List of x values.
        y (List[float]): List of y values.
        x_mean (float): Mean of x values.
        y_mean (float): Mean of y values.
        x_value (List[float]): List of x values minus x_mean.
        y_value (List[float]): List of y values minus y_mean.
        x_value_square (List[float]): List of squared x values.
        x_value_square_total (float): Sum of x_value_square.
        x_y_value_square (List[float]): List of product of x_value and y_value.
        x_y_value_square_total (float): Sum of x_y_value_square.
        b1 (float): Regression coefficient b1.
        bo (float): Regression coefficient bo.
        n (int): Number of observations.
    Methods:
        fit(X: List[float], y: List[float]) -> None: Fit the linear regression model.
        predict(x: List[float]) -> np.ndarray: Generate predicted y values based on a list of x values.
        mean_squared_error() -> float: Calculate the mean squared error of the model.
        root_mean_squared_error() -> float: Calculate the root mean squared error of the model.
        r_squared() -> float: Calculate the R-squared value of the model.
        intercept() -> float: Get the intercept value.
        coefficient() -> float: Get the coefficient value.
        model_evaluation() -> None: Display coefficient, intercept, R-squared, MSE, and RMSE in an HTML table.
    """

    def __init__(self):
        self.x = None
        self.y = None
        self.x_mean = None
        self.y_mean = None
        self.x_value = None
        self.y_value = None
        self.x_value_square = None
        self.x_value_square_total = None
        self.x_y_value_square = None
        self.x_y_value_square_total = None
        self.b1 = None
        self.bo = None
        self.n = None

    def fit(self, X: List[float], y: List[float]) -> None:
        self.x = list(X)
        self.y = list(y)
        self.n = len(X)
        self.x_mean = sum(X) / self.n
        self.y_mean = sum(y) / self.n
        self.x_value = [value - self.x_mean for value in X]
        self.y_value = [value - self.y_mean for value in y]
        self.x_value_square = [value**2 for value in self.x_value]
        self.x_value_square_total = sum(self.x_value_square)
        self.x_y_value_square = [xv * yv for xv, yv in zip(self.x_value, self.y_value)]
        self.x_y_value_square_total = sum(self.x_y_value_square)
        self.b1 = self.x_y_value_square_total / self.x_value_square_total
        self.bo = self.y_mean - (self.b1 * self.x_mean)

    def predict(self, x: List[float]) -> np.ndarray:
        return np.concatenate([self.bo + self.b1 * xi for xi in x])


    def mean_squared_error(self) -> float:
        y_pred = self.predict(self.x)
        return sum([(y_pred_i - y_i)**2 for y_pred_i, y_i in zip(y_pred, self.y)]) / self.n

    def root_mean_squared_error(self) -> float:
        return self.mean_squared_error() ** 0.5

    def r_squared(self) -> float:
        y_mean_line = [self.y_mean for _ in self.y]
        total_sum_squares = sum([(y - y_mean_line[idx])**2 for idx, y in enumerate(self.y)])
        residual_sum_squares = sum([(self.y[idx] - self.predict([xi])[0])**2 for idx, xi in enumerate(self.x)])
        return 1 - (residual_sum_squares / total_sum_squares)

    def intercept(self) -> float:
        return self.bo

    def coefficient(self) -> float:
        return self.b1

    def model_evaluation(self) -> None:
        data = [
            {"Parameter": "Intercept", "Value": round(self.bo[0], 4)},
            {"Parameter": "Slope", "Value": round(self.b1[0], 4)},
            {"Parameter": "R-squared", "Value": round(self.r_squared(), 4)},
            {"Parameter": "Mean Squared Error", "Value": round(self.mean_squared_error(), 4)},
            {"Parameter": "Root Mean Squared Error", "Value": round(self.root_mean_squared_error(), 4)}
        ]
        tab(data)


# Code developed by Hemant Thapa 
# analyticalharry@gmail.com
# Date: 22.11.2023