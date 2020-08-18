import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'jebruary', 'jarch', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

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
	city = input("Enter name of the city to analyze (Chicago, New York City or Washington): ").lower() #check if the city is correct
	while (city not in CITY_DATA.keys()):
		print ('City not registered. Enter a correct city: ')
		city = input("Enter name of the city to analyze (Chicago, New York City or Washington): ").lower()
	print()

	# get user input for month (all, january, february, ... , june)
	month = input("Enter name of the month to filter by (between January-June), or 'all' to apply no month filter: ") #check if the month is correct
	while (month not in months):
		print ('Month not correct. Enter a correct month: ')
		month = input("Enter name of the month to filter by, or 'all' to apply no month filter: ")
	print()

	# get user input for day of week (all, monday, tuesday, ... sunday)
	day = input("Enter name of the day of week to filter by, or 'all' to apply no day filter: ")
	while (day not in days): #check if the day is correct
		print ('Day not correct. Enter a correct day: ')
		day = input("Enter name of the day of week to filter by, or 'all' to apply no day filter: ")
	print()

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Popular month:', months[most_common_month-1].title())
    print()

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0] 
    print('Most Popular day:', most_common_day.title())
    print()

    # display the most common start hour
    most_common_hour = df['Start Time'].mode()[0].hour
    print('Most Popular hour:', most_common_hour)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0] 
    print('Most Popular Start Station:', most_common_start)
    print()

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0] 
    print('Most Popular End Station:', most_common_end)
    print()

    # display most frequent combination of start station and end station trip
    temporal_df = df[['Start Station','End Station']]
    temporal_df=temporal_df.groupby(["Start Station", "End Station"])['Start Station'].count().reset_index(name="count")
    temporal_df.sort_values(['count'],ascending=False, inplace=True)
    print('Most frequent combination of start station and end station trip: ')
    print(temporal_df[["Start Station", "End Station"]].head(1))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration = df['Trip Duration'].sum()
    print('The total trip duration is ' + str(duration) + ' seconds')
    print('This is ' + str(duration/3600) + ' hours or ' + str((duration/3600)/24) + ' days')
    print()

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('The mean travel time is ' + str(mean_duration) + ' seconds')
    print('This is ' + str(mean_duration/3600) + ' hours')
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The user types count is: ', df['User Type'].value_counts())
    print()

    if (city == 'washington'):
        print('The gender count is not available for Washington')
        print()
    else:
        # Display counts of gender
        print('The gender count is: ', df['Gender'].value_counts())
        print()

    if (city == 'washington'):
        print('The birth year is not available for Washington')
        print()
    else:
        # Display earliest, most recent, and most common year of birth
        df.sort_values(['Birth Year'],ascending=True, inplace=True)
        print('The earliest year of birth is: ', df['Birth Year'].head(1))
        print()
    
        df.sort_values(['Birth Year'],ascending=False, inplace=True)
        print('The most recent year of birth is: ', df['Birth Year'].head(1))
        print()
    
        df.sort_values(['Birth Year'],ascending=False, inplace=True)
        print('The most common year of birth is: ', df['Birth Year'].mode()[0])
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        
        flag = True
        
        while flag:
            see_more = input('\nWould you like to view individual trip data? Enter yes or no. \n')
            if see_more.lower() == 'yes':
                print(df.head())
                df = df.iloc[5:] #erase the 5 first rows (we have a new df without the 5 first rows)
            else:
                flag = False           
         
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
