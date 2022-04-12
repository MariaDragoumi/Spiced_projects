import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Task 1: Read the x/y data points from the file datapoints.csv into Python
df = pd.read_csv('datapoints.csv')

# Task 2: Create a scatterplot of the data.
# plt.scatter(df['x'],df['y'])
# plt.show()


def fun_y(x, a=10, b=0):
    return x*a+b


def mean_squared_error(x, ytrue, a, b=0):
    y = fun_y(x, a, b)
    N = y.size
    mse = sum((y-ytrue)**2)/N
    return mse


def optimize_a(a_init, b, x, y):
    a = a_init
    mse = mean_squared_error(df['x'], df['y'], a, b)
    for _ in range(100):
        a_new = a - 0.1
        if mse > mean_squared_error(df['x'], df['y'], a_new, b):
            mse = mean_squared_error(df['x'], df['y'], a_new, b)
            a = a_new
        else:
            break
    return a, mse


def optimize_a_and_b(a_init, b_init, x, y):
    b = b_init
    a, mse = optimize_a(a_init, b_init, x, y)
    for _ in range(100):
        b_new = b - 0.1
        if mse > optimize_a(a_init, b_new, x, y)[1]:
            a, mse = optimize_a(a_init, b_new, x, y)
            b = b_new
        else:
            break
    return a, b, mse


a, b, mse = optimize_a_and_b(10, 3, df['x'], df['y'])

with open('assessment_solution.csv', 'w') as f:
    f.write(f'a , b , MSE\n {a:.1f}, {b:.1f}, {mse:.3f}')

plt.scatter(df['x'], df['y'], label='Data points')
plt.plot(df['x'], a*df['x'] + b, label=f'y=a*x+b, a: {a:.1f}, b: {b:.1f}')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('assessment_figure.png')


# Analytical solution
'''
    a_opt = COV(X,Y)/VAR(X), b_opt = X - bar - a*Y - bar
'''
a_opt = np.cov(df['x'], df['y'])[0][1]/np.cov(df['x'], df['y'])[0][0]
b_opt = np.mean(df['y'])-a_opt*np.mean(df['x'])
mse_opt = mean_squared_error(df['x'], df['y'], a_opt, b_opt)

# print(f'Analytical solution:\n a = {a_opt}\n b = {b_opt}\n MSE = {mse_opt}')
with open('analytical_solution.csv', 'w') as f:
    f.write(f'a , b , MSE\n {a_opt:.3f}, {b_opt:.3f}, {mse_opt:.4f}')
