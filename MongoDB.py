import pymongo
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

mongo = pymongo.MongoClient("mongodb+srv://kalil:0204@kalilur2713.poem5n1.mongodb.net/?retryWrites=true&w=majority")

myDB = mongo['D44_08-oct-2022']
collections = myDB['Phonebook_task']

print('''
********** Kalil's Phonebook directory ************
Create contact , Enter : 1
Search contact , Enter : 2
Update contact , Enter : 3
Delete contact , Enter : 4''')

enter_number = int(input('Enter Number : '))

if (enter_number >= 1 and enter_number <= 4):


    if enter_number == 1:
        def create_contact():
            print(f'You entered number : {enter_number}, for creating contact')

            name = input('Enter contact name : ')
            number = int(input('Enter Phone number : '))

            mail_id = input('Enter mail ID (Eg. test@gmail.com) : ')

            #collections.drop()
            records = {
                '_id': name,
                'phone_number': number,
                'Mail_ID': mail_id}

            for checkrecord in collections.find({'_id' : name}):
                if checkrecord['_id'] == records['_id']:
                    print(f'\'{name}\' is already existed in PB directory, Contact name must be unique')
                    pass
                    break

            else:

                check_number = str(number)
                check_mail = mail_id

                validate_number = re.fullmatch('(0|91)?[6-9][0-9]{9}', check_number)
                validat_mailid = re.fullmatch('^[a-zA-Z0-9_]+@[a-zA-Z)-9]+\.[a-z]{1,3}$', check_mail)
                if validate_number != None:
                    if validat_mailid != None:

                        data = collections.insert_one(records)
                        for a in collections.find({'_id': name}):
                            print(f'Contact \'{name}\' is created')

                        def phonebook_list():
                            list_of_contacts = collections.find()
                            list_of_contacts = pd.DataFrame(list_of_contacts)
                            print(list_of_contacts)

                        phonebook_list()
                    else:
                        print('Enter valid Mail ID as mentioned')

                else:
                    print('Enter valid Mobile number')


        create_contact()

    elif enter_number == 2:
        def search_contact():
            print(f'You entered number : {enter_number}, for searching contact')

            name = input('Enter contact name : ')

            query = {'_id' : name}
            for find_contact in collections.find(query):
                #print(find_contact)
                if find_contact['_id'] in name:
                    show_contact = collections.find_one(query)
                    print(show_contact)
                    break

            else:
                print(f'Please enter exact contact name, It is not exist in phone directory : {name}')

        search_contact()

    elif enter_number == 3:
        def update_contact():
            print(f'You entered number : {enter_number}, for Updating contact')

            name = input('Enter contact name : ')
            number = int(input('Enter Phone number : '))

            update_one_contact = {'_id' : name}
            update_phone_number = {'$set' : {'phone_number' : number}}

            updated_contact = collections.update_one(update_one_contact, update_phone_number)

            for i in collections.find(update_one_contact):
                a = i['phone_number']
                print(f'Existing contact , {name}  Contact\'s phone number is updated to : {a}')

        update_contact()

    elif enter_number == 4:
        def delete_contact():
            print(f'You entered number : {enter_number}, for Deleting contact')

            name = input('Enter contact name to delete : ')
            delete_one_contact = {'_id' : name}

            print(f'You chose to delete, {name} contact')

            # create the root window
            root = tk.Tk()
            root.title('Select Delect contact for confirmation')
            root.geometry('300x250')

            # click event handler
            def confirm():
                answer = askyesno(title='confirmation',
                                  message=f'Are you sure that you want to delete \'{name}\' contact?')
                if answer:
                    root.destroy()
                    deleted_contact = collections.delete_one(delete_one_contact)
                    print(f'{deleted_contact.deleted_count}, Contact is deleted : {name}')
                else:
                    print(f'You selected \'No\' - deleting {name} contact')
                    #root.withdraw()


            ttk.Button(
                root,
                text=f'Delete \'{name}\' contact',
                command=confirm).pack(expand=True)

            # start the app
            root.mainloop()

        delete_contact()

else:
    print(f'Enter the number from 1 to 4, but the entered number is {enter_number}....Sorryy please try it again!!!')








