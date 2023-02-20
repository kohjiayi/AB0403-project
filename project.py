import csv 
from collections import defaultdict 
import itertools 
import random
from colorama import Fore, Back, Style, init
init(autoreset = False)
from datetime import datetime, date, timedelta

#press any key to continue
def press_any_key():
    input("Press any key to continue: ")         

# create columns for inserting csv data into
columns = defaultdict(list) # each value in each column is appended to a list 
global count
global points

#Check if there is a savefile in the user's computer. If no, create a new one. If yes, draw data from the new file and loop back to withdraw data again. 
while True: 
    try: 
        with open("savedata.csv") as file_pointer: 
            reader = csv.DictReader(file_pointer) 
            for row in reader: 
                for k,v in row.items(): 
                    columns[k].append(v) 
        break 
    except FileNotFoundError: 
        new_columns = ['username','pwd','name','hhmember','hhtype','points','count','trees','fore_unlocked','back_unlocked','aircon_ticks','refri_ticks','heater_wattage','water_gallons','date_weekly'] 
        dummy_value = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None] #dummy values so that dictionary can be created 
        with open("savedata.csv","w") as file_pointer: 
            csv_pointer = csv.writer(file_pointer) 
            csv_pointer.writerow(new_columns) 
            csv_pointer.writerow(dummy_value) 
        continue 
 
# Functions for new users 
def enter_household(): # determine basic info - i.e. their household member 
    while True: 
        hh = input("Please enter the number of members in your household (integer only): ") 
        try: 
            hh = int(hh) 
            if hh <= 0:
                print("The number of people in the household must be at least 1!")
                continue
            else: break 
        except ValueError: 
            print("Please enter a valid integer!") 
    global columns
    columns['hhmember'][user_index] = hh
    return hh 

def enter_hhtype():
    while True:
        hhtype = input("Please enter your household type (choose and input the index number): \n[1] 1-room or 2-room HDB\n[2] 3-room HDB\n[3] 4-room HDB\n[4] 5-room HDB/executive HDB\n[5] Private Housing/Condo\n[6] Landed Property\n====================\n")
        valid_list = ['1','2','3','4','5','6']
        if hhtype not in valid_list:
            print("Invalid household type. Please try again.")
        else:
            global columns
            columns['hhtype'][user_index] = int(hhtype)
            return int(hhtype)

# Functions for old users 
def check_olduser():
    while True:
        old_user = input("Please enter your old username (case-sensitive): \nEnter 'e' to exit.\n====================\n")
        if old_user in columns["username"]:
            if old_user == "":
                print("Invalid username! Please try again.")
                continue
            user_index = columns['username'].index(old_user)
            old_pwd = input("Please enter your password (case-sensitive): ")
            while old_pwd != columns['pwd'][user_index]:
                old_pwd = input("Wrong Password, please try again: ")
            break
        elif old_user.lower() == 'e': #exit program if old user wants to
            return 'e'
        else:
            print("====================\nThis username is not found in our database.")
    return old_user

# Help user function: instructions on how the game works and how to get points
def help_user():
    print("\n====================\nHOW THE GAME WORKS\n====================")
    print("Rewards are given by completing missions. You can get TREES and POINTS\n\nTREES\n----------\nEvery 4 times you complete your weekly missions, you will be awarded with a tree to admire!\nEvery 4 trees you get will combine to evolve into a bigger tree!\n\nPOINTS\n----------\nComplete your general missions and monthly missions to be awarded points.\nEvery 100 points earns you a new style for your trees.")
    print("\nVisit the greenhouse to view your trees and to unlock all the styles!\n====================")

print("====================\nWelcome to ElecTREEcity!\n====================") # We come up with a name for this application later
while True:
    first_time = input("Is this your first time using the application? Y/N\n====================\n")
    if first_time.upper() == 'Y':
        print("====================\nWelcome new user! This application is a fun and interactive way to encourage you to save water and electricity at home! To start off, we would like you to input the following:")
        new_user = input("Please enter your new username\nInput 'e' to go back\n====================\n")
        if new_user.lower() == 'e':
            continue
        while True:
            if new_user == "":
                print("Please do not enter an empty username!")
                new_user = input("Please enter your new username (Type 'e' to go back): ")
            elif new_user in columns['username']: #check if username has already been taken
                print("Username already taken. Please try another username.")
                new_user = input("Please enter your new username (Type 'e' to go back): ")
                if new_user.lower() == 'e':
                    break
            else:
                new_pwd = input("Please enter your new password (at least 5 characters): ")
                while len(new_pwd) < 5:
                    new_pwd = input("Password is less than 5 characters. Please try again: ")
                columns['pwd'].append(new_pwd)
                print("\nPassword accepted.")
                new_name = ""
                while new_name == "":
                    new_name = input("Please enter your name: ")
                    if new_name == "":
                        print("\nPlease do not enter an empty name!")
                columns['username'].append(new_user)
                columns['name'].append(new_name)
                user_index = columns['username'].index(new_user) # Used for later parts
                columns['hhmember'].append(0)
                columns['hhtype'].append(0)
                household_num = enter_household()
                hhtype = enter_hhtype()
                username = new_user #defining variables to track points and update for new users
                name = new_name
                hhmember = household_num
                points = 0
                count = 4
                trees = 0
                fore_unlocked = ["Default"]
                back_unlocked = ["Default"]
                aircon_ticks = 0
                refri_ticks = 0
                heater_wattage = 0
                water_gallons = 0
                date_weekly = 0
                print(f"\nThank you for your inputs {name}!")
                help_user()
                print("You get 1 tree first, make sure to take good care of it!\n====================")
                break
    elif first_time.upper() == 'N':
        old_user = check_olduser()
        if old_user == 'e':
            continue
        user_index = columns['username'].index(old_user) #define variables for update for returning users
        username = old_user
        name = columns['name'][user_index]
        hhmember = columns['hhmember'][user_index]
        hhtype = columns['hhtype'][user_index]
        points = int(columns['points'][user_index])
        count = int(columns['count'][user_index])
        trees = int(columns['trees'][user_index])
        fore_unlocked = columns['fore_unlocked'][user_index].split(" ") #converting string to list
        back_unlocked = columns['back_unlocked'][user_index].split(" ")
        date_weekly = columns['date_weekly'][user_index]
        if date_weekly != '0':
            date_weekly = datetime.strptime(date_weekly,"%Y-%m-%d")
            date_weekly = date_weekly.date()
        aircon_ticks =  int(columns['aircon_ticks'][user_index])
        refri_ticks =  int(columns['refri_ticks'][user_index])
        heater_wattage =  float(columns['heater_wattage'][user_index])
        water_gallons =  float(columns['water_gallons'][user_index])
        print(f"\nWelcome back {columns['name'][user_index]}!")
        break
    else:  #error handling if user does not input Y/N for the first question
        print("====================\nInvalid Input. Please try again (Y/N only).")
        continue
    if new_user.lower() == 'e':
        continue
    break
        
## Check if Main Menu Input (below) is eligible
def check_menu_input():
    eligible_list = ['Hhold','Tips','Ghse','Monm','Genm','Wekm','User','Help','E']
    while True:
        main_menu_input = input("Please enter where you would like to go: ")
        if main_menu_input.capitalize() in eligible_list:
            break
        else:
            print("Incorrect input. Please enter 'Hhold','Tips','Ghse','Monm','Genm', 'Wekm' or exit with 'E'.")
    return main_menu_input.capitalize()
 
## Main Menu Page 
def main_menu_page(): 
    print("\n{:^60}".format("Main Menu"))
    print("=============================================================")
    print("{:<40}| Enter 'Hhold' below".format("Update Household Information"))
    print("{:<40}| Enter 'Tips' below".format("Electricity and Water Saving Tips")) 
    print("{:<40}| Enter 'Ghse' below".format("Greenhouse (Check your trees here!)")) 
    print("{:<40}| Enter 'Monm' below".format("Monthly Missions")) 
    print("{:<40}| Enter 'Genm' below".format("General Missions")) 
    print("{:<40}| Enter 'Wekm' below".format("Weekly Missions"))
    print("{:<40}| Enter 'User' below".format("Change User Settings"))
    print("{:<40}| Enter 'Help' below".format("Help on how the game works"))
    print("{:<40}| Enter 'E' below".format("Exit application"))
    main_menu_input = check_menu_input()
    return main_menu_input 

#Check if Ghse menu input is eligible
def check_Ghse_menu_input(): 
     eligible_list = ['Trees','Styles','E'] 
     while True: 
         Ghse_menu_input = input("Please enter where you would like to go: ") 
         if Ghse_menu_input.capitalize() in eligible_list: 
             break 
         else: 
             print("Invalid input. Please enter 'Trees','Styles',or 'E'.") 
     return Ghse_menu_input    
 
## Ghse menu page
def ghse_menu_page():
    print(f"{'='*21} {'Green House Menu'} {'='*21}") 
    print("{:<40}| Enter 'Trees' below".format("View your trees")) 
    print("{:<40}| Enter 'Styles' below".format("Use points to exchange new styles")) 
    print("{:<40}| Enter 'E' below".format("Exit to main menu")) 
    Ghse_menu_input = check_Ghse_menu_input() 
    return Ghse_menu_input 

## Print Trees
def print_trees(trees,big_trees):
    tree_art = r"""
    _\/_     
     /\      
     /\      
    /  \     
    /~~\o    
   /o   \    
  /~~*~~~\   
 o/    o \   
 /~~~~~~~~\~`
/__*_______\ 
     ||      
   \====/    
    \__/     
"""
    big_tree_art = r"""
             /\             
            <  >            
             \/             
             /\             
            /  \            
           /++++\           
          /  ()  \          
          /      \          
         /~`~`~`~`\         
        /  ()  ()  \        
        /          \        
       /*&*&*&*&*&*&\       
      /  ()  ()  ()  \      
      /              \      
     /++++++++++++++++\     
    /  ()  ()  ()  ()  \    
    /                  \    
   /~`~`~`~`~`~`~`~`~`~`\   
  /  ()  ()  ()  ()  ()  \  
  /*&*&*&*&*&*&*&*&*&*&*&\  
 /                        \ 
/,.,.,.,.,.,.,.,.,.,.,.,.,.\
           |   |            
          |`````|           
          \_____/           
"""
    print(f"====================\nPrinting trees...")
    if big_trees > 0:
        repeat_num = big_trees//3
        leftover = big_trees % 3
        if repeat_num //3 >= 1:
            big_list_art = big_tree_art.splitlines()
            for i in range (0,repeat_num):
                for i in big_list_art:
                    print (i*3)
            print("\n")
            if leftover > 0:
                for i in big_list_art:
                    print (i*leftover)
        else:
            big_list_art = big_tree_art.splitlines()
            for i in big_list_art:
                print (i*big_trees)
            print("\n\n")
            
    if trees > 0:
        list_art = tree_art.splitlines()
        for i in list_art:
            print (i*trees)
        print ("\n\n")
    if trees == 0 and big_trees == 0:
        print ("\nYou do not have any trees currently! Complete more weekly missions to earn trees!")
    else:
        print(f"You have {big_trees} big trees and {trees} trees! Complete {4-count%4} more weekly mission(s) to get a tree and collect another {4-trees} tree(s) to get a big tree!")
    return

##Colour selection
def colsel():
    if fore_unlocked != ["Default"]:
        while True:
            print(f"\nYou have unlocked {fore_unlocked} for the font colour(s).")
            user_fcol = input("What colour do you want the font to be? (Enter N for default colour) : ")
            if user_fcol.capitalize() in fore_unlocked and user_fcol.capitalize() != "Default":
                print(getattr(Fore,user_fcol.upper())+f"\nThe font colour is now set to {user_fcol}.")
                break
            elif user_fcol.upper() == "N":
                print("\nThe font colour has not been changed.")
                break
            else:
                print("\nPlease make a valid selection!")
    else:
        print("\nYou have not unlocked any font colours. Head over to Styles in the Greenhouse to unlock!")
    if back_unlocked != ["Default"]:
        while True:
            print(f"\nYou have unlocked {back_unlocked} for the background colour(s).")
            user_bcol = input("What colour do you want the background to be? (Enter N for default colour)\n(Warning: If background is the same colour as font, the tree cannot be seen!) : ")
            if user_bcol.capitalize() in back_unlocked and user_bcol.capitalize() != "Default":
                print(getattr(Back,user_bcol.upper())+f"\nThe background colour is now set to {user_bcol}.")
                break
            elif user_bcol.upper() == "N":
                print("\nThe background colour has not been changed.")
                break
            else:
                print("\nPlease make a valid selection!")
    else:
        print("\nYou have not unlocked any background colours. Head over to Styles in the Greenhouse to unlock!")
        

##Style unlock
def style_unlock():
    fore_colours = ["Red","Green","White","Blue","Magenta","Cyan"]
    back_colours = ["Red","Green","White","Blue","Magenta","Cyan"]
    fore_locked = []
    back_locked = []
    global fore_unlocked
    global back_unlocked
    global points 
    for each in fore_colours:
        if each not in fore_unlocked:
            fore_locked.append(each)
            
    for each in back_colours:
        if each not in back_unlocked:
            back_locked.append(each)


    while points >= 100:
        if fore_locked == [] and back_locked == []:
            print("You have unlocked all styles! Please check back for more updates!\nReturning to main menu...")
            break
        else:
            print(f"====================\nYou have {points} points")
            print (f"You have enough points to unlock {points//100} colour(s)")
            fb_choice = input("Do you want to unlock colours for the font (F) or background (B)? (Enter E to exit): ")
            if fb_choice.upper() == "F":
                if fore_locked != []:
                    while True:
                        print(f"====================\nYou have unlocked {fore_unlocked}.")
                        print(f"The colours available for unlock are {fore_locked}.")
                        fchoice_unlock = input ("What colour do you wish to unlock? : ")
                        if fchoice_unlock in fore_locked:
                            print (f"You have unlocked {fchoice_unlock} font style!")
                            fore_unlocked.append(fchoice_unlock)
                            fore_locked.remove(fchoice_unlock)
                            points -= 100
                            break
                        else:
                            print("\nPlease make a valid selection!")
                        
                elif fore_locked == []:
                    print("You have unlocked all font colours! Returning to main menu.")
            elif fb_choice.upper() == "B":
                if back_locked != []:
                    while True:
                        print(f"====================\nYou have unlocked {back_unlocked}.")
                        print(f"The colours available for unlock are {back_locked}.")
                        bchoice_unlock = input ("What colour do you wish to unlock? : ")
                        if bchoice_unlock in back_locked:
                            print (f"You have unlocked {bchoice_unlock} background style!")
                            back_unlocked.append(bchoice_unlock)
                            back_locked.remove(bchoice_unlock)
                            points -= 100
                            break
                        else:
                            print("\nPlease make a valid selection!")
                        
                elif back_locked == []:
                    print("====================\nYou have unlocked all background colours! Returning to main menu.")
            
            elif fb_choice.upper() == "E":
                print("Returning to main menu...")
                break
            else:
                print("\nPlease enter a valid selection!")
    if points <100 and fore_locked == [] and back_locked == []:
        print("====================\nYou have unlocked all styles! Please check back for more updates!\nReturning to main menu...")
    elif points <100:
        print (f"====================\nYou do not have enough points ({points}) to unlock any colours! Complete more weekly and monthly missions to earn points!\nReturning to main menu...")
        


## Saving Tips 
def saving_tips(): 
    tips_list = ["You can save up to S$70 per year by using a 4-ticks energy saving fridge over one that is only rated 2-ticks.","Did you know that you can save up to S$25 a year for every degree you raise your air-conditioner?", 
                 "When you switch to a fan instead of an air-conditioner, you can save up to S$840 a year","By using LED lights, you can generate savings of up to S$35 per bulb every year.", 
                 "Switch off your plugs when not in use as they account for up to 10% of our electricity bill in Singapore.","Check your home for loosely fitted or corroded water pipes to prevent unnecessary water wastage (up to 14% of your water footprint can be lost to leaks).", 
                 "Consider switching to a low-flow showerhead to save 15 gallons of water during a 10-minute shower.","Start making a difference today by adopting these good water-saving habits at home:\nWASH clothes on full load\nALWAYS use half-flush when possible\nTURN off the shower when soaping\nENSURE tap is off when brushing teeth\nRINSE vegetables in a container", 
                 "Did you know that water usage among households with foreign domestic workers is 20 per cent higher than households without such helpers?","Choosing to air-dry your laundry instead of using a dryer will save you 40kwh of energy a month." 
                 "Using the cold setting on your washing machine instead of the warm water will save you around $150 every year."] 
    print("\n====================\n",random.choice(tips_list),"\n====================")
    while True:
        tip_repeat = input("Another tip? Y/N:\n") 
        if tip_repeat.upper() == "Y": 
            print("\n====================\n",random.choice(tips_list),"\n====================")
            continue
        elif tip_repeat.upper() == "N": 
            break
        else:
            print("Invalid Input, please enter Y or N only!")

# Change Household Information (Hhold)
def change_hh():
    while True:
        change_hh_input = input("Select the following to change (input the index number):\n[1] Change household member\n[2] Change household type\n[3] Back to Main Menu\n====================\n")
        if change_hh_input not in ['1','2','3']:
            print("Invalid input. Please try again.")
        elif int(change_hh_input) == 1:
            enter_household()
        elif int(change_hh_input) == 2:
            enter_hhtype()
        elif int(change_hh_input) == 3:
            return

def change_user():
    global columns
    global user_index
    while True:
        change_user_input = input("Select the following to change (input the index number):\n[1] Change password\n[2] Change name\n[3] Exit to main menu\n====================\n")
        if change_user_input not in ['1','2','3']:
            print("Invalid input. Please try again.")
        elif int(change_user_input) == 1: #Change password
            print(f"\nYour current password is: {columns['pwd'][user_index]}.")
            new_pwd = input("Please enter a new password (at least 5 characters). Enter 'e' to return:  ")
            if new_pwd.lower() == 'e':
                continue
            while len(new_pwd) < 5:
                new_pwd = input("Please enter a valid password (must be at least 5 characters). Enter 'e' to return:  ")
                if new_pwd.lower() == 'e': break
            columns['pwd'][user_index] = new_pwd
            print("\nNew password accepted.")
        elif int(change_user_input) == 2: #Change name
            user_newname = ""
            while user_newname == "":
                user_newname = input("Please enter your new name: ")
                if user_newname == "": print("\nPlease do not input an empty name!")
            columns['name'][user_index] = user_newname
            print(f"\nName changed to: {columns['name'][user_index]}.")
        elif int(change_user_input) == 3: #exit
            return
#monthly mission
def get_value (variable): #get input from user and store value in column
    while True:
        try:
            user_input = float(input(f"Please enter {variable}:"))
            if user_input > 0:
                break
            else: print("Invalid entry. Please enter a positive number")
        except:
            print("Invalid entry. Please enter a number.")
    return user_input
def get_avg_elec():
    national_avg_elct = 0
    x = int(columns['hhtype'][user_index])
    if x == 1: #1 or 2-room
        national_avg_elct = 170.2
        return national_avg_elct
    elif x == 2: #3-room
        national_avg_elct = 274.2
        return national_avg_elct
    elif x == 3: #4-room
        national_avg_elct = 375.5
        return national_avg_elct
    elif x == 4: #5-room and Exec HDB
        national_avg_elct = 456
        return national_avg_elct
    elif x == 5: #Private/condo
        national_avg_elct = 538.7
        return national_avg_elct
    elif x == 6: #Landed
        national_avg_elct = 1209.1
        return national_avg_elct

def leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

def days_in_month(month, year):
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        if leap_year(year):
            return 29
        return 28
    return 30
def get_average(data,current):
    m_count = 0
    total = 0
    for i in data:
        total += float(i)
        m_count +=1
    total += current 
    avg = total/m_count
    return avg
def print_summary (avg_electricity_usage, national_avg_elct, avg_water_usage): 
 if avg_electricity_usage < national_avg_elct and avg_water_usage < 141: 
    print(f"""====================\nWell Done! 
Your average electricity usage is {avg_electricity_usage:.2f} kWh and water usage is {avg_water_usage:.2f} litres per household member per day. This is below national average of {national_avg_elct} kWh and 114 litres. 
Keep up the good work!!\n====================\n""") 
 elif avg_electricity_usage < national_avg_elct and avg_water_usage > 141:
     print(f"""====================\nGood Job! 
Your average electricity usage is {avg_electricity_usage:.2f} kWh, which is below the national average of {national_avg_elct} kWh. However, your average water usage is {avg_water_usage:.2f} litres per household member per day, which is above national average of 114 litres.
Enter 'Tips' in main menu for tips to reduce your water usage.\n====================\n""") 
 elif avg_electricity_usage > national_avg_elct and avg_water_usage < 141:   
     print(f"""====================\nGood Job! 
Your average water usage is {avg_water_usage:.2f} litres per household member per day, which is below national average of 114 litres. However, your average electricity usage is {avg_electricity_usage:.2f} kWh, which is above the national average of {national_avg_elct} kWh.
Enter 'Tips' in main menu for tips to reduce your electricity usage.\n====================\n""") 
 elif avg_electricity_usage > national_avg_elct and avg_water_usage > 141:
     print(f"""====================\nOh no! 
Your average electricity usage is {avg_electricity_usage:.2f} kWh and water usage is {avg_water_usage:.2f} litres per household member per day. This is above national average of {national_avg_elct} kWh and 114 litres.
Enter 'Tips' in main menu for tips to reduce your electricity and water usage.\n====================\n""") 

def monm():
    monthly_columns = defaultdict(list) # each value in each column is appended to a list
    # Create/open monthly data file
    while True: 
        try:
            with open("monthlydata.csv") as file_pointer:
                reader = csv.DictReader(file_pointer)
                for row in reader:
                    for k,v in row.items():
                        monthly_columns[k].append(v)
            break
        except FileNotFoundError:
            new_columns = ['username','year','month','electricity_usage','water_usage','daily_water_usage']
            dummy_value = [None,None,None,None,None,None] #dummy values so that dictionary can be created
            with open("monthlydata.csv","w") as file_pointer:
                csv_pointer = csv.writer(file_pointer)
                csv_pointer.writerow(new_columns)
                csv_pointer.writerow(dummy_value)
            continue
        
    # get user name from savedata.csv
    global columns, user_index

    #get dates
    to_day = datetime.today()
    month = to_day.month
    year = to_day.year
    run = True
    while run == True:
        # Month dictionary for display later
        month_dict = {
                    "January": 1,
                    "February": 2,
                    "March": 3,
                    "April" : 4,
                    "May" : 5,
                    "June": 6,
                    "July": 7,
                    "August": 8,
                    "September": 9,
                    "October": 10,
                    "November": 11,
                    "December": 12
                    }
        year_month_confirmation = input(f"""Current month selected is {to_day.strftime("%B")} , {year}. To select another month or year enter 'Y', otherwise enter 'N': """)
        if year_month_confirmation.upper() == 'N' :
            # line 586 to 592's goal is to 1) detect the user trying to enter info again for the same month. If they do, then the program sends an error message and boots
            # them out to main menu. However, if it is the user's first time inputting for this month, then the program will continue.
            for k,v in enumerate(monthly_columns['username']):
                if v == columns['username'][user_index] and int(monthly_columns['year'][k]) == year and int(monthly_columns['month'][k]) == month:
                    print("\nYou already entered information for this month. Returning to main menu...")
                    return
            month_selected = month
            year_selected = year
            break
        elif year_month_confirmation.upper() == 'Y' :
            year = int(get_value("year"))

            print("{:^10s} | Month No.".format('Month'))   
            for x,y in month_dict.items():
                print(f"{x:^10s} | {y:^8d}")
            month = int(get_value("month no."))
            if month <= 12 and year > 2000 : # to prevent user from entering month 13 
               for k,v in enumerate(monthly_columns['username']):
                   if v == columns['username'][user_index] and int(monthly_columns['year'][k]) == year and int(monthly_columns['month'][k]) == month:
                       print("\nYou already entered information for this month. Returning to main menu...")
                       return
               month_selected = month
               year_selected = year
               break
            else:
                user_input= input("Invalid entry. Please try again or enter 'E' to go back to main menu:")
                if user_input.upper() == "E" :
                    return
                    
        else:
            user_input= input("Invalid entry. Please try again or enter 'E' to go back to main menu:")
            if user_input.upper() == "E" :
                return
                
   # Get electical bill input from user
    electricity_usage = get_value("electricity usage (kWh)")
    
    #waterbill
    water_usage = get_value("water usage (m^3)")  
        
    # award points    
    print(f"\n====================\nDear {columns['username'][user_index]}, thank you for entering your water and electricity usage! You have been awarded 30 points for your input.\n====================\n") 
    global points
    points += 30
    print("\n====================\nSUMMARY\n====================")
    
    #feedback based on usage
    national_avg_elct = float(get_avg_elec())
    days = days_in_month(month_selected, year_selected)
    daily_water_usage = ((water_usage*1000)/days)/int(columns['hhmember'][user_index])
    global first_timefir
    if first_time.upper() == 'Y': #for new user
        print_summary(electricity_usage, national_avg_elct, daily_water_usage)
    else:
        user_years = []
        user_months = []
        user_e_usage = []
        user_daily_w_usage = []
        for k,v in enumerate(monthly_columns['username']):
            if k == 0:
                user_years.append(0)
                user_months.append(0)
                user_e_usage.append(0)
                user_daily_w_usage.append(0)
            elif v == columns['username'][user_index]:
               user_years.append(int(monthly_columns['year'][k]))
               user_months.append(int(monthly_columns['month'][k]))
               user_e_usage.append(float(monthly_columns['electricity_usage'][k]))
               user_daily_w_usage.append(float(monthly_columns['daily_water_usage'][k]))

        latest_year = max(user_years)
        latest_yr_indexlist = []
        latest_mth_list = []
        latest_mth_indexlist = []
        for k,v in enumerate(user_years):
           if v == latest_year:
               latest_yr_indexlist.append(k)
        for k,v in enumerate(user_months):
           if k in latest_yr_indexlist:
               latest_mth_list.append(v)
               latest_mth_indexlist.append(k)

        latest_mth_list = [int(x) for x in latest_mth_list]
        for k,v in enumerate(latest_mth_list):
            if v == max(latest_mth_list):
                prev_index = k+1
                latest_mth = v
        if latest_mth == 0:
            print_summary(electricity_usage, national_avg_elct, daily_water_usage)
        else:
            #To get month name
            mth_name=list(month_dict.keys())[list(month_dict.values()).index(latest_mth)]
            #get previous entry
            previous_electricity_usage = user_e_usage[prev_index]
            previous_water_usage = user_daily_w_usage[prev_index]

            if previous_water_usage > daily_water_usage:
               print(f"Your water usage has decreased by {previous_water_usage - daily_water_usage :.2f} litre per day per household member compared to {mth_name},{latest_year}.")
            else:
              print(f"Your water usage has increased by {daily_water_usage -previous_water_usage :.2f} litre per day per household member compared to {mth_name},{latest_year}.")     
            if previous_electricity_usage > electricity_usage:
               print(f"Your electricity usage has decreased by {previous_electricity_usage - electricity_usage} kWh compared to {mth_name},{latest_year}.")
            else:
               print(f"Your electricity usage has increased by {electricity_usage - previous_electricity_usage} kWh compared to {mth_name},{latest_year}.")
               
            #average electricity usage
            avg_electricity_usage = get_average(user_e_usage, electricity_usage)
            #average daily water usage
            avg__daily_water_usage = get_average(user_daily_w_usage,daily_water_usage)
            print_summary(avg_electricity_usage, national_avg_elct, avg__daily_water_usage)
    #update monthly data
    monthly_columns['username'].append(columns['username'][user_index])
    monthly_columns['year'].append(year_selected) 
    monthly_columns['month'].append(month_selected)
    monthly_columns['electricity_usage'].append(electricity_usage) #add data to the monthlydata
    monthly_columns['water_usage'].append(water_usage)
    monthly_columns['daily_water_usage'].append(daily_water_usage)
    keys = monthly_columns.keys()      
    ## Iterate the lists (in associative list format) from defaultdict back into csv format 
    ## (represented by keys) to prepare write into savedata.csv. Fill up any blank entries with 'None'.
    csvrows = itertools.zip_longest(*[monthly_columns[k] for k in keys], fillvalue='None')
    with open('monthlydata.csv', 'w',newline="") as file_pointer:
        csvwriter = csv.writer(file_pointer)
        csvwriter.writerow(keys) #write columns into csv file
        for row in csvrows: #iterates every item within csvrows which contains the data rows.
            csvwriter.writerow(row)# Monthly Missions (Monm)

    if water_usage > 40:
         print("Currently, you are billed $3.69 per m^3 as your water usage is above PUB's threshold of 40m^3. Lower your water usage to 40m^3 to save $0.95 per m^3.\n====================")

# Genm functions 
#summary page 
def summary_page():
    tips_list = []
    print (f"""

{'='*20} Summary {'='*20}
Aircon Ticks: {aircon_ticks}                 Fridge Ticks: {refri_ticks}
Water Gallons: {water_gallons}              Heater Wattage: {heater_wattage}\n\n""")

    if aircon_ticks == 2:
       tips_list.append("Tip: Using a 3 ticks aircon can help you save $210 every year.")
    elif aircon_ticks == 3:
        tips_list.append("Tip: Using a 4 ticks aircon can help you save $180 every year.")
    elif aircon_ticks == 4:
        tips_list.append("Tip: Using a 5 ticks aircon can help you save $30 every year.")
    elif aircon_ticks == 5:
        tips_list.append("Good job! Using a 5 ticks aircon has helped you save $410 every year compared to a 2 ticks model.")

    if refri_ticks == 2:
       tips_list.append("Tip: Using a 3 ticks fridge can help you save $23 every year.")
    elif refri_ticks == 3:
        tips_list.append("Tip: Using a 4 ticks fridge can help you save $46 every year.")
    elif refri_ticks == 4:
       tips_list.append("Good job! Using a 4 ticks fridge has helped you save $69 every year compared to a 2 ticks model.")

    if heater_wattage < 4500:
        tips_list.append("\nGood job! Your water heater wattage is lower than the national average of 4500 watts.")
    elif heater_wattage == 4500: 
        tips_list.append("\nYour water heater wattage is around national average. Using a lower wattage will help save electricity!")
    elif heater_wattage > 4500: 
       tips_list.append("Your water heater wattage is higher than the national average of 4500 watts. Using a lower wattage will help save electricity!")
       
    if water_gallons == 1.6:
        tips_list.append("Your toilet uses 1.6 gallons per flush. Using a dual flush will help you save 0.8 gallons per flush.")
    elif water_gallons == 0.8:
        tips_list.append('Good job! Using a dual flush has helped you save 0.8 gallons per flush.')
        
    print(random.choice(tips_list))

#aircon, fridge ticks general
def get_ticks (airfridge , csvfile):
    global points
    ticks = 0
    if refri_ticks != 0:   #old user
        while True:
            update_ticks = input(f"====================\nDo you want to update your {airfridge} ticks? Y/N: ")
            if update_ticks.upper() == "Y":
                while True:                   
                    try:
                        update_ticks = int(input(f"How many ticks does your new {airfridge} have? (Use integers from 2-5 only for aircon, and 2-4 for fridge): "))
                        if airfridge == "aircon":
                            if update_ticks <2 or update_ticks >5:
                                print("Please enter integers from 2-5 only!")
                            else:
                                break
                            
                        elif airfridge == "fridge":
                            if update_ticks <2 or update_ticks >4:
                                print("Please enter integers from 2-4 only!")
                            else:
                                break

                    except ValueError: 
                        print("Invalid input! Please enter integer values only!")
                        
                print(f"Your {airfridge} has been updated to {update_ticks} ticks.")
                return update_ticks
                break
                
            elif update_ticks.upper() == "N":
                if airfridge == 'aircon':
                    return aircon_ticks
                elif airfridge =='fridge':
                    return refri_ticks
                break
            
            else:
                print("Please enter only Y/N!")
                         
    else:            #new user
        general = input(f"====================\nDo you know how many ticks your {airfridge} has? Y/N: ")
        while True:
            try:
                if general.upper() == "Y":
                    ticks = int(input(f"How many ticks does your {airfridge} have? (Use integers from 2-5 for aircon, and 2-4 for fridge): "))
                    if airfridge == "aircon":
                        if ticks <2 or ticks >5:
                            print("Please enter integers from 2-5 only!")
                        else:
                            break
                    elif airfridge == "fridge":
                        if ticks <2 or ticks >4:
                            print("Please enter integers from 2-4 only!")
                        else:
                            break
                        
                elif general.upper() == "N":
                    model = input(f"What is your {airfridge} model? (enter in caps, or enter 'E' if you dont know the model: ")
                    if model.upper() != "E":
                        with open(f"{csvfile}", "r") as filepointer:
                            reader = csv.reader(filepointer)
                            for each in reader:
                                if model == each[0]:
                                    print(f"Your {airfridge} has",each[1],"ticks!")
                                    ticks = each[1]
                                    break
                            if ticks == 0: #if above codes did not capture aircon ticks
                                while True:
                                    user_continue = input(f"Your {airfridge} model is not found! Enter 'N' to try again or 'E' to exit (We will set an average of 3 ticks): ")
                                    if user_continue.upper() == "N":
                                        break
                                    elif user_continue.upper() == "E":
                                        ticks = 3
                                        break
                                    else:
                                        print("Enter only 'N' to try again or 'E' to exit!")
                                    
                            if ticks != 0:
                                break
                    else:
                        print(f"We will set your {airfridge} at an average of 3 ticks.")
                        ticks = 3
                        break
                else:
                    print("Please only enter Y/N!")
                    general = input(f"Do you know how many ticks your {airfridge} has? Y/N: ")
            except ValueError:
                print("Invalid input! Please enter integer values only!")
        points += 50
        return ticks
    
# heater wattage general
def heater():
    global points
    global heater_wattage

    if heater_wattage != 0:   #old user
        while True:
            update_heater = input(f"====================\nDo you want to update your heater wattage? Y/N: ")
            if update_heater.upper() == "Y":
                while True:                   
                    try:
                        update_heater = int(input("What is your new water heater wattage? (Enter integers only): "))
                        if update_heater <= 0:
                            print("Please enter positive integers only!")
                        
                        else:
                            print(f"Your water heater has been updated to {update_heater} watts.")                      
                            return update_heater
                            break
                    
                    except ValueError: 
                        print("Invalid input! Please enter integer numbers only!")   
            
            elif update_heater.upper() == "N":
                return heater_wattage
                break
            
            else:
                print("Please enter only Y/N!")
    
    if heater_wattage == 0:            #new user
        heater_general = input(f"====================\nDo you know your water heater wattage? Y/N: ")
        while True:
            try:
                if heater_general.upper() == "Y":
                    heater_wattage = int(input("What is your water heater wattage? (Enter integers only): "))  
                    if heater_wattage <= 0:
                        print("Please enter positive integers only!")
                        heater_general = input("Do you know your water heater wattage? Y/N: ")
                    else:
                        break
                elif heater_general.upper() == "N":
                    heater_wattage = 4500 #average wattage in SG 
                    print("\nWe will set your water heater wattage at an average of 4500 watts.")
                    break
                else:
                    print("Please only enter Y/N!")
                    heater_general = input("Do you know your water heater wattage? Y/N: ")
            except ValueError:
                print("Invalid input! Please enter integer numbers only!")
        points += 50
        return heater_wattage

#toilet flush system general    
def toilet():
    global points
    global water_gallons
    
    if water_gallons != 0:   #old user
        while True:
            update_toilet = input(f"====================\nDo you want to update your toilet flush system? Y/N: ")
            if update_toilet.upper() == "Y":
                while True:
                    update_toilet = input("Is your new toilet a single or dual flush system? (Enter 'S' for single, or 'D' for dual: ")
                    if update_toilet.capitalize() == "S":
                        water_gallons = 1.6
                        print(f"Your updated toilet system uses {water_gallons} gallons per flush.")
                        print(f"\n====================\nGoodbye!")
                        return water_gallons
                        break
                    
                    elif update_toilet.capitalize() == "D":
                        water_gallons = 0.8
                        print(f"Your updated toilet system uses {water_gallons} gallons per flush.")
                        print(f"\n====================\nGoodbye!")
                        return water_gallons
                        break
                    
                    else:
                        print("Please only enter S/D!")
            
            elif update_toilet.upper() == "N":
                print(f"\n====================\nGoodbye!")
                return water_gallons
                break
            
            else:
                print("Please enter only Y/N!")

    if water_gallons == 0:           #new user
        toilet_general = input(f"====================\nIs your toilet a single or dual flush system? (Enter 'S' for single, or 'D' for dual: ")
        while True:   
            if toilet_general.upper() == "S":
                water_gallons = 1.6
                print("\nYour toilet uses 1.6 gallons per flush.")
                break
                
            elif toilet_general.upper() == "D":
                water_gallons = 0.8
                print("\nYour toilet uses 0.8 gallons per flush.")
                break
            
            else:
                print("Please only enter S/D!") 
                toilet_general = input("Is your toilet a single or dual flush system? (Enter 'S' for single, or 'D' for dual: ")
        points += 50
        print (f"\n====================\nThank you for completing your general mission. You have earned 200 points! ")
        return water_gallons   
    
##Wekm (Weekly Functions for the specific appliances)
#water_heater
def heater_usage(): 
    try:
        heater = input ("Do you switch on the water heater when you shower? Y/N ")
        while True: 
            if heater.upper() == 'Y':
                try:
                    water_heater = float(input ("How many hours per day do you use it for this week? "))
                    if water_heater >= 0 and water_heater <= 24:
                        break
                    else:
                        print("Please only use values from 0-24!")
                except ValueError:
                    print("Please only use values from 0-24!")
            elif heater.upper() == 'N':
                water_heater = 0
                break
            else:
                print ("Please enter either Y/N!")
                heater = input ("Do you switch on the water heater when you shower? Y/N ")
    except ValueError:
        print("Invalid input! PLease only enter Y/N!")
    return water_heater

#aircon                     
def aircon_usage():    
        while True:
            try:
                aircon = float(input("How many hours do you use the aircon per day on average? "))
                if aircon < 0 or aircon > 24:
                    print("Please only use values from 0-24!")
                else:
                    break
            except ValueError:
                print("Invalid input! Please enter numerical numbers only!")
        return aircon

#shower
def shower():
    while True:
        try:
            shower_frequency = int (input ("How many showers did you take this week? "))
            if shower_frequency >= 0:
                shower_time  = float(input ("Enter the average time spent in the shower per day (hours): "))
                shower_amount = shower_time * shower_frequency * 9
                if shower_time < 0 or shower_time > 24:
                    print("Please only use values from 0-24!")
                else:
                    print (f"You have used {shower_amount} litres of water on SHOWER this week.")
                    break
            else:
                print('Please only use positive integers!')
        except ValueError:
            print("Invalid input! Please enter numerical numbers only!")
    return shower_amount
              
#kitchen
def kitchen_usage():
    while True: 
        try:
            kitchen = input ("Do you wash dishes, fruits and vegetables under a running tap or in a filled sink? Enter 'R' for running tap or 'F' for filled sink. ")
            if kitchen.upper() == 'R':
                kitchen_frequency = float(input ("How often do you use the sink per day this week? "))
                if kitchen_frequency >= 0:
                    kitchen_amount = 40* kitchen_frequency * 7
                    print(f"You have used {kitchen_amount} litres of water on SINK this week.")
                    break
                else:
                    print ("Please enter a number more than 0!")
            elif kitchen.upper() == 'F':
                kitchen_frequency = float(input ("How often do you use the sink per day this week? "))
                if kitchen_frequency >=0:
                    kitchen_amount = 12 * kitchen_frequency * 7
                    print(f"You have used {kitchen_amount} litres of water on SINK this week.")
                    break
                else:
                    print ("Please enter a number more than 0!")
            else:
                print("PLease enter R or F!")
        except ValueError:
            print("Invalid input! Please enter numerical numbers only!")
    return kitchen_amount
            
#washmachine             
def washmachine_usage():
    washmachine = input ("Do you know how many ticks your washing machine has? Y/N ")
    while True:
        try:

            if washmachine.upper() == 'Y':
                washmachine_ticks = int (input ("How many ticks does your washing machine have? "))
                if washmachine_ticks < 2 or washmachine_ticks > 4:
                    print("Please only use values from 2-4!")
                else:
                    break
            elif washmachine.upper() == 'N':
                print ("We will set your washing machine ticks at an average of 3 ticks.")
                washmachine_ticks = 3
                break
            else:
                print("Please input either Y/N!")
                washmachine = input ("Do you know how many ticks your washing machine has? Y/N ")
        except ValueError:
            print("Please only enter values from 2-4!")
    return washmachine_ticks

#function that concludes and uploads the data into csv
def save_the_data():
    #for converting list to string before uploading to csv
    global fore_unlocked , back_unlocked
    fore_unlocked = " ".join(fore_unlocked)
    back_unlocked = " ".join(back_unlocked)
    
    ## updating columns in savedata.csv
    if first_time.upper() == 'N':
        columns['points'][user_index] = points
        columns['count'][user_index] = count
        columns['trees'][user_index] = trees
        columns['fore_unlocked'][user_index] = fore_unlocked
        columns['back_unlocked'][user_index] = back_unlocked
        columns['aircon_ticks'][user_index] = aircon_ticks
        columns['refri_ticks'][user_index] = refri_ticks
        columns['heater_wattage'][user_index] = heater_wattage
        columns['water_gallons'][user_index] = water_gallons
        columns['date_weekly'][user_index] = date_weekly
    else:
        columns['points'].append(points)
        columns['count'].append(count)
        columns['trees'].append(trees)
        columns['fore_unlocked'].append(fore_unlocked)
        columns['back_unlocked'].append(back_unlocked)
        columns['aircon_ticks'].append(aircon_ticks)
        columns['refri_ticks'].append(refri_ticks)
        columns['heater_wattage'].append(heater_wattage)
        columns['water_gallons'].append(water_gallons)
        columns ['date_weekly'].append(date_weekly)
    ## reupload columns into csv file, savedata.csv 
    keys = columns.keys() 
    ## Iterate the lists (in associative list format) from defaultdict back into csv format  
    ## (represented by keys) to prepare write into savedata.csv. Fill up any blank entries with 'None'. 
    csvrows = itertools.zip_longest(*[columns[k] for k in keys], fillvalue='None') 
    with open('savedata.csv', 'w', newline ="") as file_pointer: 
        csvwriter = csv.writer(file_pointer) 
        csvwriter.writerow(keys) #write columns into csv file 
        for row in csvrows: #iterates every item within csvrows which contains the data rows. 
            csvwriter.writerow(row) 

#Accessing the main menu page    
while True:
    press_any_key()
    main_menu_input = main_menu_page() 
    if main_menu_input == "Tips": 
        saving_tips()
    elif main_menu_input == 'E': 
        print("Exiting application...")
        save_the_data()
        break
    elif main_menu_input == "Hhold":
        change_hh()
    elif main_menu_input == "User":
        change_user()
    elif main_menu_input == "Help":
        help_user()
    elif main_menu_input == "Ghse": 
        Ghse_menu_input = ghse_menu_page()
        if Ghse_menu_input.capitalize() == "Trees":
            trees = (count % 16)//4
            big_trees = count // 16
            colsel()
            print_trees(trees,big_trees)
            print(Style.RESET_ALL)
        elif Ghse_menu_input.capitalize() == "Styles":
            style_unlock()
        elif Ghse_menu_input.upper() == "E":
            continue ## Replace 'continue' with your code after you finish 
    elif main_menu_input == "Monm": 
        monm()
    elif main_menu_input == "Genm":
        if aircon_ticks != 0:
            summary_page()
        aircon_ticks = get_ticks("aircon","aircon_model_ticks.csv")
        refri_ticks = get_ticks("fridge","refri_model_ticks.csv")
        heater_wattage = heater()
        water_gallons = toilet()
    elif main_menu_input == "Wekm": 
        #weekly missions
        print ("""====================\nWelcome to weekly missions! Pass four weekly missions to grow some trees!""")
        score = 0
        if date_weekly == 0 or date_weekly == '0':
            date_weekly = datetime.today().date()
            days_passed = timedelta(0)
            first_time_user = True
        else:
            to_day = datetime.today().date()
            days_passed = to_day - date_weekly
            first_time_user = False
        if days_passed.days < 7 and first_time_user == False:
            print (f"Come back in {7-days_passed.days} more days for your next weekly missions!")
        else:
            print("====================\nPlease answer the following questions for this week:")
            questions = ['Did you turn off the lights when you are not using them? Y/N ' ,
                         'Did you turn off ceiling lights and use table lamps instead? Y/N ' ,
                         'Did you turn off running water while using the tap? Y/N ' ,
                         'Did you use the fan instead of the aircon this week? Y/N ' ,
                         'Did you unplug your unused electronics this week? Y/N ' ,
                         'Do you use natural light instead of ceiling lights during the day? Y/N ' ,
                         'Did you use a full load of laundry this week? Y/N ',
                         'Did you wash your laundry in cold? Y/N ',
                         'Do you maintain a clean and air-tight refrigerator? Y/N ' ,
                         'Do you only have a single fridge? Y/N ' ,
                         'Do you not open your fridge door often? Y/N ' ,
                         'Did you air-dry your clothes this week? Y/N ' ,
                         'Do you use traditional incandescent lights? Y/N ' ,
                         'Did you keep your showers to less than 10 mins? Y/N ' ,
                         'Did you turn off your appliances when they are not in use? Y/N ' ,
                         'Do you set your computer to sleep or hiberate when you are not using them instead of using screen saver? Y/N ' ,
                         'Did you not use the dishwasher this week? Y/N ' ,
                         'Do you use a low-flow showerhead? Y/N ' ,
                         'Do you use aerators on your faucets? Y/N ' ]
            
            rand = random.sample(questions,7)
            for i in rand:
                while True:
                    user_input = input(i)
                    if user_input.upper() == 'N':
                        break
                    elif user_input.upper() == 'Y':
                        score += 1
                        break
                    else: 
                        print ("Invalid Entry! Please enter either Y/N. ")
                        
            my_list = [heater_usage,aircon_usage,kitchen_usage,shower,washmachine_usage]
            for i in range(1):
                rand = random.choice(my_list)
                if rand == heater_usage:
                    water_heater = heater_usage()
                    if water_heater < 0.2:
                        score += 1
                        
                elif rand == aircon_usage:
                    aircon = aircon_usage()
                    if aircon < 5:
                        score += 1
                        
                elif rand == kitchen_usage:
                    kitchen_amount = kitchen_usage()
                    if kitchen_amount < 400:
                       score += 1
                       
                elif rand == shower:
                    shower_amount = shower()
                    if shower_amount < 8:
                        score += 1
                        
                elif rand == washmachine_usage: 
                    washmachine_ticks = washmachine_usage()
                    if washmachine_ticks >= 3:
                        score+=1
        
            if score > 4:
                count += 1
                print(f"====================\nYou have a score of {score}! Congratuluations on scoring higher than 4 points! You have come one step closer to your tree!")
            else:
                print(f"====================\nYou have a score of {score}! Let's score above 4 next mission!")
