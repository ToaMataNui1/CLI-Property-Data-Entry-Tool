import pandas as pd
from typing import TypedDict, List
from datetime import date


print("CLI Property Data Entry and Storage Tool")
key = input("Press any key to continue, x to exit.")

class DataDict(TypedDict):
    entry_id: List[int]
    address: List[str]
    city: List[str]
    state: List[str]
    zip: List[int]
    propertyType: List[str]
    bedQty: List[int]
    bathQty: List[int]
    sqft: List[float]
    yearBuilt: List[int]
    lastSalePrice: List[float]
    lastSaleDate: List[date]

data: DataDict = {
        "entry_id":[],
        "address":[],
        "city":[],
        "state":[],
        "zip":[],
        "propertyType":[],
        "bedQty": [],
        "bathQty": [],
        "sqft": [],
        "yearBuilt":[],
        "lastSalePrice":[],
        "lastSaleDate":[],
    }

expected_types = {
        "entry_id": int,
        "address": str,
        "city": str,
        "state": str,
        "zip": int,
        "propertyType": str,
        "bedQty": int,
        "bathQty": int,
        "sqft": float,
        "yearBuilt": int,
        "lastSalePrice": float,
        "lastSaleDate": date
    }

df = pd.DataFrame(data)

def create():
    global df
    if not df.empty:
        counter = max(data['entry_id'], default=int(df.iloc[-1]['entry_id'])) + 1
    else:
        counter = max(data["entry_id"], default=0) + 1
    entryQty = input("How many entries do you want to enter?")

    for i in range(int(entryQty)):
        print(f"Begin entering data here for entry {i+1}:")
        for key in data.keys():
            if key == "entry_id":
                data["entry_id"].append(counter)
                counter += 1
                continue
            while True:
                res = input(f"Enter {key}: ")
                expected_type = expected_types[key]
                try:
                    if expected_type == date:
                        parsed = date.fromisoformat(res)
                    else:
                        parsed = expected_type(res)
                    data[key].append(parsed)
                    break
                except Exception as e:
                    print(f"Invalid input. Expected {expected_type.__name__}. Try again.")
        res = input("To save the data, enter s. Any other key to return to the menu: ")
        if res != "s":
            break
        else:
            print("Saving...")
            new_rows = pd.DataFrame(data)
            df = pd.concat([df, new_rows], ignore_index=True)

            for key in data:
                data[key] = []
            print("Data saved successfully.")

def read():
    global df
    res = input("Enter the id of the entry you want to access (type 'all' to read all entries): ")
    try:
        if res == "all":
            if not df.empty:
                print(df.to_string())
            else:
                print("No entries found.")
            return  # prevent further execution
        else:
            if df.empty:
                print("No entries found.")
                return
            res_id = int(res)
            result = df[df['entry_id'] == res_id]
            if not result.empty:
                print(result.to_string())
            else:
                print("No entry with that id found.")
    except ValueError:
        print("Please enter a valid id.")

def update():
    global df
    try:
        entry_id = int(input("ID of entry to update: "))
        index_list = df.index[df['entry_id'] == entry_id].tolist()
        if not index_list:
            print("Entry not found.")
            return
        index = index_list[0]
        field = input(f"Field to update ({', '.join(df.columns)}): ")
        if field not in df.columns:
            print("Invalid field.")
            return
        new_value = input("New value: ")
        if df[field].dtype == int:
            new_value = int(new_value)
        df.at[index, field] = new_value
        print("Entry updated.")
    except ValueError:
        print("Invalid input.")

def delete():
    global df
    try:
        entry_id = int(input("ID of entry to delete: "))
        index_list = df.index[df['entry_id'] == entry_id].tolist()
        if not index_list:
            print("Entry not found.")
            return
        df.drop(index_list[0], inplace=True)
        df.reset_index(drop=True, inplace=True)
        print("Entry deleted.")
    except ValueError:
        print("Invalid input.")


def exitProgram():
    res = input("Do you wish to save your data? (y/n)")
    if res == "y":
        try:
            print("Saving...")
            df.to_csv("property_data.csv", index=False)
            print("Saved successfully.")
        except FileNotFoundError:
            print("Failed to save.")
        exit()
    elif res == "n":
        exit()

def menu():
    while True:
        print("Options:")
        option = input(
            "Create a new entry(c)\nRead an entry(r)\nUpdate an existing entry(u)\nDelete an existing entry(d)\nExit(x)")
        if option == "c":
            create()
        elif option == "r":
            read()
        elif option == "u":
            update()
        elif option == "d":
            delete()
        elif option == "x":
            exitProgram()

if key == "x":
    exit()
else:
    res = input("Load previous instance? (y/n)")
    if res == "y":
        file_path = 'property_data.csv'
        df = pd.read_csv(file_path)
        menu()
    else:
        menu()

