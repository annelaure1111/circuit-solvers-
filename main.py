import sys
import matplotlib.pyplot as plt

from code.classes.Grid import Grid
from code.classes.House import House
from code.classes.Battery import Battery

from code.algoritmen.fill_grid import fill_grid_greedy
from code.algoritmen.switch_pairs import switch_pairs
from code.algoritmen.random import random_connect

from code.data_analyse.data_analysis import get_average, get_deviation, get_high, get_low


from code.vizualization.visualize import visualize


import scipy.stats as stats
import numpy as np


def print_progress(n, max_n):
    characters = round(50 * n / max_n)

    print("Progress: ["+"#"*characters + " "*(50 - characters) + "]", end='\r')

if len(sys.argv) == 1:
    print("Usage: python main.py [-v] <district_number>")
    sys.exit(1)


def plot_histogram(district, iterations, grid_costs):
    plt.title(f"District: {district}\n n = {iterations}\nAverage = {round(np.mean(grid_costs), 2)} $\sigma$ = {round(np.std(grid_costs), 2)}")
    plt.xlabel("grid cost")
    plt.hist(grid_costs, bins=100, density=True)

    sigma = np.std(grid_costs)
    mu = np.mean(grid_costs)
    x = np.linspace(min(grid_costs), max(grid_costs), 1000)
    y = 1 / (2 * np.pi * sigma ** 2) ** 0.5 * np.exp(-1 / 2 * (x - mu) ** 2 / sigma ** 2)

    print(min(grid_costs), max(grid_costs))
    print(f"{mu=}, {sigma=}")

    plt.plot(x, y)
    plt.show()


arguments = sys.argv[1:]

needs_visualize = False
district = None

algo_greedy = False
algo_random = False
algo_switch = False

for arg in arguments:
    if arg == "-g":
        print("Greedy algorithm chosen")
        algo_greedy = True

    if arg == "-r":
        print("Random algorithm chosen")
        algo_random = True

    if arg == "-s":
        print("Switch algorithm chosen")
        algo_switch = True

    if arg == "-v":
        needs_visualize = True

    if "1" <= arg <= "3":
        district = int(arg)

if district is None:
    print("Usage: python main.py [-v] <district_number>")
    sys.exit(1)



if __name__ == "__main__":

    grid = Grid(district)
    grid.load_houses(r"data/district_X/district-X_houses.csv".replace("X", str(district)))
    grid.load_batteries(r"data/district_X/district-X_batteries.csv".replace("X", str(district)))
    

    grid_costs = []

    iterations = 10

    lowest = 61729
 
    for i in range(iterations):
        print_progress(i, iterations)

        # choose way to fill grid (required)
        if algo_greedy == True:
            fill_grid_greedy(grid)

        if algo_random == True:
            while not random_connect(grid):
                grid.reset()

        if algo_greedy == False and algo_random == False:
            print("You must select greedy or random algirthm <-g> <-r>")

        # choose optimalization algorithm
        if algo_switch == True:
            while switch_pairs(grid):
                print("New cost: ", grid.calc_costs())
                pass

        if grid.calc_costs() < lowest:
            grid.write_out(r"data/outputs/output_district-X-random.json".replace("X", str(district)))

            lowest = grid.calc_costs()
        grid_costs.append(grid.calc_costs())

    print("Finished")
    print("Lowest cost: ", get_low(grid_costs))

    plot_histogram(district, iterations, grid_costs)

    # data = [your data values]

        # print(grid.calc_costs())
        # grid.write_out(r"data/random_connections/output_district-X_Y.json".replace("X", str(district)).replace("Y", str(grid.calc_costs())))

    # assert grid.is_filled()
    # print("Cost = ", grid.calc_costs())

    # grid.reset()
    # fill_grid_greedy(grid)

    # while switch_pairs(grid):
    #     print("New cost: ", grid.calc_costs())

    assert grid.is_filled()

    grid.write_out(r"data/outputs/output_district-X.json".replace("X", str(district)))

    if needs_visualize:
        visualize(district)
