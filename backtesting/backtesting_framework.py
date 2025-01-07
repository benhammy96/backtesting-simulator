import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#This function creates synthetic data for the simulation of price and volume over time
def create_synthetic_data(samples=100):
    time_stamps = pd.date_range(start="2025-01-04", periods=samples, freq="T") 
    price_changes = np.cumsum(np.random.normal(0, 1, samples)) + 100   #sim price changes as a random walk
    trading_volumes = np.random.randint(1, 100, size=samples)  #random values
    return pd.DataFrame({"time": time_stamps, "price": price_changes, "volume": trading_volumes})

#calculates the TWAP price by averaging prices over time intervals
def twap(data, total_volume):
    periods = len(data)
    volume_per_period = total_volume / periods
    prices_traded = [] #list to store executed prices
    for _, record in data.iterrows():
        prices_traded.append(record["price"]) #append price for each trade
    avg_price = np.mean(prices_traded)
    return avg_price, prices_traded

#calculates the VWAP by taking the weighted average of price and volume
def vwap(data):
    total_traded_volume = np.sum(data["volume"])
    vwap_value = np.sum(data["price"] * data["volume"]) / total_traded_volume
    return vwap_value

#slippage is the diff between the expected price and the actual execution price
def estimate_slippage(executed_prices, predicted_price):
    average_executed_price = np.mean(executed_prices) #this calculates total volume traded
    price_diff = average_executed_price - predicted_price
    return price_diff

#function to visualize the data
def display_price_chart(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data["time"], data["price"], label="Price")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Sim Price Data")
    plt.legend()
    plt.show()

def main():
    synthetic_data = create_synthetic_data()
    total_order_quantity = 1000 #set total quantity for the trade

    print("Execution Using Time-Weighted Average Price (TWAP)...")
    avg_twap_price, executed_price_list = twap(synthetic_data, total_order_quantity)

    print("Key Metrics...")
    vwap_value = vwap(synthetic_data)
    cost_of_execution = avg_twap_price - vwap_value
    slippage_value = estimate_slippage(executed_price_list, avg_twap_price)

    print(f"TWAP Price: {avg_twap_price:.2f}")
    print(f"VWAP Price: {vwap_value:.2f}")
    print(f"Execution Cost: {cost_of_execution:.2f}")
    print(f"Slippage: {slippage_value:.2f}")
    display_price_chart(synthetic_data)

if __name__ == "__main__":
    main()
