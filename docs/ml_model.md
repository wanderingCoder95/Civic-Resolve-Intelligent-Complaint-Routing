# Machine Learning Integration

The core intelligence of Civic Resolve lies in its ability to automatically route complaints to the correct maintenance department.

## Model Overview

We use a Natural Language Processing (NLP) pipeline to analyze the text of maintenance complaints.

- **Preprocessing**: Complaint descriptions are tokenized and cleaned.
- **Vectorization**: We use a `TfidfVectorizer` to convert text into numerical features, emphasizing unique keywords that define different maintenance wings.
- **Classifier**: The system uses a machine learning model (Multinomial Naive Bayes) trained on historical complaint data.

## Features

- **Real-time Prediction**: When a user submits a complaint, the model predicts the wing instantly before saving the record.
- **High Accuracy**: The model is trained to distinguish between similar categories like "Electrical - Lighting" and "Electrical - Power Outage".
- **Extensible**: New categories can be added by retraining the model with updated data in `model.ipynb`.

## Files

- `project/model.ipynb`: Contains the training logic, exploratory data analysis (EDA), and model evaluation metrics.
- `project/model.pkl`: The exported model ready for production use.
- `project/vectorizer.pkl`: The saved TF-IDF vectorizer ensures that input text is processed identically during inference as it was during training.

## Retraining the Model

To update the model with new data:
1. Update `project/data/complaints.csv` with fresh samples.
2. Open `project/model.ipynb` in a Jupyter environment.
3. Run all cells to retrain and export the new `.pkl` files.
4. Restart the Flask application to load the updated model.
