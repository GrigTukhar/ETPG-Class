import athlete
import coach
import predefined


choices = ("athlete", "coach", "predefined", "exit")

def main():
    choice = "x"
    print("\nETPG® | The training schedule program for any endurance trainer and athlete")
    while (choice not in  choices) or choice !="exit":
        choice = str(input("\nGeneral Menu | Choose any of the following options (" + (", ").join(choices) + "): "))
        if (choice not in choices):
            print("Invalid input, try again")
        elif (choice == "athlete"):
            athlete.main()
        elif (choice == "coach"):
            coach.main()
        elif (choice == "predefined"):
            predefined.main()
        elif (choice =="exit"):
            print("\nThank you for using ETPG® | The training schedule program for any endurance trainer and athlete")

main()
