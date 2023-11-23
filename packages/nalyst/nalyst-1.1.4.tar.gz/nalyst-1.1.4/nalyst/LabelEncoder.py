class LabelEncoder:
    """
    A custom label encoder for converting categorical data into numerical labels.

    Methods:
        fit(data):
            Fit the encoder to the given categorical data.

        transform(data):
            Transform the provided categorical data into numerical labels based on the fitted encoder.

        fit_transform(data):
            Fit the encoder to the given data and transform it into numerical labels.

        inverse_transform(encoded_data):
            Inverse transform the encoded numerical labels back to their original categorical form.

    Attributes:
        classes_ (dict): Dictionary containing the mapping of unique values to numerical labels.

    Example:
        encoder = CustomLabelEncoder()
        data = ['red', 'green', 'blue', 'green', 'red']
        encoded_data = encoder.fit_transform(data)
        print("Encoded data:", encoded_data)
        # Inverse transform
        decoded_data = encoder.inverse_transform(encoded_data)
        print("Decoded data:", decoded_data)
    """
    def fit(self, data):
        """
        Fit the encoder to the given categorical data.

        Args:
            data (list): The categorical data to fit the encoder.
        """
        self.classes_ = {val: index for index, val in enumerate(set(data))}
        
    def transform(self, data):
        """
        Transform the provided categorical data into numerical labels based on the fitted encoder.

        Args:
            data (list): The categorical data to be transformed.

        Returns:
            list: Transformed data as numerical labels.
        """
        return [self.classes_[val] for val in data]
    
    def fit_transform(self, data):
        """
        Fit the encoder to the given data and transform it into numerical labels.

        Args:
            data (list): The categorical data to fit and transform.

        Returns:
            list: Transformed data as numerical labels.
        """
        self.fit(data)
        return self.transform(data)
    
    def inverse_transform(self, encoded_data):
        """
        Inverse transform the encoded numerical labels back to their original categorical form.

        Args:
            encoded_data (list): The encoded numerical labels to be inverse transformed.

        Returns:
            list: Inverse transformed data in their original categorical form.
        """
        inverted = {index: val for val, index in self.classes_.items()}
        return [inverted[index] for index in encoded_data]

    def get_label_mapping(self):
        """
        Generates a summary of numerical labels assigned to each variable.

        Returns:
            dict: Summary of numerical labels assigned to each unique variable.
        """
        return {value: key for key, value in self.classes_.items()}