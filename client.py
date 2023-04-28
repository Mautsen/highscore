import requests

while True:
    print("1) Add customer")
    print("2) Delete customer with id")
    print("3) Fetch all")
    print("4) Fetch scores of your choice")
    print("5) Fetch score based on ID")
    print("6) Quit")

    choice = int(input())

    url = 'http://scores-shxw.onrender.com/scores?pw=secret'

    if choice == 1:
        username = input("Enter the username: ")
        customer_points = int(input("Enter the customers points: "))
        myobj = {'name': username, 'points': customer_points}
        x = requests.post(url, json = myobj)
        if x.status_code == 200:
            print("Customer added succesfully")
        else:
            print("Your username is already in use or it is invalid, please choose another.")
        print(x.status_code)
    elif choice == 2:
        the_id=input("Give the customer id you want to delete:\n")
        d = requests.delete(f"http://scores-shxw.onrender.com/scores/{the_id}?pw=secret")
        if d.status_code == 204:
            print("Delete complete.")
        else:
            print(f"ID {the_id} not found")
        print(d.status_code)
    elif choice == 3:
        r = requests.get('http://scores-shxw.onrender.com/scores?pw=secret')
        print(r.text)
    elif choice == 4:
        sort_order = input("Sort in ascending or descending order? (asc/desc): ")
        limit = int(input("How many top scores do you want to fetch?: "))
        params = {"sort": sort_order, "limit": limit}
        r = requests.get(f"{url}?pw=secret", params=params)
        print(r.text)
    elif choice == 5:
        score_id = input("Enter the score id: ")
        r = requests.get(f"http://scores-shxw.onrender.com/scores/{score_id}?pw=secret")
        if r.status_code == 200:
            score = r.json()
            print(f"Score id: {score['id']}, Name: {score['name']}, Points: {score['points']}")
        else:
            print("Score not found.")
    elif choice == 6:
        print("Bye.")
        break
    else:
        print("Give a number between 1-6:")