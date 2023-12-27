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
        if len(sfMap) > len(ourMap):
            for move in sfMap.keys():
                if move not in ourMap.keys():
                    print(f"our list of moves doesn't have: {move}")
        else:
            for move in ourMap.keys():
                if move not in sfMap.keys():
                    print(f"sf list of moves doesn't have: {move}")
    else:
        for move in sfMap.keys():
            sfCount = sfMap[move]
            count = ourMap[move]

            if count != sfCount:
                print(f"incorrect stockfish had: {sfCount} and ours had: {count} on move: {move}")


compareOutput()