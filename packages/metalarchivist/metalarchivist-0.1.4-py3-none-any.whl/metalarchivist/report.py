from .export import Band, Album

import pandas as pd


def get_bands(profile_urls: list[str], verbose=False) -> pd.DataFrame:
    band_profile = Band.get_profiles(profile_urls, verbose=verbose)
    band_profile = pd.DataFrame(list(map(lambda n: n.to_dict(), band_profile)))
    band_profile_desc = pd.DataFrame(list(band_profile['description']))

    band_profile = band_profile.drop(columns=['description'])
    genres = pd.DataFrame(list(band_profile['genres']))
    themes = pd.DataFrame(list(band_profile['themes']))

    band_profile = band_profile.drop(columns=['genres', 'themes'])
    band_profile_desc = band_profile_desc.drop(columns=['genre', 'themes', 'lyrical_themes'])

    return pd.concat([band_profile, band_profile_desc, genres, themes], axis=1)


def get_albums(range_start=None, range_stop=None, verbose=False) -> pd.DataFrame:
    if range_start:
        release_page = Album.get_range(range_start, range_stop, verbose=verbose)
    else:
        release_page = Album.get_upcoming(verbose=verbose)

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
