import pickle
import os

class predictSentiment():
    def __init__(self) -> None:
        with open(os.path.join("models", "model_ann.pkl"), 'rb') as f:
            self.model_ann = pickle.load(f)
    
    def predict(self, vect) -> str:
        return self.model_ann.predict(vect)[0]