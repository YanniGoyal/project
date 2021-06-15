import random
no_of_people = int(input("Enter the number of friends joining (including you): \n"))
if no_of_people <= 0:
    print("No one is joining for the party")
else:
    dict = {}
    print("\nEnter the name of every friend (including you), each on a new line: ")
    for i in range(no_of_people):
        name = input()
        dict[name] = 0 
    total_bill = int(input("\nEnter the total bill value: \n")) 
    for key, value in dict.items():
        dict[key] = round(total_bill / no_of_people , 2)
    print("\nDo you want to use the \"Who is lucky?\" feature? Write Yes/No:")
    ans = input()
    if ans == "Yes":
        lucky_name = random.choice(list(dict.keys()))
        for key, value in dict.items():
            if key == lucky_name :
                dict[key] = 0
            else:
                dict[key] = round(total_bill / (no_of_people - 1) , 2)
                
        print(f"\n{lucky_name} is the lucky one!")
    else:
        print("\nNo one is going to be lucky")
    print(f"\n{dict}")