
import json
from dataclasses import asdict

import pandas as pd

from ..export import Band


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
