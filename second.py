import pandas as pd
import plotly.express as px


diamonds = pd.read_csv("diamonds.csv")
pd.options.display.width = None
print(diamonds[0:5])

print()
print(len(diamonds.values))


data = diamonds
# print(diamonds.get('total_sales_price'))
minimum = (-1, 10000000000)
maximum = (-1, -1)
for i in enumerate(diamonds.get('total_sales_price')):
    if i[1] > maximum[1]:
        maximum = i
    if i[1] < minimum[1]:
        minimum = i
print(*minimum, sep=' - ')
print(*maximum, sep=' - ')
print()


counter_bad = 0
for i in diamonds.values:
    for j in i:
        if j == 'unknown' or j == 'None':
            counter_bad += 1
print(counter_bad)
print()


columns = set()
for i in diamonds.keys():
    for j in diamonds.get(i):
        if j == 'unknown' or j == 'None':
            columns.add(i)
            break
print(*columns, sep='\n')
print()


cnt = 0
for i in diamonds.keys():
    if i.startswith('fancy_color_') or i.startswith('fluor_'):
        cnt += 1
print(cnt)


cnt_not_empty = 0
for i in diamonds.keys():
    if i.startswith('fancy_color_') or i.startswith('fluor_'):
        cnt = 0
        print(i, end=': ')
        for j in diamonds.get(i):
            if j != 'unknown' and j != 'None':
                cnt += 1
        print(cnt)
        cnt_not_empty += cnt
print('Summary:', cnt_not_empty)
print()


for i in diamonds.keys():
    if i.startswith('fancy_color_') or i.startswith('fluor_'):
        diamonds.drop(i, axis=1, inplace=True)
print(len(diamonds.keys()))
print()


#---
cnt = 0
for i in diamonds.keys():
    if i.startswith('culet_'):
        cnt += 1
print(cnt)

cnt_not_empty = 0
for i in diamonds.keys():
    if i.startswith('culet_'):
        cnt = 0
        print(i, end=': ')
        for j in diamonds.get(i):
            if j != 'unknown' and j != 'None':
                cnt += 1
        print(cnt)
        cnt_not_empty += cnt
print('Summary:', cnt_not_empty)

print(len(diamonds.keys()))
for i in diamonds.keys():
    if i.startswith('culet_'):
        diamonds.drop(i, axis=1, inplace=True)
print(len(diamonds.keys()))
print()
#---

dollars = 0
for k in diamonds.get('total_sales_price'):
    dollars += k
print("Summary price: ", "{:,}".format(dollars), '$', sep='')
print()

print(diamonds[::2])
print()

print(diamonds[::6])
print()

print(diamonds.select_dtypes(exclude=["number","bool_"]))
print()

arr = [i for i in diamonds.get('total_sales_price')]
res = sum([i*i for i in arr])
print("{:,}".format(res))
print()

fig = px.bar(diamonds[diamonds.color != 'unknown'], y="total_sales_price", x="color", barmode="group")
# fig.show()

fig = px.scatter(diamonds[diamonds.color != 'unknown'], y="total_sales_price", x="color")
# fig.show()

count = {}
for i in diamonds.get('lab'):
    count[i] = count.get(i, 0) + 1
fig = px.bar(pd.DataFrame([[i, count[i]] for i in count.keys()], columns=['lab', 'number']), x="lab", y="number")
# fig.show()


fig = px.scatter(diamonds, y="total_sales_price", x="carat_weight")
# fig.show()

count = {}
for i in diamonds.get('cut_quality'):
    count[i] = count.get(i, 0) + 1
fig = px.bar(pd.DataFrame([[i, count[i]] for i in count.keys()], columns=['cut_quality', 'number']), x="cut_quality", y="number")
# fig.show()