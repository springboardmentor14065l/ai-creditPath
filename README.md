# AI Credit Risk Prediction

## Project Overview

This project predicts whether a loan applicant is likely to **default on a loan** using Machine Learning.
The model is trained on a dataset containing financial and demographic information of applicants.

The goal is to help financial institutions **assess credit risk** and make better lending decisions.

---

## Dataset

File: `Loan_default.csv`

The dataset contains various features related to loan applicants such as:

* Income
* Loan amount
* Credit history
* Other financial indicators

### Target Variable

`Default`

* **0 → No Default**
* **1 → Default**

---

## Project Structure

```
ai-creditPath/
│
├── analyze_data.py      # Data analysis and exploration
├── load_dataset.py      # Loads the dataset
├── preprocess.py        # Data preprocessing
├── train_model.py       # Train the machine learning model
├── save_model.py        # Save the trained model
├── Loan_default.csv     # Dataset
├── loan_model.pkl       # Trained model
└── README.md            # Project documentation
```

---

## Technologies Used

* Python
* Pandas
* Scikit-learn
* Joblib

---

## Machine Learning Model

Model Used:
**Random Forest Classifier**

The dataset is split into **training and testing sets** to evaluate model performance.

### Model Accuracy

Example Accuracy:

```
Accuracy ≈ 0.88
```

---

## How to Run the Project

### 1. Load Dataset

```
python load_dataset.py
```

### 2. Analyze Data

```
python analyze_data.py
```

### 3. Train Model

```
python train_model.py
```

### 4. Save Model

```
python save_model.py
```

After running the scripts, the trained model will be saved as:

```
loan_model.pkl
```

---

## Future Improvements

* Deploy the model using Flask API
* Build a web interface for predictions
* Improve model performance with advanced algorithms

---

## Author

AI Credit Risk Prediction Project
