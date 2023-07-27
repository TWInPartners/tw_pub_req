import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry

recipient_dictionary = {}

template_dictionary = {
    'water list': 
    ['Public Request', 
    f'Pursuant to Article I, section 24 of the Florida Constitution, and chapter 119, F.S., I am requesting an opportunity to inspect or obtain copies of public records that indicate addresses that have had their water disconnected within the past 60 days. I would prefer that the account still be disconnected and include the name and contact number on the account. If there are any fees for searching or copying these records, please inform me before filling my request. Should you deny my request, or any part of the request, please state in writing the basis for the denial, including the exact statutory citation authorizing the denial.'],
     
    'code violation list':
    ['Public Request',
    f'Pursuant to Article I, section 24 of the Florida Constitution, and chapter 119, F.S. I am requesting an opportunity to inspect or obtain copies of public records that indicate addresses that have code violations for high grass, structural damage, and/or mold within the past 60 day. Please include the name and contact number associated with the account. If there are any fees for searching or copying these records, please inform me before filling my request. Should you deny my request, or any part of the request, please state in writing the basis for the denial, including the exact statutory citation authorizing the denial as required by s. 119.07(1)(d), F.S. I will contact your office within 24 hours to discuss when I may expect fulfillment of my request, and payment of any statutorily prescribed fees.  If you have any questions in the interim, you may contact me at 972-415-8550. Thank you Nathaniel Wilson']
}

class Select_Recipients(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # place location here
        self.pack()      

                
        # create the table
        treeview = ttk.Treeview(self, columns=('First Name', 'Organization'), show='headings')
        treeview_label = ttk.Label(self, text='Select Recipients')
        treeview.heading('First Name', text='First Name')
        treeview.heading('Organization', text='Organization')
        treeview_label.pack()
        treeview.pack(fill='both', expand=True, padx=5, pady=5)

        # Add the data to the table
        #for company, recipient_data in recipient_dictionary.items():
            #treeview.insert('', 'end', values=[recipient_data['first_name'], company])
        self.treeview = treeview

            

        # Bind the on_select() furnction to the treeview's selection event
        self.treeview.bind('<<TreeviewSelect>>', self.select_recipients)

    def select_recipients(self, event):
        # Get table from dictionary with table rows being selectable and store the data
        selected_item = self.treeview.selection()[0]
        recipient_data = recipient_dictionary[self.treeview.item(selected_item)['values'][1]]
        first_name = recipient_data['first_name']
        email = recipient_data['email']

        scrollbar_table = ttk.Scrollbar(self, orient='vertical', command=self.treeview.yview)
        scrollbar_table.place(relx=1, rely=0, relheight=1, anchor='ne')

    def update_table(self):
        # clear existing rows in the table
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Add the data to the table
        for company, recipient_data in recipient_dictionary.items():
            self.treeview.insert('', 'end', values=[recipient_data['first_name'], company])


class App(ttk.Window):
    def __init__(self):
        # setup
        super().__init__(themename='cyborg')
        self.title('Public Request')
        self.geometry('800x600')
        self.minsize(600,300)

        self.select_recipients = Select_Recipients(self)
        self.select_template = Select_Template(self)
        self.set_start = Set_Start(self)
        self.add_recipients = Add_recipients(self)

        # Bind save option to a function that saves the data
        def save_data(self):
            # Save the data to a file
            with open('data.txt', 'w') as file:
                file.write(str(recipient_dictionary))

        # Bind open option to function that opens the data file
        def open_data(self):
            # Open the data file
            global recipient_dictionary
            with open('data.txt', 'r') as file:
                recipient_dictionary = eval(file.read())

        # Bind send option to function that sends the email
        def send_email(self):
            # Send the email
            pass

        # create menu bar
        menubar = ttk.Menu(self)

        # Add a menu to the menu bar
        filemenu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)

        # Add a save option to the menu
        filemenu.add_command(label='Save', command=save_data)
        filemenu.add_command(label='Open', command=open_data)

        # Add a send option to the menu
        filemenu.add_command(label='Send', command=send_email)

        # Add the menu bar
        self.config(menu=menubar)

        # Populate the table initially
        self.update_table_data()

        # run
        self.mainloop()

    def update_table_data(self):
        # Update the table with the latest data from the recipient_dictionary
        self.select_recipients.update_table()

class Add_recipients(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # place location here
        self.app_instance = parent
        self.pack()

        self.add_recipient_first_name_string = tk.StringVar()
        self.add_recipient_last_name_string = tk.StringVar()
        self.add_recipient_organization_string = tk.StringVar()
        self.add_recipient_email_string = tk.StringVar()

        self.add_recipient_name()

    # Add the recipient to the recipient dictionary
    def add_recipient_to_dictionary(self):
        # Get the users-entered data
        first_name = self.add_recipient_first_name_string.get()
        last_name = self.add_recipient_last_name_string.get()
        organization = self.add_recipient_organization_string.get()
        email = self.add_recipient_email_string.get()

        # Create a dictionary entry using the company name as the key.
        recipient_data = {
            'first_name': self.add_recipient_first_name_string.get(),
            'last_name': self.add_recipient_last_name_string.get(),
            'organization': self.add_recipient_organization_string.get(),
            'email': self.add_recipient_email_string.get()
        }

        recipient_dictionary[organization] = recipient_data

        # After adding the recipient, update the table data
        self.app_instance.update_table_data()

        # Clear the entry fields
        self.add_recipient_first_name_string.set('')
        self.add_recipient_last_name_string.set('')
        self.add_recipient_organization_string.set('')
        self.add_recipient_email_string.set('')

    def add_recipient_name(self):

        # create widgets
        add_recipient_first_name_entry = ttk.Entry(self, textvariable=self.add_recipient_first_name_string)
        add_recipient_first_name_label = ttk.Label(self, text='First Name')
        add_recipient_last_name_entry = ttk.Entry(self, textvariable=self.add_recipient_last_name_string)
        add_recipient_last_name_label = ttk.Label(self, text='Last Name')
        add_recipient_organization_entry = ttk.Entry(self, textvariable=self.add_recipient_organization_string)
        add_recipient_organization_label = ttk.Label(self, text='Organization Name')
        add_recipient_email_entry = ttk.Entry(self, textvariable=self.add_recipient_email_string)
        add_recipient_email_label = ttk.Label(self, text='Email Address')

        # create submit button
        add_recipient_submit_button = ttk.Button(self, text='Add Recipient', command=self.add_recipient_to_dictionary)

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


        #self.update_table()
        

class Select_Template(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        #template combobox
        selection_string = tk.StringVar()
        template_selection = ttk.Combobox(self, textvariable=selection_string)
        template_selection_label = ttk.Label(self, text='Select A Template')
        template_selection_label.pack()
        template_selection['values'] = list(template_dictionary.keys())
        template_selection.bind('<<ComboboxSelected>>', template_selection)
        template_selection.pack(pady=7)

    def template_selection_callback(self, event):
        selected_template = event.widget.get()

class Set_Start(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        # create widget
        calendar = DateEntry(self)
        calendar_label = ttk.Label(self, text='Select Start Date')
        
        # layout
        calendar_label.pack()
        calendar.pack(pady=10)


App()