class DailyActivitiesCmd:
    # use tuple to store the days of the week and use this to construct the dictionary
    daysOfWeek = ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY")
    activites_dict = {} # initialize empty dict.
    activities = ['Exercise\nShower\n[Eat]',
                  'Exercise\nShower\n[Gardening]',
                  'Exercise\nShower\n[Read Online News]',
                  'Exercise\nShower\n[Trash Disposal]',
                  'Exercise\nShower\n[Organise days activities]',
                  'Exercise\nShower\n[Get grocery]',
                  'Exercise\nShower\n[Play with children]'] #list which is used to contruct the dictionary
	#construct the dictionary. The logic is resused from the GUI format. Else we can get rid of list etc and use dictionary alone.
    #besides here I demostrate use of for loops.
    for x in daysOfWeek:
            act = activities[0]
            activites_dict[x] = act
            activities.remove(act)
	#init method called by default in a class
    def __init__(self):
		#looped until exit criteria is met
        while True:
            print("**************************************************************")
            print("Enter the day of the week to check your activities.")
            print("Options::: Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday")
            print("Press Enter to quit")
            print("**************************************************************")
            i = input(":")

            if not i:
                print("***************************************")
                print("YOU HAVE EXITED THE PROGRAM")
                print("***************************************")
                break
            elif i.upper() not in self.daysOfWeek: #user input converted into uppercase before checking to make checking ignorecase
                print("****************")
                print("Check your input!")
                print("****************")
            else:
                print("Your activities for "+i+" are:")
                print(self.activites_dict.get(i.upper()))
           
app = DailyActivitiesCmd()
