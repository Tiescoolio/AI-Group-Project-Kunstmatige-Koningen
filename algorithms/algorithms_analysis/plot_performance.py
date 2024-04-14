import matplotlib.pyplot as plt

def plot_avg(*args):
    colors = ["red", "blue", "green", "pink", "yellow"]
    plt.figure(figsize=(8, 6), dpi=200)

    for i, arg in enumerate(args):
        color = colors[i]
        avg_list = calculate_avg_list(arg)
        plt.plot(range(len(avg_list)), avg_list, color=color)
        plt.scatter(range(len(avg_list)), avg_list, marker='.', color=color)

    plt.title("average time for n runs")
    plt.ylabel("average time")
    plt.xlabel("run times n")
    plt.grid()
    plt.show()


def calculate_avg(data: list) -> float:
    return round((sum(data) / len(data)), 4)


def calculate_avg_list(data: list) -> list:
    avg_list = []
    for i in range(len(data)):
        avg_list.append(calculate_avg(data[:i + 1]))
    return avg_list


if __name__ == '__main__':
    lst_1 = [1,6,9,100]
    lst_2 = [2,4,7]

    plot_avg(lst_1, lst_2)