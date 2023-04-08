import requests

while True:
    print("1) Add customer")
    print("2) Delete customer with id")
    print("3) Fetch all")
    print("4) Quit")

    choise = int(input())

    url = 'http://scores-shxw.onrender.com/scores'

    if choise == 1:
        customer_name = input("Enter the customer name: ")
        customer_points = int(input("Enter the customers points: "))
        myobj = {'name': customer_name, 'points': customer_points}
        x = requests.post(url, json = myobj)
        if x.status_code == 201:
            print("Customer added succesfully")
        else:
            print("Your name is already in use, please choose another.")
        #print(x.status_code)
    elif choise == 2:
        the_id=input("Give the customer id you want to delete:\n")
        d = requests.delete(f"http://scores-shxw.onrender.com/scores/{the_id}")
        if d.status_code == 204:
            print("Delete complete.")
        else:
            print(f"ID {the_id} not found")
        #print(d.status_code)
    elif choise == 3:
        r = requests.get('http://scores-shxw.onrender.com/scores')
        print(r.text)
    elif choise == 4:
        print("Bye.")
        break
    else:
        print("Give a number between 1-4:")