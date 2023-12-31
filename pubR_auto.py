import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry

#Load recipient data from a JSON file (if it exists)
try:
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as file:
            json.dump({}, file)

    with open('data.json', 'r') as file:
        recipient_dictionary = json.load(file)
except FileExistsError:
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
        self.app_instance = parent
        # place location here
        self.pack()      
        self.treeview = self.create_treeview()
        self.treeview.bind('<<TreeviewSelect>>', self.select_recipients)
        self.create_remove_button()
                
    def create_treeview(self):
        treeview_label = ttk.Label(self, text='Select Recipients')
        treeview_label.pack()

        # create the table
        self.treeview = ttk.Treeview(self, columns=('First Name', 'Organization'), show='headings')
        self.treeview.heading('First Name', text='First Name', anchor=tk.W)
        self.treeview.heading('Organization', text='Organization', anchor=tk.W)
        self.treeview.pack(fill='both', expand=True, padx=5, pady=5)

        self.scrollbar_table = ttk.Scrollbar(self, orient='vertical', command=self.treeview.yview)
        self.scrollbar_table.place(relx=1, rely=0, relheight=1, anchor='ne')

        self.treeview.config(yscrollcommand=self.scrollbar_table.set)
        self.treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)

        return self.treeview
    
    def select_recipients(self, event):
        try:
            # Get table from dictionary with table rows being selectable and store the data
            selected_item = self.treeview.selection()[0]
            recipient_data = recipient_dictionary[self.treeview.item(selected_item)['values'][1]]
            first_name = recipient_data['first_name']
            email = recipient_data['email']

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while selecting recipients: {e}')

    def update_table(self):
        # clear existing rows in the table
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Add the data to the table
        for company, recipient_data in recipient_dictionary.items():
            self.treeview.insert('', 'end', values=[recipient_data['first_name'], company])

    def create_remove_button(self):
        self.remove_button = ttk.Button(self, text='Remove Recipient', command=self.remove_recipient)
        self.remove_button.pack()

    def remove_recipient(self):
        try:
            selected_item = self.treeview.selection[0]
            organization_name = self.treeview.item(selected_item)['values'][1]

            # confirm removal
            result = messagebox.askquestion('Remove Recipient', f'Are you sure you want to remove {organization_name}?', icon='warning')
            if result == 'no':
                return
            
            # remove from treeview
            self.treeview.delete(selected_item)

            # remove from dictionary
            del recipient_dictionary[organization_name]

            # update the JSON file
            self.update_json_file()

        except IndexError:
            messagebox.showwarning('No Selection', 'No recipient selected to remove.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occured when removing the recipient: {e}')

    def update_json_file(self):
        try:
            with open('data.json', 'w') as file:
                json.dump(recipient_dictionary, file)
        except IOError as e:
            messagebox.showerror('Error', f'An error occurred while saving the data to the JSON file: {e}')

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

    # Add the recipient to the recipient dictionary
    def add_recipient_to_dictionary(self):
        try:
            # Get the users-entered data
            first_name = self.add_recipient_first_name_string.get()
            last_name = self.add_recipient_last_name_string.get()
            organization = self.add_recipient_organization_string.get()
            email = self.add_recipient_email_string.get()

            if not all([first_name, last_name, organization, email]):
                messagebox.showwarning('Warning','All fields must be filled out.')
                return

            # Create a dictionary entry using the company name as the key.
            recipient_data = {
                'first_name': self.add_recipient_first_name_string.get(),
                'last_name': self.add_recipient_last_name_string.get(),
                'organization': self.add_recipient_organization_string.get(),
                'email': self.add_recipient_email_string.get()
            }

            # check if orginization is the same messagebox popup
            if organization in recipient_dictionary:
                result = messagebox.askquestion('Duplicate Organization', 'An entry with this organization name already exists. Do you want to overwrite it?', icon='warning')
                if result == 'no':
                    return

            recipient_dictionary[organization] = recipient_data

            # After adding the recipient, update the table data
            self.app_instance.update_table_data()

            # Clear the entry fields
            self.add_recipient_first_name_string.set('')
            self.add_recipient_last_name_string.set('')
            self.add_recipient_organization_string.set('')
            self.add_recipient_email_string.set('')

        except ValueError as e:
                messagebox.showerror('Error', f'An error occurred while adding the recipient: {e}')

    def update_json_file(self):
        try:
            with open('data.json', 'w') as file:
                json.dump(recipient_dictionary, file)
        except IOError as e:
            messagebox.showerror('Error', f'An error occurred while saving the data to the JSON file: {e}')

class Select_Template(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.create_template_selection()

    def create_template_selection(self):
        #template combobox
        selection_string = tk.StringVar()
        template_selection = ttk.Combobox(self, textvariable=selection_string)
        template_selection_label = ttk.Label(self, text='Select A Template')
        template_selection_label.pack()
        template_selection['values'] = list(template_dictionary.keys())
        template_selection.bind('<<ComboboxSelected>>', self.template_selection_callback)
        template_selection.pack(pady=7)

    def template_selection_callback(self, event):
        try:
            selected_template = event.widget.get()
            if not selected_template:
                messagebox.showerror('Error', 'You must select a template.')
                return
            
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while selecting the template: {e}')   

class Set_Start(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.create_calendar()

    def create_calendar(self):
        # create widget
        calendar = DateEntry(self)
        calendar_label = ttk.Label(self, text='Select Start Date')
        
        # layout
        calendar_label.pack()
        calendar.pack(pady=10)

class App(ttk.Window):
    def __init__(self):
        # setup
        super().__init__(themename='cyborg')
        self.title('Public Request')
        self.geometry('800x600')
        self.minsize(600,300)

        self.setup_menu()

        self.select_recipients = Select_Recipients(self)
        self.select_template = Select_Template(self)
        self.set_start = Set_Start(self)
        self.add_recipients = Add_recipients(self)

        # Populate the table initially
        self.update_table_data()

        # run
        self.mainloop()

    def setup_menu(self):
        # create menu bar
        menubar = ttk.Menu(self)
        # Add the menu bar
        self.config(menu=menubar)
        self.create_menu_bar(menubar)

    def create_menu_bar(self, menubar):
        # Add a menu to the menu bar
        filemenu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        # Add a save option to the menu
        filemenu.add_command(label='Save', command=self.save_data)
        filemenu.add_command(label='Open', command=self.open_data)
        filemenu.add_command(label='Send', command=self.send_email)

        # add a separator
        filemenu.add_separator()

        # add a 'close' option
        filemenu.add_command(label='Close', command=self.close_app)

        self.config(menu=menubar)

        # edit menu
        editmenu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label='Edit Recipient', command=self.edit_recipient)

    def show_edit_dialog(self, recipient_data):
        # create new top-level window
        edit_window = tk.Toplevel(self)
        edit_window.title('Edit Recipient')
        edit_window.geometry('300x300')

        # temporary variables to hold the new values
        new_first_name = tk.StringVar(value=recipient_data['first_name'])
        new_last_name = tk.StringVar(value=recipient_data['last_name'])
        new_email = tk.StringVar(value=recipient_data['email'])

        # create and place widgets
        ttk.Label(edit_window, text='First Name').grid(row=0, column=0)
        ttk.Entry(edit_window, textvariable=new_first_name).grid(row=0, column=1)

        ttk.Label(edit_window, text='Last Name').grid(row=1, column=0)
        ttk.Entry(edit_window, textvariable=new_last_name).grid(row=1, column=1)

        ttk.Label(edit_window, text='Email').grid(row=2, column=0)
        ttk.Entry(edit_window, textvariable=new_email).grid(row=2, column=1)

        # create a submit buttom
        ttk.Button(edit_window, text='Submit', command=lambda: self.update_recipient(recipient_data['organization'], new_first_name.get(), new_last_name.get(), new_email.get(), edit_window)).grid(row=3, columnspan=2)
    
    def update_recipient(self, organization, new_first_name, new_last_name, new_email, edit_window):
        # update the data
        recipient_dictionary[organization]['first_name'] = new_first_name
        recipient_dictionary[organization]['last_name'] = new_last_name
        recipient_dictionary[organization]['email'] = new_email

        # update JSON file
        self.save_data()

        # update the table
        self.update_table_data()

        # close the edit window
        edit_window.destroy()

    def edit_recipient(self):
        try:
            selected_item = self.select_recipients.treeview.selection()[0]
            organization_name = self.select_recipients.treeview.item(selected_item)['values'][1]
            recipient_data = recipient_dictionary[organization_name]

            # show edit dialog
            self.show_edit_dialog(recipient_data)

        except IndexError:
            messagebox.showwarning('No Selection', 'No recipient selected to edit.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred when editing the recipient: {e}')

    def save_data(self):
        try:
            # Save the data to a file
            with open('data.json', 'w') as file:
                json.dump(recipient_dictionary, file)
        except IOError as e:
            self.show_error('Error', f'An error occurred while saving data: {e}')
        
    def open_data(self):
        try:
            # Check if the file exists before attempting to open
            if not os.path.exists('data.json'):
                self.show_error('Error', 'The data file does not exist.')
                return
            
            # Open and read the JSON data file
            global recipient_dictionary
            with open('data.json', 'r') as file:
                recipient_dictionary.update(json.load(file))
        except FileNotFoundError:
            self.show_error('Error', 'The data file does not exist.')
        except json.JSONDecodeError as e:
            self.show_error('Error', f'An error occurred while opening data: {e}')

    def send_email(self):
        try:
            # Send the email
            pass
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while sending the email: {e}')
        # Add a send option to the menu

    def update_table_data(self):
        # Update the table with the latest data from the recipient_dictionary
        self.select_recipients.update_table()

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def close_app(self):
        user_response = messagebox.askyesnocancel('Save changes', 'Do you want to save changes before closing?')

        # cancel was clicked; do not close the app
        if user_response is None:
            return
        
        # Yes was clicked; Ask wether to overwite current file
        elif user_response is True:
            
            #Logic for saving data
            save_option = messagebox.askyesno('Save Data', 'Do you want to overwrite the existing data file?')
            filename = 'data.json'

            # overwrite current file
            if save_option is True:
                pass
            else:
                # ask for a new filename
                filename = simpledialog.askstring('Input', 'Enter the new filename:')
                # cancel was clicked in the filename dialog; do not close the app
                if filename is None:
                    return
                # append .json if not present
                filename = f'{filename}.json' if not filename.endswith('.json') else filename

        # close the app
        self.quit()

if __name__ == '__main__':
    App()