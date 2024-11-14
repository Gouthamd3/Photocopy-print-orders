# import pandas
import pandas as pd

# List of Tuples
employees = [('Stuti', 28, 'Varanasi', 20000),
            ('Saumya', 32, 'Delhi', 25000),
            ('Aaditya', 25, 'Mumbai', 40000),
            ('Saumya', 32, 'Delhi', 35000),
            ('Saumya', 32, 'Delhi', 30000),
            ('Saumya', 32, 'Mumbai', 20000),
            ('Aaditya', 40, 'Dehradun', 24000),
            ('Seema', 32, 'Delhi', 70000)
            ]

# Create a DataFrame object from list
df = pd.DataFrame(employees,
                columns =['Name', 'Age',
                'City', 'Salary'])

# Set 'Name' column as index
# on a Dataframe
df.set_index("Age", inplace = True)
print(df)
# Using the operator .loc[]
# to select single row
df = df.drop(df[28])
result = df.loc[32]

'''
data = data.drop(data.index[1])
# Delete some chosen rows by row numbers - 2nd, 10th, 30th:
data = data.drop(data.index[[1, 9, 29]])
# Delete the first 5 rows
data = data.drop(data.index[range(5)])
# Delete the last row in the DataFrame
data = data.drop(data.index[-1])
'''
# Show the dataframe
print(result)
