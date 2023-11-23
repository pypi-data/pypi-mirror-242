class SimpleMovingAverage:
    def __init__(self, data, window):
        self.data = data
        self.window = window

    def calculate_sma(self):
        sma = []
        for i in range(len(self.data) - self.window + 1):
            window_data = self.data[i:i + self.window]
            window_avg = sum(window_data) / self.window
            sma.append(window_avg)
        return sma

    def get_sma_summary(self):
        """
        Generates a summary of the Simple Moving Average calculation.

        Returns:
            dict: Summary of SMA calculation factors and resulting values.
        """
        summary = {
            'Data': self.data,
            'Window': self.window,
            'SMA': self.calculate_sma()
        }
        return summary