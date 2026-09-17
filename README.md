本项目为个人学习与研究目的而开源。在实现过程中，我独立完成了对 NetShort 协议的分析与还原。考虑到相关技术方案已被多次询问，且部分交流方缺乏基本的逆向工程能力，我决定将实现公开，供社区参考与学习。

This project is open-sourced for personal learning and research purposes. During implementation, I independently completed the analysis and reverse-engineering of the DramaBox and NetShort protocols. Since the technical approach has been repeatedly requested, and some parties lack basic reverse-engineering capability, I decided to make the implementation public for the community to reference and learn from.

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
