import numpy as np

def proportionalAllocation(total_shots,newCounts,usershots):
    proportions = {key: value / total_shots for key, value in newCounts.items()}
    # Calculate the number of shots to allocate to each key
    allocated_shots = {key: round(proportions[key] * usershots) for key in proportions.keys()} # round(...) or int(...). int is faster but round is more accurate
    # Create a new dictionary to store the counts of the allocated shots
    selected_counts = {key: allocated_shots[key] for key in allocated_shots.keys() if allocated_shots[key] > 0}
    return selected_counts

def stratifiedSampling(total_shots,newCounts,usershots):
    keys = list(newCounts.keys())
    probabilities = [value / total_shots for value in newCounts.values()]
    # Sample from the keys based on their probabilities
    sampled_keys = np.random.choice(keys, size=usershots, replace=True, p=probabilities) #This uses numpy instead of doing it manually to make it more readable
    # Create a new dictionary to store the counts of the sampled keys
    selected_counts = {key: np.count_nonzero(sampled_keys == key) for key in keys}
    return selected_counts

def divideResults(counts, shots, provider, qb, users, circuit_name):
    result = []
    for i in range(len(shots)):
        
        newCounts = {}

        for key, value in counts.items(): #Reducing each dictionary so that it contains the useful part of each user
            rightRemovedQubits = sum(qb[0:i])  #Values to remove from the right
            leftRemovedQubits = sum(qb[i+1:len(qb)])  #Values to remove from the left
            if provider == 'aws':
                data = key[rightRemovedQubits:]  #Data is the custom value of each user
                data = data[:(len(data)-leftRemovedQubits)]
                data = data[::-1] #AWS gives the results backwards compared to IBM, to have a standard, the result is reversed
            else:
                data = key[leftRemovedQubits:]  #Data is the custom value of each user
                data = data[:(len(data)-rightRemovedQubits)]
            
            if data in newCounts:
                newCounts[data] += value
            else:
                newCounts[data] = value

        # Calculate the total number of shots
        total_shots = sum(newCounts.values())
        # Check if the total number of shots is equal to the number of executed shots
        if total_shots == shots[i]:
            # If they are equal, use newCounts directly
            selected_counts = newCounts
        else:
            selected_counts = stratifiedSampling(total_shots,newCounts,shots[i])
            #selected_counts = proportionalAllocation(total_shots,newCounts,shots[i])

        print(users[i],': ',selected_counts) #Return the number of shots corresponding to each user
        result.append({(users[i],circuit_name[i]):selected_counts})

    return result