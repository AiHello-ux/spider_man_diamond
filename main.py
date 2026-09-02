import os

while True:
    print("\n--- MAIN MENU ---")
    print("1. Gokul-heart")
    print("2. melvin-diamond")
    print("3. pawan-club")
    print("4. spider code-spade")
    print("0. Exit")
    
    choice = input("Enter your choice (0-4): ")
    
    if choice == '1':
        os.system('python Gokul-heart.py')
        
    elif choice == '2':
        os.system('python melvin-diamond.py')
        
    elif choice == '3':
        os.system('python pawan-club.py')
        
    elif choice == '4':
        os.system('python "spider code-spade.py"')
        
    elif choice == '0':
        print("Exiting...")
        break
        
    else:
        print("Invalid choice. Please try again.")
