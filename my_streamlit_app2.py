# import pip
# pip.main(['install','seaborn'])

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io



st.title('Hello Wilders, welcome to my application!')

# import fichier
link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)

# formattage colonnes
df_cars = df_cars.rename(columns={"cubicinches":"cubic_inches", "weightlbs" : "weight_lbs"})
df_cars['weight_lbs'] = df_cars['weight_lbs'].apply(lambda x: f'{x:,}'.replace(',', ''))
df_cars['weight_lbs'] = df_cars['weight_lbs'].astype(int)
df_cars['year'] = df_cars['year'].apply(lambda x: f'{x:,}'.replace(',', ''))
df_cars['year'] = df_cars['year'].astype(int)
df_cars['continent'] = df_cars['continent'].str.replace('.', '').astype(str).str.strip()


# Sidebar with filter options
st.sidebar.header('Filter by Continent')
selected_continent = st.sidebar.radio('Select Continent', ['All', 'US', 'Europe', 'Japan'])

# Apply filter based on selected continent
if selected_continent != 'All':
    filtered_df_cars = df_cars[df_cars['continent'] == selected_continent]
else:
    filtered_df_cars = df_cars  # Show all data if 'All' is selected

# # Display filtered data
# st.subheader('Filtered Results')
# st.write(filtered_df_cars)

# affichage du df
st.write("## Dataset : ")
st.write(filtered_df_cars)
st.write('')

# affichage du df.info
st.write("## Dataset info: ")
buffer = io.StringIO()
filtered_df_cars.info(buf=buffer)
info = buffer.getvalue()
# Display the captured info in Streamlit
st.text(info)
st.write('')

# affichage du df.describe()
st.write("## Dataset descriptive analysis: ")
description = filtered_df_cars.describe()
# Display the description in Streamlit
st.write(description)
st.write('')

# affichage du value counts par continent
st.write("## Value Counts for 'continent' column:")
continent_counts = filtered_df_cars['continent'].value_counts()
st.write(continent_counts)


# analyse de corrélation 
st.write("# Correlation Analysis:")

correlation_matrix = filtered_df_cars.select_dtypes('number').corr()

viz_correlation = sns.heatmap(correlation_matrix, 
								center=0,
								cmap='coolwarm',
                                annot=True
								)
st.pyplot(viz_correlation.figure)

st.write("Très forte corrélation entre cubic_inches et cylindres et entre cubic_inches et hp. Information redondante ?")

# une analyse de distribution


# Define columns and subplots
columns = ['mpg', 'cylinders', 'cubic_inches', 'hp', 'weight_lbs', 'time-to-60', 'year']
num_plots = len(columns)

# Calculate the number of rows and columns for subplots
num_rows = (num_plots + 1) // 2  # Add 1 to round up when there's an odd number of plots
num_cols = 2

# Create subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, num_rows * 4))

# Flatten the axes array to iterate over each subplot
axes = axes.flatten()

# Plot each column in a subplot
for i, column in enumerate(columns):
    sns.histplot(filtered_df_cars[column], ax=axes[i], kde=True)
    axes[i].set_title(f'Distribution of {column}')
    axes[i].set_xlabel(column)
    axes[i].set_ylabel('Frequency')

# Remove any unused subplots
for j in range(num_plots, num_rows * num_cols):
    fig.delaxes(axes[j])

# Adjust layout and display plots
st.write("# Distribution Analysis:")
fig.tight_layout()
st.pyplot(fig)


st.write("Box Plot Mpg / Continent:")
fig, ax = plt.subplots()
sns.boxplot(x='continent', y='mpg', data=filtered_df_cars, ax=ax)
ax.set_xlabel('continent')
ax.set_ylabel('mpg')
st.pyplot(fig)
st.markdown("> JP : Les voitures JP sont les moiins consommatrices du dataset. \n"
            "75% des voitures US consomment plus que de 25% des voitures EU. \n"
            "Très peu d'outliers pour le Japon contrairement aux voitures EU et US.")

st.write("Box Plot time-to-60 / Continent:")
fig, ax = plt.subplots()
sns.boxplot(x='continent', y='time-to-60', data=filtered_df_cars, ax=ax)
ax.set_xlabel('continent')
ax.set_ylabel('time-to-60')
st.pyplot(fig)

st.markdown("> EU : Les voitures EU semblent prendre le plus de temps pour passer de 0 à 60 miles par heures.\n"
            "US : Les voitures sont les plus rapides à passer de 0 à 60 miles par heures.\n"
            "JP : les données sont plus concentrées")

st.write("Box Plot weight_lbs / Continent:")
fig, ax = plt.subplots()
sns.boxplot(x='continent', y='weight_lbs', data=filtered_df_cars, ax=ax)
ax.set_xlabel('continent')
ax.set_ylabel('weight_lbs')
st.pyplot(fig)

st.markdown("> EU : Dans le dernier quartile les voitures sont beaucoup plus lourdes ?.\n"
            "US : Les voitures sont les plus lourdes. Les valeurs sont très étendues.\n"
            "JP : les données sont plus concentrées")

# st.write("Box Plot cylinders / Continent:")
# fig, ax = plt.subplots()
# sns.boxplot(x='continent', y='cylinders', data=df_cars, ax=ax)
# ax.set_xlabel('continent')
# ax.set_ylabel('cylinders')
# st.pyplot(fig)


st.write("Box Plot cubic_inches / Continent:")
fig, ax = plt.subplots()
sns.boxplot(x='continent', y='cubic_inches', data=filtered_df_cars, ax=ax)
ax.set_xlabel('continent')
ax.set_ylabel('cubic_inches')
st.pyplot(fig)

st.markdown("> US : Les voitures sont très haut dessus sur cette variable.")

st.write("Box Plot hp / Continent:")
fig, ax = plt.subplots()
sns.boxplot(x='continent', y='hp', data=filtered_df_cars, ax=ax)
ax.set_xlabel('continent')
ax.set_ylabel('hp')
st.pyplot(fig)

st.markdown("> US : Les voitures US sont les plus puissantes du dataset.")