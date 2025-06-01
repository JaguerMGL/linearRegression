import csv
import matplotlib.pyplot as plt

def load_data(filename):
    """Load data from CSV file"""
    km = []
    price = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            km.append(float(row['km']))
            price.append(float(row['price']))
    return km, price

def create_ticks(min_val, max_val, num_ticks):
    """Create evenly spaced tick values"""
    if num_ticks <= 1:
        return [min_val]
    
    step = (max_val - min_val) / (num_ticks - 1)
    ticks = []
    for i in range(num_ticks):
        tick = min_val + i * step
        ticks.append(tick)
    return ticks

def plot_data_distribution(km, price):
    """Create a data distribution chart"""
    plt.figure(figsize=(10, 6))
    
    # Main chart with data points
    plt.scatter(km, price, color='blue', alpha=0.7, s=50)
    plt.xlabel('Mileage (km)')
    plt.ylabel('Price (€)')
    plt.title('Price vs Mileage Distribution')
    plt.grid(True, alpha=0.3)
    
    # Add more reference values on axes
    km_min, km_max = min(km), max(km)
    price_min, price_max = min(price), max(price)
    
    # Set more ticks on x-axis (mileage)
    km_ticks = create_ticks(km_min, km_max, 10)
    plt.xticks(km_ticks, [f'{int(tick):,}' for tick in km_ticks], rotation=45)
    
    # Set more ticks on y-axis (price)
    price_ticks = create_ticks(price_min, price_max, 8)
    plt.yticks(price_ticks, [f'{int(tick):,}' for tick in price_ticks])
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        km, price = load_data("data.csv")
        plot_data_distribution(km, price)
    except FileNotFoundError:
        print("❌ Error: File 'data.csv' not found.")
        print("   Make sure the file exists in the current directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")