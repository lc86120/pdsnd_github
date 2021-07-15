import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

WEEK_DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

CLOSING_LINE = '-'*70 + '\n'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    while True:
        try:
            city = str(input("For which city would you like to uncover the\
 patterns in bike share usage?\n"))
            if city.isnumeric():
                exit_message = 'attempted. Input not a valid city name.'
            else:
                city = city.lower()
                if city == 'chicago' or city == 'new york city' or city == 'washington':
                    exit_message = 'completed.\n' + CLOSING_LINE
                    break
                else:
                    exit_message = 'attempted. City name not recognised.\nPlease select a\
 large US city: Chicago, New York City or Washington DC. Then enter its name.'
        except KeyboardInterrupt:
            exit_message = 'completed. City name not specified.\nInsted, exit command\
 received.\n' + CLOSING_LINE
            city = None
            break
        finally:
            print('Selection city ' + exit_message)

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            bool_month = str(input('Would you like to filter the data by month or not at all?\n'))
            bool_month = bool_month.lower()
            if bool_month.isalpha() and (bool_month == 'yes' or bool_month == 'no'):
                exit_message = 'completed.\n' + CLOSING_LINE
                break
            else:
                exit_message = 'attempted. Please answer either \'Yes\' or \'No\'.'
        except KeyboardInterrupt:
            exit_message = 'attempted. Month filter not specified.\nInsted, exit command\
 received.\n' + CLOSING_LINE
            bool_month = None
            break
        finally:
            print('Selection monthly filter ' + exit_message)


    if bool_month == None:
        month = None
    else:
        if bool_month == 'no':
            month = 'all'
        else:
            while True:
                try:
                    month = str(input('What month would you like to filter?\n'))
                    month = month.lower()
                    if month.isalpha() and (month in MONTHS):
                        exit_message = 'completed.\n' + CLOSING_LINE
                        break
                    else:
                        exit_message = 'attempted. Please enter a valid month from January to June inclusive.'
                except KeyboardInterrupt:
                    exit_message = 'attempted. Month not specified.\nInsted, exit command\
 received.\n' + CLOSING_LINE
                    month = None
                    break
                finally:
                    print('Selection month ' + exit_message)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            bool_day = str(input('Would you like to filter the data by day or not at all?\n'))
            bool_day = bool_day.lower()
            if bool_day.isalpha() and (bool_day == 'yes' or bool_day == 'no'):
                exit_message = 'completed.\n' + CLOSING_LINE
                break
            else:
                exit_message = 'attempted. Please answer either \'Yes\' or \'No\'.'
        except KeyboardInterrupt:
            exit_message = 'completed. Day filter not specified.\nInsted, exit command\
 received.\n' + CLOSING_LINE
            bool_day = None
            break
        finally:
            print('Selection daily filter ' + exit_message)


    if bool_day == None:
        day = None
    else:
        if bool_day == 'no':
            day = 'all'
        else:
            while True:
                try:
                    day = str(input('What day would you like to filter?\n'))
                    day = day.lower()
                    if day.isalpha() and (day in WEEK_DAYS):
                        exit_message = 'completed.\n' + CLOSING_LINE
                        break
                    else:
                        exit_message = 'attempted. Please enter a valid day of the week.'
                except KeyboardInterrupt:
                    exit_message = 'completed. Day not specified.\nInsted, exit command\
 received.\n' + CLOSING_LINE
                    day = None
                    break
                finally:
                    print('Selection day ' + exit_message)

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    # extract day from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday

    # extract hour from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the day to get the corresponding int
        day_of_week = WEEK_DAYS.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_of_week]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = MONTHS[popular_month - 1]
    print('The most common month is ' + popular_month.title() + '.')

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day = WEEK_DAYS[popular_day]
    print('The most common day of the week is ' + popular_day.title() + '.')

    # display the most common start hour
    popular_month = df['hour'].mode()[0]
    print('The most common start hour is ' + str(popular_month) + ':00.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(CLOSING_LINE)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is ' + popular_start_station + '.')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ' + popular_end_station + '.')

    # display most frequent combination of start station and end station trip
    df['Start-End Stations'] = df['Start Station'] + ' -- ' + df['End Station']
    popular_start_end_station = df['Start-End Stations'].mode()[0]
    popular_start_station, popular_end_station = popular_start_end_station.split('--')
    print('The most frequent trip is from ' + popular_start_station
          + '(start station) to' + popular_end_station +' (end station).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(CLOSING_LINE)

def convert_seconds(seconds):
    ''' Function to convert seconds to years, days, hours, minutes and seconds.'''
    minutes = seconds//60
    seconds -= minutes*60
    hours = minutes//60
    minutes -= hours*60
    days = hours//24
    hours -= days*24
    years = days//365
    days -= years*365
    if years>0:
        return '{y} yr, {d} days, {h} hrs, {m} min and {s} sec'.format(y=years,
                d=days,h=hours,m=minutes,s=seconds)
    if years==0  and days>0:
        return '{d} days, {h} hrs, {m} min and {s} sec'.format(d=days,h=hours,
                m=minutes,s=seconds)
    elif days==0  and hours>0:
        return '{h} hrs, {m} min and {s} sec'.format(h=hours,m=minutes,s=seconds)
    elif hours == 0 and minutes > 0:
        return '{m} min and {s} sec'.format(m=minutes,s=seconds)
    elif hours == 0 and minutes == 0:
        return '{s} sec'.format(s=seconds)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is ' + convert_seconds(total_time) + '.')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is ' + convert_seconds(int(mean_time)) + '.')

    # display mean travel time of subscriber users
    subscriber_mean_time = df[df['User Type']=='Subscriber']['Trip Duration'].mean()
    print('For subscriber users the mean travel time is '
          + convert_seconds(int(subscriber_mean_time)) + '.')

    # display mean travel time of customer users
    customer_mean_time = df[df['User Type']=='Customer']['Trip Duration'].mean()
    print('For customer users the mean travel time is '
          + convert_seconds(int(customer_mean_time)) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(CLOSING_LINE)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print('The subscriber users are ' + str(user_types['Subscriber']) + '.')
    print('The customer users are ' + str(user_types['Customer']) + '.')

    if city=='chicago' or city=='new york city':
        # Display counts of gender
        user_gender = df["Gender"].value_counts()
        print('The total female users are ' + str(user_gender['Female']) + '.')
        print('The total male users are ' + str(user_gender['Male']) + '.')

        # Display counts of gender by user type
        subscriber_user_gender = df[df['User Type']=='Subscriber']["Gender"].value_counts()
        customer_user_gender = df[df['User Type']=='Customer']["Gender"].value_counts()
        # Display counts of female users as provided in the data
        if 'Female' in subscriber_user_gender:
            print('The knownn female subscribers are ' + str(subscriber_user_gender['Female']) + '.')
        else:
            print('The knownn female subscribers are 0.')
        if 'Female' in customer_user_gender:
            print('The knownn female customers are ' + str(customer_user_gender['Female']) + '.')
        else:
            print('The knownn female customers are 0.')
        # Display counts of male users as provided in the data
        if 'Male' in subscriber_user_gender:
            print('The knownn male subscribers are ' + str(subscriber_user_gender['Male']) + '.')
        else:
            print('The knownn male subscribers are 0.')
        if 'Male' in customer_user_gender:
            print('The knownn male customers are ' + str(customer_user_gender['Male']) + '.')
        else:
            print('The knownn male customers are 0.')

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest year of birth is ' + str(int(earliest_birth_year)) + '.')

        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent year of birth is ' + str(int(most_recent_birth_year)) + '.')

        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most common year of birth is ' + str(int(most_common_birth_year)) + '.')

        # calculate the mean travel time for each year of birth
        unique_years = df['Birth Year'].dropna().sort_values(ascending=False).unique()
        mean_time_years = []
        for year in unique_years:
            mean_time_years.append(df[df['Birth Year']==year]['Trip Duration'].mean())
        data_mean_time_years = {'Birth Year' : unique_years, 'Mean Travel Time' : mean_time_years}
        df_mean_years = pd.DataFrame(data_mean_time_years)

        # display the 5 years where the mean travel time is highest
        print('The five years where the mean travel time (sec) is highest are:')
        print(df_mean_years.sort_values('Mean Travel Time',ascending=False).head())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print(CLOSING_LINE)

def display_data(df):
    '''Display the input bike usage data 5 lines at the time until the user wants to stop.'''
    num_lines = 5;
    more=''
    while True:
        try:
            bool_display = str(input('Would you like to see 5 ' + more + 'lines of data?\n'))
            bool_display = bool_display.lower()
            if bool_display=='yes' or bool_display=='no':
                if bool_display=='yes':
                    print(df.head(num_lines))
                    num_lines+=5
                    more='more '
                    exit_message='attempted.'
                elif bool_display=='no':
                    exit_message='completed.\n' + CLOSING_LINE
                    break
            else:
                exit_message = 'attempted. Please answer either \'Yes\' or \'No\'.'
        except KeyboardInterrupt:
            exit_message = 'completed. Display data terminated by exit key.\n' + CLOSING_LINE
            break
        finally:
            print('Display data ' + exit_message)



def main():
    ''' Function to compute and display the bike share usage statistics.'''
    while True:
        # Read the city name, the montly filter and the daily filter.
        city, month, day = get_filters()
        # Check whether the city name, the montly and daily filters are valid.
        if city == None or month == None or day == None:
            # city name and filters are invalid.
            print('Unable to uncover bike share usage patterns.')
            if city == None:
                print('City unknown.')
            if month == None:
                print('Montly filter unknown.')
            if day == None:
                print('Daily filter unknown.')
            print(CLOSING_LINE)
        else:
            # city name and filters are valid.
            # load and display data
            df = load_data(city, month, day)
            display_data(df)

            # calculating the descriptive statistics
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(city, df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
