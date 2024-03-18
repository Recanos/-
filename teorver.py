import numpy as np
import matplotlib.pyplot as plt

def generate_data(model, size):
    if model == 1:
        return np.random.normal(0, 0.01, size) + 1
    elif model == 2:
        return np.random.normal(0, 0.05, size) + 1
    elif model == 3:
        return np.random.uniform(-0.01, 0.01, size) + 1
    elif model == 4:
        return np.random.uniform(-0.05, 0.05, size) + 1

def calculate_estimates(data, sample_size):
    sample_mean = np.mean(data)
    midrange = (np.max(data) + np.min(data)) / 2
    sample_median = np.median(data)
    if sample_size < 10:
        k = 1
    elif sample_size < 15:
        k = 2
    else:
        k = 3
    sorted_data = np.sort(data)
    trimmed_data = sorted_data[k:-k]
    trimmed_mean = np.mean(trimmed_data)
    return sample_mean, midrange, sample_median, trimmed_mean

def conduct_experiment(model, sample_sizes, num_experiments):
    estimates = {size: [] for size in sample_sizes}
    for size in sample_sizes:
        for _ in range(num_experiments):
            data = generate_data(model, size)
            sample_mean, midrange, sample_median, trimmed_mean = calculate_estimates(data, size)
            estimates[size].append((sample_mean, midrange, sample_median, trimmed_mean))
        
    return estimates

models = [1, 2, 3, 4]
sample_sizes = [15, 30, 100, 1000]
num_experiments = 50

all_estimates = {}
for model in models:
    all_estimates[model] = conduct_experiment(model, sample_sizes, num_experiments)

for num, model in enumerate(models):
    print(f"модель {model}")
    errors = []
    for size in sample_sizes:
        err1 = [abs(1 - i[0]) for i in all_estimates[model][size]]
        err2 = [abs(1 - i[1]) for i in all_estimates[model][size]]
        err3 = [abs(1 - i[2]) for i in all_estimates[model][size]]
        err4 = [abs(1 - i[3]) for i in all_estimates[model][size]]
        errors.append((sum(err1)/num_experiments, sum(err2)/num_experiments, sum(err3)/num_experiments, sum(err4)/num_experiments)) 

    for n, i in enumerate(errors):
        print(f'Oбъём: {sample_sizes[n]} значений: ', *[round(j,8) for j in i])
        

for model in models:
    fig, axs = plt.subplots(1, 4, figsize=(18, 6))
    fig.suptitle(f"Model {model}")
    for j, estimate in enumerate(["выборочное среднее", "полусумма максимума и минимума", "выборочная медиана", "ср арифм с отбросом"]):
        for size in sample_sizes:
            x_values = np.array([size] * num_experiments)
            y_values = np.array([np.mean(all_estimates[model][size][exp][j]) for exp in range(num_experiments)])
            axs[j].scatter(x_values, y_values, label=f"N={size}", alpha=0.5)
            axs[j].set_title(estimate)
            axs[j].set_xscale("log")
            axs[j].legend()

plt.tight_layout()
plt.show()
