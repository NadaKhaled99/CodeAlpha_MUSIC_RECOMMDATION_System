import streamlit as st
import pickle
import pandas as pd
import requests
import urllib.parse
'''
Fixing URL Format: Ensure the music title in the URL is properly encoded to handle spaces and special characters.
Error Handling: Add error handling for the API request and potential missing data.
Refactor Fetch Poster Function: Simplify the function and make sure it checks the response properly.
Improve Readability: Add comments and refactor for better readability.
'''
'''
Explanation of Changes:
URL Encoding: The urllib.parse.quote() function ensures that the music title is properly encoded for the URL.
Error Handling: Added try-except blocks to handle errors gracefully for both fetching posters and recommendations.
Streamlit Error Messages: Use st.error() to display error messages within the Streamlit app.
Return None on Error: If fetching a poster fails, return None and handle it in the main recommendation function to avoid breaking the app.
Simplified Poster Handling: Added a check to display a placeholder text if a poster is not available.
'''
# Load music data and similarity matrix
#music_dict = pickle.load(open('music_rec.pkl', 'rb'))
#music_df = pd.DataFrame(music_dict)
#similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))

# Assuming 'file_path' contains the correct path to your file
with open(/content/drive/MyDrive/SpotifyDataset/TrainData/ex.csv, 'rb') as f:
    # Process the file contents using f here
    # For example:
    music_dict = pickle.load(f)


# Fetch poster for a given music title
#Key Parts of the Code
#1. Fetching the Poster

def fetch_poster(music_title):
    try:
        # Properly encode the music title to handle special characters and spaces
        encoded_title = urllib.parse.quote(music_title)
        response = requests.get(f"https://saavn.me/search/songs?query={encoded_title}&page=1&limit=2")
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        # Return the poster link if available
        return data['data']['results'][0]['image'][2]['link']
    except Exception as e:
        st.error(f"Error fetching poster for {music_title}: {e}")
        return None  # Return None if there's an issue
'''
Changes Made:

Encoding the Title: Used urllib.parse.quote() to encode the music title. This ensures that the URL is correctly formatted even if the title contains spaces or special characters.
Error Handling: Wrapped the API call in a try-except block to catch and handle any exceptions, such as network issues or incorrect responses. This prevents the app from crashing and provides user feedback with st.error().
Return Value: Returns None if there's an error fetching the poster, so the calling function can handle this case.
'''
#2. Recommending Music
def recommend(musics):
    try:
        music_index = music[music['title'] == musics].index[0]
        distances = similarity[music_index]
        music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_music = []
        recommended_music_poster = []
        for i in music_list:
            music_title = music.iloc[i[0]].title
            recommended_music.append(music_title)
            poster_link = fetch_poster(music_title)
            recommended_music_poster.append(poster_link if poster_link else "")
        return recommended_music, recommended_music_poster
    except IndexError:
        st.error("Music not found in the dataset.")
        return [], []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [], []
'''
Handling Index Errors: Added a try-except block to handle cases where the selected music title is not found in the dataset. This prevents the app from crashing and informs the user.
General Exception Handling: Added a general exception handler to catch and report any other errors.
Check for Poster Links: Ensures that a missing poster link does not break the app by appending an empty string if no poster is found.
'''
#3.Load data
music_dict = pickle.load(open('music_rec.pkl', 'rb'))
music = pd.DataFrame(music_dict)
similarity = pickle.load(open('similarities.pkl', 'rb'))
'''
Explanation:
Loading Pickled Data: The music dataset and similarity matrix are loaded from pickled files. The dataset is converted to a DataFrame for easier manipulation.
'''
#4.Streamlit App Structure
st.title('Music Recommendation System')

# Dropdown for selecting music
selected_music_name = st.selectbox('Select a music you like', music['title'].values)

# Dropdown for selecting music
# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_music_name)
    if names:
        # Display recommendations in columns
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                if poster:
                    st.image(poster)
                else:
                    st.text("Poster not available")
'''
Changes Made:

Title and Dropdown: Added a title and a dropdown for selecting music using st.title() and st.selectbox().
Recommend Button: Added a button that triggers the recommendation function.
Displaying Results: Used columns to display recommended music titles and their posters. If a poster is not available, it displays a placeholder text.

Benefits of These Changes
URL Encoding: Ensures that the API request works correctly for all music titles.
Error Handling: Prevents the app from crashing and provides useful feedback to the user if something goes wrong.
Robustness: The app can handle missing data and unexpected issues gracefully.
User Feedback: The app informs the user if there is an issue fetching data or if the selected music is not in the dataset.
Readability: Improved code readability and maintainability with comments and better structure.

'''

'''
Application Interface
Title: At the top of the page, you will see the title "Music Recommendation System".

Dropdown Menu: Below the title, there is a dropdown menu where you can select a music title from the dataset. The dropdown is populated with values from the music['title'].values.

Recommend Button: Below the dropdown, there is a "Recommend" button. When you click this button, the app fetches recommendations based on the selected music title.

Recommendations Display: After clicking the "Recommend" button, the app displays five recommended music titles along with their corresponding posters. These are displayed in a row, each in a separate column.

Example Output
Let's walk through an example scenario:

Selecting a Music Title: You select "Shape of You" from the dropdown menu.

Clicking the Recommend Button: You click the "Recommend" button.

Displaying Recommendations: The app performs the following:

It finds similar music titles based on the precomputed similarity matrix.
It fetches the poster images for each recommended music title using the fetch_poster function.
It displays the recommended titles and their posters in five columns.
'''
