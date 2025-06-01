import csv
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
        print("Error: model.json not found. Run train.py first.")
        return None, None, None, None

def normalize_km(km, x_min, x_max):
    return (km - x_min) / (x_max - x_min)

def estimate_price(km_normalized, theta0, theta1):
    return theta0 + theta1 * km_normalized

def calculate_accuracy(km, price, theta0, theta1, x_min, x_max):
    print("-" * 80)
    print(f"{'Index':<6} {'Mileage (km)':<12} {'Real Price':<12} {'Estimated':<12} {'Error':<10} {'Error %':<8}")
    print("-" * 80)
    
    total_error_percentage = 0
    valid_comparisons = 0
    for i in range(len(km)):
        km_normalized = normalize_km(km[i], x_min, x_max)
        estimated_price = estimate_price(km_normalized, theta0, theta1)
        real_price = price[i]
        error = abs(estimated_price - real_price)
        error_percentage = (error / real_price) * 100 if real_price > 0 else 0
        total_error_percentage += error_percentage
        valid_comparisons += 1
        print(f"{i+1:<6} {km[i]:<12,.0f} {real_price:<12,.0f} {estimated_price:<12,.0f} {error:<10,.0f} {error_percentage:<8.1f}%")
    
    average_error_percentage = total_error_percentage / valid_comparisons if valid_comparisons > 0 else 0
    global_precision_percentage = 100 - average_error_percentage
    print("=" * 80)
    print("GLOBAL PRECISION RESULTS")
    print(f"Total comparisons: {valid_comparisons}")
    print(f"Average error percentage: {average_error_percentage:.2f}%")
    print(f"GLOBAL PRECISION: {global_precision_percentage:.2f}%")
    
    excellent_predictions = sum(1 for i in range(len(km)) 
                               if abs(estimate_price(normalize_km(km[i], x_min, x_max), theta0, theta1) - price[i]) / price[i] <= 0.05)
    good_predictions = sum(1 for i in range(len(km)) 
                          if abs(estimate_price(normalize_km(km[i], x_min, x_max), theta0, theta1) - price[i]) / price[i] <= 0.10)
    acceptable_predictions = sum(1 for i in range(len(km)) 
                                if abs(estimate_price(normalize_km(km[i], x_min, x_max), theta0, theta1) - price[i]) / price[i] <= 0.20)
    return global_precision_percentage

def main():
    try:
        km, price = load_data("data.csv")
        theta0, theta1, x_min, x_max = load_model()
        if theta0 is None:
            return
        precision = calculate_accuracy(km, price, theta0, theta1, x_min, x_max)
        print()
            
    except FileNotFoundError:
        print("Error: File 'data.csv' not found.")
        print("Make sure the file exists in the current directory.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()