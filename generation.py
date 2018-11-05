import random, copy
from network import Network

class Generation():
  def __init__(self):
    self.genomes = []
    self.population = 50
    self.keep_best = 10
    self.lucky_few = 10
    self.chance_of_mutation = 0.1

  def set_initial_genomes(self):
    genomes = []
    for i in range(self.population):
      genomes.append(Network())
    return genomes

  def set_genomes(self, genomes):
    self.genomes = genomes

  def keep_best_genomes(self):
    self.genomes.sort(key=lambda x: x.fitness, reverse=True)
    self.best_genomes = self.genomes[:self.keep_best]

    # self.lucky_genomes = random.sample(self.genomes, k=self.lucky_few)

    # self.best_genomes.extend(self.lucky_genomes)

    self.genomes = copy.deepcopy(self.best_genomes[:])

  def mutations(self):
    while len(self.genomes) < self.keep_best * 4:
      genome1 = random.choice(self.best_genomes)
      genome2 = random.choice(self.best_genomes)
      self.genomes.append(self.mutate(self.cross_over(genome1, genome2)))

    while len(self.genomes) < self.population:
      genome = random.choice(self.best_genomes)
      self.genomes.append(self.mutate(genome))

    random.shuffle(self.genomes)

    return self.genomes

  def cross_over(self, genome1, genome2):
    new_genome = copy.deepcopy(genome1)
    other_genome = copy.deepcopy(genome2)

    cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
    for i in range(cut_location):
      new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]

    cut_location = int(len(new_genome.W2) * random.uniform(0, 1))
    for i in range(cut_location):
      new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]

    cut_location = int(len(new_genome.W3) * random.uniform(0, 1))
    for i in range(cut_location):
      new_genome.W3[i], other_genome.W3[i] = other_genome.W3[i], new_genome.W3[i]
    return new_genome

  def mutate_weights(self, weights):
    # print(weights)
    if random.uniform(0, 1) < self.chance_of_mutation:
      return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
    else:
      return 0

  def mutate(self, genome):
    new_genome = copy.deepcopy(genome)
    new_genome.W1 += self.mutate_weights(new_genome.W1)
    new_genome.W2 += self.mutate_weights(new_genome.W2)
    new_genome.W3 += self.mutate_weights(new_genome.W3)
    return new_genome
