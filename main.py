"""
    Zadanie 2 - UI:  8-puzzle s obojsmernym prehladavanim
"""
import random
import time

MINIMUM = 2

# reprezentacia uzlu
class Node():
    def __init__(self, state, parent, prev_move, depth): # konstruktor
        self.state = state
        self.parent = parent
        self.previous_move = prev_move
        self.depth = depth



"""    OPERATORY     """
def hore(state):
    new_state = [row[:] for row in state]
    pos_0_x, pos_0_y = get_x_y(new_state, 0)
    if( (pos_0_x - 1) < 0):
        return False
    else:
        temp = new_state[pos_0_x][pos_0_y]      # ulozim hodnotu O
        new_state[pos_0_x][pos_0_y] = new_state[pos_0_x - 1][pos_0_y]   #tam kde bola 0 dam hodnotu zhoda
        new_state[pos_0_x - 1][pos_0_y] = temp  # hore dam hodnotu 0
        return new_state

def dole(state):
    new_state = [row[:] for row in state]
    pos_0_x, pos_0_y = get_x_y(new_state, 0)
    if ( (pos_0_x + 1) > (len(new_state) - 1) ):    #nemozem ist s nulou dole
        return False
    else:
        temp = new_state[pos_0_x][pos_0_y]  # ulozim hodnotu O
        new_state[pos_0_x][pos_0_y] = new_state[pos_0_x + 1][pos_0_y]  # tam kde bola 0 dam hodnotu zhoda
        new_state[pos_0_x + 1][pos_0_y] = temp  # hore dam hodnotu 0
        return new_state

def pravo(state):
    new_state = [row[:] for row in state]
    pos_0_x, pos_0_y = get_x_y(new_state, 0)
    if ((pos_0_y + 1) > (len(new_state[0]) - 1)):  # nemozem ist s nulou dole
        return False
    else:
        temp = new_state[pos_0_x][pos_0_y]  # ulozim hodnotu O
        new_state[pos_0_x][pos_0_y] = new_state[pos_0_x][pos_0_y + 1]  # tam kde bola 0 dam hodnotu zhoda
        new_state[pos_0_x][pos_0_y + 1] = temp  # hore dam hodnotu 0
        return new_state

def lavo(state):
    new_state = [row[:] for row in state]
    pos_0_x, pos_0_y = get_x_y(new_state, 0)
    if( (pos_0_y - 1) < 0):
        return False
    else:
        temp = new_state[pos_0_x][pos_0_y]      # ulozim hodnotu O
        new_state[pos_0_x][pos_0_y] = new_state[pos_0_x][pos_0_y - 1]   #tam kde bola 0 dam hodnotu zhoda
        new_state[pos_0_x][pos_0_y - 1] = temp  # hore dam hodnotu 0
        return new_state

""" Tu sa nachadzaju funckie ktore sluzia iba na transformovanie nejakeho listu do stringu alebo do 2D listu """


# funkcie aby som si vedel prelozit z 1D listu stav do 2D listu, ktorym reprezentujem stav
def transfer_list_to_state(input, m, n):
    state = []
    pomocny_state = []
    m = int(m)
    n = int(n)
    riadok = 0
    for i in range(0, (m * n) + 1, 1):
        if( i // m == riadok):
            pomocny_state.append(input[i])     #input[i]
        else:
            if(i == m * n):
                state.append(pomocny_state[:])
                return state
            else:
                riadok += 1
                state.append(pomocny_state[:])
                pomocny_state.clear()
                pomocny_state.append(input[i])

def transfer_state_to_list(state):
    list = []
    for i in state:
        for j in range(0, len(state[0]), 1):
            list.append(i[j])
    return list
# stav premeni na string, pouzivam pri hash tabulke ako kluc
def state_to_string(state,m,n):
    string = ""
    for i in range(0, m, 1):
        for j in range(0, n, 1):
            string += str(state[i][j]) + " "
    return string

def string_to_list(string):
    a_list = string.split()
    a = map(int, a_list)
    b = list(a)
    return b

###########################################
""" funckia overi ci je uloha riesitelna, pomocou inverzie = da sa pouzit iba pri stave 3x3"""
# kontrola na skontrolovanie vstupu, ci je od 0 - (n-1), n je pocet policok
def check_valid_input(input, m, n): # kontroluje ci je dobry vstup
    for i in range(0, m * n, 1):
        if(input[i] >= 0 and input[i] < m * n):
            continue
        else:
            return False
    return True

def check_solvable(s_state, f_state):
    s_list = s_state[:]
    f_list = f_state[:]
    s_list.remove(0)
    f_list.remove(0)

    s_inversion = get_inversion(s_list)
    f_inversion = get_inversion(f_list)
    if(s_inversion % 2 == f_inversion % 2): # ak spadaju obidve do rovnakej podtriedy, je solvable (ci zvysok je parny alebo neparny)
        return True
    else:
        return False

# pomocna funkcia pre check_solvable, vypocitava inverziu
def get_inversion(list_state):
    counter = 0

    list_pomocny = list(range(1,len(list_state)+1)) #vytvorim si pole aby som vedel skrtat

    for i in range(0, len(list_state), 1):
        for j in range(0, len(list_state), 1):
            if(list_state[i] > list_pomocny[j] and list_pomocny[j] != 0):
                counter += 1
            elif(list_state[i] == list_pomocny[j]):
                list_pomocny[j] = 0
                break

    return counter

############################################
# pomocna funkcia aby som vedel ziskat poziciu urciteho cisla zo stavu
def get_x_y(state, num):
    for i in range(0, len(state), 1):
        for j in range(0, len(state[i]), 1):
            if(state[i][j] == num):
                return i, j

# pomocne funkcie pre vypis cesty
def print_path_recursively(node):
    if(node.parent == None):
        for one in node.state:
            print(one)
        return 0
    print_path_recursively(node.parent)
    print("||||||  " + str(node.previous_move) + "  ||||||||")
    for one in node.state:
        print(one)

def print_path(node):
    for one in node.state:
        print(one)
    if (node.parent != None):
        print("||||||  " + str(prehod_smer(node.previous_move)) + "  ||||||||")
    if (node.parent == None):
        return 0
    print_path(node.parent)

# pri vypise z koncoveho stavu potrebujem vypisovat opacne pohyby kedze sa vlastne vraciam, ked ma Node hodnotu UP, potrebujem vypisat DOWN
def prehod_smer(smer):
    if(smer == "up"):
        return "down"
    elif (smer == "down"):
        return "up"
    elif (smer == "left"):
        return "right"
    elif (smer == "right"):
        return "left"

# pomocna funkcia pre tester kde si generujem nahodny stav
def generuj_nahodny_list(num):
    a = list(range(0, num))
    b = list()
    #print(a)
    while(len(a) > 0):
        c = random.choice(a)
        a.remove(c)
        b.append(c)
    return b

# funkcia ktora vykonava ulohu testera
def tester(m,n):
    while(True):
        start_state = generuj_nahodny_list(m*n)
        goal_state = generuj_nahodny_list(m*n)
        if(check_solvable(start_state,goal_state)):
            main(start_state, goal_state,m,n)
            break


# hlavna funkcia kde sa uz priamo riesi uloha
def main(s_state,f_state,riadky,stlpce):
    if(s_state == f_state):
        print("Pociatocny stav sa rovna koncovemu")
        return 0

    # definujem si oba stavy, z ktorych bude zacinat BFS
    start_RootNode = Node(transfer_list_to_state(s_state,stlpce,riadky),None,None,0)
    goal_RootNode = Node(transfer_list_to_state(f_state,stlpce,riadky), None, None, 0)

    # hash tabulky, kde uchovavam vsetky doteraz vygenerovane stavy, aby som v bududcnosti negeneroval kopie
    hash_table1 = {}
    hash_table2 = {}

    start_queue = []
    goal_queue = []
    start_explored= []
    goal_explored = []

    start_queue.append(start_RootNode)
    goal_queue.append(goal_RootNode)
    hash_table1[state_to_string(start_RootNode.state, riadky, stlpce)] = start_RootNode
    hash_table2[state_to_string(goal_RootNode.state, riadky, stlpce)] = goal_RootNode

    start = time.time()

    while (len(start_queue) > 0 and len(goal_queue) > 0):
        # vyberiem si po jednom z oboch listov, kde sa nachadzaju nespracovane uzly
        temp1 = start_queue.pop(0)
        temp2 = goal_queue.pop(0)

        # ak som smerom z pociatocneho stavu uz niekedy vygeneroval stav, ktory som si prave vybral z goal_queue, znamena to ze sa mi stretli oba smery
        if(hash_table1.get(state_to_string(temp2.state, riadky, stlpce)) != None):  # ak vrati None, takyto stav este nebol vygenerovany
            end = time.time()
            total_depth = temp2.depth +  hash_table1.get(state_to_string(temp2.state, riadky, stlpce)).depth
            print("Cena cesty: " + str(total_depth))
            print("start_queue: "+ str(len(start_queue)))
            print("goal_queue: " + str(len(goal_queue)))
            print("start_explored: " + str(len(start_explored)))
            print("goal_explored: " + str(len(goal_explored)))
            print("CESTA:")
            print_path_recursively(hash_table1.get(state_to_string(temp2.state, riadky, stlpce)))
            print("-------------------------------- Tu sa stretli ---------------------------------------------------")
            print("||||||  " + str(prehod_smer(temp2.previous_move)) + "  ||||||||")
            print_path(temp2.parent)
            print("\n")
            print("Total time: " + str(round(end - start, 2)) + " seconds")
            return 0

        # rovnako ako vyssie ale prehodene, ak som smerom z cieloveho stavu uz vygeneroval stav rovnaky Nodu, ktory som prave vybral z start_queue, pretli sa mi
        elif(hash_table2.get(state_to_string(temp1.state, riadky, stlpce)) != None):
            end = time.time()
            total_depth = temp1.depth + hash_table2.get(state_to_string(temp1.state, riadky, stlpce)).depth
            print("Cena cesty: " + str(total_depth))
            print("start_queue: " + str(len(start_queue)))
            print("goal_queue: " + str(len(goal_queue)))
            print("start_explored: " + str(len(start_explored)))
            print("goal_explored: " + str(len(goal_explored)))
            print("Cesta:")
            print_path_recursively(temp1)
            print("-------------------------------- Tu sa stretli ---------------------------------------------------")
            print("||||||  " + str(prehod_smer(hash_table2.get(state_to_string(temp1.state, riadky, stlpce)).previous_move)) + "  ||||||||")
            print_path(hash_table2.get(state_to_string(temp1.state, riadky, stlpce)).parent)
            print("\n")
            print("Total time: " + str(round(end - start, 2)) + " seconds")
            return 0


        """ Spracovanie uzla smer z pociatocneho stavu """
        up_1 = Node(hore(temp1.state), temp1, "up", temp1.depth + 1)    # vytvorim uzol
        if (up_1.state != False and temp1.previous_move != "down"):    # ak je mozne sa pohnut danym smerom a nebudem generovat spatny chod, idem dalej
            if(hash_table1.get(state_to_string(up_1.state, riadky, stlpce)) == None): # pokial som este takyto stav v minulosti nevygeneroval, idem dalej
                start_queue.append(up_1)    # novy node pridam na koniec listu pre nespracovane
                hash_table1[state_to_string(up_1.state,riadky,stlpce)] = up_1   # novy stav vlozim do hast tabulky aj s pointrom na dany uzol


        down_1 = Node(dole(temp1.state), temp1, "down", temp1.depth + 1)
        if (down_1.state != False and temp1.previous_move != "up"):
            if (hash_table1.get(state_to_string(down_1.state, riadky, stlpce)) == None):
                start_queue.append(down_1)
                hash_table1[state_to_string(down_1.state, riadky, stlpce)] = down_1

        right_1 = Node(pravo(temp1.state), temp1, "right", temp1.depth + 1)
        if (right_1.state != False and temp1.previous_move != "left"):
            if (hash_table1.get(state_to_string(right_1.state, riadky, stlpce)) == None):
                start_queue.append(right_1)
                hash_table1[state_to_string(right_1.state, riadky, stlpce)] = right_1

        left_1 = Node(lavo(temp1.state), temp1, "left", temp1.depth + 1)
        if (left_1.state != False and temp1.previous_move != "right"):
            if (hash_table1.get(state_to_string(left_1.state, riadky, stlpce)) == None):
                start_queue.append(left_1)
                hash_table1[state_to_string(left_1.state, riadky, stlpce)] = left_1

        #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        """ Spracovanie uzla smerom z koncoveho stavu """
        up_2 = Node(hore(temp2.state), temp2, "up", temp2.depth + 1)
        if (up_2.state != False and temp2.previous_move != "down"):
            if (hash_table2.get(state_to_string(up_2.state, riadky, stlpce)) == None):
                goal_queue.append(up_2)
                hash_table2[state_to_string(up_2.state, riadky, stlpce)] = up_2

        down_2 = Node(dole(temp2.state), temp2, "down", temp2.depth + 1)
        if (down_2.state != False and temp2.previous_move != "up"):
            if (hash_table2.get(state_to_string(down_2.state, riadky, stlpce)) == None):
                goal_queue.append(down_2)
                hash_table2[state_to_string(down_2.state, riadky, stlpce)] = down_2

        right_2 = Node(pravo(temp2.state), temp2, "right", temp2.depth + 1)
        if (right_2.state != False and temp2.previous_move != "left"):
            if (hash_table2.get(state_to_string(right_2.state, riadky, stlpce)) == None):
                goal_queue.append(right_2)
                hash_table2[state_to_string(right_2.state, riadky, stlpce)] = right_2

        left_2 = Node(lavo(temp2.state), temp2, "left", temp2.depth + 1)
        if (left_2.state != False and temp2.previous_move != "right"):
            if (hash_table2.get(state_to_string(left_2.state, riadky, stlpce)) == None):
                goal_queue.append(left_2)
                hash_table2[state_to_string(left_2.state, riadky, stlpce)] = left_2

        # na konci oba spracovavane uzly presuniem do listu pre spracovane uzly
        start_explored.append(temp1)
        goal_explored.append(temp2)

    # ak sa nikde nepretli, riesenie neexistuje
    for i in start_RootNode.state:
        print(i)
    print("----------------")
    for j in goal_RootNode.state:
        print(j)
    print("\nRiesenie neexistuje.")


"""     Test pre 3x2
start_state = [0,1,2,3,4,5]
goal_state = [3,4,5,0,1,2]
        Testy pre 3x3
start_state = [0,1,2,3,4,5,6,7,8]
goal_state = [8,0,6,5,4,7,2,3,1]
         TEST 4x2 
start_state = [0,1,2,3,4,5,6,7]
goal_state = [3,2,5,4,7,6,1,0]
        TEST 5x2
start_state = [0,1,2,3,4,5,6,7,8,9]
goal_state = [4,3,2,6,1,9,8,7,5,0]
"""

stlpce = int()
riadky = int()

while(1):
    print("\n\n--------------------------------------------------------------------------------------------")
    print("manual = zadam vstup manualne: naprv zadam velkost plochy a nasledne zadam stavy")
    print("tester = zadam velkosti pola a nasledne sa mi vygeneruje par prikaldov")
    print("quit = ukonci program")
    vstup = input("\nZadajte vstup(manual/tester/quit): ")
    if(vstup == "manual"):
        print("Zadajte parametre plochy v rozmedzi (2x2,3x2,3x3,4x2,5x2)")
        riadky = input("Pocet riadkov: ")
        stlpce = input("Pocet stlpcov: ")
        if(riadky.isnumeric() and stlpce.isnumeric()):
            riadky = int(riadky)
            stlpce = int(stlpce)
            if(riadky >= MINIMUM and stlpce >= MINIMUM):
                print("Pozor aby sa cisla neopakovali")
                print("Stav zadavajte sposobom: 0 1 2 3 4 5 6 7")
                pociatocny_stav = input("Zadajte pociatocny stav:")
                koncovy_stav = input("Zadajte koncovy stav:")
                start_state = string_to_list(pociatocny_stav)
                goal_state = string_to_list(koncovy_stav)
                if(len(start_state) == riadky * stlpce and len(goal_state) == riadky * stlpce):
                    if(stlpce == 3 and riadky == 3):        # pre pripad 3x3 viem urcit ci je princip riesitelny pomocou inverzie
                        if (check_solvable(start_state, goal_state)):
                            main(start_state, goal_state,riadky, stlpce)
                    else:
                        main(start_state, goal_state, riadky, stlpce)

    elif(vstup == "tester"):
        print("Zadajte parametre plochy v rozmedzi (2x2,3x2,3x3,4x2,5x2)")
        riadky = input("Pocet riadkov: ")
        stlpce = input("Pocet stlpcov: ")
        if (riadky.isnumeric() and stlpce.isnumeric()):
            riadky = int(riadky)
            stlpce = int(stlpce)
            if (riadky >= MINIMUM and stlpce >= MINIMUM):
                tester(riadky,stlpce)

    elif (vstup == "quit"):
        exit()

