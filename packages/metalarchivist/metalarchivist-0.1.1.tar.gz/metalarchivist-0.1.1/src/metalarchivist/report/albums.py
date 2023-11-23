from ..export import Albums
from .bands import get_bands

import pandas as pd


def get_albums(range_start=None, range_stop=None, verbose=False):
    if range_start:
        release_page = Albums.get_range(range_start, range_stop, verbose=verbose)
    else:
        release_page = Albums.get_upcoming(verbose=verbose)

    release = pd.DataFrame(release_page.data)

    # hoist out the link attributes from each band
    profile_urls = release['band'].apply(lambda n: n['link'])
    profile_urls = pd.DataFrame(profile_urls.to_list(), columns=['band_url'])

    band = get_bands(list(profile_urls['band_url'].unique()), verbose=verbose)

    album = pd.DataFrame(list(release['album']))
    album = album.rename(columns=dict(name='album', link='album_url'))

    band = band.rename(columns=dict(url='band_url'))
    release = release.drop(columns=['genres', 'band', 'album'])
    album = pd.concat([album, profile_urls, release], axis=1)

    return pd.merge(left=album, right=band, how='left', 
                    left_on='band_url', right_on='band_url')
