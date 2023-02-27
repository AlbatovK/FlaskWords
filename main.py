import random
from random import choice

from flask import Flask, render_template, redirect
from pymorphy2 import MorphAnalyzer

from CoalForm import CoalForm
from decision_form import DecisionForm
from question_form import QuestionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key'


@app.route('/<title>')
def template(title: str):
    return render_template("base.html", title=title)


@app.route('/training/<prof>')
def training(prof: str):
    return render_template("training.html", title=prof, prof=prof)


@app.route('/kalik', methods=['GET', 'POST'])
def kalik():
    form = CoalForm()
    if form.validate_on_submit():
        txt = form.text.data

        words = txt.split()
        morph = MorphAnalyzer()
        dct = {
            'Пыхтеть': '💨💨💨',
            'Попыхтеть': '💨💨💨',
            'Раскумарить': '☺☺☺',
            'Раскумар': '🏭🏭🏭',
            'Дуть': '💨💨💨',
            'Дудка': '🤙🤙🤙',
            'Дабл-эпл': '🍏🍎⚽',
            'Забивуля': '😘😘😘',
            'Мундштук': '👑👑👑',
            'Дымануть': '😤😤😤',
            'Под': '❤❤❤',
            'Подик': '🥺🥺🥺',
            'Раскумаренный': '🤰🤰🤰',
            'Пыхтельня': '🥴🥴🥴',
            'Калюндупула': '😺😺😺',
            'Парилка': '🤐🤐🤐',
            'Жижка': '👹👹👹',
            'Бак': '🤑🤑🤑',
            'Раскалюмбасить': '🤝🤝🤝',
            'Попыхать': '🧘🧘🧘',
            'Забивочка': '💨💨💨',
            'Плотная': '💨💨💨',
            'Кайфарик': '🎉🎉🎉',
            'Гарик': '🌬🌬🌬',
            'Дудонить': '🌪🌪🌪',
            'Дымуля': '🥵🥵🥵',
            'Распыханный': '🤬🤬🤬',
            'Калик': '🏭🏭🏭',
            'Дымок': '🌫🌫🌫',
            'Кайфануть': '⚪⚪⚪',
            'Пыхтящий': '😈😈😈',
            'Животрепещущий': '💀💀💀',
            'Уголёк': '🥵🥵🥵',
            'Сижка': '🚬🚬🚬',
            'Краля': '🌝🌝🌝',
            'Пыхтун': '🥴🥴🥴',
            'Накумарить': '🙌🙌🙌',
            'Кумар': '👶👶👶',
            'Подымить': '😤😤😤',
            'Пыхотно': '🌚🌚🌚',
            'Крепчайшая': '💪💪💪',
            'Задувочка': '🌬🌬🌬'
        }
        print(morph.parse('Пыхтеть'))

        res = ''
        for word in words:
            prs = morph.parse(word)[0]
            if ('NOUN' in prs.tag or 'VERB' in prs.tag or 'ADJF' in prs.tag or 'INFN' in prs.tag) \
                    and random.randint(0, 10) in range(1, 6):
                print(prs.tag.POS)
                tg = prs.tag
                tags = [tg.POS, tg.animacy, tg.gender, tg.number, tg.involvement, tg.case, tg.aspect, tg.mood,
                        tg.person, tg.tense, tg.transitivity, tg.voice]
                tags = [str(x) for x in tags if x is not None]
                rnds = [x for x in dct.keys()
                        if any([True if (
                            y.tag.POS == prs.tag.POS or sorted([y.tag.POS, prs.tag.POS]) == sorted(
                        ['INFN', 'VERB'])) else False for
                                y in morph.parse(x)])
                        ]
                print(rnds, word)
                good = True
                random.shuffle(rnds)
                for rnd in rnds:
                    rnd_p = choice(morph.parse(rnd))
                    if rnd_p.inflect({*tags}) is not None:
                        print(rnd_p, tags)
                        res += (rnd_p.inflect({*tags}).word if rnd_p.inflect({*tags}) is not None else word) + ' ' + \
                               dct[
                                   rnd] + ' '
                        good = False
                        break
                if good is True:
                    res += word + ' '


            else:
                res += word + ' '

        return render_template('kalik_done.html', text=res)

    return render_template('kalik_form.html', form=form)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    form = QuestionForm()
    if form.validate_on_submit():
        dct = {
            'surname': form.surname.data,
            'name': form.name.data,
            'education': form.education.data,
            'profession': form.profession.data,
            'sex': form.sex.data,
            'motivation': form.motivation.data,
            'ready': form.ready.data,
        }
        return render_template('auto_answer.html', args=dct, form=None, title='Результаты анкеты')

    return render_template('auto_answer.html', title='Анкета', form=form)


@app.route('/login')
def decision():
    form = DecisionForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('decision.html', title='Аварийный доступ', form=form)


@app.route('/list_prof/<tag>')
def show_list(tag: str):
    lst = {
        'items': [
            'Инженер',
            'Строитель',
            'Учёный',
            'Ещё кто-то'
        ]
    }

    return render_template('list.html', title=tag, tag=tag, list=lst)


@app.route('/success')
def success():
    return 'Success'


if '__main__' == __name__:
    app.run(port=8080, host='0.0.0.0')
