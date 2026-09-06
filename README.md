# NetShort-API

A simple API wrapper to fetch NetShort series episodes and details via `book_id`.

## Features

- Get series details (title, cover, total episodes, tags, etc.)
- Fetch episode video URLs (1080p/720p/480p)
- Batch download support
- Lightweight and easy to integrate

## Usage

```python
if __name__ == '__main__':
    book_id = '2095785831247122434'
    ptest1 = NetShortDownloadAPI()
    episode_data = ptest1.get_episodes_from_unlockAdEpisode(book_id)
    print(episode_data['shortPlayEpisodeInfos'])
```
