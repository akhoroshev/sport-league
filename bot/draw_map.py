from gmplot import gmplot


def draw_goggle_map(lst, file_name='my_map.html', user_latitude=59.980655, user_longitude=30.324426):
    """
    :param lst:              Список локаций.
    :param file_name:        С каким именем сохранить файл
    :param user_latitude:    Широта, по которой центрируется карта
    :param user_longitude:   Долгота, по которой центрируется карта
    :return:                 Ничего не возращает
    """
    gmap = gmplot.GoogleMapPlotter(user_latitude, user_longitude, 15, apikey='AIzaSyDbdUT9KE3bRf9PtkibgvAiuB4fLdFDWrU')
    for marker in lst:
        hidden_gem_lat, hidden_gem_lon = marker['latitude'], marker['longitude']
        gmap.marker(hidden_gem_lat, hidden_gem_lon, 'red', title=marker['name'])
    gmap.draw(file_name)
