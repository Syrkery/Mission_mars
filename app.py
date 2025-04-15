from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    page_title = request.args.get('title', 'Страница подготовки к миссии')
    return render_template('base.html', title=page_title)


@app.route('/training/<prof>')
def training(prof):
    lower_prof = prof.lower()
    if ('инженер' in lower_prof) or ('строитель' in lower_prof):
        heading = "Инженерные тренажёры"
        image_filename = 'engineer.png'
    else:
        heading = "Научные симуляторы"
        image_filename = 'science.png'

    page_title = "Тренировки на Марсе"
    return render_template(
        'training.html',
        title=page_title,
        heading=heading,
        image=image_filename
    )


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = [
        "инженер-исследователь",
        "пилот",
        "строитель",
        "экзобиолог",
        "врач",
        "инженер по терраформированию",
        "климатолог",
        "специалист по радиационной защите",
        "астрогеолог",
        "гляциолог",
        "инженер-жизнеобеспечения",
        "оператор марсохода",
        "киберинженер",
        "штурман",
        "пилот дронов"
    ]
    page_title = "Список профессий"
    return render_template(
        'list_prof.html',
        title=page_title,
        list_type=list_type,
        professions=professions
    )


@app.route('/answer')
def auto_answer():

    user_data = {
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }

    return render_template('auto_answer.html', **user_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        astronaut_id = request.form.get('astronaut_id')
        astronaut_password = request.form.get('astronaut_password')
        captain_id = request.form.get('captain_id')
        captain_token = request.form.get('captain_token')

        cur = sqlite3.connect('mission_bd.sqlite').cursor()
        try:
            pass_ast = cur.execute("""SELECT password FROM Astrounat WHERE Id = ?""", astronaut_id)
        except sqlite3.Error as error:
            print(error)
        try:
            pass_capt = cur.execute("""SELECT password FROM Captian WHERE Id = ?""", captain_id)
        except sqlite3.Error as error:
            print(error)

        print("Получены данные:")
        print("ID астронавта:", astronaut_id)
        print("Пароль астронавта:", astronaut_password)
        print("ID капитана:", captain_id)
        print("Пароль капитана:", captain_token)

        return "Данные получены. Астронавт: {}, Капитан: {}".format(astronaut_id, captain_id)
    else:
        return render_template('login.html', title='Аварийный доступ')


@app.route('/distribution')
def distribution():
    astronauts = [
        "Ридли Скотт",
        "Энди Уир",
        "Марк Уотни",
        "Венката Капур",
        "Тедди Сандерс",
        "Шон Бин"
    ]
    return render_template(
        'distribution.html',
        title='Размещение по каютам',
        astronauts=astronauts
    )


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='127.0.0.1')
