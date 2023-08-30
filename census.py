import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings

warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above.

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

st.title("Census Data Visualization Web app")
st.sidebar.title("Menu")

# Using the 'if' statement, display raw data on the click of the checkbox.
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Census Data set")
    st.dataframe(census_df)
    st.write("Number of Rows: ", census_df.shape[0])
    st.write("Number of Columns: ", census_df.shape[1])

# Add a multiselect widget to allow the user to select multiple visualisations.
# Add a subheader in the sidebar with the label "Visualisation Selector"
st.sidebar.subheader("Visualisation Selector")


# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
plot_list = st.sidebar.multiselect("Select the Charts/Plots:",
                                   ('Pie Chart', 'Box Plot', 'Count Plot'))

# Display pie plot using matplotlib module and 'st.pyplot()'
if 'Pie Chart' in plot_list:
    st.subheader("Pie Chart")
    column = st.sidebar.multiselect("Select the column for pie chart",
                                  ('income', 'gender'))

    for i in column:
	    pie_data = census_df[i].value_counts()
	    plt.figure(figsize = (5, 5))
	    plt.title(f"Distribution of records for different {i} groups")
	    plt.pie(pie_data, labels = pie_data.index, autopct = '%1.2f%%',
	            startangle = 30, explode = np.linspace(.01, .05, len(pie_data)))
	    st.pyplot()


# Display box plot using matplotlib module and 'st.pyplot()'
if 'Box Plot' in plot_list:
    st.subheader("Box Plot for the Hours Worked Per Week")
    hue_columns = st.sidebar.multiselect("Select the column for grouping the distribution of records in the boxplot",
                                  ('income', 'gender'))
    for i in hue_columns:
	    plt.figure(figsize = (12, 4))
	    plt.title(f"Distribution of Hour Worked Per Week for different {i} groups")
	    sns.boxplot(census_df['hours-per-week'], y = census_df[i])
	    st.pyplot()


# Display count plot using seaborn module and 'st.pyplot()'
if 'Count Plot' in plot_list:
    st.subheader("Count plot for distribution of records for unique workclass groups")
    plt.figure(figsize = (12, 5))
    sns.countplot(x = 'workclass', hue = 'income', data = census_df)
    st.pyplot()