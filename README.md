本项目为个人学习与研究目的开源。NetShort 的协议分析均由我独立完成。此前在与 **枫叶互动（北京）公司** 的技术交流中，对方整体水平过于低下，反复询问实现细节只为白嫖方案，却未推进任何实质合作。为避免重复解释，现将方案公开，供社区参考。技术应当开放，而不是被用来消耗他人时间。其中公钥私钥自行在git上其他地方寻找，开源一大堆。不会问AI。

This project is open-sourced for personal learning and research purposes. The protocol analysis of NetShort was completed independently by me. During previous technical exchanges with **Crazy Maple Studio**, the overall level of the other party was too low—they repeatedly asked about implementation details solely to get the solution for free, yet did not advance any substantive cooperation. To avoid repeating explanations, I am now making the solution public for the community's reference. Technology should be open, rather than being used to consume others' time. As for the public and private keys, find them yourself elsewhere on Git—there are plenty in open source. If you don't know, ask AI.

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
