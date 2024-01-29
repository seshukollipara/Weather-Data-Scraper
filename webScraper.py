# web scraper
# scrapes temperatures in Darmstadt
# up to 16 days

import re
import requests
from bs4 import BeautifulSoup

# create new request for the temperature page
main_page = requests.get(
    "https://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/darmstadt/DE0001961.html")
detail_page = requests.get(
    "https://www.wetter.com/deutschland/darmstadt/DE0001961.html")
# initialize html parser from bs4
soup = BeautifulSoup(main_page.content, 'html.parser')
# parse second, detailed page
current_soup = BeautifulSoup(detail_page.content, 'html.parser')

calendar = soup.find(id="kalender")
current_overview = current_soup.find(class_=
                                     "[ pack__item one-third ph- ] [ bg--blue text--white desk-pv- relative ]"
                                     " [ lap-one-half lap-pr0 lap-pv- ] [ palm-block palm-one-whole ]")

# find all dates
dates = calendar.find_all(class_=re.compile("text--"))

# find min temps
min_temperatures = calendar.find_all(class_="temp-min")
# find max temps
max_temperatures = calendar.find_all(class_="temp-max")

# find weather state
weather_states = calendar.find_all(class_="weather-state")

date_list = []


def process_dates():
    for day in dates:
        day = str(day.get_text())
        date_list.append(day)


process_dates()

min_temp_list = []
max_temp_list = []


def process_temps():
    for temp in min_temperatures:
        temp = str(temp.get_text())
        temp = re.sub("/", "", temp)
        temp = ''.join(temp.split())
        min_temp_list.append(temp)

    for temp in max_temperatures:
        max_temp_list.append(str(temp.get_text()))


process_temps()

weather_state_list = []


def process_weather_state():
    for state in weather_states:
        state = str(state.get_text())
        state = ' '.join(state.split())
        weather_state_list.append(state)


process_weather_state()

current_temp = current_overview.find(class_="text--white beta")
current_temp = current_temp.get_text()

overview_items = current_overview.find(class_="[ pack__item desk-pt- ]")
current_state = overview_items.find(class_="text--small")
current_state = current_state.get_text()

a_time_when_calculated = current_overview.find(class_="[ currentWeather ] text--white palm-hide")
time_when_calculated = a_time_when_calculated.find(class_="text--small")
time_when_calculated = time_when_calculated.get_text()
time_when_calculated = re.sub("[A-Za-z]", "", time_when_calculated)
calc_time = ' '.join(time_when_calculated.split())

current_weather = [current_temp, current_state, calc_time]
current_weather_desc = ["Current temperature:", "Current state:", "Calculated:"]

forecast_dict = {
    'date': [],
    'min_temp': [],
    'max_temp': [],
    'weather_state': []
}


def process_forecast():
    for date in date_list:
        forecast_dict['date'].append(date)
    for min_temp in min_temp_list:
        forecast_dict['min_temp'].append(min_temp)
    for max_temp in max_temp_list:
        forecast_dict['max_temp'].append(max_temp)
    for weather_state in weather_state_list:
        forecast_dict['weather_state'].append(weather_state)

    global forecast_values
    forecast_values = zip(forecast_dict['date'], forecast_dict['min_temp'],
                          forecast_dict['max_temp'], forecast_dict['weather_state'])


process_forecast()


def print_current():
    print()
    for weather_desc, weather_value in zip(current_weather_desc, current_weather):
        print(weather_desc, weather_value)
    print()


def print_today():
    print("\nLet's see what the weather is like today on: ")
    print(date_list[0])
    print("Max temperature: " + max_temp_list[0] + "C")
    print("Min temperature: " + min_temp_list[0] + "C")
    print("State: " + weather_state_list[0])
    print()


def print_forecast():
    print("Let's see what the weather is like in Darmstadt for the next 16 days:")
    for date_value, min_temp_value, max_temp_value, weather_state_value in forecast_values:
        print("Date:", date_value, "Min temperature:", min_temp_value,
              "Max temperature:", max_temp_value, "Weather state:", weather_state_value)


user_input_done = False


def prompt_restart():
    global user_input_done
    while user_input_done is False:
        try:
            user_command = str.lower(input("Is there anything else you want to do (type 'yes' or 'no')?\n"))
            yes_or_no = ["yes", "no"]

            if user_command == "yes" in yes_or_no:
                choose_output()
                user_input_done = True
            elif user_command == "no" in yes_or_no:
                quit("\nQuitting program..")
            elif user_command not in yes_or_no:
                print("You can only type 'yes' or 'no'.")
                continue
            else:
                break
        except ValueError:
            print("Value error in code. Check if everything is right, then try again.")
            continue


def choose_output():
    commands = {
        'current': 'Prints out current temperature, weather state and the time it was calculated.',
        'today': 'Prints out the date, the minimal and maximal temperature, as well as the weather state of the day.',
        'forecast': 'Prints out a 16-day forecast with all dates and the corresponding temperatures and states.',
        'commands': 'Lists all commands currently available.',
        'help': 'The help command shows all available commands and this information you are looking at.',
        'quit': 'Does exactly what it says. It quits/terminates the program.'
    }

    global user_input_done
    while user_input_done is False:
        try:
            user_command = str.lower(input("Enter command:\n"))

            if user_command not in commands.keys():
                print("Not a valid command. Type 'commands' for a list of commands"
                      " and 'help' to get more information")
                continue

            elif user_command == "current" in commands.keys():
                print("Printing current weather data..")
                print_current()
                prompt_restart()
                user_input_done = True

            elif user_command == "today" in commands.keys():
                print("Printing weather data for today..")
                print_today()
                prompt_restart()
                user_input_done = True

            elif user_command == "commands":
                print("Available commands:")
                for command in commands.keys():
                    if command != list(commands.keys())[-1]:
                        print(command, end=", ")
                    else:
                        print(command)

            elif user_command == "forecast":
                print_forecast()
                prompt_restart()
                user_input_done = True

            elif user_command == "help":
                for command in commands.items():
                    print(command)

            elif user_command == "quit":
                quit("\nQuitting program..")

            else:
                break

        except ValueError:
            print("Value error in code. Check if everything is right, then try again.")
            continue


def starting_point():
    print("Welcome to Paddy's little weather scraper!",
          "\nThis little script pulls weather data from 'wetter.com', a german weather site."
          "\nIt's currently able to scrape the weather forecast for up to 16 days."
          "\nThe only location currently supported is 'Darmstadt, Hesse'.",
          "\nHave fun and type 'commands' for a list of commands.")
    choose_output()


if __name__ == '__main__':
    starting_point()

# TODO:
#   - Add support for other cities (might not be easily possible)
#   - implement pandas (?)
