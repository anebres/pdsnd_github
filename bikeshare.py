import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA:
            break
        else:
            print('\nPlease enter a valid city name.')

    # Get time filter.
    while True:
        time_filter = input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n')
        if time_filter in ['none', 'month', 'day', 'both']:
            break
        else:
            print('\nPlease enter a valid option.')
    
    # Get user input for month (all, january, february, ... , june).
    if time_filter in ['both', 'month']:
        while True:
            month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('\nPlease enter a valid option.')
    else:
        month = 'all'

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    if time_filter in ['day', 'both']:
        while True:
            day = input('\nWhich day? Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n').lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('\nPlease enter a valid option.')
    else:
        day = 'all'

    print('-'*40)
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
    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable.
    if month != 'all':
        # Filter by month to create the new dataframe.
        df = df[df['month'] == month.title()]

    # Filter by day of week if applicable.
    if day != 'all':
        # Filter by day of week to create the new dataframe.
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month if the column exists.
    if 'month' in df:
        popular_month = df['month'].mode()[0]
        print('The most popular month: ', popular_month)
    
    # Display the most common day of week if the column exists.
    popular_weekday = df['day_of_week'].mode()[0]
    print('\nThe most popular day: ', popular_weekday)
    
    # Display the most common start hour.
    # Extract hour from the Start Time column to create an hour column.
    df['hour'] = df['Start Time'].dt.hour

    # Find the most popular hour.
    popular_hour = df['hour'].mode()[0]
    print('\nThe most popular hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used Start Station.
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular Start Station: ', popular_start_station)
    
    # Display most commonly used End Station.
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most popular End Station: ', popular_end_station)

    # Display most frequent combination of Start Station and End Station trip.
    combination_station = df.groupby(['Start Station', 'End Station']).size()
    frequent_station_combination  = combination_station.idxmax()
    print('\nThe most popular combination of Start and End Stations: ', frequent_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_timme = df['Trip Duration'].sum()
    days = int(total_travel_timme // (24 * 3600))
    hours = int((total_travel_timme % (24 * 3600)) // 3600)
    minutes = int((total_travel_timme % 3600) // 60)
    seconds = int(total_travel_timme % 60)
    print(f'Total travel time for this period: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds')
    
    # Display mean travel time.
    mean_time = df['Trip Duration'].mean()
    minutes = int(mean_time // 60)
    remaining_seconds = int(mean_time % 60)
    print(f'\nAverage travel time for this period: {minutes} minutes, {remaining_seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
 
    # Display counts of User Types.
    user_types = df['User Type'].value_counts()
    print(user_types, '\n')

    # Display counts of Gender.
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender,'\n')
    else:
        print('\nGender information is not available.\n')

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        oldest_rider = int(df['Birth Year'].min())
        print(f'Oldest rider was born in {oldest_rider}.')
        youngest_rider = int(df['Birth Year'].max())
        print(f'Youngest rider was born in {youngest_rider}.')
        common_year = int(df['Birth Year'].mode()[0])
        print(f'Most riders were born in {common_year}.')
    else:
        print('\nBirth Year information is not available.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_stats(df):
    # Display all DataFrame columns.
    pd.set_option('display.max_columns', None)
    # Initialize position tracker.
    start_index = 0
    
    while True:
        stats = input('Would you like to see the next 5 rows of raw data? Enter yes or no.\n').lower()
        if stats == 'no':
            break
        elif stats == 'yes':
            # Print the current set of statistics.
            end_index = min(len(df), start_index + 5)
            print(df.iloc[start_index:end_index])
            start_index = end_index
        else:
            print('\nPlease enter a valid option.')
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()
