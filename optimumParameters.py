import csv
import json
from train import load_data, normalize_features, estimate_price

def test_hyperparameters():
    x, y = load_data("data.csv")
    x_normalized, x_min, x_max = normalize_features(x)
    m = len(x_normalized)
    
    learning_rates = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    max_iterations = 2000
    
    results = []
    
    for lr in learning_rates:
        print(f"\nTesting with learning_rate = {lr}")
        
        theta0 = 0.0
        theta1 = 0.0
        prev_cost = float('inf')
        convergence_iteration = max_iterations
        
        for iteration in range(max_iterations):
            sum_error_0 = 0
            sum_error_1 = 0
            
            for i in range(m):
                prediction = estimate_price(x_normalized[i], theta0, theta1)
                error = prediction - y[i]
                sum_error_0 += error
                sum_error_1 += error * x_normalized[i]
            
            theta0 = theta0 - (lr * sum_error_0 / m)
            theta1 = theta1 - (lr * sum_error_1 / m)
            
            if iteration % 100 == 0:
                cost = sum((estimate_price(x_normalized[i], theta0, theta1) - y[i])**2 for i in range(m)) / (2*m)                
                if abs(prev_cost - cost) / prev_cost < 0.001:
                    convergence_iteration = iteration
                    print(f"  Convergence reached at iteration {iteration}, Cost: {cost:.2f}")
                    break
                prev_cost = cost
        
        final_cost = sum((estimate_price(x_normalized[i], theta0, theta1) - y[i])**2 for i in range(m)) / (2*m)
        results.append({
            'learning_rate': lr,
            'convergence_iteration': convergence_iteration,
            'final_cost': final_cost,
            'theta0': theta0,
            'theta1': theta1
        })
    
    return results

if __name__ == "__main__":
    results = test_hyperparameters()
    
    print("\n" + "="*60)
    print("OPTIMIZATION RESULTS")
    print("="*60)
    
    for result in results:
        print(f"Learning Rate: {result['learning_rate']:<6} | "
              f"Convergence: {result['convergence_iteration']:<4} iter | "
              f"Final Cost: {result['final_cost']:.2f}")
    
    best = min(results, key=lambda x: x['convergence_iteration'])
    print(f"\nOPTIMAL: learning_rate={best['learning_rate']}, "
          f"iterations={best['convergence_iteration']}")