import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

Cities = ['chicago', 'new york city', 'washington']
Months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
Days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city you like to see data from [Chicago, New York City, or Washington]: ').lower()
        if city not in Cities:
            print('Invalid Answer. Please enter a valid response')
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to filter from: [all, january, february, march, april, may, or june]: ').lower()
        if month not in Months:
            print('Invalid Answer. Please enter a valid response')
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to filter by: [all, sunday, monday, tuesday, wednesday, thursday, friday, or saturday]: ').lower()
        if day not in Days:
            print('Invalid Answer. Please enter a valid response')
            continue
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])

    # Convert "Start Time" colume into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create columns for month, day and hour
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    #filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    #filter by day of the week
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        df = df[df['Day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Dictionary of month numbers
    month_numbers = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June'}

    # TO DO: display the most common month
    common_month = df['Month'].mode()[0]
    month_str = month_numbers[str(common_month)]
    print('The most common month was: ', month_str)

    # TO DO: display the most common day of week
    common_day = df['Day_of_week'].mode()[0]
    print('The most common day of the week was: ', common_day)

    # TO DO: display the most common start hour
    common_hour = df['Hour'].mode()[0]
    print('The most common hour was: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station was: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station was: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    common_start_end_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name='counts')
    common_start_pair = common_start_end_station['Start Station'][0]
    common_end_pair = common_start_end_station['End Station'][0]
    print('The most common start and end station combination was: {}, {}'.format(common_start_pair, common_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print(user_type_counts)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        nan_count = df['Gender'].isna().sum()
        print('Gender Count: {}. There were {} NaN values'.format(gender_count, nan_count))
    else:
        print('There is no column named Gender')


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}. \nMost recent birth year: {}. \nMost coomon birth year: {}'.format(earliest, most_recent, most_common))
    else:
        print('There is no column for Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Display raw data
def display_data():
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').strip().lower()
    if view_data in ('yes'):
        start_loc = 0
        while True:
            if (i + 5 > len(df.index) - 1):
                print(df.iloc[0:5])
                start_loc += 5
                view_display = input('Do you wish to continue?: ').lower()
                break
            if view_data not in ('yes'):
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
