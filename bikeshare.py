import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['all', 'January', 'February', 'March', 'April', 'May', 'June']
days = ['all', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Welcome to the Bikeshare Data Exploration System by Shaunna (BDESS)!')

    # get user input for city (chicago, new york city, washington).

    user_input = " "
    month = "all"
    day = "all"

    city = input("Enter a city: Chicago, New York City, or Washington:\n").lower()
    while city not in cities:
        city = input("Please enter a valid city: Chicago, New York, or Washington.\n").lower()

    # get user input for month (all, january, february, ... , june)

    user_input = input("You can filter the data by month, day, both, or not at all (type 'all' for this option).\n").lower()

    if user_input == "month" or user_input == "both":
        month = input("Enter a month: January, February, March, April, May, or June:\n").title()
        while month not in months:
            month = input("Please enter one of the months that data is currently available for.\n").title()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    if user_input == "day" or user_input == "both":
        day = input("Enter a day: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday:\n").title()
        while day not in days:
            day = input("Please enter a valid day.\n").title()

    print('-'*50)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create he new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nBDESS is calculating the most frequent travel times...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]

    print('Most common month travelled:', common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]

    print('Most common day of week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nBDESS is calculating the most popular stations and trips...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print('Most common start station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print('Most common end station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_station_combination = (df['Start Station'] + " "  + df['End Station']).mode()[0]

    print('Most frequent combination of start station and end station trip: ', frequent_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nBDESS is calculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print("The total travel time is: ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print("\nThe mean travel time is: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nBDESS is calculating user statistics...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()

    print('The number of each user type is:\n', count_user_types)

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print('\nThe number of each type of gender is:\n', count_gender)

    except KeyError:
        print('Washington does not have gender information')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_yr = df['Birth Year'].min()
        recent_birth_yr = df['Birth Year'].max()
        common_birth_yr = df['Birth Year'].mode()[0]
        print('\nThe earliest birth year is: ', earliest_birth_yr)
        print('\nThe most recent birth year is: ', recent_birth_yr)
        print('\nThe most common birth year is: ', common_birth_yr)

    except KeyError:
        print('Washington does not have birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def raw_data(df):
    x = 0
    y = 5
    while x < len(df.index):
        display_data = input('Would you like to see the first 5 lines of raw data? Enter yes, or no\n').lower()
        if display_data == 'yes':
            x += 5
            y += 5
            print(df.iloc[x:y])
        else:
            break

        # display_data = input('Would you like to see the first 5 lines of raw data? Enter yes, or no\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart BDESS? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
