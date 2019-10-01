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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    city = input('\nWould you like to explore data for Chicago, New York City, or Washington?\n\n').lower()
    filt = input('\n\nWould you like to filter by month, day, or both?\n\n')

    if filt == 'both':
        month = input("\n\nWe have data for the months of January, February, March, April, May, and June.  Which month would you like?\n\n").lower()
        if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print("You may have selected a month we do not have data for.")
                print("Please select from the following months:")
                month = input("January, February, March, April, May, June")
        day = input("\n\nWhich day of the week would you like to explore? (eg. 'Monday')\n\n").lower()
        print("\n\nBelow is " + city.title() + "'s bikeshare data for " + day.title() + "'s in " + month.title() + ".")
    
    elif filt == 'month':
        month = input("\n\nWe have data for the months of January, February, March, April, May, and June.  Which month would you like?\n\n").lower()
        if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print("You may have selected a month we do not have data for.")
                print("Please select from the following months:")
                month = input("January, February, March, April, May, June")
        day = 'None specified'
        print("\n\nBelow is " + city.title() + "'s bikeshare data for the month of " + month.title() + ".")

    elif filt == 'day':
        month = 'None specified'
        day = input("\n\nWhich day of the week would you like to explore? (eg. 'Monday')\n\n").lower()
        print("\n\nBelow is " + city.title() + "'s bikeshare data for all " + day.title() + "'s in the months from January to June.")
    
    print('-'*40)
    return(city, month, day, filt)

def load_data(city, month, day, filt):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filt - 
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

    # filter by both if applicable
    if filt == 'both':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    # filter by month if applicable
    elif filt == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day if applicable
    elif filt == 'day':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df 

def time_stats(df, filt):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    popMonth = df['Start Time'].dt.month.mode()[0]
    popDay = df['Start Time'].dt.weekday_name.mode()[0]
    popHour = df['Start Time'].dt.hour.mode()[0]

    print("The most popular hour is {}:00.".format(popHour))
        
    if filt == 'month':
        print("The most popular day is {}.".format(popDay))
    
    if filt == 'day':
        print("The most popular month is {}.".format(popMonth))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popStartSta = df['Start Station'].mode()[0]
    popEndSta = df['End Station'].mode()[0]
    popStartEndSta = df.groupby('Start Station')['End Station'].value_counts().nlargest(1)
    
    print("The most common start station was {}.".format(popStartSta))
    print("The most common end station was {}.".format(popEndSta))
    print("\nThe most common trip was:\n\n{}.".format(popStartEndSta))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    totTravel = df['Trip Duration'].sum()
    avgTravel = df['Trip Duration'].mean()
   
    # display total travel time
    totTravel_hrs = totTravel/120
    avgTravel_mins = avgTravel/60
    print("This is the total travel time:")
    print("{} hours".format(totTravel_hrs))
    print("\n\nThis is the average travel time:")
    print("{} minutes".format(avgTravel_mins))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("This is the breakdown of user types.")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city.lower() in ("chicago", "new york city"):
        print("\n\nThis is the breakdown of users by gender.")
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city.lower() in ("chicago", "new york city"):
        print("\nThe is the earliest birth year.")
        print(df['Birth Year'].min())
        print("\nThe is the latest birth year.")
        print(df['Birth Year'].max())
        print("\nThe is the most common birth year.")
        print(df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
    
def main():
    while True:        
        city, month, day, filt = get_filters()
        df = load_data(city, month, day, filt)
        time_stats(df, filt)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        # Start code for raw data by user input
        points = 0
        q1 = input('\nDo you want to see raw data? Enter yes or no.\n')
        if q1.lower() == 'yes':
            df = pd.read_csv(CITY_DATA[city])
            print(df.iloc[points:points+5])
            points = points + 5
            q2 = input('\nDo you want to see 5 more rows? Enter yes or no.\n')
            while q2.lower() == 'yes':
                if points < (df.shape[0]-5):
                    print(df.iloc[points:points+5])
                    points = points +5
                    q2 = input('\nDo you want to see 5 more rows? Enter yes or no.\n')
                else:
                    print("\nActually, that's all the data we have.\n")
                    break 
        # End code for raw data by user input
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()  

# Sources used:
# SciPy Daniel Chen YouTube Video: https://www.youtube.com/watch?v=dye7rDktJ2E
# Data School YouTube Videos: https://www.youtube.com/channel/UCnVzApLJE2ljPZSeQylSEyg
# Python Documentation: https://docs.python.org/3/index.html
    
    