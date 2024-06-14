import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_movie_data():
    page_url = 'https://www.imdb.com/search/title/?title_type=feature'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Lists to store data
    names, years, durations, rates, ratings, hrefs, genres, image_urls = [], [], [], [], [], [], [], []

    # Find all movie containers
    movie_containers = soup.find_all('div', class_='sc-74bf520e-3 klvfeN dli-parent')

    for container in movie_containers:
        # Name
        name_tag = container.find('h3', class_='ipc-title__text')
        name = name_tag.text.split('. ')[1] if name_tag else 'N/A'
        names.append(name)

        # Metadata
        metadata_tag = container.find('div', class_='sc-b189961a-7 feoqjK dli-title-metadata')
        metadata_items = metadata_tag.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')

        # Year
        year = metadata_items[0].text if len(metadata_items) > 0 else 'N/A'
        years.append(year)

        # Duration
        duration = metadata_items[1].text if len(metadata_items) > 1 else 'N/A'
        durations.append(duration)

        # Certification
        rate = metadata_items[2].text if len(metadata_items) > 2 else 'N/A'
        rates.append(rate)

        # Rating
        rating_tag = container.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
        rating = rating_tag['aria-label'].split()[2] if rating_tag else 'N/A'  # Extract numeric rating value
        ratings.append(rating)

        # Href
        href_tag = container.find('a', class_='ipc-lockup-overlay ipc-focusable')
        href = 'https://www.imdb.com' + href_tag['href'] if href_tag else 'N/A'
        hrefs.append(href)

        # Request genre information from movie detail page
        if href != 'N/A':
            try:
                response = requests.get(href, headers=headers)
                soup_genre = BeautifulSoup(response.content, 'html.parser')

                # Genres
                genre_tags = soup_genre.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
                genre_list = [genre.text for genre in genre_tags]
                genres.append(', '.join(genre_list) if genre_list else 'N/A')

                # Image URL
                image_div = soup_genre.find('div', class_='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img')
                if image_div:
                    image_tag = image_div.find('img')
                    image_url = image_tag['src'] if image_tag else 'N/A'
                    image_urls.append(image_url)
                else:
                    image_div_alt = soup_genre.find('div', class_='ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2')
                    if image_div_alt:
                        image_tag = image_div_alt.find('img')
                        image_url = image_tag['src'] if image_tag else 'N/A'
                        image_urls.append(image_url)
                    else:
                        print(f"Image div not found for {href}")
                        image_urls.append('N/A')

            except Exception as e:
                print(f"Error fetching data for {href}: {e}")
                genres.append('N/A')
                image_urls.append('N/A')

    # Create a DataFrame to store the data
    movies_df = pd.DataFrame({
        'Name': names,
        'Year': years,
        'Duration': durations,
        'Rate': rates,
        'Rating': ratings,
        'Genres': genres,
        'Image_URL': image_urls,
        'URL': hrefs
    })

    return movies_df
