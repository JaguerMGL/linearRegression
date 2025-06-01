# 🚗 ft_linear_regression

> A simple introduction to Machine Learning with gradient descent – 42 Network project

## 📌 Objective

The goal of this project is to implement a basic **linear regression** model to predict the **price of a car** based on its **mileage**, using **gradient descent**.

---

## 🧠 Concept

The model uses the following hypothesis:

estimatePrice(mileage) = theta0 + theta1 * mileage

---

## 📁 Project Structure

- `train.py`: trains the model on `data.csv` and saves the learned parameters in `model.json`.
- `predict.py`: loads the model and predicts a car's price based on user-input mileage.
- `data.csv`: contains training data (mileage, price).
- `model.json`: generated file with learned θ0 and θ1 values.
---

## 🚀 How to Use

### 1. Add your data

Create a file named `data.csv`:

km,price
240000,3650
139800,3800
...

### 2. Train the model

Run the following command : python3 train.py

### 3. Predict a price

Run the following command : python3 predict.py
Then enter a mileage when prompted, and the program will return the estimated price.
---

### 🔧 Tuning the Model

To experiment with different values for the learning rate and number of iterations, you can run: python3 test.py
This script can help you find better hyperparameters for faster or more accurate convergence.


