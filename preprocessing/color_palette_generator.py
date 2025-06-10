import matplotlib.colors as mcolors
import seaborn as sns

def generate_country_colors(data, column='Country', fallback_palette='Set2'):
    manual_colors = {
        'USA': '#4F8EF7',     
        'Russia': '#F74F4F',    
        'Kazakhstan': '#FFB84D',
        'Ukraine': '#F7B32B',   
        'China': '#FF8C8C',     
        'Germany': '#23263A',  
        'France': '#7EC4FF',  
        'UK': '#FFD166',
        'Others': "#C3C3C3",       
    }

    all_countries = data[column].unique().tolist()
    remaining_countries = [c for c in all_countries if c not in manual_colors]

    fallback_colors = sns.color_palette(fallback_palette, len(remaining_countries))
    fallback_hex = [mcolors.to_hex(c) for c in fallback_colors]
    auto_color_map = dict(zip(remaining_countries, fallback_hex))

    return {**manual_colors, **auto_color_map}