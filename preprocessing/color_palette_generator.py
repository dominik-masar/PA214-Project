import matplotlib.colors as mcolors
import seaborn as sns

def generate_country_colors(data, column='Country', fallback_palette='hls'):
    manual_colors = {
        'USA': '#2d4ed2',
        'India': '#ea9a15',
        'Kazakhstan': '#15d7ea',
        'France': '#dbe11e',
        'Russia': '#ff0c00',
        'Pacific Ocean': '#5da0ff',
        'Japan': '#fea2ff'
    }

    all_countries = data[column].unique().tolist()

    remaining_countries = [c for c in all_countries if c not in manual_colors]

    fallback_colors = sns.color_palette(fallback_palette, len(remaining_countries))
    fallback_hex = [mcolors.to_hex(c) for c in fallback_colors]
    auto_color_map = dict(zip(remaining_countries, fallback_hex))

    return {**manual_colors, **auto_color_map}