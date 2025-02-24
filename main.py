import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def calculate_demographic_data(file_path, print_data=True):
    try:
        # Load data from the user-selected CSV file
        df = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file:\n{e}")
        return

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

    # Prepare the results for display
    results = {
        'Number of each race': race_count.to_string(),
        'Average age of men': average_age_men,
        'Percentage with Bachelors degrees': f"{percentage_bachelors}%",
        'Percentage with advanced education that earn >50K': f"{percentage_advanced_education_rich}%",
        'Percentage without advanced education that earn >50K': f"{percentage_non_advanced_education_rich}%",
        'Minimum work hours per week': min_work_hours,
        'Percentage of rich among those who work fewest hours': f"{rich_percentage_min_hours}%",
        'Country with highest percentage of rich': highest_rich_country,
        'Highest percentage of rich people in country': f"{highest_rich_country_percentage}%",
        'Top occupation in India for those earning >50K': top_india_occupation
    }

    if print_data:
        output = ""
        for key, value in results.items():
            output += f"{key}: {value}\n"
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output)
    
    return results

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select a CSV file for analysis"
    )
    if file_path:
        file_label.config(text=file_path)
        analyze_button.config(state=tk.NORMAL)
    else:
        file_label.config(text="No file selected")
        analyze_button.config(state=tk.DISABLED)

def run_analysis():
    file_path = file_label.cget("text")
    if file_path and file_path != "No file selected":
        calculate_demographic_data(file_path)
    else:
        messagebox.showwarning("Warning", "Please select a CSV file first.")

# Create the main window
root = tk.Tk()
root.title("Demographic Data Analysis Tool")

# Create and place the file selection button
select_button = tk.Button(root, text="Select CSV File", command=select_file, width=30)
select_button.pack(pady=10)

# Label to display the selected file path
file_label = tk.Label(root, text="No file selected", wraplength=500)
file_label.pack(pady=5)

# Button to run the analysis (initially disabled until a file is selected)
analyze_button = tk.Button(root, text="Run Analysis", command=run_analysis, state=tk.DISABLED, width=30)
analyze_button.pack(pady=10)

# Text widget to display the analysis results
output_text = tk.Text(root, wrap=tk.WORD, height=15, width=80)
output_text.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
