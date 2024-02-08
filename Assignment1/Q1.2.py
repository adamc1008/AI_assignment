import random

target_string = "101011100011001111001000100100"

def score_f(bit_string):
    score = 0
    for i in range(len(bit_string)):
        if bit_string[i] == target_string[i]:
            score = score + 1

    return score

def tournament(pop_list):
    preferred_list = []
    for x in range(50):
        string1 = pop_list[random.randrange(len(pop_list))]
        string2 = pop_list[random.randrange(len(pop_list))]
        if score_f(string1) <= score_f(string2):
            preferred_list.append(string2)
        else:
            preferred_list.append(string1)
    #print(len(preferred_list))
    return preferred_list

def crossover(oldGen):
    nextGen = []
    scores = []
    for x in oldGen:
        scores.append(score_f(x))
    nextGen.append(oldGen[scores.index(max(scores))])
    scores[scores.index(max(scores))] = 0
    nextGen.append(oldGen[scores.index(max(scores))])

    for x in range(24):
        splitPoint = random.randint(0,29)
        string1 = oldGen[random.randrange(len(oldGen))]
        string2 = oldGen[random.randrange(len(oldGen))]
        nextGen.append(string1[:splitPoint]+string2[splitPoint:])
        nextGen.append(string2[:splitPoint]+string1[splitPoint:])
    return nextGen

def mutate(oldList):
    newList = []
    change_location = random.randint(0,len(oldList[0]))
    bit_to_change_to = random.randint(0,1)
    
    for x in oldList:
        chance_to_mutate = random.randint(0,100)
        if chance_to_mutate % 10 == 0: # and score_f(x) < 28:
            x = x[:change_location] + str(bit_to_change_to) + x[change_location+1:]
            #print(len(x))
            newList.append(x)

    return newList
        

#import initial seeds from txt file
population_list = []
with open('pop.txt', 'r') as file:
    content = file.read().strip()

population_list = content.split('\n')
#--------------------------------------------------
    

#main loop
f = open("results2.txt", "w")

for x in range(1000):
    parents = tournament(population_list)
    new_population_list = crossover(parents)
    mutate(new_population_list)

    average_score = [score_f(x) for x in new_population_list]

    average_result = sum(average_score)/len(average_score)
    f.write(str(average_result)+"\n")

    population_list = new_population_list

f.close()
        








