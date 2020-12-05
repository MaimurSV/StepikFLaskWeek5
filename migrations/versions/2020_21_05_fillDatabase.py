"""empty message

Revision ID: 2020_21_05_fillDatabase
Revises:
Create Date: 2020-12-05 23:41:47.353067

"""
import json
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '2020_21_05_fillDatabase'
down_revision = 'e585d5ab7334'
branch_labels = None
depends_on = None


def upgrade():
    meals_categories_json = r"""[
                                {
                                    "id" : 1,
                                    "title" : "Суши"
                                },
                                {
                                    "id" : 2,
                                    "title" : "Стритфуд"
                                },
                                {
                                    "id" : 3,
                                    "title" : "Пицца"
                                },
                                {
                                    "id" : 4,
                                    "title" : "Паста"
                                },
                                {
                                    "id" : 5,
                                    "title" : "Новинки"
                                }
                            ]"""

    meals_json = r"""[
                    {
                        "id" : 1,
                        "title" : "Ролл \"Томато\"",
                        "price" : 370,
                        "description" : "Лосось, снежный краб, вяленые томаты, авокадо, сыр, микс соусов, кунжут, 6 шт.",
                        "picture" : "dish1.jpg",
                        "category_id" : 1
                    },
                    {
                        "id" : 2,
                        "title" : "Паста Карбонара",
                        "price" : 339,
                        "description" : "Бекон, Лук репчатый, Сливки, Спагетти, Сыр пармезан, Черный перец, Чеснок",
                        "picture" : "dish2.jpeg",
                        "category_id" : 4
                    },
                    {
                        "id" : 3,
                        "title" : "Ролл \"Трюфельный\"",
                        "price" : 395,
                        "description" : "Лакедра, лосось, трюфельный сыр, авокадо, трюфельная паста, соус «Спайс», тобико, перец, кунжут, зеленый лук , 6 шт.",
                        "picture" : "dish3.jpeg",
                        "category_id" : 1
                    },
                    {
                        "id" : 4,
                        "title" : "Шаверма с цыпленком",
                        "price" : 270,
                        "description" : "Капуста китайская, Куриная грудка, Лаваш армянский, Огурцы, Помидоры, Соус сливочный, Соус Черный перец",
                        "picture" : "dish4.jpeg",
                        "category_id" : 2
                    },
                    {
                        "id" : 5,
                        "title" : "Паста Три мяса",
                        "price" : 329,
                        "description" : "Бекон, Курица, Лук репчатый, Свинина, Сливки, Спагетти, Сыр пармезан, Чеснок",
                        "picture" : "dish5.jpeg",
                        "category_id" : 4
                    },
                    {
                        "id" : 6,
                        "title" : "Грин Карри",
                        "price" : 390,
                        "description" : "Курица, креветки, зеленый карри, кокосовое молоко, шампиньоны, брокколи, цукини",
                        "picture" : "dish6.jpeg",
                        "category_id" : 5
                    },
                    {
                        "id" : 7,
                        "title" : "Ролл \"Игай\"",
                        "price" : 360,
                        "description" : "Лосось, мидии, огурец, перец гриль, зеленый лук, 6 шт.",
                        "picture" : "dish7.jpeg",
                        "category_id" : 1
                    },
                    {
                        "id" : 8,
                        "title" : "Суши \"Желтохвост спайс\"",
                        "price" : 95,
                        "description" : "Спайси хамачи",
                        "picture" : "dish8.jpeg",
                        "category_id" : 1
                    },
                    {
                        "id" : 9,
                        "title" : "Ролл \"Курай\"",
                        "price" : 360,
                        "description" : "Лосось, угорь, сыр, кунжут и острый соус, 6 шт.",
                        "picture" : "dish9.jpeg",
                        "category_id" : 1
                    },
                    {
                        "id" : 10,
                        "title" : "Пицца Маргарита классическая",
                        "price" : 390,
                        "description" : "Базилик, Моцарелла, Помидоры, Томатный пицца-соус",
                        "picture" : "dish10.jpeg",
                        "category_id" : 3
                    },
                    {
                        "id" : 11,
                        "title" : "Бургер Бродвей",
                        "price" : 312,
                        "description" : "Булочка с кунжутом белая, Говядина, Огурцы маринованные, Помидоры, Салат Айсберг, Соус барбекю, Соус сливочный, Сыр Чеддер",
                        "picture" : "dish11.jpeg",
                        "category_id" : 2
                    },
                    {
                        "id" : 12,
                        "title" : "Паста с баклажанами",
                        "price" : 250,
                        "description" : "Спагетти, баклажаны, пармезан, перец чили, чеснок, томатный соус, специи, зелень, базилик.",
                        "picture" : "dish12.jpeg",
                        "category_id" : 4
                    },
                    {
                        "id" : 13,
                        "title" : "Спагетти с морепродуктами, запечённые в пергаменте по-лигурийски",
                        "price" : 290,
                        "description" : "Спагетти, салатные мидии, филе кальмара, тигровые креветки, лук порей, помидоры черри, чеснок, базилик, соус песто, кедровые орешки, пармезан.",
                        "picture" : "dish13.jpeg",
                        "category_id" : 4
                    },
                    {
                        "id" : 14,
                        "title" : "Пицца Карбонара классическая",
                        "price" : 499,
                        "description" : "Бекон, Моцарелла, Соус сливочный, Сыр пармезан",
                        "picture" : "dish14.jpeg",
                        "category_id" : 3
                    },
                    {
                        "id" : 15,
                        "title" : "Пицца Барбекю классическая",
                        "price" : 480,
                        "description" : "Колбаски охотничьи, Курица, Моцарелла, Соус барбекю, Томатный пицца-соус, укроп",
                        "picture" : "dish15.jpeg",
                        "category_id" : 3
                    },
                    {
                        "id" : 16,
                        "title" : "Паста с рагу из индейки и шпинатом",
                        "price" : 290,
                        "description" : "Спагетти, индейка, сливки, шампиньоны, лук репчатый, пармезан, шпинат, чеснок.",
                        "picture" : "dish16.jpeg",
                        "category_id" : 4
                    },
                    {
                        "id" : 17,
                        "title" : "Буррито",
                        "price" : 289,
                        "description" : "Капуста китайская, Курица, Лук красный, Моцарелла, Перец болгарский, Помидоры, Рис, Соус мексиканский, Тортилья, Фасоль красная",
                        "picture" : "dish17.jpeg",
                        "category_id" : 2
                    },
                    {
                        "id" : 18,
                        "title" : "Бургер Гранд Каньон",
                        "price" : 299,
                        "description" : "Булочка белая, Капуста китайская, Куриная грудка, Огурцы маринованные, Помидоры, Соус барбекю, Соус сливочный, Сыр Чеддер",
                        "picture" : "dish18.jpeg",
                        "category_id" : 2
                    },
                    {
                        "id" : 19,
                        "title" : "Овощной салат с цыпленком",
                        "price" : 250,
                        "description" : "Куриное филе, огурцы , помидоры, полба, пармезан, соус Цезарь, зелень, кинза, базилик, яйцо.",
                        "picture" : "dish19.jpeg",
                        "category_id" : 5
                    },
                    {
                        "id" : 20,
                        "title" : "Фреш-ролл с курицей",
                        "price" : 269,
                        "description" : "Капуста китайская, Курица, Огурцы, Помидоры, Соус Тар-тар, Сыр пармезан, Тортилья",
                        "picture" : "dish20.jpeg",
                        "category_id" : 2
                    },
                    {
                        "id" : 21,
                        "title" : "Харчо",
                        "price" : 220,
                        "description" : "Говядина, лук репчатый, томатная паста, чеснок, рис, кинза, специи, зелень",
                        "picture" : "dish21.jpeg",
                        "category_id" : 5
                    },
                    {
                        "id" : 22,
                        "title" : "Пицца Деревенская классическая",
                        "price" : 569,
                        "description" : "Бекон, Грибы шампиньоны, Лук красный, Моцарелла, Свинина, Томатный пицца-соус, укроп",
                        "picture" : "dish22.jpeg",
                        "category_id" : 3
                    },
                    {
                        "id" : 23,
                        "title" : "Ролл Такаши",
                        "price" : 300,
                        "description" : "Угорь, огурец, чукка, рис, сливочный сыр, авокадо, кунжут, спайси соус, унаги соус.",
                        "picture" : "dish23.jpeg",
                        "category_id" : 5
                    },
                    {
                        "id" : 24,
                        "title" : "Рис с овощами, свининой и шампиньонами с соусом удон",
                        "price" : 320,
                        "description" : "Рис, морковь, цукини, перец болгарский, китайская капуста, шампиньоны, свинина, кунжут, соус удон",
                        "picture" : "dish24.jpeg",
                        "category_id" : 5
                    },
                    {
                        "id" : 25,
                        "title" : "Пицца Четыре сыра классическая",
                        "price" : 559,
                        "description" : "Моцарелла, Сливочный пицца-соус, Сыр Дор Блю, Сыр пармезан, Сыр Чеддер",
                        "picture" : "dish25.jpeg",
                        "category_id" : 3
                    }
                ]
"""
    meals_categories = json.loads(meals_categories_json)
    meals = json.loads(meals_json)

    meals_categories_table = table('meal-categories',
                                   column('id', sa.Integer()),
                                   column('title', sa.String()))
    meals_table = table('meals',
                        column('id', sa.Integer()),
                        column('title', sa.String(length=25)),
                        column('price', sa.Integer()),
                        column('description', sa.String()),
                        column('picture', sa.String()),
                        column('category_id', sa.Integer()))

    meals_category_dict = []
    for category in meals_categories:
        meals_category_dict.append({"id": category["id"], "title": category["title"]})
    op.bulk_insert(meals_categories_table, meals_category_dict)

    meals_dict = []
    for meal in meals:
        id = meal["id"]
        title = meal["title"]
        price = int(meal["price"])
        description = meal["description"]
        picture = meal["picture"]
        category_id = meal["category_id"]
        meals_dict.append({"id": id, "title": title, "price": price, "description": description, "picture": picture,
                           "category_id": category_id})
    op.bulk_insert(meals_table, meals_dict)


def downgrade():
    """Очистить таблицы посредством SQL запросов
    SQLITE не имеет в своем составе команду TRUNCATE
    """
    op.execute("DELETE FROM `meals`;")
    op.execute("REINDEX  `meals`;")
    op.execute("DELETE FROM `meal-categories`;")
    op.execute("REINDEX  `meal-categories`;")
    op.execute("VACUUM;")
