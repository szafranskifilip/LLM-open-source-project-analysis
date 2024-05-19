import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('../data/github_final.csv')

# Create a title for your app
st.title('Most Impactful LLM-related Open Source Software (OSS) Projects')
st.markdown("""Let's see our data:

The table summarizes key data for a selection of GitHub repositories, focusing on their popularity, contribution metrics, and classification. It provides repository names, descriptions, creation dates, and the number of stars and forks, alongside license information and age. The inclusion of average daily forks and stars provides insight into growth trends, and predefined categories like 'Tutorials' or 'Applications' help categorize each repository's purpose or domain within the field of Large Language Models (LLMs).
            

            """)
# Show the DataFrame on the app
st.write(df)

fig = px.scatter(df, x="days_since_created", y="stargazers_count", hover_data=['name'], trendline="ols", trendline_color_override='#FF0000')
st.plotly_chart(fig, use_container_width=True)
st.caption('Fig. 1. Trend of GitHub Stars Over Repository Age')

st.write("""This scatter plot above maps the relationship between a GitHub repository's age and its popularity, as measured by star count. A trend line shows a general pattern where older repositories have more stars, hinting at a gradual accumulation over time. Notably, we see a few repositories with star counts far exceeding the average, suggesting exceptional popularity.""")

repo_counts = df[['created_at','name']].groupby('created_at').count().reset_index()
repo_counts.rename(columns={'name': 'repos_count'}, inplace=True)
fig = px.line(repo_counts, x='created_at', y='repos_count', markers=False)
st.plotly_chart(fig, use_container_width=True)
st.caption('Fig. 2. Growth in Repository Creations Over Time')

st.write("""This visualization presents a timeline of GitHub repository creations. The chart indicates sporadic activity in earlier years, with a substantial increase in repository creation frequency in 2023. The density of plot in the most recent years reflects the rising interest in software development related to LLMs. """)

st.header('What are OSS projects?')
st.markdown("""The determination of whether a GitHub repository is open source primarily revolves around the type of license it is distributed under.
            
A repository is considered open source if it includes a license that complies with the Open Source Initiative (OSI) Open Source Definition. This definition includes several criteria, such as free redistribution, source code availability, derivative works permission, and no discrimination against persons or groups.
            
Common open-source licenses include the MIT License, Apache License 2.0, GNU General Public License (GPL)""")

# Assuming 'df' is your DataFrame and it has a 'license' column
license_counts = df['license'].value_counts().nlargest(3).reset_index()

# Create a pie chart
fig = px.pie(license_counts, values='count', names='license')
st.plotly_chart(fig, use_container_width=True)
st.caption('Fig. 3. License Distribution in Our Dataset')

st.header('The most impactful projects')
# User inputs for weights
st.markdown(""" 
Determining the "most impactful" projects involves analyzing various metrics that reflect the project's popularity, or technical contribution. On platforms like GitHub, certain data points can serve as indicators of a project's impact. Here are two main criteria that the impact will be measured by:

1. Star Count
- What It Indicates: A high star count is often seen as a sign of the project's popularity and community approval.
- Limitations: Stars can sometimes reflect momentary interest rather than long-term value or impact.
2. Forks Count
- What It Indicates: Forks indicate other developers are interested in building upon or with the project. A high fork count suggests the project is a valuable resource or foundation within the community.
- Limitations: Not all forks lead to significant contributions or variations.
3. Age of Repository
- What It Indicates: The age or longevity of a project can indicate its enduring relevance and stability in the open-source community. Older projects have had more time to accumulate contributions, users, and recognition.
- Limitations: Age alone does not indicate quality or active maintenance. A project's recent activity should also be considered.
4. Repository Category
- What It Indicates: The category of a repository can provide insights into its domain of influence and typical use cases. It helps in understanding the sector of technology the project is impacting, whether it be web development, data science, machine learning, etc.
- Limitations: A repository’s category doesn't measure its quality or influence directly. A project might be influential within a niche category or could be pioneering a new category of technology.
            
Select the presets below and adjust the sliders to find th emost impactful OSS projects.
            
            
            """)

# Define presets
category_presets = {
    'All': ['Tutorials', 'Applications', 'AI engineering', 'Model development', 'Model repo', 'Infrastructure', 'Lists', 'Unknown'],
    'Tutorials': ['Tutorials'],
    'Applications': ['Applications'],
    'AI engineering': ['AI engineering'],
    'Model development': ['Model development'],
    'Model repo': ['Model repo'],
    'Infrastructure': ['Infrastructure'],
    'Lists': ['Lists']
}

presets = {
    'Balanced': {'stargazers_count': 0.5, 'forks_count':0.5, 'days_since_created':0.5},
    'Popularity Focused': {'stargazers_count': 0.9, 'forks_count':0.3, 'days_since_created':0.5},
    'Contribution Focused': {'stargazers_count': 0.3, 'forks_count':0.9, 'days_since_created':0.5},
}

selected_category_preset = st.selectbox('Select a category', options=list(category_presets.keys()))
# Dropdown for selecting a preset
selected_preset = st.selectbox('Select a weights preset', options=list(presets.keys()))

# Get the weights for the selected preset
selected_weights = presets[selected_preset]

weight_stargazers_count = st.slider('Weight for Stars', min_value=0.0, max_value=1.0, value=selected_weights['stargazers_count'], step=0.1)
weight_forks_count = st.slider('Weight for Forks', min_value=0.0, max_value=1.0, value=selected_weights['forks_count'], step=0.1)
weight_days_since_created = st.slider('Weight for Repository Age (Days)', min_value=0.0, max_value=1.0, value=selected_weights['days_since_created'], step=0.1)

weights = {'stargazers_count': weight_stargazers_count, 'forks_count':weight_forks_count, 'days_since_created': weight_days_since_created}

df_adjusted = df[df['categories'].isin(category_presets[selected_category_preset])]

# Calculate and display ranked projects
df_adjusted['Weighted_Score'] = sum(df_adjusted[factor] * weight for factor, weight in weights.items())
df_filtered = df_adjusted[['name', 'description', 'categories', 'stargazers_count', 'forks_count', 'Weighted_Score']]

st.write('Ranked Projects:', df_filtered.nlargest(30, ['Weighted_Score']))

fig = px.scatter(df_adjusted.nlargest(30, ['Weighted_Score']), x="forks_count", y="stargazers_count", size='days_since_created', hover_data=['name', 'license'], title="The Most Impactful OSS Projects")
# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)
st.caption("Fig. 4. Size of each point representing the repository's age.")