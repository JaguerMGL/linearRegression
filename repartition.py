import csv
import matplotlib.pyplot as plt
import json

def load_data(filename):
    km = []
    price = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            km.append(float(row['km']))
            price.append(float(row['price']))
    return km, price

def load_model(filename="model.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data["theta0"], data["theta1"], data["x_min"], data["x_max"]
    except FileNotFoundError:
        return None, None, None, None

def normalize_km(km, x_min, x_max):
    return (km - x_min) / (x_max - x_min)

def estimate_price(km_normalized, theta0, theta1):
    return theta0 + theta1 * km_normalized

def create_ticks(min_val, max_val, num_ticks):
    if num_ticks <= 1:
        return [min_val]
    
    step = (max_val - min_val) / (num_ticks - 1)
    ticks = []
    for i in range(num_ticks):
        tick = min_val + i * step
        ticks.append(tick)
    return ticks

def plot_data_distribution(km, price):
    plt.figure(figsize=(10, 6))
    
    plt.scatter(km, price, color='blue', alpha=0.7, s=50, label='Data points')
    plt.xlabel('Mileage (km)')
    plt.ylabel('Price (€)')
    plt.title('Price vs Mileage Distribution with Linear Regression')
    plt.grid(True, alpha=0.3)
    
    theta0, theta1, x_min, x_max = load_model()
    if theta0 is not None:
        km_min, km_max = min(km), max(km)
        km_line = create_ticks(km_min, km_max, 100)
        price_line = []
        
        for km_val in km_line:
            km_normalized = normalize_km(km_val, x_min, x_max)
            predicted_price = estimate_price(km_normalized, theta0, theta1)
            price_line.append(max(0, predicted_price))  # Ensure price >= 0
        
        plt.plot(km_line, price_line, color='red', linewidth=2, 
                label=f'Linear regression: y = {theta0:.0f} + {theta1:.2f}x')
        plt.legend()
    else:
        print("⚠️  Warning: model.json not found. Run train.py first to see the regression line.")
    
    km_min, km_max = min(km), max(km)
    price_min, price_max = min(price), max(price)
    km_ticks = create_ticks(km_min, km_max, 10)
    plt.xticks(km_ticks, [f'{int(tick):,}' for tick in km_ticks], rotation=45)
    price_ticks = create_ticks(price_min, price_max, 8)
    plt.yticks(price_ticks, [f'{int(tick):,}' for tick in price_ticks])
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        km, price = load_data("data.csv")
        plot_data_distribution(km, price)
    except FileNotFoundError:
        print("Error: File 'data.csv' not found.")
        print("Make sure the file exists in the current directory.")
    except Exception as e:
        print(f"Unexpected error: {e}")