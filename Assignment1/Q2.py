import math
import random

current_best_score = 0
best_genome = 0

def min_bins(list_weights,list_num_items):
    weight = 0.0
    for x in range(0,len(list_weights)):
        weight+=(list_weights[x]*list_num_items[x])
    num_bins = int(math.ceil(weight/1000))
    return num_bins

def check_best_solution(genome,score,best_genome):
    if score > current_best_score:
        current_best_score = score
        best_genome = genome
    return best_genome



def score_f(bin_values, list_weights, bin_capacity, list_num_items):
    weights = calc_weight(bin_values, list_weights)
    score = 0
    for x in weights:
        if x > bin_capacity:
            score -= bin_capacity - x
        elif x <= bin_capacity:
            score += 100
    compare_list = [0] * len(list_num_items)
    
    for string in bin_values:
        num = 0
        for char in string:
            compare_list[num] += int(char)
            num+=1
    if compare_list != list_num_items:
        score-=500

    #check_best_solution(bin_values)
    return score

def gen_population(num_weights, list_weights, list_num_items, bin_capacity, num_bins):
    #max_items = max(list_num_items)
    bins = []
    for _ in range(num_bins):
        weight = 0
        stringGen = [0] * num_weights  # Initialize stringGen outside the loop
        while(weight < bin_capacity):
            if all(element == 0 for element in list_num_items):
                break
            rand_num = random.randint(0, num_weights-1)
            if list_num_items[rand_num] > 0:
                stringGen[rand_num] += 1
                list_num_items[rand_num] -= 1  # Decrease count of items
                weight += list_weights[rand_num]  # Update total weight
        bins.append(''.join(str(num) for num in stringGen))

    print(bins)
    return bins

def calc_weight(bins, list_weights):
    weight_vals = []
    for str in bins:
        weight = 0
        for idx,char in enumerate(str):
            weight += int(char) * list_weights[idx]
        weight_vals.append(weight)
    return(weight_vals)

def tournament(pop_list, num_weights):
    preferred_list = []
    for x in range(50):
        list1 = pop_list[random.randrange(len(pop_list))]
        list2 = pop_list[random.randrange(len(pop_list))]
        if score_f(list1,list_weights, bin_capacity, list_num_items) > score_f(list2,list_weights, bin_capacity, list_num_items):
            preferred_list.append(list1)
        else:
            preferred_list.append(list2)
    return preferred_list

def crossover(oldGen,num_weights):
    nextGen = []
    scores = []
    for x in oldGen:
        scores.append(score_f(x,list_weights, bin_capacity, list_num_items))
    nextGen.append(oldGen[scores.index(max(scores))])
    scores[scores.index(max(scores))] = 0
    nextGen.append(oldGen[scores.index(max(scores))])

    for x in range(50):
        splitPoint = random.randint(0,num_weights-1)
        list1 = oldGen[random.randrange(len(oldGen))]
        list2 = oldGen[random.randrange(len(oldGen))]
        bin1 = list1[splitPoint]
        bin2 = list2[splitPoint]
        list1[splitPoint] = bin2
        list2[splitPoint] = bin1
        nextGen.append(list1)
        nextGen.append(list2)
    

    return nextGen

def mutate(oldList):
    newList = []
    change_location = random.randint(0,len(oldList))
    change_location_to = random.randint(0,len(oldList))
    bit_to_change = random.randint(0,num_weights)
    
    bin1_char = oldList[change_location][bit_to_change]
    bin2_char = oldList[change_location_to][bit_to_change]

    oldList[change_location_to][bit_to_change] = bin1_char
    oldList[change_location][bit_to_change] = bin2_char

    return oldList
        

#import initial seeds from txt file
population_list = []

#--------------------------------------------------
    
list_weights = []
list_num_items = []

#main loop
with open("bin-p1.txt", "r") as file:
    line_num = 0
    for line in file:
        line_num+=1
        if line_num == 1:
            num_weights = int(line.strip())
        
        if line_num == 2:
            bin_capacity = int(line.strip())

        if line_num > 2:
            list_weights.append(int(line.strip().split()[0]))
            list_num_items.append(int(line.strip().split()[1]))


num_bins = min_bins(list_weights,list_num_items)
population_list = []
scores = []
for _ in range(100):
    genome = gen_population(num_weights, list_weights, list_num_items, bin_capacity, num_bins)
    population_list.append(genome)
for x in population_list:
    scores.append(score_f(x,list_weights,bin_capacity,list_num_items))

filepath = "Q2resultsP1"
with open(filepath, 'w') as file:


    for x in range(1000):
        parents = tournament(population_list, num_weights)
        new_population_list = crossover(parents, num_weights)
        mutate(new_population_list)

        average_score = [score_f(x,list_weights,bin_capacity,list_num_items) for x in new_population_list]

        average_result = sum(average_score)/len(average_score)
        file.write(str(average_result)+"\n")

        population_list = new_population_list
