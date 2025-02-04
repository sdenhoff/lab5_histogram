"""
    Program to analyze population and housing data
"""

import os
import platform
import sys
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError as e:
    print(f"You do not seem to have {e.name} installed.")
    print("Install it and come back")
    sys.exit(1)
try:
    import numpy as np
except ModuleNotFoundError as e:
    print(f"You do not seem to have {e.name} installed.")
    print("Install it and come back")
    sys.exit(1)
try:
    import pandas as pd
except ModuleNotFoundError as e:
    print(f"You do not seem to have {e.name} installed.")
    print("Install it and come back")
    sys.exit(1)

helper_dict = [
    {
        "filename": "Housing.csv",
        "data_wanted": "Housing Data",
        "data": [
		{
			"column": "AGE",
            "title": "Ages of Houses",
            "xaxis": "Years Old",
            "yaxis": "Count of Each"
        },
        {
            "column": "BEDRMS",
            "title": "Bedrooms Count",
            "xaxis": "Nmbr of Bedrooms",
            "yaxis": "Count of Each"
        },
        {
            "column": "ROOMS",
            "title": "Number of Rooms",
            "xaxis": "Number of Rooms",
            "yaxis": "Count of Each"
        },
        {
            "column": "UTILITY",
            "title": "Utility Square Feet",
            "xaxis": "Utility Sq Fr",
            "yaxis": "Count of Each"
        }]
    },
    {
        "filename": "PopChange.csv",
        "data_wanted": "Population Data",
        "data": [
		{
            "column": "Pop Apr 1",
            "title": "Population in April",
            "xaxis": "apr pop",
            "yaxis": "Count of Each"
        },
        {
            "column": "Pop Jul 1",
            "title": "Population in July",
            "xaxis": "jul pop",
            "yaxis": "Count of Each"
        },
        {
            "column": "Change Pop",
            "title": "Population changes between April and July",
            "xaxis": "apr pop",
            "yaxis": "Count of each delta"
        }]
    }
]

# Helper functions
def clear_screen():
    """ 
    Function to clear the screen
    did not want to use the curses module 
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def any_key():
    """ The any key function """
    input("Press enter to continue")

def choice_question():
    """ Commonly used question to determine if the user approved of the choice """
    while True:
        user_choice = str(input("Enter Y for yes and N for no: "))
        if user_choice.lower() == "y":
            return True
        if user_choice.lower() == "n":
            return False

def continue_question():
    """ Commonly used question to determine if the user wanted to continue """
    print("Would you like to continue?")
    if choice_question():
        return True
    return False

def positive_check(*args):
    """ Check that the numbers are positive """
    for num in args:
        if num <= 0:
            return False
    return True

def name_test(string):
    """ Test for only name characters """
    other_chars = ["-", "'", " "]
    for letter in string:
        if not letter.islower() and letter not in other_chars:
            return False
    return True

class DisplayData:
    """ Class to work with and display data """
    def __init__(self, data_frame, data_dict):
        """ Class Initiation """
        self.data_frame = data_frame
        self.count = self.extract_count()
        self.mean = self.extract_mean()
        self.stddev = self.extract_std_dev()
        self.min, self.max = self.extract_min_max()
        self.data_struct = data_dict

    def extract_count(self):
        """ 
        Return:
            datafr.count = Count number of non-NA/null observations
        """
        df_count = self.data_frame.count()
        return df_count

    def extract_mean(self):
        """ 
        Return:
            datafr.mean = Mean of the values
        """
        df_mean = self.data_frame.mean().round(4)
        return df_mean

    def extract_std_dev(self):
        """ 
        Return:
            datafr.std = Standard deviation of the observations
        """
        df_std_dev = self.data_frame.std().round(4)
        return df_std_dev

    def extract_min_max(self):
        """ 
        Return:
            datafr.min = Minimum of the values in the object
            datafr.mean = Mean of the values
        """
        df_min = self.data_frame.min()
        df_max = self.data_frame.max()
        return df_min, df_max

    def print_data(self):
        """ Print Data to screen """
        print(f"You selected {self.data_struct['column']}\nThe statistics for this column are:")
        print(f"{'Count':<23} {'Mean':<23} {'Std Dev':<23} {'Min':<23} {'Max':<23}")
        print(f"{self.count:<23} {self.mean:<23} {self.stddev:<23,} {self.min:<23} {self.max:<23}")

    def display_histogram(self, bins_choice="auto"):
        """ Display Histogram """
        plt.close()
        plt.hist(self.data_frame, bins=bins_choice, edgecolor='red')
        plt.title(self.data_struct['title'])
        plt.xlabel(self.data_struct['xaxis'])
        plt.ylabel(self.data_struct['yaxis'])
        plt.show()
        plt.clf()

    def calculate_bins(self, choice):
        """ Possibly Calculate bins based on different theories """
        # Sturges' Rule:
        if choice == 1:
            bins = int(np.ceil(np.log2(len(self.data_frame)) + 1))
            return bins
        # Square Root Rule:
        if choice == 2:
            bins = int(np.ceil(np.sqrt(len(self.data_frame))))
            return bins
        # Freedman-Diaconis Rule:
        if choice == 3:
            iqr = np.percentile(self.data_frame, 75) - np.percentile(self.data_frame, 25)
            bins = int(np.ceil(2 * iqr / (len(self.data_frame) ** (1/3))))
            return bins
        return False

def read_data(filename):
    """ Read from the file """
    try:
        data_frame = pd.read_csv(filename)
    except FileNotFoundError as e:
        print(f"The {e.filename} file seems to be missing, please try again")
        any_key()
        sys.exit(1)
    return data_frame

def main_menu():
    """ Main menu - to decide the dataset to use """
    file_data = []
    file_data = helper_dict.copy()
    for number, item in enumerate(file_data):
        if not os.path.isfile(item['filename']):
            file_data.pop(number)
    file_data.append({'data_wanted' : 'Exit Program'})
    print("Welcome to the Python Data Analysis App")
    print("Select the file you want to analyze:")
    while True:
        try:
            for num, item in enumerate(file_data):
                print(f"{num+1} {item['data_wanted']}")
            choice = int(input("Please make a selection: "))
        except ValueError:
            print("Please pick a number from the choices.")
            any_key()
            continue
        if choice == len(file_data):
            return False
        if choice > len(file_data):
            print("Please pick a number from the choices.")
            any_key()
            continue
        file_data.pop()
        return file_data[choice-1]

def sub_menu(main_choice):
    """ Secondary menu """
    ## Check to see if there is an exit option
    #exit_option = False
    #for exit_item in main_choice['data']:
    #    if exit_item['title'] == 'Exit Column':
    #        exit_option = True
    ## If no exit option - put one in
    #if not exit_option:
    main_choice['data'].append({'title' : 'Exit Column'})
    print(f"You have entered {main_choice['data_wanted']}")
    while True:
        try:
            for num, item in enumerate(main_choice['data']):
                print(f"{num+1} {item['title']}")
            sub_choice = int(input("Select the column you want to analyze: "))
        except ValueError:
            print("You picked something strange. Please pick a number from the choices.")
            any_key()
            continue
        if sub_choice > len(main_choice['data']):
            print("Please pick a number from the choices.")
            any_key()
            continue
        if sub_choice == len(main_choice['data']):
            return False
        return main_choice['data'][sub_choice-1]

def main():
    """ Main function """
    while True:
        clear_screen()
        menu_choice = main_menu()
        # Population Data
        if not menu_choice:
            print('Thanks for using the Data Analysis App')
            break
        full_data_frame = read_data(menu_choice['filename'])
        data_choice = sub_menu(menu_choice)
        if not data_choice:
            continue
        # data_frame, data_dict
        output = DisplayData(full_data_frame[data_choice['column']], data_choice)
        #for i in [1, 2, 3]:
        #    bins_value = output.calculate_bins(i)
        #    output.print_data()
        #    output.display_histogram(bins_choice=bins_value)
        output.print_data()
        output.display_histogram()
        any_key()


if __name__ == "__main__":
    main()
