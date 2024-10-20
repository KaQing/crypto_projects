import pandas as pd
import requests
from bs4 import BeautifulSoup

# Create a list for page numbers, adjust to max pages for coingecko
page_list = list(range(1, 150))
all_tokens = []  # Initialize a list to store data from all pages

# Loop through the pages
for page in page_list:
    # URL to the CoinGecko table (update the page number in the URL)
    url = f"https://www.coingecko.com/de?page={page}"
    
    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all rows in the table containing token data
    rows = soup.find_all('tr')  # Assuming token data is in table rows
    
    # Loop through each row to extract token name, symbol, and market cap
    for row in rows:
        # Find the outer div for the token name and symbol
        outer_div = row.find('div', class_='tw-text-gray-700 dark:tw-text-moon-100 tw-font-semibold tw-text-sm tw-leading-5')
        
        # if outer_div exists we get the token name and the inner_div
        if outer_div:
            # Extract token name
            token_name = outer_div.contents[0].strip()  # Get only the first part of the div
            inner_div = outer_div.find('div')  # Find the inner div for token symbol
    
            # Extract token symbol from the text of the inner_div
            token_symbol = inner_div.get_text(strip=True) if inner_div else ""
    
            # Find the market cap in the appropriate <td>
            market_cap_td = row.find_all('td', class_='tw-text-end tw-px-1 tw-py-2.5 2lg:tw-p-2.5 tw-bg-inherit tw-text-gray-900 dark:tw-text-moon-50')
    
    
            # Initialize market cap as "N/A"
            market_cap = "N/A"  # Default value in case of failure
            
            # Market cap extraction with added safety checks
            if len(market_cap_td) > 5:
                market_cap_span = market_cap_td[5].find('span')
                if market_cap_span:  # Check if the span element exists
                    market_cap = market_cap_span.get_text(strip=True)

            # Store the token information in a dictionary
            token_info = {
                'Token Name': token_name,
                'Token Symbol': token_symbol,
                'Market Cap': market_cap
            }
            all_tokens.append(token_info)  # Append each token's info to the list
    
            # Print the results
            print(f"Token Name: {token_name}")
            print(f"Token Symbol: {token_symbol}")
            print(f"Market Cap: {market_cap}")
            print()  # Just to add a blank line between entries

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_tokens)

# Save the DataFrame to a CSV file
df.to_csv('coingecko_tokens.csv', index=False)

# Display the DataFrame
print(df)