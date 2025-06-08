#############################################
__author__ = "Prabal Jain"  #
__LinkedIn__ = "prabaljainn"  #
__Github__ = "prabaljainn"  #

#############################################


from . import constants
from tkinter import *
import tkinter.font as tkFont
from . import selenium_Funct
import threading
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

constants.username = os.getenv("LINKEDIN_USERNAME") or "Enter Your Username"
constants.password = os.getenv("LINKEDIN_PASSWORD") or "Password please"
constants.commaseparated = os.getenv("LINKEDIN_FIELDS") or "Field1;Field2;field3"
constants.upto_page = 1


def start_automate(e1, e2, e3, e4, e5, root):
    constants.username = e1.get()
    constants.password = e2.get()
    constants.commaseparated = e3.get()
    constants.upto_page = e4.get()
    constants.location = e5.get()
    selenium_Funct.main()
    root.destroy()


def guibuild():
    root = Tk()
    root.configure(background='lightblue')

    root.geometry("660x800")
    root.title("LinkedIn Conection Bot")
    link = "https://github.com/prabaljainn/Linkedin_Connection_Bot.git"
    text = Text(root, height=1, padx=10, borderwidth=1, bg="cyan")
    text.insert(1.0, link)
    text.configure(state="normal")
    text.grid(row=0, column=0)
    text.configure(inactiveselectbackground=text.cget("selectbackground"))

    # canvas = Canvas(root, width=448, height=226)
    # canvas.grid(row=1, column=0, )
    # img = ImageTk.PhotoImage(Image.open("linkin.png"))
    # canvas.create_image(20, 20, anchor=NW, image=img)
    fontstyle = tkFont.Font(family="Ubuntu", size=22)
    labe_head = Label(root, text="LinkedIn Connection Bot", fg="blue", font=fontstyle).grid(row=1, column=0)
    labe_des = Label(root, text="A bot to Target Mass connections for Purpose", fg="blue",
                     font=fontstyle).grid(row=2,
                                          column=0)
    label_username = Label(root, text="Enter Username ").grid(row=4, column=0)
    e1 = Entry(root, width=50, borderwidth=10, bg="white", fg='black')
    e1.insert(0, constants.username)
    e1.grid(row=6, column=0, columnspan=3, padx=10, pady=7)
    label_password = Label(root, text="Enter Password").grid(row=8, column=0)
    e2 = Entry(root, show="*", width=50, borderwidth=10, bg="white", fg='black')
    e2.insert(0, constants.password)
    e2.grid(row=10, column=0, columnspan=3, padx=10, pady=7)
    label = Label(root, text="Now Below enter your intrests separated by ;").grid(row=11, column=0)
    label2 = Label(root, text="for eg. to search for TCS , Accenture and Wipro Enter: ").grid(row=12, column=0)
    label3 = Label(root, text="TCS;Accenture;Wipro").grid(row=13, column=0)
    e3 = Entry(root, width=50, borderwidth=3, bg="white", fg='black')
    e3.insert(0, constants.commaseparated)
    e3.grid(row=15, column=0, columnspan=3, padx=10, pady=7)
    
    # Add location field
    label_location = Label(root, text="Enter locations separated by semicolons (e.g., 'United States; California, United States; India')").grid(row=16, column=0)
    e5 = Entry(root, width=50, borderwidth=3, bg="white", fg='black')
    e5.insert(0, constants.location if hasattr(constants, 'location') else "")
    e5.grid(row=17, column=0, columnspan=3, padx=10, pady=7)
    
    e4 = Entry(root, width=50, borderwidth=3, bg="white", fg='black')
    labelx = Label(root, text="How many pages you want to automate, for the First time use enter 1").grid(row=18,
                                                                                                          column=0)
    e4.insert(0, constants.upto_page)
    e4.grid(row=20, column=0, columnspan=3, padx=10, pady=7)
    label_username = Label(root, text="On the Same Directory Excel File will be Exported of Connected Users").grid(
        row=22, column=0)

    buttonsubmit = Button(root, text="Start The Automation!!", fg='blue', height=5, width=40,
                          command=lambda: start_automate(e1, e2, e3, e4, e5, root)).grid(row=24,
                                                                                     columnspan=3,
                                                                                     column=0,
                                                                                     padx=10,
                                                                                     pady=7)

    link = "https://www.linkedin.com/in/prabaljainn"
    text = Text(root, height=1, padx=10, borderwidth=1, bg="cyan")
    text.insert(1.0, link)
    text.configure(state="normal")
    text.grid(row=30, column=0)
    text.configure(inactiveselectbackground=text.cget("selectbackground"))

    link = "https://github.com/prabaljainn"
    text = Text(root, height=1, padx=10, borderwidth=1, bg="cyan")
    text.insert(1.0, link)
    text.configure(state="normal")
    text.grid(row=32, column=0)
    text.configure(inactiveselectbackground=text.cget("selectbackground"))
    Button(root, text="Quit", command=root.destroy).grid(row=34)

    root.mainloop()


class LinkedInBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Connection Bot")
        self.root.geometry("600x800")
        self.root.configure(bg='#f0f0f0')

        # Create main frame
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Title
        title_label = tk.Label(main_frame, text="LinkedIn Connection Bot", font=('Helvetica', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Email Frame
        email_frame = tk.Frame(main_frame, bg='#f0f0f0')
        email_frame.pack(fill='x', pady=5)
        
        email_label = tk.Label(email_frame, text="Email:", width=10, anchor='w', bg='#f0f0f0')
        email_label.pack(side='left')
        
        self.email_entry = tk.Entry(email_frame, width=40)
        self.email_entry.pack(side='left', padx=5)

        # Password Frame
        password_frame = tk.Frame(main_frame, bg='#f0f0f0')
        password_frame.pack(fill='x', pady=5)
        
        password_label = tk.Label(password_frame, text="Password:", width=10, anchor='w', bg='#f0f0f0')
        password_label.pack(side='left')
        
        self.password_entry = tk.Entry(password_frame, width=40, show="*")
        self.password_entry.pack(side='left', padx=5)

        # Keywords Frame
        keywords_frame = tk.Frame(main_frame, bg='#f0f0f0')
        keywords_frame.pack(fill='x', pady=5)
        
        keywords_label = tk.Label(keywords_frame, text="Keywords:", width=10, anchor='w', bg='#f0f0f0')
        keywords_label.pack(side='left')
        
        self.keywords_entry = tk.Entry(keywords_frame, width=40)
        self.keywords_entry.pack(side='left', padx=5)

        # Pages Frame
        pages_frame = tk.Frame(main_frame, bg='#f0f0f0')
        pages_frame.pack(fill='x', pady=5)
        
        pages_label = tk.Label(pages_frame, text="Pages:", width=10, anchor='w', bg='#f0f0f0')
        pages_label.pack(side='left')
        
        self.pages_entry = tk.Entry(pages_frame, width=40)
        self.pages_entry.pack(side='left', padx=5)

        # Location Frame
        location_frame = tk.Frame(main_frame, bg='#f0f0f0')
        location_frame.pack(fill='x', pady=5)
        
        location_label = tk.Label(location_frame, text="Location:", width=10, anchor='w', bg='#f0f0f0')
        location_label.pack(side='left')
        
        # Create a text entry for location
        self.location_entry = tk.Entry(location_frame, width=40)
        self.location_entry.pack(side='left', padx=5)
        self.location_entry.insert(0, "United States")  # Default value

        # Add a helper label for location format
        location_help = tk.Label(main_frame, 
                               text="Enter locations separated by semicolons (e.g., 'United States; California, United States; India')", 
                               bg='#f0f0f0', fg='gray', font=('Helvetica', 8))
        location_help.pack(pady=2)

        # Connection Message Frame
        message_frame = tk.Frame(main_frame, bg='#f0f0f0')
        message_frame.pack(fill='x', pady=5)
        
        message_label = tk.Label(message_frame, text="Message:", width=10, anchor='w', bg='#f0f0f0')
        message_label.pack(side='left')
        
        self.message_text = tk.Text(message_frame, height=4, width=40)
        self.message_text.pack(side='left', padx=5)

        # Buttons Frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=20)

        # Start Button
        self.start_button = tk.Button(buttons_frame, text="Start Bot", command=self.start_bot,
                                    bg='#0077b5', fg='white', width=15, height=2)
        self.start_button.pack(side='left', padx=10)

        # Stop Button
        self.stop_button = tk.Button(buttons_frame, text="Stop Bot", command=self.stop_bot,
                                   bg='#dc3545', fg='white', width=15, height=2, state='disabled')
        self.stop_button.pack(side='left', padx=10)

        # Status Frame
        status_frame = tk.Frame(main_frame, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=10)
        
        self.status_label = tk.Label(status_frame, text="Status: Ready", bg='#f0f0f0')
        self.status_label.pack()

        # Progress Frame
        progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        progress_frame.pack(fill='x', pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x')

        # Log Frame
        log_frame = tk.Frame(main_frame, bg='#f0f0f0')
        log_frame.pack(fill='both', expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=60)
        self.log_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Initialize bot thread
        self.bot_thread = None
        self.stop_event = threading.Event()

    def update_constants(self):
        # Update constants.py with GUI values
        with open('Scripts/constants.py', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith('username ='):
                lines[i] = f'username = "{self.email_entry.get()}"\n'
            elif line.startswith('password ='):
                lines[i] = f'password = "{self.password_entry.get()}"\n'
            elif line.startswith('commaseparated ='):
                lines[i] = f'commaseparated = "{self.keywords_entry.get()}"\n'
            elif line.startswith('upto_page ='):
                lines[i] = f'upto_page = {self.pages_entry.get()}\n'
            elif line.startswith('connection_mess ='):
                lines[i] = f'connection_mess = """{self.message_text.get("1.0", tk.END).strip()}"""\n'
            elif line.startswith('location ='):
                lines[i] = f'location = "{self.location_entry.get()}"\n'

        with open('Scripts/constants.py', 'w') as file:
            file.writelines(lines)
