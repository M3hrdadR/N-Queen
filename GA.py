import random
import copy


class Gen:
    def __init__(self, number_of_elements, no_generation=200, p_cross_over=0.95,
                 p_mutation=0.2, p_trunc=0.5, no_population=1000):
        self.best = [[], 50]
        self.number_of_generations = no_generation
        self.p_cross_over = p_cross_over
        self.p_mutation = p_mutation
        self.p_trunc = p_trunc
        self.population = list()
        self.population_size = no_population
        self.initialize_population(number_of_elements)
        return

    def initialize_population(self, n):
        for i in range(self.population_size):
            tmp = list()
            while len(tmp) != n:
                x = random.randint(0, n-1)
                if x not in tmp:
                    tmp.append(x)
            lst = [tmp.copy(), self.evaluation(tmp.copy())]
            self.population.append(lst)
        self.population.sort(key=lambda x: x[1])
        return

    def evaluation(self, lst):
        collision = 0
        for i in range(0, len(lst)-1):
            for j in range(i+1, len(lst)):
                if abs(lst[i] - lst[j]) == abs(i - j):
                    collision += 1
        return collision

    def select_parents(self):
        selected = []
        count = 0
        number_different_answer = 0
        different_answer = []
        N = len(self.population) * self.p_trunc * 0.5

        for i in range(int(len(self.population)*self.p_trunc)):
            if self.population[i] not in different_answer:
                different_answer.append(self.population[i])
                number_different_answer += 1
        if N > number_different_answer:
            N = number_different_answer
        while count < N:
            index = random.randint(0, len(self.population) * self.p_trunc)
            if self.population[index] not in selected:
                selected.append(self.population[index])
                count += 1
        return selected

    def order_recombination(self, p1, p2):
        c1 = [0] * len(p1)
        c2 = [0] * len(p2)
        i = random.randint(0, len(p1) - 1)
        j = random.randint(0, len(p1) - 1)
        while i >= j:
            i = random.randint(0, len(p1) - 1)
            j = random.randint(0, len(p1) - 1)
        # print(i, j)
        for k in range(i, j + 1):
            c1[k] = p1[k]
            c2[k] = p2[k]
        index_1 = (j + 1) % len(p1)
        index_2 = (j + 1) % len(p1)
        for k in range(j + 1, len(p1)):
            if p2[k] not in c1:
                c1[index_1] = p2[k]
                index_1 = (index_1 + 1) % len(p1)
            if p1[k] not in c2:
                c2[index_2] = p1[k]
                index_2 = (index_2 + 1) % len(p1)
        for k in range(0, j + 1):
            if p2[k] not in c1:
                c1[index_1] = p2[k]
                index_1 = (index_1 + 1) % len(p1)
            if p1[k] not in c2:
                c2[index_2] = p1[k]
                index_2 = (index_2 + 1) % len(p1)
        return c1, c2

    def cross_over(self, parents):
        used_parents = []
        count = 0
        children = []
        while count < len(parents) // 2:
            i = random.randint(0, len(parents)-1)
            j = random.randint(0, len(parents)-1)
            while i in used_parents or j in used_parents or i == j:
                i = random.randint(0, len(parents) - 1)
                j = random.randint(0, len(parents) - 1)
            p = random.random()
            if p < self.p_cross_over:
                c1, c2 = self.order_recombination(parents[i][0], parents[j][0])
                tmp1 = [c1.copy(), 0]
                tmp2 = [c2.copy(), 0]
                children.append(tmp1.copy())
                children.append(tmp2.copy())
                used_parents.append(i)
                used_parents.append(j)
            count += 1
        return children

    def swap_mutation(self, child):
        mutated = child.copy()
        i = random.randint(0, len(child)-1)
        j = random.randint(0, len(child)-1)
        while i == j:
            i = random.randint(0, len(child) - 1)
            j = random.randint(0, len(child) - 1)
        tmp = mutated[i]
        mutated[i] = mutated[j]
        mutated[j] = tmp
        return mutated

    def mutation(self, chlidren):
        for child in chlidren:
            p = random.random()
            if p < self.p_mutation:
                self.swap_mutation(child[0])
            child[1] = self.evaluation(child[0])
        return chlidren

    def replace(self, children):
        constant = len(self.population) - len(children)
        for i in range(constant, len(self.population)):
            index = i - constant
            self.population[i] = copy.deepcopy(children[index])
        self.population.sort(key=lambda x: x[1])
        self.best = copy.deepcopy(self.population[0])
        return

    def stop(self, n):
        if n >= self.number_of_generations or self.best[1] == 0:
            return True
        return False

    def evolution(self):
        count_generation = 0
        while not self.stop(count_generation):
            selected_parents = self.select_parents()
            children = self.cross_over(selected_parents)
            children = self.mutation(children)
            self.replace(children)

            print("iteration =", count_generation, ",number of collisions =", self.best[1], ",Solution =", self.best[0])
            count_generation += 1
        return
