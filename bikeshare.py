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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    Cities = ['chicago', 'new york city', 'washington']
    city = ""
    city_count = 0
    while city not in Cities:
        if city_count == 0:
            city = str(input('Please enter one of the cities from Chicago, New York City or Washington:')).lower() #https://www.geeksforgeeks.org/isupper-islower-lower-upper-python-applications/
            city_count = city_count + 1
        else:
            city = str(input('Your input is not in expected cities. Please enter one of the cities from Chicago, New York City or Washington:')).lower()

    # get user input for month (all, january, february, ... , june)
    Months = [ 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december','all']
    Months_without_data = [ 'july', 'august', 'september', 'october', 'november', 'december']
    month = ""
    month_count = 0
    while month not in Months:
        if month_count == 0:
            month = str(input('Please enter the month (all for all months):')).lower()
            while month in Months_without_data:
                month = str(input('There is no data for this month. Please enter another month (all for all months):')).lower()
            month_count = month_count + 1
        else:
            month = str(input('Your input is not in expected months. Please enter the month (all for all months):')).lower()
            while month in Months_without_data:
                month = str(input('There is no data for this month. Please enter another month (all for all months):')).lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    Days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    day_count = 0
    while day not in Days:
        if day_count == 0:
            day = str(input('Please enter the day (all for all days):')).lower()
            day_count = day_count + 1
        else:
            day = str(input('Your input is not in expected days. Please enter the day (all for all days):')).lower()


    print('_'*40)
    return city, month, day


def load_data(city, month, day):
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.weekday.html
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if all months selected

    popular_month = df['month'].mode()[0] #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mode.html
    print('Most popular month:' , popular_month)

    # display the most common day of week if all days selected

    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day:' , popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour:' , popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:' , popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:' , popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Station Combination'] = df[['Start Station', 'End Station']].agg(' - '.join, axis=1) #https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
    popular_station_combination = df['Station Combination'].mode()[0]
    print('Most popular station combination:' , popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    # display total travel time
    total_travel_time = df['Travel Time'].sum()
    print('Total travel time:' , total_travel_time)
    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean travel time:' , mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser types:\n' , df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGender:\n' , df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: #https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
        print('\nEarliest year of birth:' , df['Birth Year'].min())
        print('Most recent year of birth:' , df['Birth Year'].max())
        print('Most common year of birth:' , df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

		#Display 5 rows of raw information to user 
        raw_data = input('\n Would you like to see individual trip data?\n')
        row_no = 0
        while raw_data.lower() == 'yes':
            print(df.iloc[row_no:row_no+5]) #https://stackoverflow.com/questions/52126139/how-to-get-desired-row-and-with-column-names-in-pandas-dataframe
            row_no = row_no + 5
            raw_data = input('\n Would you like to see individual trip data?\n')


        restart = input('\nIf you would like to restart, please enter yes.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
