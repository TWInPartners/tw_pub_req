import tkinter as tk
import ttkbootstrap as ttk

recipient_dictionary = {}

class App(ttk.Window):
    def __init__(self):
        # setup
        super().__init__(themename='cyborg')
        self.title('Public Request')
        self.geometry('800x600')
        self.minsize(600,300)

        self.add_recipients = Add_recipients(self)

        # run
        self.mainloop()

class Start_Automation(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # place location here
        self.pack()

    def select_recipients(self):
        # Get table from dictionary with table rows being selectable and to

class Add_recipients(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # place location here
        self.pack()

        self.add_recipient_name()

    # Add the recipient to the recipient dictionary
    def add_recipient_to_dictionary(self):
        # Get the users-entered data
        first_name = first_name_string.get()
        last_name = last_name_string.get()
        company_name = company_name_string.get()
        email = email_string.get()

        # Create a dictionary entry using the company name as the key.
        recipient_data = {
            'first_name': first_name,
            'last_name': last_name,
            'company_name': company_name,
            'email': email
        }

        recipient_dictionary[company_name] = recipient_data

        # Clear the entry fields
        add_recipient_first_name_string.set('')
        add_recipient_last_name_string.set('')
        add_recipient_organization_string.set('')
        add_recipient_email_string.set('')

        # Print the updated recipient dictionary
        print(recipient_dictionary)

    def add_recipient_name(self):

        # create widgets
        add_recipient_first_name_string = tk.StringVar()
        add_recipient_first_name_entry = ttk.Entry(self, textvariable=add_recipient_first_name_string)
        add_recipient_first_name_label = ttk.Label(self, text='First Name')
        add_recipient_last_name_string = tk.StringVar()
        add_recipient_last_name_entry = ttk.Entry(self, textvariable=add_recipient_last_name_string)
        add_recipient_last_name_label = ttk.Label(self, text='Last Name')
        add_recipient_organization_string = tk.StringVar()
        add_recipient_organization_entry = ttk.Entry(self, textvariable=add_recipient_organization_string)
        add_recipient_organization_label = ttk.Label(self, text='Organization Name')
        add_recipient_email_string = tk.StringVar()
        add_recipient_email_entry = ttk.Entry(self, textvariable=add_recipient_email_string)
        add_recipient_email_label = ttk.Label(self, text='Email Address')

        # create submit button
        add_recipient_submit_button = ttk.Button(self, text='Submit', command=self.add_recipient_to_dictionary)

        # create grid
        self.columnconfigure((0,1), weight=1,uniform='a')
        self.rowconfigure((0,1,2,3,4), weight=1,uniform='a')

        # place widgets
        add_recipient_first_name_label.grid(column=0, row=0, padx=3, pady=3)
        add_recipient_first_name_entry.grid(column=1, row=0, padx=3, pady=3)
        add_recipient_last_name_label.grid(column=0, row=1, padx=3, pady=3)
        add_recipient_last_name_entry.grid(column=1, row=1,padx=3, pady=3)
        add_recipient_organization_label.grid(column=0, row=2, padx=3, pady=3)
        add_recipient_organization_entry.grid(column=1, row=2, padx=3, pady=3)
        add_recipient_email_label.grid(column=0, row=3, padx=3, pady=3)
        add_recipient_email_entry.grid(column=1, row=3, padx=3, pady=3)
        add_recipient_submit_button.grid(columnspan=2, row=4)

App()