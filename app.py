from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sladkiy-ray-secret'
DB_PATH = os.path.join(os.path.dirname(__file__), 'cakes.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    # Таблица тортов
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article TEXT NOT NULL,
            name TEXT NOT NULL,
            unit TEXT DEFAULT 'шт.',
            price REAL NOT NULL,
            brand TEXT,
            cake_type TEXT,
            category TEXT,
            discount INTEGER DEFAULT 0,
            stock INTEGER DEFAULT 0,
            description TEXT,
            photo TEXT
        )
    ''')

    # Таблица пользователей
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Заполнение тортов
    count = conn.execute('SELECT COUNT(*) FROM cakes').fetchone()[0]
    if count == 0:
        cakes = [
            ('T001C1', 'Наполеон', 'шт.', 2190, 'Сладкая радость', 'Классический бисквитный', 'Праздничный', 5, 8, 'Классический торт "Наполеон" с заварным кремом и слоеными коржами, 2 кг', 'napoleon.jpg'),
            ('T002F4', 'Красный бархат', 'шт.', 3244, 'Вкусный дом', 'Американский', 'День рождения', 2, 13, 'Яркий бисквит с какао и сливочно-сырным кремом "Чизкейк", 1.8 кг', 'red_velvet.jpg'),
            ('T003B5', 'Медовик', 'шт.', 4499, 'Сладкая радость', 'Классический медовый', 'Любой повод', 4, 5, 'Нежный торт с медовыми коржами и сметанным кремом, 2 кг', 'medovik.jpg'),
            ('T004R7', 'Птичье молоко', 'шт.', 3900, 'Тортэйшн', 'Суфлейный (с агар-агаром)', 'Юбилей', 2, 8, 'Воздушное суфле на агар-агаре и шоколадная глазурь по ГОСТу, 1.5 кг', 'ptichye_moloko.jpg'),
            ('T005M3', 'Трюфельный', 'шт.', 3800, 'Вкусный дом', 'Шоколадный муссовый', 'Для него', 2, 16, 'Шоколадный торт с нежным муссом и карамельной прослойкой, 1.7 кг', 'truffel.jpg'),
            ('T006K8', 'Фруктовый рай', 'шт.', 4100, 'Фруттиссимо', 'Фруктово-ягодный', 'Летний, Свадьба', 3, 6, 'Легкий бисквит с йогуртовым кремом и свежими сезонными ягодами, 2 кг', 'fruit_paradise.jpg'),
            ('T007H7', 'Прага', 'шт.', 2700, 'Сладкая радость', 'Шоколадный бисквитный', 'Праздничный', 2, 14, 'Шоколадный торт по рецепту пражского ресторана, с абрикосовым конфитюром, 1.6 кг', 'prague.jpg'),
            ('T008H3', 'Капкейки "Ассорти" (12 шт.)', 'шт. (набор)', 1890, 'Кексик и Ко', 'Капкейки', 'Детский праздник', 4, 4, 'Набор из 12 капкейков с разными начинками и украшениями', 'cupcakes.jpg'),
            ('T009R5', 'Сникерс', 'шт.', 4300, 'Вкусный дом', 'Десертный (с нугой и карамелью)', 'Для нее', 2, 6, 'Торт-десерт на основе знаменитого батончика: арахис, нуга, карамель, шоколад, 1.8 кг', 'snickers.jpg'),
            ('T010E4', 'Морковный торт', 'шт.', 2800, 'Сладкая радость', 'Овощной бисквитный', 'Здоровое питание', 3, 15, 'Влажный бисквит с морковью, орехами и сливочным сыром, 1.5 кг', 'carrot_cake.jpg'),
            ('T011E3', 'Чизкейк Нью-Йорк', 'шт.', 3556, 'Тортэйшн', 'Чизкейк (выпеченный)', 'Фуршет, Кофе-брейк', 3, 6, 'Классический выпеченный чизкейк на песочной основе, 1.2 кг', 'ny_cheesecake.jpg'),
            ('T012B5', 'Малиновый меридиан', 'шт.', 3800, 'Фруттиссимо', 'Ягодный муссовый', 'Свадьба', 2, 14, 'Нежное малиновое муссовое кольцо на миндальном бисквите, 1.6 кг', 'raspberry_mousse.jpg'),
            ('T013R4', 'Детский "Смешарики"', 'шт.', 5500, 'Вкусный дом', 'Тематический бисквитный', 'Детский праздник', 3, 6, 'Торт в виде любимых персонажей, цветной бисквит, сливочный крем, 2.5 кг', 'smeshariki.jpg'),
            ('T014F4', 'Кофейный "Гляссе"', 'шт.', 2100, 'Тортэйшн', 'Кофейно-сливочный', 'Для взрослых', 2, 3, 'Торт со вкусом кофе гляссе, кофейные коржи и нежный крем, 1.4 кг', 'coffee_glace.jpg'),
            ('T015F5', 'Свадебная феерия (3 яруса)', 'шт.', 15400, 'Вкусный дом', 'Многоярусный бисквитно-муссовый', 'Свадебный', 4, 1, 'Трехъярусный свадебный торт с ванильным муссом и цветочным декором из мастики, 7 кг', 'wedding_cake.jpg'),
            ('T016F4', 'Тирамису', 'шт.', 4600, 'Сладкая радость', 'Итальянский десерт', 'Романтический ужин', 2, 9, 'Классическое тирамису на основе маскарпоне, савоярди и кофе, 1.5 кг', 'tiramisu.jpg'),
            ('T017R5', 'Пирожное "Картошка" (10 шт.)', 'шт. (набор)', 900, 'Кексик и Ко', 'Кондитерское изделие', 'Чайный стол', 3, 12, 'Набор из 10 пирожных "Картошка", посыпанных какао', 'kartoshka.jpg'),
            ('T018G4', 'Лимонный курд', 'шт.', 6800, 'Фруттиссимо', 'Цитрусовый муссовый', 'Весенний праздник', 3, 15, 'Освежающий торт с лимонным курдом, безе и хрустящим слоем, 1.8 кг', 'lemon_curd.jpg'),
            ('T019G5', 'Черный лес', 'шт.', 4200, 'Тортэйшн', 'Шоколадно-вишневый', 'Праздничный', 2, 9, 'Немецкий торт с шоколадными бисквитами, вишней и взбитыми сливками, 2 кг', 'black_forest.jpg'),
            ('T020R5', 'Безглютеновый шоколадный', 'шт.', 4800, 'Вкусный дом', 'Безглютеновый', 'Для аллергиков', 4, 11, 'Богатый шоколадный торт на миндальной муке, без глютена и лактозы, 1.5 кг', 'gluten_free.jpg'),
        ]
        conn.executemany(
            'INSERT INTO cakes (article, name, unit, price, brand, cake_type, category, discount, stock, description, photo) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            cakes
        )

    # Заполнение пользователей из файла импорта
    user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if user_count == 0:
        users = [
            ('Администратор', 'Кондратьева Алиса Михайловна', 'kondratieva@cake-shop.ru', 'AdCk76#'),
            ('Администратор', 'Волошин Игорь Сергеевич', 'voloshin@cake-shop.ru', 'XyZ$89p'),
            ('Администратор', 'Сладкоежкина Виктория Павловна', 'sladkoezhkina@cake-shop.ru', 'T0rt!k45'),
            ('Менеджер', 'Кремов Артем Дмитриевич', 'kremov@cake-shop.ru', 'Mn7@gP23'),
            ('Менеджер', 'Бисквитов Петр Владимирович', 'biskvitov@cake-shop.ru', 'Rt5#fH67'),
            ('Менеджер', 'Ягодная Елена Игоревна', 'yagodnaya@cake-shop.ru', 'Ber3ry$1'),
            ('Авторизированный клиент', 'Сахарова Анна Викторовна', 'saharova.client@mail.ru', 'Cli3nt#9'),
            ('Авторизированный клиент', 'Вафельный Максим Олегович', 'waffle.client@gmail.com', 'WafFl3$5'),
            ('Авторизированный клиент', 'Шоколадов Кирилл Александрович', 'chocolate.client@yandex.ru', 'Ch0c0L8*'),
            ('Авторизированный клиент', 'Фруктовская Ольга Сергеевна', 'fruit.client@outlook.com', 'FrU1t%22'),
        ]
        conn.executemany(
            'INSERT INTO users (role, full_name, login, password) VALUES (?,?,?,?)',
            users
        )

    conn.commit()
    conn.close()


# ── АУТЕНТИФИКАЦИЯ ──────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        password_val = request.form.get('password', '').strip()

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE login = ? AND password = ?',
            (login_val, password_val)
        ).fetchone()
        conn.close()

        if user:
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('login.html')


# ── КАТАЛОГ ТОРТОВ ──────────────────────────────────────────────────────────

@app.route('/cakes')
def index():
    conn = get_db()
    search = request.args.get('search', '').strip()
    brand_filter = request.args.get('brand', '').strip()
    sort = request.args.get('sort', '')

    query = 'SELECT * FROM cakes WHERE 1=1'
    params = []
    if search:
        query += ' AND (name LIKE ? OR description LIKE ? OR article LIKE ?)'
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    if brand_filter:
        query += ' AND brand = ?'
        params.append(brand_filter)

    if sort == 'price_asc':
        query += ' ORDER BY price ASC'
    elif sort == 'price_desc':
        query += ' ORDER BY price DESC'
    elif sort == 'name':
        query += ' ORDER BY name ASC'
    elif sort == 'discount':
        query += ' ORDER BY discount DESC'
    else:
        query += ' ORDER BY id ASC'

    cakes = conn.execute(query, params).fetchall()
    brands = [r[0] for r in conn.execute('SELECT DISTINCT brand FROM cakes ORDER BY brand').fetchall()]
    conn.close()
    return render_template('index.html', cakes=cakes, brands=brands,
                           search=search, brand_filter=brand_filter, sort=sort)


@app.route('/cake/new', methods=['GET', 'POST'])
def new_cake():
    if request.method == 'POST':
        data = (
            request.form['article'], request.form['name'], request.form['unit'],
            float(request.form['price']), request.form['brand'], request.form['cake_type'],
            request.form['category'], int(request.form['discount']),
            int(request.form['stock']), request.form['description'], request.form['photo']
        )
        conn = get_db()
        conn.execute(
            'INSERT INTO cakes (article,name,unit,price,brand,cake_type,category,discount,stock,description,photo) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            data
        )
        conn.commit()
        conn.close()
        flash('Торт успешно добавлен!', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', cake=None, title='Добавить торт')


@app.route('/cake/<int:cake_id>/edit', methods=['GET', 'POST'])
def edit_cake(cake_id):
    conn = get_db()
    cake = conn.execute('SELECT * FROM cakes WHERE id=?', (cake_id,)).fetchone()
    if not cake:
        conn.close()
        flash('Торт не найден', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        data = (
            request.form['article'], request.form['name'], request.form['unit'],
            float(request.form['price']), request.form['brand'], request.form['cake_type'],
            request.form['category'], int(request.form['discount']),
            int(request.form['stock']), request.form['description'], request.form['photo'],
            cake_id
        )
        conn.execute(
            'UPDATE cakes SET article=?,name=?,unit=?,price=?,brand=?,cake_type=?,category=?,discount=?,stock=?,description=?,photo=? WHERE id=?',
            data
        )
        conn.commit()
        conn.close()
        flash('Торт успешно обновлён!', 'success')
        return redirect(url_for('index'))
    conn.close()
    return render_template('form.html', cake=cake, title='Редактировать торт')


@app.route('/cake/<int:cake_id>/delete', methods=['POST'])
def delete_cake(cake_id):
    conn = get_db()
    conn.execute('DELETE FROM cakes WHERE id=?', (cake_id,))
    conn.commit()
    conn.close()
    flash('Торт удалён из каталога.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
