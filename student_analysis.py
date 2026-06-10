import pandas as pd

df = pd.read_csv("data/student_clean.csv")

# Average Marks
df["AverageMarks"] = (
    df[["Math", "Science", "English"]]
    .mean(axis=1)
)

print("Average Marks:")
print(df["AverageMarks"])

# Top Student
top_student = df.loc[
    df["AverageMarks"].idxmax()
]

print("\nTop Student:")
print(top_student)

# Correlation
print("\nCorrelation Matrix:")
print(
    df[
        ["Math", "Science", "English", "Attendance"]
    ].corr()
)

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())