

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the webpage want to scrape
url = 'https://results.eci.gov.in'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a list to store the data
    data = []

    # List of classes to scrape
    classes = [
        'state-item blue-bg pc-wrap',
        'state-item olive-bg',
        'state-item pine-bg',
        'state-item gry-bg' 
    ]

    # Loop through each class and scrape data
    for class_name in classes:
        element = soup.find('div', class_=class_name)
        if element:
            h2_text = element.find('h2').text.strip() if element.find('h2') else ''
            h1_text = element.find('h1').text.strip() if element.find('h1') else ''
            a_href = element.find('a')['href'].strip() if element.find('a') else ''
            data.append([h2_text, h1_text, a_href])

    # Example: scraping specific details like 'ANDHRA PRADESH', 'ODISHA', 'BYE ELECTIONS'
    states_data = soup.find_all('div', class_='state-card')  

    for state in states_data:
        state_name = state.find('h2').text.strip() if state.find('h2') else ''  
        assembly_constituencies = state.find('span', class_='assembly-constituencies').text.strip() if state.find('span', 'assembly-constituencies') else ''  
        data.append([state_name, '', '', assembly_constituencies])

    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=['Parliamentary Constituencies', 'Assembly Constituencies', 'Result Link'])

    # Save the DataFrame to a CSV file
    df.to_csv('Election_Results.csv', index=False)

    print('Data saved to Election_Results.csv')

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
