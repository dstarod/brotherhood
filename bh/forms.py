from django import forms

from .models import (
    EventType,
    Staff,
    Role,
    Skill,
    SignedDocument,
)


class SimpleSearch(forms.Form):
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


class ExtendedSearch(forms.Form):

    full_name = forms.CharField(
        label='Фамилия, имя, отчество',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия, имя, отчество'}),
        required=False,
    )
    baptized = forms.ChoiceField(
        choices=((2, 'Не важно'), (1, 'Да'), (0, 'Нет')),
        label='Крещен'
    )
    member = forms.ChoiceField(
        choices=((2, 'Не важно'), (1, 'Да'), (0, 'Нет')),
        label='Член церкви'
    )
    staff = forms.ChoiceField(choices=[], label='Должность в церкви')

    role = forms.ChoiceField(choices=[], label='Служение/роль в активностях')

    gender = forms.ChoiceField(
        choices=(('o', 'Не важно'), ('m', 'Мужской'), ('f', 'Женский')),
        label='Пол'
    )
    married = forms.ChoiceField(
        choices=((2, 'Не важно'), (0, 'Не в браке'), (1, 'В браке')),
        label='Женат/замужем'
    )
    age_older_than_choices = [(n, n) for n in range(100)]
    age_older_than_choices.insert(0, (-1, 'Не важно'))
    age_older_than = forms.ChoiceField(
        choices=age_older_than_choices,
        label='Возраст, от'
    )
    age_younger_than_choices = [(n, n) for n in range(1, 100)]
    age_younger_than_choices.append((-1, 'Не важно'))
    age_younger_than = forms.ChoiceField(
        choices=age_younger_than_choices,
        label='Возраст, до'
    )

    in_small_group = forms.ChoiceField(
        choices=((2, 'Не важно'), (0, 'Посещает'), (1, 'Не посещает')),
        label='Посещение малой группы'
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

    signed_documents = forms.ModelMultipleChoiceField(
        queryset=SignedDocument.objects.all(),
        label='Подписанные документы (любой из выбранных)',
        widget=forms.SelectMultiple,
        required=False
    )

    sort = forms.ChoiceField(
        choices=((0, 'Не важно'), (1, 'Возраст'),),
        label='Сортировка'
    )

    def __init__(self, *args, **kwargs):
        super(ExtendedSearch, self).__init__(*args, **kwargs)
        self.fields['staff'].choices = Staff.make_choices()
        self.fields['role'].choices = Role.make_choices()
        self.fields['age_older_than'].initial = -1
        self.fields['age_younger_than'].initial = -1
