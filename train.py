import csv
import json

def load_data(filename):
    x = []
    y = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x.append(float(row['km']))
            y.append(float(row['price']))
    return x, y

def normalize_features(x):
    x_min = min(x)
    x_max = max(x)
    x_normalized = [(xi - x_min) / (x_max - x_min) for xi in x]
    return x_normalized, x_min, x_max

def estimate_price(km, theta0, theta1):
    return theta0 + theta1 * km

def train(x, y, learning_rate=0.3, iterations=400):
    # Normaliser les features
    x_normalized, x_min, x_max = normalize_features(x)
    
    theta0 = 0.0
    theta1 = 0.0
    m = len(x_normalized)
    
    for iteration in range(iterations):
        sum_error_0 = 0
        sum_error_1 = 0
        for i in range(m):
            prediction = estimate_price(x_normalized[i], theta0, theta1)
            error = prediction - y[i]
            sum_error_0 += error
            sum_error_1 += error * x_normalized[i]
        
        tmp_theta0 = theta0 - (learning_rate * sum_error_0 / m)
        tmp_theta1 = theta1 - (learning_rate * sum_error_1 / m)
        theta0 = tmp_theta0
        theta1 = tmp_theta1
        
        # if iteration % 250 == 0:
        #     cost = sum((estimate_price(x_normalized[i], theta0, theta1) - y[i])**2 for i in range(m)) / (2*m)
        #     print(f"Iteration {iteration}, Cost: {cost:.2f}")
    
    return theta0, theta1, x_min, x_max

def save_model(theta0, theta1, x_min, x_max, filename="model.json"):
    with open(filename, "w") as f:
        json.dump({
            "theta0": theta0, 
            "theta1": theta1,
            "x_min": x_min,
            "x_max": x_max
        }, f)

if __name__ == "__main__":
    x, y = load_data("data.csv")
    theta0, theta1, x_min, x_max = train(x, y)
    save_model(theta0, theta1, x_min, x_max)
    # print("training completed.")
    # print(f"theta0 = {theta0}")
    # print(f"theta1 = {theta1}")