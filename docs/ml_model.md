# Machine Learning Integration

The core intelligence of Civic Resolve lies in its ability to automatically route complaints to the correct maintenance department while filtering out noise and ambiguous inputs.

## Model Overview

We use a Natural Language Processing (NLP) pipeline to analyze the text of maintenance complaints.

- **Preprocessing**: Complaint descriptions are processed using `TfidfVectorizer` to capture technical keywords and phrases.
- **Classifier**: The system uses a **Multinomial Naive Bayes** classifier, which is a probabilistic model well-suited for text classification tasks.

## Intelligent Triage (Spam & Uncertainty)

The model goes beyond simple classification by detecting when it is "confused" or when the input is low-quality:

- **Spam Detection**: If the maximum probability for any wing is below **30%**, or if the description is shorter than 10 characters, the ticket is flagged as `Spam/General`.
- **Uncertainty Routing**: If the confidence is between **30% and 50%**, the ticket is flagged as `Uncertain/General`. 
- **Universal Visibility**: All flagged tickets are routed to the `General` wing, making them visible to all maintenance staff for manual triage.

## Files

- `project/model.ipynb`: The primary notebook for data analysis, cleaning, and model training.
- `project/model.pkl`: The exported Multinomial Naive Bayes model.
- `project/vectorizer.pkl`: The saved TF-IDF vectorizer.

## Retraining the Model

To update the model with new data:
1. Ensure `project/data/complaints.csv` contains accurate labels.
2. Open `project/model.ipynb` and run the cells to re-train and export the model.
3. The new `.pkl` files will be generated in the project root.
4. Restart the Flask application to load the improved model.
