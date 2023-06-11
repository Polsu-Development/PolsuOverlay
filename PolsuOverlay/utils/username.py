characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]
        
        
def isValidPlayer(player: str) -> bool:
    # Max username size
    if len(player)>16:
        return False
    else:
        return all(char in characters for char in player)
    

def removeRank(player: str) -> str:
    x = player.split(' ')
    if len(x) > 1:
        player = x[1]

    return player
