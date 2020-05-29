import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days_list = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']

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
    city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()
    while True:
        if city in CITY_DATA:
            break
        elif city == 'exit':
            exit()
        else:
            city = input('Please enter a valid city, or enter exit to quit: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please enter the desired month from January up to June, or All to analyze all months: ').lower()
    while True:
        if month in months_list:
            break
        elif month == 'exit':
            exit()
        else:
            month = input('Please enter a valid month, or enter exit to quit: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please enter the desired day i.e. Saturday, or All to analyze all days: ').lower()
    while True:
        if day in days_list:
            break
        elif day == 'exit':
            exit()
        else:
            day = input('Please enter a valid day, or enter exit to quit: ').lower()

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'] == month.title()]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = df['month'].mode()[0]
    print('Most Common Month is:', most_common_month)

    # display the most common day of week

    most_common_dow = df['day_of_week'].mode()[0]
    print('Most Common Day of Week is:', most_common_dow)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour is:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    most_common_ss = df['Start Station'].mode()[0]
    print('Most Common Start Station is:', most_common_ss)

    # display most commonly used end station

    most_common_es = df['End Station'].mode()[0]
    print('Most Common End Station is:', most_common_es)

    # display most frequent combination of start station and end station trip

    most_common_ses = df.groupby(['Start Station'])['End Station'].value_counts().nlargest(1)
    print('Most Common Trip is From {} Station to {} Station With a Count of {} Trips'.format(most_common_ses.index[0][0], most_common_ses.index[0][1], most_common_ses[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: {} Seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time is: {} Seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].fillna('Undefined').value_counts()
    print('User Types Counts Are: \n')
    for i in range(user_types.shape[0]):
        print(user_types.index[i], user_types[i])

    # Display counts of gender

    print('\nUser Gender Counts Are: \n')
    if 'Gender' not in df:
        print('No Gender Data Exists for {}'.format(city).title())
    else:
        gender_types = df['Gender'].fillna('Undefined').value_counts()
        for i in range(gender_types.shape[0]):
            print(gender_types.index[i], gender_types[i])

    # Display earliest, most recent, and most common year of birth

    print('\nYear of Birth Statistics Are: \n')
    if 'Birth Year' not in df:
        print('No Year of Birth Data Exists for {}'.format(city).title())
    else:
        min_yob = df['Birth Year'].min()
        print('Earliest Year of Bearth is:',int(min_yob))
        max_yob = df['Birth Year'].max()
        print('Most Recent Year of Bearth is:',int(max_yob))
        most_common_yob = df['Birth Year'].mode()[0]
        print('Most Common Year of Bearth is:',int(most_common_yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def row_data(df):
    i = 0
    choice = input('\nWould You Like To See The Raw Data, Enter yes or no?: ').lower()
    while True:
        if choice == 'yes' or choice == 'no':
            break
        else:
            choice = input('Please enter a valid response: ').lower()
    while choice == 'yes':
        print(df.iloc[i:i+5, 0:-3])
        i += 5
        choice = input('\nWould You Like To See additional Raw Data, Enter yes or no?: ').lower()
        while True:
            if choice == 'yes' or choice == 'no':
                break
            else:
                choice = input('Please enter a valid response: ').lower()
        if choice == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no?: ').lower()
        while True:
            if restart == 'yes' or restart == 'no':
                break
            else:
                restart = input('Please enter a valid response: ').lower()
        if restart == 'no':
            break

if __name__ == "__main__":
    main()
