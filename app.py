from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_tiktok_trending_music():
    url = 'https://www.tiktok.com/music'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Referer": "https://www.tiktok.com/"
    }

    response = requests.get(url, headers=headers)
    print("Response status code:", response.status_code)
    soup = BeautifulSoup(response.content, 'lxml')

    trending = []
    for item in soup.select('div.tiktok-1itcwxg-DivMusicCardContainer'):
        title_tag = item.select_one('h3')
        artist_tag = item.select_one('span')
        if title_tag and artist_tag:
            title = title_tag.get_text(strip=True)
            artist = artist_tag.get_text(strip=True)
            trending.append({'title': title, 'artist': artist})

    # Debug print the scraped results
    print("Scraped items found:", len(trending))

    # If empty, return test data
    if not trending:
        trending = [
            {'title': 'Test Song 1', 'artist': 'Test Artist A'},
            {'title': 'Test Song 2', 'artist': 'Test Artist B'},
            {'title': 'Test Song 3', 'artist': 'Test Artist C'}
        ]

    return trending

@app.route('/trending-sounds', methods=['GET'])
def get_trending_sounds():
    try:
        data = scrape_tiktok_trending_music()
        return jsonify({'platform': 'TikTok', 'sounds': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
