import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML

class PolynomialRegression:
    def __init__(self, degree, learning_rate, epochs):
        self.degree = degree
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.theta = None
        self.train_mse_history = []
        self.test_mse_history = []
        self.evaluation_results = None

    def _create_polynomial_features(self, X):
        X_poly = np.c_[np.ones((len(X), 1)), X]
        for d in range(2, self.degree + 1):
            X_poly = np.c_[X_poly, X**d]
        return X_poly

    def fit(self, X_train, y_train, X_test, y_test):
        X_poly_train = self._create_polynomial_features(X_train)
        X_poly_test = self._create_polynomial_features(X_test)

        self.theta = np.random.randn(self.degree + 1, 1)
        #clear the train MSE history
        self.train_mse_history = [] 
        #clear the test MSE history
        self.test_mse_history = []  

        for epoch in range(self.epochs):
            y_pred_train = X_poly_train.dot(self.theta)
            gradients = 2/len(y_train) * X_poly_train.T.dot(y_pred_train - y_train)
            self.theta -= self.learning_rate * gradients

            # Calculate and store train Mean Squared Error
            train_mse = np.mean((y_pred_train - y_train)**2)
            self.train_mse_history.append(train_mse)

            # Calculate and store test Mean Squared Error
            y_pred_test = X_poly_test.dot(self.theta)
            test_mse = np.mean((y_pred_test - y_test)**2)
            self.test_mse_history.append(test_mse)

    def predict(self, X):
        X_poly = self._create_polynomial_features(X)
        return X_poly.dot(self.theta)

    def model_evaluation(self, X_test, y_test):
        y_pred_test = self.predict(X_test)

        # Calculate R-squared
        ss_total = np.sum((y_test - np.mean(y_test))**2)
        ss_residual = np.sum((y_test - y_pred_test)**2)
        r_squared = 1 - (ss_residual / ss_total)

        # Calculate MSE and MAE
        mse = np.mean((y_test - y_pred_test)**2)
        mae = np.mean(np.abs(y_test - y_pred_test))

        self.evaluation_results = {
            'R-squared': r_squared,
            'Mean Squared Error': mse,
            'Mean Absolute Error': mae
        }

        # Display evaluation results
        self._display_evaluation_results()

    def _display_evaluation_results(self):
        if not isinstance(self.evaluation_results, dict):
            raise ValueError("Evaluation results should be a dictionary.")

        columns = list(self.evaluation_results.keys())
        values = list(self.evaluation_results.values())

        table_html = "<table>"
        table_html += "<tr>"
        for col in columns:
            table_html += f"<th>{col}</th>"
        table_html += "</tr>"

        table_html += "<tr>"
        for val in values:
            table_html += f"<td>{val:.4f}</td>"
        table_html += "</tr>"

        table_html += "</table>"

        display(HTML(table_html))

    def plot_mse_history(self):
        plt.plot(range(1, self.epochs + 1), self.train_mse_history, label='Train')
        plt.plot(range(1, self.epochs + 1), self.test_mse_history, label='Test')
        plt.grid(True, ls='--', color='grey', alpha=0.5)
        plt.title('Learning Curve')
        plt.xlabel('Epochs')
        plt.ylabel('Mean Squared Error')
        plt.legend()
        plt.show()

# Example usage:
degree = 2
learning_rate = 0.01
epochs = 50

# Sample data
np.random.seed(0)
X_train = 2 * np.random.rand(100, 1)
y_train = 4 + 3 * X_train + 1.5 * X_train**2 + np.random.randn(100, 1)

X_test = 2 * np.random.rand(20, 1)
y_test = 4 + 3 * X_test + 1.5 * X_test**2 + np.random.randn(20, 1)

# Create and train the model
poly_model = PolynomialRegression(degree, learning_rate, epochs)
poly_model.fit(X_train, y_train, X_test, y_test)

# Evaluate the model and display results
poly_model.model_evaluation(X_test, y_test)

# Plot MSE history for both training and test data
poly_model.plot_mse_history()
