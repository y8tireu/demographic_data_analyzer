import pandas as pd

def calculate_demographic_data(print_data=True):
    # Load data
    df = pd.read_csv('your_dataset.csv')

    # How many people of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df['education'] == 'Bachelors').mean() * 100, 1)

    # What percentage of people with advanced education (Bachelors, Masters, or Doctorate) make more than 50K?
    advanced_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    percentage_advanced_education_rich = round(
        (df[advanced_education & (df['salary'] == '>50K')].shape[0] / df[advanced_education].shape[0]) * 100, 1
    )

    # What percentage of people without advanced education make more than 50K?
    no_advanced_education = ~advanced_education
    percentage_non_advanced_education_rich = round(
        (df[no_advanced_education & (df['salary'] == '>50K')].shape[0] / df[no_advanced_education].shape[0]) * 100, 1
    )

    # What is the minimum number of hours a person works per week?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?
    min_hours_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage_min_hours = round(
        (min_hours_workers[min_hours_workers['salary'] == '>50K'].shape[0] / min_hours_workers.shape[0]) * 100, 1
    )

    # What country has the highest percentage of people that earn >50K?
    rich_country_percentage = (df[df['salary'] == '>50K']['native-country'].value_counts() /
                                df['native-country'].value_counts()) * 100
    highest_rich_country = rich_country_percentage.idxmax()
    highest_rich_country_percentage = round(rich_country_percentage.max(), 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india_rich_occupations = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation']
    top_india_occupation = india_rich_occupations.value_counts().idxmax()

    # Print data if required
    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with advanced education that earn >50K: {percentage_advanced_education_rich}%")
        print(f"Percentage without advanced education that earn >50K: {percentage_non_advanced_education_rich}%")
        print(f"Minimum work hours per week: {min_work_hours}")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage_min_hours}%")
        print("Country with highest percentage of rich:", highest_rich_country)
        print(f"Highest percentage of rich people in country: {highest_rich_country_percentage}%")
        print("Top occupation in India for those earning >50K:", top_india_occupation)

    # Return results as a dictionary for testing
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'percentage_advanced_education_rich': percentage_advanced_education_rich,
        'percentage_non_advanced_education_rich': percentage_non_advanced_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage_min_hours': rich_percentage_min_hours,
        'highest_rich_country': highest_rich_country,
        'highest_rich_country_percentage': highest_rich_country_percentage,
        'top_india_occupation': top_india_occupation
    }

# Uncomment the following line to test the function manually
# calculate_demographic_data(print_data=True)
