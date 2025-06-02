def set_max_count_to_app(app, csv_data, precision=2):
    full_data = csv_data.copy()

    full_data['lat_round'] = full_data['Latitude'].round(precision)
    full_data['lon_round'] = full_data['Longitude'].round(precision)

    grouped_full = full_data.groupby(['lat_round', 'lon_round']).size()

    app.max_missions = grouped_full.max()
