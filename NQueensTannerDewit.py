import random
import time
def queen_chooser(solutions, probabilities):
    total_probability = sum(probabilities)
    normalized_probabilities = []
    for p in probabilities:
        normalized_probabilities.append(p / total_probability)
    selected_solution = random.choices(solutions, normalized_probabilities, k=1)
    return selected_solution[0]

def print_board(s):
    board = []
    ncr = len(s)
    for _ in range(ncr):
        board.append(["_"] * n)

    for i in range(ncr):
        board[i][s[i]-1] = "Q"
    for row in board:
        print(" ".join(row))


def cross(Q1, Q2):
    n = len(Q1)
    sp = random.randint(0, n - 1)
    return Q1[0:sp] + Q2[sp:n]


def mutate(s):
    n = len(s)
    Q = random.randint(0, n - 1)
    pc = random.randint(1, n)
    s[Q] = pc
    return s


def gene_splice(solutions, fitness, doubleMutation):
    mutation_probability = 0.2
    new_solutions = []
    probabilities = [probability(s) for s in solutions]
    for i in range(len(solutions)):
        Q1 = queen_chooser(solutions, probabilities)
        Q2 = queen_chooser(solutions, probabilities)
        child = cross(Q1, Q2)
        if random.random() < mutation_probability:
            child = mutate(child)
            if doubleMutation and random.random() < mutation_probability:
                child = mutate(child)
        print_child(child)
        new_solutions.append(child)
        if fitness(child) == mFit:
            break
    return new_solutions


def print_child(s):
    print("Child = {}  Fitness = {}".format(str(s), fitness(s)))

def fitness(s):
    horizontal_contests = 0
    for q in set(s):
        horizontal_contests += s.count(q)-1
    horizontal_contests = horizontal_contests/2
    diagonal_contests = 0
    numDiag = (n * 2 - 1)
    rd = [0] * numDiag
    ld = [0] * numDiag
    for i in range(n):
        ld[i + s[i]-1] += 1
        rd[len(s)-2 - i + s[i]] += 1
    for i in range(numDiag):
        counter = 0
        if ld[i] > 1:
            counter += ld[i]-1
        if rd[i] > 1:
            counter += rd[i]-1
        diagonal_contests += counter
    return int(mFit - (horizontal_contests + diagonal_contests))

def probability(s):
    return fitness(s) / mFit

if __name__ == "__main__":
    while True:
        solutions = []

        n = int(input("Enter a integer value between 4-20 for number of queens(to stop enter a value not between 4 and 20):"))
        start_time = time.time()
        gen = 1
        if n < 4 or n > 20:
            break
        mFit = (n * (n - 1)) / 2

        for _ in range(100):
            s = []
            for _ in range(n):
                s.append(random.randint(1, n))
            solutions.append(s)

        while not mFit in [fitness(s) for s in solutions]:
            print("Generation {}".format(gen-1))
            if gen > 1000:
                solutions = gene_splice(solutions, fitness, True)
            else:
                solutions = gene_splice(solutions, fitness, False)
            print()
            maxFit = max([fitness(n) for n in solutions])
            print("Maximum Fitness = {}".format(maxFit))
            print("Solutions with maximum fitness:")
            for s in solutions:
                if fitness(s) == maxFit:
                    print("Child = {} Fitness = {}".format(str(s), fitness(s)))
            print("")
            if gen > 10000:
                solutions.clear()
                for _ in range(100):
                    s = []
                    for _ in range(n):
                        s.append(random.randint(1, n))
                    solutions.append(s)
            gen += 1
        final_Solution = []
        end_time = time.time()
        runtime = end_time - start_time
        print("Found at Generation {}".format(gen-1))
        for s in solutions:
            if fitness(s) == mFit:
                print()
                print("Found solution: ")
                final_Solution = s
                print_child(s)
                print("Runtime of the process: {} seconds".format(runtime))
        print()
        print_board(final_Solution)
        print()