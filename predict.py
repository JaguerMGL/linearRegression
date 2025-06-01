import json

def estimate_price(km, theta0, theta1):
    return theta0 + theta1 * km

def normalize_km(km, x_min, x_max):
    return (km - x_min) / (x_max - x_min)

def load_model(filename="model.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["theta0"], data["theta1"], data["x_min"], data["x_max"]

def find_zero_price_km(theta0, theta1, x_min, x_max):
    # km_normalized = -theta0 / theta1
    km_normalized = -theta0 / theta1
    # Dénormaliser: km = km_normalized * (x_max - x_min) + x_min
    km_zero = km_normalized * (x_max - x_min) + x_min
    return km_zero

if __name__ == "__main__":
    try:
        theta0, theta1, x_min, x_max = load_model()
    except FileNotFoundError:
        print("JSON not found. Run train.py first.")
        exit(1)
    try:
        user_input = input("How many km? ")
        km = float(user_input)
        if km < 0:
            raise ValueError("Negative value not allowed")
    except ValueError:
        print("Invalid input.")
        exit(1)
    
    km_normalized = normalize_km(km, x_min, x_max)
    price = estimate_price(km_normalized, theta0, theta1)
    
    if price < 0:
        km_zero = find_zero_price_km(theta0, theta1, x_min, x_max)
        print(f"Estimated price: 0.00 €")
        print(f"Price becomes 0 at {km_zero:.0f} km")
    else:
        print(f"Estimated price: {price:.2f} €")