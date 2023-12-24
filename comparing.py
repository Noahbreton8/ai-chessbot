def compareOutput():
    sfMap = {}
    ourMap = {}

    with open('sfoutput.txt', 'r') as file:
        for line in file:
            line = line.strip()
            key, value = line.split(':')
            sfMap[key] = int(value)
    
    with open('output.txt', 'r') as file:
        for line in file:
            line = line.strip()
            key, value = line.split(':')
            ourMap[key] = int(value)

    if len(sfMap) != len(ourMap):
        print("not same size")

    for move in sfMap.keys():
        sfCount = sfMap[move]
        count = ourMap[move]

        if count != sfCount:
            print(f"incorrect stockfish had: {sfCount} and ours had: {count} on move: {move}")


compareOutput()