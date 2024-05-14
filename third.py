import pandas as pd
import matplotlib.pyplot as plt


diamonds = pd.read_csv("diamonds.csv")
diamonds = diamonds[["meas_length","meas_width", "meas_depth", "total_sales_price"]]
print(diamonds[:10])
print()

diamonds = diamonds.sample(frac=1)
print(diamonds)
print()

sum_mink = []
for i in diamonds[["meas_length","meas_width", "meas_depth"]].values:
    now = 0
    for j in i:
        now += j ** 3
    now **= 1/3
    sum_mink.append([now])
df = pd.DataFrame(sum_mink, columns=['sum_mink'])
print(df)
print()

new_data = pd.concat([df, diamonds['total_sales_price']], axis=1).sample(frac=1)
print(new_data)
print()

border = len(new_data) // 10 * 8
training = new_data[:border]
testing = new_data[border:]
print(training)
print(testing)

graph = plt
graph.scatter(training['sum_mink'], training['total_sales_price'], alpha=0.05, c='blue')
graph.show()

graph.scatter(training['sum_mink'], training['total_sales_price'], alpha=0.05, c='blue')
graph.scatter(testing['sum_mink'], testing['total_sales_price'], alpha=0.05, c='red')
graph.show()