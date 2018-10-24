from gmplot import gmplot
from flask import Flask, render_template, url_for, send_from_directory, request, redirect
import os.path


def draw_goggle_map(lst, file_name='my_map.html', user_latitude=59.980655, user_longitude=30.324426):
    """
    Основной метод, рисует карту. В процессе работы создает файл с указыным именем в 'templates', но не удаляет его.
    :param lst:              Список локаций.
    :param file_name:        С каким именем сохранить файл
    :param user_latitude:    Широта, по которой центрируется карта
    :param user_longitude:   Долгота, по которой центрируется карта
    :param host:             Собственно, где будем хоститься
    :return:
    """
    gmap = gmplot.GoogleMapPlotter(user_latitude, user_longitude, 15, apikey='AIzaSyDbdUT9KE3bRf9PtkibgvAiuB4fLdFDWrU')
    for marker in lst:
        hidden_gem_lat, hidden_gem_lon = marker['latitude'], marker['longitude']
        gmap.marker(hidden_gem_lat, hidden_gem_lon, 'red', title=marker['name'])
    gmap.color = 'F0000'
    gmap.coloricon = '/uploads/%s.png'
    print(gmap.coloricon)
    gmap.draw('templates/' + file_name)


UPLOAD_FOLDER = 'markers'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def get_map():
    return render_template('my_map.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    draw_goggle_map([{'name': 'Test', 'latitude': 59.980655, 'longitude': 30.324426},
                     {'name': 'Test_1', 'latitude': 59.970655, 'longitude': 30.326426}])
    app.run()
