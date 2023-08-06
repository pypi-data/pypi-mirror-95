# async_videoindexer
An async video indexer package for querying [Microsoft Media Services Video Indexer](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/) in Python.

# Installation
   ```bash
   $ pip3 install aio-videoindexer
   ```


# Usage:
```python
from asyncvideoindexer import AsyncVideoIndexer

VIDEO_INDEXER_ACCOUNT_ID = "your-account-id"
VIDEO_INDEXER_KEY = "your-account-key"
VIDEO_INDEXER_ACCOUNT_LOCATION = "your-account-location"


async def get_video_indexer():
    video_indexer = await AsyncVideoIndexer.create(
        VIDEO_INDEXER_ACCOUNT_ID,
        VIDEO_INDEXER_KEY,
        VIDEO_INDEXER_ACCOUNT_LOCATION,
    )
```

For more information, see [https://aio-videoindexer.readthedocs.io/en/latest/](https://aio-videoindexer.readthedocs.io/en/latest/).

# Contact Information
Feel free to contact me [on Twitter](https://twitter.com/sealjay_clj). For bugs, please raise an issue on GitHub.

aio-videoindexer is available under the [MIT Licence](./LICENCE).

# Background
Forked from my [Teams Vid](https://github.com/sealjay-clj/teams-vid) project.

# Contributing
Contributions are more than welcome.
- Create a fork
- Create a feature branch `git checkout -b feature/featurename`
- Commit your changes `git commit -am 'Fixed a bug'`
- Push to the branch `git push`
- Create a new Pull Request to this repository