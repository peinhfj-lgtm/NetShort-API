本项目为个人学习与研究目的开源。NetShort 的协议分析均由我独立完成。此前在与某公司的技术交流中，对方反复询问实现思路，却未推进任何实质合作。为避免重复解释，现将方案公开，供社区参考。技术应当开放，而不是被用来消耗他人时间。
This project is open-sourced for personal learning and research. The protocol analysis for NetShort was done independently by me. During a previous technical exchange with a company, the other party repeatedly asked for implementation details without moving forward with any substantive collaboration. To avoid repeating explanations, I am making the approach public for the community. Technology should be open, not used to waste other people's time.

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
