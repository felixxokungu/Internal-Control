#-------
# PACKAGES
#--------

#-----------------
# Text Formatting
#------------------

import textwrap

from datetime import datetime

try:
    from colorama import Fore, Style
except ImportError:   
    class _NoColor:
        def __getattr__(self, name):
            return ""

    Fore = Style = _NoColor()

#----------------
#Anthropic API Key
#----------------

import os

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

#----------
# HEADER
#----------

def display_header():    

    import sqlite3        
    conn = sqlite3.connect("internal_control.db", isolation_level=None)
    tbl_control_framework = conn.execute("SELECT * FROM tbl_control_framework").fetchall()

    # Current date and time
    current_date_time = datetime.now()
    print()
    print('Today is ' + current_date_time.strftime("%A") + " " + current_date_time.strftime("%d") + " " + current_date_time.strftime("%B") + "," + " "+ current_date_time.strftime("%Y") + ".")
    print()

    # Framework Versions
    print(textwrap.fill(f"The effective versions of the frameworks are 1) COSO's {tbl_control_framework[0][1]} (May 2013) 2) GAO's {tbl_control_framework[1][1]} (GAO-25-107721, May 2025)"))
    print()

    # Program Description
    print(textwrap.fill("This program provides auditors with real‑world examples of internal control deficiencies and their consequences. These examples are organized by internal control component, principle, industry, and department, allowing users to select the categories most relevant to their engagement. The code pulls data from an SQLite database with the following tables a) Framework b) Component c) Principle d) Industry e) Department. Using the data from the tables and user input, the code composes a Claude AI prompt, connects to Claude AI via an API, prompts it and puts result in a text file."))
    print()
    print("-------------------------------")
    print()

#------------
# FUNCTIONS
#------------

def display_framework():

    import sqlite3        
    conn = sqlite3.connect("internal_control.db", isolation_level=None)

    # Fetch principles options from the database
    tbl_control_framework = conn.execute("SELECT * FROM tbl_control_framework").fetchall()

    print(textwrap.fill("The following two frameworks are widely recognized in the field of enterprise risk management and auditing in the United States of America:"))
    print()
    for row in tbl_control_framework:
        print(textwrap.fill(Fore.BLUE + f"{row[0]} {row[1]}" + Style.RESET_ALL))
        print(textwrap.fill(Fore.BLUE + f"{row[2]}" + Style.RESET_ALL))
        print()
    
    print(textwrap.fill("Select a framework by entering below, its corresponding number above."))
    print()

    while True:
        selected_framework = input("Select framework: ").strip()

        if selected_framework in [str(row[0]) for row in tbl_control_framework]:
            row = next(r for r in tbl_control_framework if str(r[0]) == selected_framework)
            print()
            print(textwrap.fill(Fore.GREEN + f"You have selected {row[1]} internal control framework." + Style.RESET_ALL))
            print()
            return row[1]

        print()
        print(textwrap.fill(Fore.RED + "Your selection is invalid. Please try again." + Style.RESET_ALL))
        print()

def display_component(selected_framework):

    import sqlite3
    conn = sqlite3.connect("internal_control.db", isolation_level=None)

    # Fetch only the components that belong to the selected framework
    components = [row for row in conn.execute("SELECT * FROM tbl_control_component").fetchall()
                  if row[4] == selected_framework]

    print(textwrap.fill(f"The {selected_framework} internal control framework has the following components:"))
    print()
    for row in components:
        print(textwrap.fill(Fore.BLUE + f"{row[2]} {row[1]}. {row[3]}" + Style.RESET_ALL))
        print()
    print(textwrap.fill("Select a control component by entering below, its corresponding number from above."))
    print()

    # Map the number shown on screen to its row
    choices = {str(row[2]): row for row in components}

    while True:
        selected = input("Enter the number of the selected control component: ").strip()
        print()
        if selected in choices:
            row = choices[selected]
            print(textwrap.fill(Fore.GREEN + f"You have selected {row[1]} component of the {selected_framework} internal control framework." + Style.RESET_ALL))
            print()
            return row[1]
        print(textwrap.fill(Fore.RED + "Invalid selection. Please try again." + Style.RESET_ALL))
        print()


def display_principle(selected_framework, selected_component):

    import sqlite3
    conn = sqlite3.connect("internal_control.db", isolation_level=None)

    # Fetch only the principles for the selected framework and component
    principles = [row for row in conn.execute("SELECT * FROM tbl_control_principle").fetchall()
                  if row[1] == selected_framework and row[2] == selected_component]

    print(textwrap.fill(f"The {selected_component} component of the {selected_framework} internal control framework has the following principles:"))
    print()
    for row in principles:
        print(textwrap.fill(Fore.BLUE + f"{row[3]} {row[4]}. {row[5]}" + Style.RESET_ALL))
        print()
    print(textwrap.fill("Select a control principle by entering below, its corresponding number from above."))
    print()

    # Map the principle number shown on screen to its row
    choices = {str(row[3]): row for row in principles}

    while True:
        selected = input("Enter the number of the selected control principle: ").strip()
        print()
        if selected in choices:
            row = choices[selected]
            print(textwrap.fill(Fore.GREEN + f"You have selected Principle {row[3]} of the {selected_component} component in the {selected_framework} internal control framework." + Style.RESET_ALL))
            print()
            return row[3], row[5]
        print(textwrap.fill(Fore.RED + "Invalid selection. Please try again." + Style.RESET_ALL))
        print()
    
def display_industry():

    import sqlite3
    import textwrap
    from colorama import Fore, Style

    conn = sqlite3.connect("internal_control.db", isolation_level=None)

    # Fetch industry options from the database
    tbl_control_industry = conn.execute("SELECT * FROM tbl_control_industry").fetchall()

    print(textwrap.fill("The following industries are available:"))
    print()

    # ---------- FIXED-WIDTH MULTI-COLUMN DISPLAY ----------
    col_width = 35     # width of each column
    cols = 2           # number of columns to display

    for i in range(0, len(tbl_control_industry), cols):
        row = tbl_control_industry[i:i+cols]
        formatted = ""

        for r in row:
            entry = f"{r[0]}. {r[1]}"
            formatted += f"{Fore.BLUE}{entry:<{col_width}}{Style.RESET_ALL}"

        print(formatted)
        print()
    # ------------------------------------------------------

    print(textwrap.fill("Select an industry by entering below, its corresponding number from above."))
    print()

    while True:
        selected_industry = input("Enter the number of the selected industry: ")
        print()

        if selected_industry not in [str(row[0]) for row in tbl_control_industry]:
            print(textwrap.fill(Fore.RED + f"Invalid selection. Please try again." + Style.RESET_ALL))
            print()
            exit()
        else:
            index = int(selected_industry) - 1
            print(textwrap.fill(Fore.GREEN + f"You have selected {tbl_control_industry[index][1]} industry." + Style.RESET_ALL))
            print()
            return tbl_control_industry[index][1]

def display_department():

    import sqlite3
    import textwrap
    from colorama import Fore, Style

    conn = sqlite3.connect("internal_control.db", isolation_level=None)

    # Fetch department options from the database
    tbl_control_department = conn.execute("SELECT * FROM tbl_control_department").fetchall()

    print(textwrap.fill("The following departments are available:"))
    print()

    # ---------- FIXED-WIDTH MULTI-COLUMN DISPLAY ----------
    col_width = 35     # width of each column
    cols = 2           # number of columns to display

    for i in range(0, len(tbl_control_department), cols):
        row = tbl_control_department[i:i+cols]
        formatted = ""

        for r in row:
            entry = f"{r[0]}. {r[1]}"
            formatted += f"{Fore.BLUE}{entry:<{col_width}}{Style.RESET_ALL}"

        print(formatted)
        print()
    # ------------------------------------------------------

    print(textwrap.fill("Select a department by entering below, its corresponding number from above."))
    print()

    while True:
        selected_department = input("Enter the number of the selected department: ")
        print()

        if selected_department not in [str(row[0]) for row in tbl_control_department]:
            print(textwrap.fill(Fore.RED + f"Invalid selection. Please try again." + Style.RESET_ALL))
            print()
            exit()
        else:
            index = int(selected_department) - 1
            print(textwrap.fill(Fore.GREEN + f"You have selected {tbl_control_department[index][1]} department." + Style.RESET_ALL))
            print()
            return tbl_control_department[index][1]
    
def compose_prompt(selected_framework, selected_component, selected_principle, selected_industry, selected_department, selected_principle_description):
    prompt = (f"I am a performance auditor. I am assessing internal control for an entity in the {selected_industry} industry, specifically within the {selected_department} department, using the {selected_framework} internal control framework, focusing on the {selected_component} component and Principle {selected_principle} - {selected_principle_description} Give me real life examples over the past 20 years in the US of when an entity's internal control related to this principle failed or succeeded.")

    print(textwrap.fill("The following prompt will be inserted into Claude AI:"))
    print()
    print(textwrap.fill(f"{Fore.BLUE}{prompt}{Style.RESET_ALL}"))
    print()
    return prompt

def insert_prompt_Claude(prompt):
    print(textwrap.fill(Fore.GREEN + "One moment. Communicating with Claude AI..." + Style.RESET_ALL))
    print()

def deploy_prompt_Claude(prompt):
    AI_Prompt = prompt

    load_dotenv()  # Load environment variables from .env file

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": AI_Prompt}],
    )
   
    with open("prompt_results.txt", "w", encoding = "utf-8") as f:
        f.write(message.content[0].text)
    print(Fore.BLUE + "Write complete. See prompt_results.txt file.")
    print(Fore.WHITE)

#--------
# MAIN
#--------
display_header()
selected_framework = display_framework()
selected_component = display_component(selected_framework)
selected_principle, selected_principle_description = display_principle(selected_framework, selected_component)
selected_industry = display_industry()
selected_department = display_department()
prompt = compose_prompt(selected_framework, selected_component, selected_principle, selected_industry, selected_department, selected_principle_description)
insert_prompt_Claude(prompt)
deploy_prompt_Claude(prompt)



