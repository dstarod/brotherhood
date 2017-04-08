from django import forms
from .models import STATUS_CHOICES, EventType, Skill


class ExtendedSearch(forms.Form):

    full_name = forms.CharField(
        label='Фамилия, имя, отчество',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия, имя, отчество'})
    )
    baptized = forms.ChoiceField(
        choices=((2, 'Не важно'), (1, 'Да'), (0, 'Нет')),
        label='Крещен'
    )
    member = forms.ChoiceField(
        choices=((2, 'Не важно'), (1, 'Да'), (0, 'Нет')),
        label='Член церкви'
    )
    gender = forms.ChoiceField(
        choices=(('o', 'Не важно'), ('m', 'Мужской'), ('f', 'Женский')),
        label='Пол'
    )
    married = forms.ChoiceField(
        choices=((2, 'Не важно'), (0, 'Не в браке'), (1, 'В браке')),
        label='Женат/замужем'
    )
    gone_to_eternity = forms.BooleanField(
        label='Отображать отошедших в вечность',
        required=False,
    )
    gone_to_another_church = forms.BooleanField(
        label='Отображать перешедших в другую церковь',
        required=False,
    )
    gone = forms.BooleanField(
        label='Отображать ушедших из церкви',
        required=False,
    )

    statuses = list(STATUS_CHOICES)
    statuses.insert(0, (1000, 'Не важно'))

    status = forms.ChoiceField(
        choices=statuses,
        label='Статус'
    )

    circles = list(CIRCLE_CHOICES)
    circles.insert(0, (1000, 'Не важно'))

    circle = forms.ChoiceField(
        choices=circles,
        label='Круг посвящения'
    )

    event_presents = forms.ModelMultipleChoiceField(
        queryset=EventType.objects.all(),
        label='Посетил(а) события (все выбранные)',
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    event_absents = forms.ModelMultipleChoiceField(
        queryset=EventType.objects.all(),
        label='Не принимал(а) участия в событиях (ни в одном из выбранных)',
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        label='Дары и таланты (любой из выбранных)',
        widget=forms.SelectMultiple,
        required=False
    )

    sort = forms.ChoiceField(
        choices=((0, 'Не важно'), (1, 'Возраст'),),
        label='Сортировка'
    )
