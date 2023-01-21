#Bryan Koh (S10223617) - IT04
#Started: 17 July 2021

#Imports
import random   #imported to generate randomized buildings during the game

#--------------------------------------------------- Functions for Main features of the game ---------------------------------------------------#
#Prints Main Menu.
def display_main_menu():
    print('Welcome, mayor of Simp City!')
    print('----------------------------')
    print('1. Start new game')
    print('2. Load saved game')
    print('3. Show high scores')
    print()
    print('0. Exit')

#New game starting values.
def start_new_game():
    print()
    turn = 1
    buildings_info = [['House', 'HSE', 'If it is next to a factory (FAC), then it scores 1 point only. Otherwise, it scores 1 point for each adjacent house (HSE) or shop (SHP), and 2 points for each adjacent beach (BCH)'],\
                      ['Factory', 'FAC', 'Scores 1 point per factory (FAC) in the city, up to a maximum of 4 points for the first 4 factories. All subsequent factories only score 1 point each.'],\
                      ['Shop', 'SHP', 'Scores 1 point per different type of building adjacent to it.'],\
                      ['Highway', 'HWY','Scores 1 point per connected highway (HWY) in the same row.'],\
                      ['Beach', 'BCH', 'Scores 3 points if it is built on the left or right side of the city, or 1 point otherwise.'],\
                      ['Park', 'PRK', 'The score of the park is determined by how many parks are connected to each other.']]
    game_setup = False
    while game_setup == False:
        i = 1
        print('Please select 5 buildings in the list of buildings shown below, separated by commas. (e.g. 1,2,3,4,5)') #Allow player to select buildings, construct buildings_list
        print('-----------------------------------------------------------------------------------------------------')
        print('Buildings:')
        for building in buildings_info:
            print('{}. {} - {}'.format(i, building[0], building[2]))
            i += 1
        print('-----------------------------------------------------------------------------------------------------')

        buildings_list = input('Please input your choice: ')
        try:
            buildings_list = buildings_list.split(',')          #Remove repeated numbers
            temporary_buildings_list = []
            for number in buildings_list:
                if number not in temporary_buildings_list:
                    temporary_buildings_list.append(number)
            buildings_list = temporary_buildings_list.copy() 


            if len(buildings_list) == 5:                        #Check if player selected 5 buildings
                for index in range(len(buildings_list)):
                    buildings_list[index] = int(buildings_list[index])
                    if buildings_list[index] == 0:  #Raise error if index = 0
                        raise IndexError
                buildings_list.sort()
                for index in range(len(buildings_list)): #Obtains building code from buildings_info 
                    buildings_list[index] = [buildings_info[buildings_list[index] - 1][1]]

                game_setup = True
                          
            else:
                raise Exception


        except IndexError: #Number input is not part of buildings_info
            print()
            print('Please select buildings within the list.')
            
        except:            #Input does not meet specifications (i.e not 5 buildings, repeated building indexes)
            print()
            print('Input unaccepted.')
    
              
    for building in buildings_list:
        building.append(8)                          #Assign 8 for each building
        building.append([])                         #Position list given for each building, registers all positions of that particular building.

    position_list = [[[0,0],[0,0],[0,0],[0,0]],\
                     [[0,0],[0,0],[0,0],[0,0]],\
                     [[0,0],[0,0],[0,0],[0,0]],\
                     [[0,0],[0,0],[0,0],[0,0]]]     #Position list (4x4 map), (first zero represents building code e.g HSE, second zero represents position code e.g a1)

    start_game_position = 0                         #start_game_position is used to tell the code that the player can build anywhere.
                                                    #After the first turn, the player is only allowed to build adjacent to built buildings.
    building1, building2 = randombuilding(buildings_list) #2 random buildings will be assigned at the start
    return (turn, buildings_list, position_list, start_game_position, building1, building2)

#Load saved game data if save file exists.
def load_saved_game():
    saved_data = open('savefile.txt', 'r')
    position_list = []                              #Construct position_list
    for x in range(4):
        position_list.append([])
        for y in range(4):
            line = saved_data.readline()
            line = line.strip('\n')
            line = line.split(',')
            if line[0] == '0':
                line[0], line[1] = int(line[0]), int(line[1])
            position_list[-1] += [line]

    buildings_list = []                             #Construct buildings_list
    for i in range(5):                            
        temporary_position_list = []
        line = saved_data.readline()
        line = line.strip('\n')
        line = line.split(',')
        line.pop()
        line[1] = int(line[1])
        for position in range(2, len(line)):
            temporary_position_list += [line[position]]
        del line[2:]
        line += [temporary_position_list]
        buildings_list.append(line)

    turn = int((saved_data.readline()).strip('\n'))                     #Retrieve turn count
    start_game_position = int((saved_data.readline()).strip('\n'))      #Retrieve start_game_position
    building1 = (saved_data.readline()).strip('\n')                     #Retrieve first randomly generated building
    building2 = (saved_data.readline()).strip('\n')                     #Retreive second randomly generated building

    saved_data.close()
    return (position_list, buildings_list, turn, start_game_position, building1, building2)   

#Prints game map and remaining buildings.
def game_map(position_list):   
    map_row_number = 1
    print('     A     B     C     D   ', end = '')
    print('      {:<19}{}'.format('Building', 'Remaining'))
    print('  +-----+-----+-----+-----+', end = '')
    print('      {:<19}{}'.format('--------', '---------'))
    for map_row in range(8):
        if map_row%2 == 0:
            print(' {}'.format(map_row_number), end = '') #Prints row number
            for map_column in range(4):
                if position_list[map_row_number - 1][map_column][0] != 0:
                    print('|{:^5}'.format(position_list[map_row_number - 1][map_column][0]), end = '') #Prints building code found in position list
                else:
                    print('|{:^5}'.format(''), end = '') #if no building code in position, print blank
            print('|', end = '')
            try:
                print('      {:<19}{}'.format(buildings_list[map_row][0], buildings_list[map_row][1])) #Print remaining buildings
            except:
                print() #Prints spacing to close end = ''
            map_row_number += 1
        else:
            print('  ', end = '')
            for map_column in range(4):    #Print pattern
                print('+-----', end = '') 
            print('+', end = '')
            try:
                print('      {:<19}{}'.format(buildings_list[map_row][0], buildings_list[map_row][1])) #Print remaining buildings
            except:
                print() #Prints spacing to close end = ''

#Print game options.
def game_select_options(building1, building2):
    print('1. Build a {}'.format(building1))
    print('2. Build a {}'.format(building2))
    print('3. See current score')
    print()
    print('4. Save game')
    print('0. Exit to main menu')

#Generates 2 random buildings based on remaining buildings.
def randombuilding(buildings_list):
    remaining_buildings_list = buildings_list.copy()    #Creates copy of buildings_list for removal of buildings which has 0 buildings
    to_be_removed = []
    for building in buildings_list:
        if building[1] == 0:
            remaining_buildings_list.remove(building)
    
    random1 = random.choice(remaining_buildings_list)

    building1 = random1.copy()
    for building in buildings_list:
        if building == building1:
            building[1] -= 1 #Deducts 1 building
            if building[1] == 0:
                remaining_buildings_list.remove(building) #Removes building from remaining_buildings_list if left 0 buildings, so second random option will not display this building
    building1 = building1[0]
    
    random2 = random.choice(remaining_buildings_list)
    building2 = random2.copy()
    for building in buildings_list:
        if building == building2:
            building[1] -= 1 #Deducts 1 building
    building2 = building2[0]
    
    return(building1, building2)

#Validation of selected building position.
def build(building, position, position_list, start_game_position): 
    if len(position) != 2:                                              #If input not two characters long, invalid input.
        print('Please enter a valid position.')
        print()
        return True

    abc_string = 'abcd'
    number_list = [0,1,2,3]
    if (position[0] not in abc_string) or ((int(position[1]) - 1) not in number_list): #Check if position is out of bounds.
        print('Please enter a position that is within the map.')
        print()
        return True

    
    column_index = abc_string.find(position[0])
    row_index = int(position[1]) - 1   


    if start_game_position == 0: #Check if it is the start of the game, whereby the map has no buildings at all.
        position_list[row_index][column_index][0] = building
        position_list[row_index][column_index][1] = position
        return False
        
    elif position_list[row_index][column_index][0] == 0: #Check if position has already been taken
        while True:                                      #Check if building is placed adjacent to another building
            if column_index + 1 <= 3:
                if position_list[row_index][column_index + 1][0] == 0:
                    illegal_flag = 1
                else:
                    illegal_flag = 0
                    break

            if column_index - 1 >= 0:
                if position_list[row_index][column_index - 1][0] == 0:
                    illegal_flag = 1
                else:
                    illegal_flag = 0
                    break

            if row_index + 1 <= 3:
                if position_list[row_index + 1][column_index][0] == 0:
                    illegal_flag = 1
                    if not (row_index - 1 >= 0):
                        break
                else:
                    illegal_flag = 0
                    break

            if row_index - 1 >= 0:
                if position_list[row_index - 1][column_index][0] == 0:
                    illegal_flag = 1
                    break
                else:
                    illegal_flag = 0
                    break

        if illegal_flag == 0: #If all specifications are met and building is placed adjacent to another building, illegal_position is False.
            position_list[row_index][column_index][0] = building
            position_list[row_index][column_index][1] = position
            return False
        else:
            print('You must build next to an existing building.') #If building is not adjacent to another building
            print()
            return True
            
    else:
        print('A building has already been built on this spot. Please select another spot.') #If spot has been taken.
        print()
        return True


#If selected building position is validated.
def game_progress(turn, building, start_game_position, buildings_list, position):
    if start_game_position == 0:                                        #From turn 2 onwards, buildings must be placed adjacent to buildings that have been built.
        start_game_position = 1
    for buildings in buildings_list:                                    #Append position of building to individual position list in buildings_list
        if buildings[0] == building:
            buildings[2] += [position] 
    turn += 1                                                           #Increase turn counter
    if turn != 17:                                                      #Only randomise and deduct buildings during the game. After the last turn, no buildings should be deducted.
        building1, building2 = randombuilding(buildings_list)
        return (turn, building1, building2, start_game_position)
    else:
        return (turn, start_game_position)

#If 'See current score' option is selected during game, scores for each building will be calculated through their respective functions.   
def score_building(buildings_list, score_list, position_list): #Try & Exception is used because player can choose their buildings at the start, hence some building functions are not passed.
    try:
        beach(buildings_list, score_list) #Calculate beach score.
    except:
        pass
    
    try: 
        factory(buildings_list, score_list) #Calculate factory score.
    except:
        pass

    try:
        house(buildings_list, score_list, position_list) #Calculate house score.
    except:
        pass

    try:
        shop(buildings_list, score_list, position_list) #Calculate shop score.
    except:
        pass

    try:
        highway(buildings_list, score_list, position_list) #Calculate highway score.
    except:
        pass

    try:
        park(buildings_list, score_list) #Calculate park score.
    except:
        pass


#This function is used to sort the positions based on the row that the building is positioned.
def position_sorting(element):
    return element[1]
    

#This function calculates the score for beaches.
def beach(buildings_list, score_list):
    beach_index = ''
    for building_index in range(len(buildings_list)):          #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'BCH':         
            beach_index = building_index
            break
            
    beach_positions = (buildings_list[beach_index][2]).copy()  #Individual position list taken from buildings_list.
    beach_positions.sort()
    beach_positions.sort(key = position_sorting)


    for positions in beach_positions:
        if positions[0] == 'a' or positions[0] == 'd':
            score_list[beach_index] += [3]                  #If beach placed in column A or D, append 3 points to respective score list
        else:
            score_list[beach_index] += [1]                  #Else, append 1 point only.


#This function calculates the score for factories.
def factory(buildings_list, score_list):
    factory_index = ''
    for building_index in range(len(buildings_list)):               #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'FAC':
            factory_index = building_index
            break

    factory_positions = (buildings_list[factory_index][2]).copy()   #Individual position list taken from buildings_list.
    factory_positions.sort()
    factory_positions.sort(key = position_sorting)
    
    if 0 < len(factory_positions) <= 4:                               #'if' statement is conditional (with 0 included) so that the code will run when one building has been placed
        for times in range(len(factory_positions)):
            score_list[factory_index] += [1 * len(factory_positions)] #For the first four factories, score awarded for each factory is equal to number of factories built e.g 3 factories = 9 points

    elif len(factory_positions) > 4:                                  #If more than four factories are built,
        for times in range(4):                                        #first four factories are worth 4 points each, while the rest are worth 1 point each
            score_list[factory_index] += [4]
        for times in range(len(factory_positions) - 4):
            score_list[factory_index] += [1]

        
#This function calculates the score for houses.
def house(buildings_list, score_list, position_list):           
    house_index = ''
    for building_index in range(len(buildings_list)):                 #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'HSE':                
            house_index = building_index
            break

    house_positions = (buildings_list[house_index][2]).copy()         #Individual position list taken from buildings_list.
    house_positions.sort()
    house_positions.sort(key = position_sorting)
    abc_string = 'abcd'

    def house_calculation(house_index, score_list, row, column):      #Inner function created to calculate score for house, also check if factory is present
        if ('FAC' in (position_list[row][column][0])):
            score_list[house_index][-1] = 1
            return True
        elif ('HSE' in (position_list[row][column][0])) or ('SHP' in (position_list[row][column][0])):
            score_list[house_index][-1] += 1
            return False
        elif ('BCH' in (position_list[row][column][0])):
            score_list[house_index][-1] += 2
            return False


    for house in house_positions:
        column_index = abc_string.find(house[0])
        row_index = int(house[1]) - 1
        score_list[house_index] += [0]

        if column_index + 1 <= 3:
            if position_list[row_index][column_index + 1][0] != 0:
                FAC_present = house_calculation(house_index, score_list, row_index, column_index + 1)
                if FAC_present == True:                                                                     #If factory is present, other directions will not be considered.
                    continue
                
        if column_index - 1 >= 0:
            if position_list[row_index][column_index - 1][0] != 0:
                FAC_present = house_calculation(house_index, score_list, row_index, column_index - 1)
                if FAC_present == True:
                    continue

        if row_index + 1 <= 3:  
            if position_list[row_index + 1][column_index][0] != 0:
                FAC_present = house_calculation(house_index, score_list, row_index + 1, column_index)
                if FAC_present == True:
                    continue

        if row_index - 1 >= 0:
            if position_list[row_index - 1][column_index][0] != 0:
                FAC_present = house_calculation(house_index, score_list, row_index - 1, column_index)
                if FAC_present == True:
                    continue
                

#This function calculates the score for shops.
def shop(buildings_list, score_list, position_list):
    shop_index = ''
    for building_index in range(len(buildings_list)):           #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'SHP':          
            shop_index = building_index
            break
    
    shop_positions = buildings_list[shop_index][2]              #Individual position list taken from buildings_list.
    shop_positions.sort()
    shop_positions.sort(key = position_sorting)
    abc_string = 'abcd'

    def shop_calculation(shop_index, position_list, score_list, remaining_buildings, row, column): #Inner function created to calculate score for shop
        for building in remaining_buildings:
            if building in position_list[row][column][0]:
                score_list[shop_index][-1] += 1
                remaining_buildings.remove(position_list[row][column][0])   #Removes building from remaining_buildings so no points is awarded for same building in other directions.

    for shop in shop_positions:
        column_index = abc_string.find(shop[0])
        row_index = int(shop[1]) - 1
        score_list[shop_index] += [0]
        remaining_buildings = []
        for building in buildings_list:     #Construct remaining_buildings list each iteration
            remaining_buildings.append(building[0])
        
        if column_index + 1 <= 3:
            if position_list[row_index][column_index + 1][0] != 0:
                shop_calculation(shop_index, position_list, score_list, remaining_buildings, row_index, column_index + 1)

        if column_index - 1 >= 0:    
            if position_list[row_index][column_index - 1][0] != 0:
                shop_calculation(shop_index, position_list, score_list, remaining_buildings, row_index, column_index - 1)

        if row_index + 1 <= 3:  
            if position_list[row_index + 1][column_index][0] != 0:
                shop_calculation(shop_index, position_list, score_list, remaining_buildings, row_index + 1, column_index)

        if row_index - 1 >= 0:
            if position_list[row_index - 1][column_index][0] != 0:
                shop_calculation(shop_index, position_list, score_list, remaining_buildings, row_index - 1, column_index)


#This function calculates the score for highways.
def highway(buildings_list, score_list, position_list):
    highway_index = ''
    for building_index in range(len(buildings_list)):       #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'HWY':
            highway_index = building_index
            break

    highway_score_amount = [] #Represents score for each building (in a chain)
    highway_times = [] #Represent number of times to append score to score_list
    score = 0
    times = 0
    for rows in position_list:
        highway_score_amount += [score] #After one row is done, values are appended to highway_score_amount and highway_times, score and times are reset.
        highway_times += [times]
        score = 0
        times = 0

        for columns in rows:
            if columns[0] == 'HWY': #If there is a highway in this position, score and times increase by 1
                score += 1
                times += 1

            else:
                highway_score_amount += [score] #If there is no highway in this position, values are appended to highway_score_amount and highway_times, score and times are reset.
                highway_times += [times]
                score = 0
                times = 0

    highway_score_amount += [score] #Append final row's score and times.
    highway_times += [times]

    for i in range(len(highway_score_amount)): #Using 
        if highway_score_amount[i] * highway_times[i] != 0:
            for copies in range(highway_times[i]):
                score_list[highway_index] += [highway_score_amount[i]]



#This function calculates the score for parks:
def park(buildings_list, score_list):
    park_index = ''
    for building_index in range(len(buildings_list)):       #Find correct index to retrieve correct position list from buildings_list and append score to correct list.
        if buildings_list[building_index][0] == 'PRK':
            park_index = building_index
            break

    park_positions = (buildings_list[park_index][2]).copy() #Individual position list taken from buildings_list.
    park_positions.sort()
    park_positions.sort(key = position_sorting)
    park_score_list = [1, 3, 8, 16, 22, 23, 24, 25]

    connected_list = []
    abc_string = 'abcd'

    def append_adjacent_park(park, connected_list, adj_position):
        for index in range(len(connected_list)):
            for value in connected_list[index]:
                if value == park:                                   #Finds its own position, adds adjacent buildings to its own group
                    connected_list[index].append(adj_position)
    
    
    for park in park_positions:
        flag = 0                        #Flag to check if park is already registered into connected_list.
        for group in connected_list:
            for value in group:
                if value == park:
                    flag = 1
        if flag == 0:
            connected_list += [[park]]


        column_index = abc_string.find(park[0])
        row_index = int(park[1]) - 1


        #Check if adjacent building is a park
        if column_index + 1 <= 3:
            adj_column_letter = abc_string[column_index + 1]
            adj_position = adj_column_letter + str(row_index + 1)

            if adj_position in park_positions:
                append_adjacent_park(park, connected_list, adj_position)

        if column_index - 1 >= 0:
            adj_column_letter = abc_string[column_index - 1]
            adj_position = adj_column_letter + str(row_index + 1)

            if adj_position in park_positions:
                append_adjacent_park(park, connected_list, adj_position)

        if row_index + 1 <= 3:
            adj_row_number = row_index + 1
            adj_position = park[0] + str(adj_row_number + 1)

            if adj_position in park_positions:
                append_adjacent_park(park, connected_list, adj_position)

        if row_index - 1 >= 0:
            adj_row_number = row_index - 1
            adj_position = park[0] + str(adj_row_number + 1)

            if adj_position in park_positions:
                append_adjacent_park(park, connected_list, adj_position)
                

    #If position in one list can be also found in another list, append both lists together.
    final_connected_list = []
    unique_connected_list = []
    copy_list = connected_list.copy()
    for indexfirstlist in range(len(connected_list)):
        for itemfirstlist in connected_list[indexfirstlist]:
            for indexsecondlist in range(len(copy_list)):
                same_value = False
                for itemsecondlist in copy_list[indexsecondlist]:
                    if itemfirstlist == itemsecondlist and indexsecondlist != indexfirstlist: #Ensures checking of another list and not same list.
                        if connected_list[indexfirstlist] + copy_list[indexsecondlist] not in final_connected_list:
                            final_connected_list.append(connected_list[indexfirstlist] + copy_list[indexsecondlist])
                            same_value = True
                if same_value == False:
                    unique_connected_list.append(copy_list[indexsecondlist])
                    
    final_connected_list.extend(unique_connected_list)

    #Remove repeated positions in each group and remove repeated groups.
    park_group_list = []
    for group in final_connected_list:    
        temporary_list = []     #Clear temporary_list after one group is completed.
        for value in group:
            if value not in temporary_list:
                temporary_list.append(value) 

        temporary_list.sort()
        temporary_list.sort(key = position_sorting)
        if temporary_list not in park_group_list: #Check if the group is repeated before appending group into park_group_list.
            park_group_list.append(temporary_list)      


    #Extra cleaning. If position in one list can be also found in another list, removes the extra list.
    copy_list = park_group_list.copy()
    index_remove_list = []
    for indexfirstlist in range(len(park_group_list)):
        if indexfirstlist in index_remove_list: #Skip if list index is already appended into index_remove_list.
            continue
        for itemfirstlist in park_group_list[indexfirstlist]:
            for indexsecondlist in range(len(copy_list)):
                for itemsecondlist in copy_list[indexsecondlist]:
                    if itemfirstlist == itemsecondlist and indexsecondlist != indexfirstlist: #Ensures checking of another list and not same list.
                        if indexsecondlist not in index_remove_list:
                            index_remove_list += [indexsecondlist]

    for remove_index in index_remove_list:                     
        park_group_list.remove(copy_list[remove_index])   
   
    #Append score into score_list.
    for group in park_group_list:
        score_list[park_index] += [park_score_list[len(group) - 1]] #Retrieves value from park_score_list based on size of each group in final_connected_list.


#After scores for all buildings are calculated and appended into score_list, this function prints the score.
def current_score(buildings_list, score_list):
    buildings = []
    for building in buildings_list:
        buildings.append(building[0])

    total_score = 0
    for index in range(len(buildings_list)):
        print('{}: '.format(buildings[index]), end = '') #Print building name
        if len(score_list[index]) == 0: 
            print(0)
        else:
            for score in range(len(score_list[index]) - 1): 
                print('{} + '.format(score_list[index][score]), end = '')
            print('{}'.format(score_list[index][-1]), end = '')
            print(' = {}'.format(sum(score_list[index])))
            total_score += sum(score_list[index])
    print('Total score: {}'.format(total_score))
    return total_score #Total score is returned to check if player can be placed in highscore board.


#This function is called if the option to 'Save game' is selected during the game.
def save_game(position_list, buildings_list, turn, start_game_position, building1, building2):
    print()
    saved_data = open('savefile.txt', 'w') #Overwrites/Creates save file
    for row in position_list:
        for column in row:
            saved_data.write('{},{}\n'.format(column[0], column[1]))    #Writes all the positions on the map onto the save file
            
    for building in buildings_list:                                     #Writes all values in buildings_list onto the save file
        saved_data.write('{},{},'.format(building[0], building[1])) 
        for position in building[2]:
            saved_data.write('{},'.format(position))
        saved_data.write('\n')

    saved_data.write('{}\n'.format(turn))                               #Writes turn counter onto the save file
    saved_data.write('{}\n'.format(start_game_position))                #Writes start_game_position onto the save file
    saved_data.write('{}\n'.format(building1))                          #Writes first randomized building onto the save file
    saved_data.write('{}\n'.format(building2))                          #Writes second randomized building onto the save file
    
    saved_data.close()
    print('Game saved!')
    print()


#This function is called after turn 16 of the game. Prints the final layout (the game map, remaining building, score), and determines if player is eligible to be placed in high score board.
def end_of_game(position_list, buildings_list, score_list):
    print('Final layout of Simp City:')
    game_map(position_list)
    score_building(buildings_list, score_list, position_list)
    total_score = current_score(buildings_list, score_list)

    #if high score data already exists
    try:
        highscore_list = highscore_retrieve()                                   #Retrieve high score data and check if total_score meets criteria to be in highscore_list
        if (total_score > highscore_list[-1][1]) or len(highscore_list) < 10:
            if len(highscore_list) == 10:
                highscore_list.pop(9)
            repeated_values_list = []
            player_rank_index = 9
            for rank_index in range(len(highscore_list)):
                if total_score > highscore_list[rank_index][1]:
                    player_rank_index = rank_index                      
                    break
                
                elif total_score == highscore_list[rank_index][1]:              #'same score' scenario, player ranking is below players with same score
                    repeated_values_list.append(highscore_list[rank_index])
                    player_rank_index = rank_index + 1
            
            player_rank = player_rank_index + 1     #Display Player's ranking
            print('Congratulations! You made the high score board at position {}!'.format(player_rank))

            while True:
                player_name = input('Please enter your name (max 20 chars): ')
                if len(player_name) <= 20:
                    break
                else:
                    print()
                    print('Input unaccepted.')

            player_rank_info = [player_name, total_score]

            #'Same score as other players' scenario
            if len(repeated_values_list) > 0:       
                i = 1
                for value in repeated_values_list:   #Pass by Reference used to update repeated value index in highscore_list
                    value[2] = i
                    i += 1
                player_rank_info.append(i)  #add repeated value index to player_rank_info
            else:
                player_rank_info.append(0)

         
            highscore_list.insert(player_rank_index, player_rank_info) #Insert player's ranking into highscore_list


            single_value_list = [] #Update repeated value index for scores that are not repeated
            flag = 0
            for value_index in range(len(highscore_list)):
                flag = 0
                for othervalue_index in range(len(highscore_list)):
                    if value_index != othervalue_index:  
                        if highscore_list[value_index][1] == highscore_list[othervalue_index][1]:
                            flag = 1
                if flag == 0: #if score is unique, append score information to single_value_list
                    single_value_list.append(highscore_list[value_index])
            for value in single_value_list: #Check that repeated value index for unique scores is 0.
                if value[2] != 0:
                    value[2] = 0

            highscore_data = open('highscore.txt', 'w') #Write highscore_list to highscore_data
            for score in highscore_list:
                highscore_data.write('{},{},{}\n'.format(score[0], score[1], score[2]))
            highscore_data.close()

            #Print highscore board.
            print()
            highscore_list = highscore_retrieve() 
            highscore_print(highscore_list)
            print()


    #if no high score data exists, create new high score board
    except: 
        print('Congratulations! You made the high score board at position 1!')
        while True:
            player_name = input('Please enter your name (max 20 chars): ')
            if len(player_name) <= 20:
                break
            else:
                print()
                print('Input unaccepted.')

        highscore_data = open('highscore.txt', 'w')
        highscore_data.write('{},{},{}\n'.format(player_name, total_score, 0))
        highscore_data.close()

        #Print highscore_board
        print()
        highscore_list = highscore_retrieve()
        highscore_print(highscore_list)
        print()
    

#High score Functions  
#Finds highscore.txt to retrieve highscore data.
def highscore_retrieve():
    highscore_data = open('highscore.txt', 'r')
    highscore_list = []
    for line in highscore_data:
        line = line.strip('\n')
        line = line.split(',')
        line[1], line[2] = int(line[1]), int(line[2])
        highscore_list += [line]

    highscore_data.close()
    
    def sortposition(element):
        return element[2]

    def sortrank(element):
        return element[1]

    highscore_list.sort(key = sortposition)                 #Sort using repeated values
    highscore_list.sort(key = sortrank, reverse = True)     #Sort in descending order based on score
    return highscore_list

#Prints high score board.
def highscore_print(highscore_list):
    print('--------- HIGH SCORES ---------')
    print('{:<3} {:<22}{:<5}'.format('Pos', 'Player', 'Score'))
    print('{:<3} {:<22}{:<5}'.format('---', '------', '-----'))

    for i in range(len(highscore_list)):
        print('{:>3} {:<22}{:>5}'.format(str(i+1) + '.', highscore_list[i][0], highscore_list[i][1]))
        
    print('-------------------------------')


#--------------------------------------------------- Game Main Program ---------------------------------------------------#
#Main Menu screen
#In the main menu screen, the player can choose between 4 options, Start new game, Load saved game, Show high scores, or Exit.
#'Start new game' will give the player all the necessary variables (turn, buildings_list, position_list, start_game_position, building1, building2) in order to start the game.
#'Load saved game' will retrieve the player's saved data from the save file (located in the same destination as this Python file) and return saved values (position_list, buildings_list, turn, start_game_position, building1, building2)
#'Show high scores' will retrieve a high score list from the high score data (located in the same destination as this Python file) and display the high score board.
#'Exit' will exit the game.

while True:
    display_main_menu() #Print main menu
    menuchoice = input('Your choice? ')

    if menuchoice == '1': #Start new game.
        turn, buildings_list, position_list, start_game_position, building1, building2 = start_new_game()
    elif menuchoice == '2': #Load saved game
        try:
            position_list, buildings_list, turn, start_game_position, building1, building2 = load_saved_game()
        except:
            print()
            print('----------------------------------------------------------------------------')
            print('Saved data is not found or has been corrupted. Please select another option.') #No save file found or save file has been tampered with.
            print('----------------------------------------------------------------------------')
            print()
            continue
    elif menuchoice == '3': #Show high scores
        try:
            print()
            highscore_list = highscore_retrieve() #Prints high score board if high score file exists.
            highscore_print(highscore_list)
            print()
            print('Please select an option.')
            print()
            continue
        except:
            print('No highscore data found.') #No high score file found.
            print()
            continue

    elif menuchoice == '0': #Exit
        break
    else:
        print('Input unaccepted. Please select an option.')
        print()
        continue
        
#Game
#The player is given 16 turns.
#In the game, the player is given 5 options, Build the first randomized building, Build the second randomized building, See current score, Save game, or Exit to main menu.
#The player will also be shown a game map that displays a 4 x 4 map. If options 1 and 2 are selected, the player needs to select a square to build. The game map also displays the remaining buildings.
#Options 1 and 2 allows players to pick between 2 buildings. The 2 buildings are randomized each turn and deducted from the remaining buildings.
#Option 3 will calculate the score for the buildings that have been built and display the score.
#Option 4 will allow the player to save their game progress.
#Option 0 allows the player to return to the main menu. The player will be asked if he/she wants to return to the main menu with a warning that unsaved data cannot be retrieved.
    
    print()
    score_list = [[],[],[],[],[]] #An empty score_list is provided once the game starts
    while turn <= 16:
        illegal_position = True             #Player will loop in this current turn until they have built the building correctly (e.g adjacent to a building, valid input)
        while illegal_position == True:
            print('Turn {}'.format(turn))
            game_map(position_list)         #Prints game map and remaining buildings

            game_select_options(building1, building2)

            gamechoice = input('Your choice? ')

            if gamechoice == '1': #Build first randomized building.
                position = input('Build where? ') #Player prompted for position to build building
                position = position.lower()
                illegal_position = build(building1, position, position_list, start_game_position) #Checks if position is valid.
                if illegal_position == False: #Runs only if position is valid. If position not valid, player is to retry this turn again.
                    if turn != 16:
                        turn, building1, building2, start_game_position = game_progress(turn, building1, start_game_position, buildings_list, position) #Updates turn, randomized buildings and start_game_position.
                    else:
                        turn, start_game_position = game_progress(turn, building1, start_game_position, buildings_list, position) #After 16th turn, do not randomise and deduct buildings.
                    
            elif gamechoice == '2': #Build second randomized building.
                position = input('Build where? ') #Player prompted for position to build building
                position = position.lower()
                illegal_position = build(building2, position, position_list, start_game_position) #Checks if position is valid.
                if illegal_position == False: #Runs only if position is valid. If position not valid, player is to retry this turn again.
                    if turn != 16:
                        turn, building1, building2, start_game_position = game_progress(turn, building2, start_game_position, buildings_list, position) #Updates turn, randomized buildings and start_game_position.
                    else:
                        turn, start_game_position = game_progress(turn, building2, start_game_position, buildings_list, position) #After 16th turn, do not randomise and deduct buildings.

            elif gamechoice == '3': #Calculate and display score.
                print()
                score_building(buildings_list, score_list, position_list)
                current_score(buildings_list, score_list)
                score_list = [[],[],[],[],[]] #An empty score_list is provided so that the score_list is reset.
                print()
            
            elif gamechoice == '4': #Save game.
                save_game(position_list, buildings_list, turn, start_game_position, building1, building2)

            elif gamechoice == '0': #Return to main menu.
                return_main_menu = input('Are you sure you would like to return to the Main Menu?\n(Unsaved game data cannot be retrieved!)  Yes | No : ')
                return_main_menu = return_main_menu.lower()
                if return_main_menu == 'yes':
                    print('Returning to Main Menu...')
                    turn = 1000
                    break

            else:
                print('Input unaccepted. Please select an option.')
                print()

    
        print()
        print('-----------------------------------------------------------------')
        print()   

#After 16 turns, the game ends. The final layout of the building (the game map, remaining buildings, score) will be displayed for the player to see.
#If the player' score is more than the 10th player's score on the high score board (or if high score board has less than 10 players), the player will be prompted his/her name and will be placed on the high score board.
#If no high score data is found in same destination as this Python file, a new high score board will be created, with the player placed in the first position.

    if turn == 17:
        end_of_game(position_list, buildings_list, score_list)

        #Options after finishing game
        print('You have finished Simp City!')
        print('Type 1 to Return to Main Menu')
        print('Type 2 to Exit')
        while True:
            finished_menu = input('Your choice? ')
            if finished_menu == '1':
                print('Returning to Main Menu...')
                print()
                print('--------------------------------------------------')
                print()
                break
            elif finished_menu == '2':
                break
            else:
                print()
                print('Please select an option.')
        if finished_menu == '2':
            break
                

