import os
import time
import joblib
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier

class Machine:

    def __init__(self, df: DataFrame = None, model_path: str = None, _from_open: bool = False):
        """
        Initializes the Machine instance by either training a new model using the provided DataFrame
        or loading an existing model from the specified model_path.

        Parameters:
        - df (DataFrame): DataFrame containing the training data with features and target.
        - model_path (str): File path to load the saved model from.
        - _from_open (bool): Whether the model is loaded from an existing model.

        """
        self.name = "Random Forest Classifier"
        self.initialized_at = time.time()

        if _from_open:
            # Allow instantiation without df or model_path when called from open()
            return
        if model_path and os.path.exists(model_path):
            # Load the model from the specified path
            self.model = joblib.load(model_path)
            self.initialized_at = os.path.getmtime(model_path)
        elif df is not None:
            # Prepare training data
            self.target = df["Rarity"]
            self.features = df.drop(columns=["Rarity"])
            # Initialize and train the model
            self.model = RandomForestClassifier(random_state=42)
            self.model.fit(self.features, self.target)
        else:
            raise ValueError("Either df or model_path must be provided to initialize the Machine.")

    def __call__(self, feature_basis: DataFrame):
        """
        Makes a prediction based on the provided feature data.

        Parameters:
        - feature_basis (DataFrame): DataFrame containing the feature data for prediction.

        Returns:
        - prediction (str): The predicted class label.
        - confidence (float): The probability of the prediction.
        """
        # Ensure pred_basis has the correct columns
        expected_features = ['Level', 'Health', 'Energy', 'Sanity']
        pred_basis = feature_basis[expected_features]

        # Make prediction
        prediction = self.model.predict(pred_basis)
        probabilities = self.model.predict_proba(pred_basis)

        # Get the index of the predicted class
        predicted_class_index = list(self.model.classes_).index(prediction[0])

        # Get the confidence of the prediction
        confidence = probabilities[0][predicted_class_index]

        return prediction[0], confidence


    def save(self, filepath: str):
        """
        Saves the trained model to the specified filepath using joblib.

        Parameters:
        - filepath (str): The path where the model will be saved.
        """
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")

    @staticmethod
    def open(filepath: str):
        """
        Loads a saved machine learning model from the specified filepath using joblib.

        Parameters:
        - filepath (str): The path to the saved model file.

        Returns:
        - instance (Machine): An instance of the Machine class with the loaded model
        """
        if os.path.exists(filepath):
            instance = Machine(_from_open=True)
            instance.model = joblib.load(filepath)
            instance.name = "Random Forest Classifier"
            instance.initialized_at = os.path.getmtime(filepath)
            return instance
        else:
            raise FileNotFoundError(f"No model found at {filepath}")

    def info(self):
        """
        Returns a string with the name of the base model and the timestamp of initialization.

        Returns:
        - info_str (str): Information about the model.
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.initialized_at))
        return f"Model: {self.name}, Initialized at: {timestamp}"
