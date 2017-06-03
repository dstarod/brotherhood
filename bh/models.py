import os
import time
from hashlib import md5

from django.db import models
from django_resized import ResizedImageField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


DOW_CHOICES = (
    (0, 'Воскресенье'), (1, 'Понедельник'), (2, 'Вторник'),
    (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота')
)


def hash_name(base):
    """
    :type base: str
    :rtype: str
    """
    return md5(base.encode('utf-8')).hexdigest()


def user_directory_path(instance, filename):
    """
    Returns url like /media/avatars/ad688b26ba3876751699c540e0e23ede.jpeg
    :type instance: Person
    :type filename: str
    :rtype: str
    """
    ext = filename.split('.')[-1].lower()
    path = 'avatars/{}.{}'.format(hash_name(str(instance)), ext)
    os_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.isfile(os_path):
        os.remove(os_path)
    return path


def photo_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    dir_path = 'gallery_{}'.format(instance.gallery.pk)
    os_dir_path = os.path.join(settings.MEDIA_ROOT, dir_path)
    if os.path.exists(dir_path) and not os.path.isdir(os_dir_path):
        os.remove(dir_path)
    if not os.path.isdir(os_dir_path):
        os.mkdir(os_dir_path, 0o777)

    file_path = os.path.join(
        dir_path, '{}.{}'.format(hash_name(str(time.time())), ext)
    )
    os_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.isfile(os_path):
        os.remove(os_path)
    return file_path


class Gallery(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class Photo(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Название'
    )
    image = ResizedImageField(
        upload_to=photo_path, null=False, blank=False,
        verbose_name='Фото', size=(1200, 1200),
    )
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, null=False, blank=False,
        verbose_name='Галерея', related_name='photos'
    )

    def image_tag(self):
        return mark_safe('<img src="{}" width=100 height=100 />'.format(self.image.url))
    image_tag.short_description = 'Изображение'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Address(models.Model):
    """
    Физический адрес проживания
    """

    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Название'
    )
    description = models.CharField(
        null=True, blank=True, max_length=256,
        verbose_name='Описание'
    )
    text = models.CharField(
        null=True, blank=True, max_length=256,
        verbose_name='Адрес'
    )
    # Точка на карте
    lng = models.FloatField(
        null=True, blank=True,
        verbose_name='Долгота'
    )
    lat = models.FloatField(
        null=True, blank=True,
        verbose_name='Широта'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['name']


STATUS_CHOICES = (
    (0, 'Сочувствующий'),
    (1, 'Прихожанин'),
    (2, 'Номинальный член церкви'),
    (3, 'Пассивный член церкви'),
    (4, 'Активный член церкви'),
    (5, 'ДВР')
)

CIRCLE_CHOICES = (
    (0, 'Общество'),
    (1, 'Собрание'),
    (2, 'Община'),
    (3, 'Ученики'),
    (4, 'Служители'),
    (5, 'Посланники'),
)


class Person(models.Model):
    first_name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Имя'
    )
    middle_name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Отчество'
    )
    last_name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Фамилия'
    )
    maiden_name = models.CharField(
        null=True, blank=True, max_length=256,
        verbose_name='Девичья фамилия'
    )
    gender = models.CharField(
        choices=(('m', 'Мужской'), ('f', 'Женский')),
        default='m', null=False, blank=False, max_length=256,
        verbose_name='Пол'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, editable=False
    )
    birthday = models.DateField(
        null=True, blank=True,
        verbose_name='День рождения'
    )
    occupation = models.CharField(
        null=True, blank=True, max_length=255,
        verbose_name='Род занятий'
    )
    specialty = models.CharField(
        null=True, blank=True, max_length=255,
        verbose_name='Образование, специальность'
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Примечания'
    )
    baptized = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Крещен'
    )
    baptized_at = models.DateField(
        null=True, blank=True,
        verbose_name='Дата крещения'
    )
    married = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Женат/Замужем'
    )
    married_at = models.DateField(
        null=True, blank=True,
        verbose_name='Дата бракосочетания'
    )
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Адрес', related_name='people'
    )
    status = models.SmallIntegerField(
        null=True, blank=True, choices=STATUS_CHOICES,
        verbose_name='Статус'
    )
    circle = models.SmallIntegerField(
        null=True, blank=True, choices=CIRCLE_CHOICES,
        verbose_name='Круг посвящения',
    )
    image = ResizedImageField(
        upload_to=user_directory_path, null=True, blank=True, default=None,
        verbose_name='Фото', size=(500, 500)
    )
    skills = models.ManyToManyField(
        'Skill',  blank=True,  related_name='people',
        verbose_name='Дары и таланты',
    )
    member = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Член церкви'
    )
    gone_to_eternity = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Отошел в вечность'
    )
    gone = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Ушел из церкви'
    )
    gone_to_another_church = models.BooleanField(
        null=False, blank=False, default=False,
        verbose_name='Перешел в другую церковь'
    )
    staff = models.ForeignKey(
        'Staff', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Должность в церкви', related_name='people'
    )

    def clean(self):
        if self.baptized_at and not self.baptized:
            self.baptized = True

    def __str__(self):
        return '{} {} {}'.format(
            self.last_name, self.first_name, self.middle_name
        )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Email(models.Model):
    """
    Адрес электронной почты.
    У одного человека может быть много адресов.
    """
    address = models.CharField(
        null=False, blank=False, unique=True, max_length=255,
        verbose_name='Адрес'
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='email'
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'E-mail'


class Social(models.Model):
    """
    Персональные страницы в социальных сетях.
    У одного человека может быть много аккаунтов.
    """
    SOCIAL = (
        ('vk', 'ВКонтакте'),
        ('fb', 'Facebook'),
        ('ln', 'LinkedIn'),
        ('tw', 'Twitter'),
        ('od', 'Одноклассники'),
        ('sk', 'Skype'),
    )
    name = models.CharField(
        null=False, choices=SOCIAL, max_length=2,
        verbose_name='Сеть'
    )
    link = models.CharField(
        null=False, blank=False, unique=True, max_length=255,
        verbose_name='Ссылка'
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='social'
    )

    def __str__(self):
        return self.link


class Phone(models.Model):
    """
    Телефонные номера
    """
    number = models.CharField(
        null=False, blank=False, max_length=255,
        verbose_name='Номер'
    )
    type = models.CharField(
        null=True, max_length=255, choices=(
            ('cell', 'Мобильный'), ('home', 'Домашний'),
            ('work', 'Рабочий'), ('other', 'Другое')
        ),
        verbose_name='Тип'
    )
    person = models.ForeignKey(
        'Person', blank=True, null=True, related_name='phone'
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'


class Relation(models.Model):
    """
    Родственные связи
    """
    RELATIVES = (
        ('husband', 'муж'),
        ('wife', 'жена'),
        ('son', 'сын'),
        ('daughter', 'дочь'),
        ('father', 'отец'),
        ('mother', 'мать'),
        ('brother', 'брат'),
        ('sister', 'сестра'),
        ('grandfather', 'дедушка'),
        ('grandmother', 'бабушка'),
        ('grandson', 'внук'),
        ('granddaughter', 'внучка'),
        ('great_grandfather', 'прадедушка'),
        ('great_grandmother', 'прабабушка'),
        ('great_grandson', 'правнук'),
        ('great_granddaughter', 'правнучка'),
        ('father_in_low_m', 'тесть'),
        ('father_in_low_f', 'свекр'),
        ('mother_in_low_m', 'теща'),
        ('mother_in_low_f', 'свекровь'),
        ('son_in_low', 'зять'),
        ('daughter_in_low', 'невестка'),
        ('uncle', 'дядя'),
        ('aunt', 'тётя'),
        ('nephew', 'племянник'),
        ('niece', 'племянница')
    )
    type = models.CharField(
        max_length=25, choices=RELATIVES, null=False, blank=False,
        verbose_name='Тип'
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE,
        related_name='relations'
    )
    rel = models.ForeignKey(
        'Person', on_delete=models.CASCADE,
        verbose_name='Родственник'
    )

    def __str__(self):
        return '{}: {}'.format(self.type, self.rel)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        back_rel_type = None
        if self.type == 'husband':
            back_rel_type = 'wife'
        elif self.type == 'wife':
            back_rel_type = 'husband'
        elif self.type in ('son', 'daughter'):
            if self.person.gender == 'm':
                back_rel_type = 'father'
            else:
                back_rel_type = 'mother'
        elif self.type in ('father', 'mother'):
            if self.person.gender == 'm':
                back_rel_type = 'son'
            else:
                back_rel_type = 'daughter'
        elif self.type in ('brother', 'sister'):
            if self.person.gender == 'm':
                back_rel_type = 'brother'
            else:
                back_rel_type = 'sister'
        elif self.type in ('grandfather', 'grandmother'):
            if self.person.gender == 'm':
                back_rel_type = 'grandson'
            else:
                back_rel_type = 'granddaughter'
        elif self.type in ('grandson', 'granddaughter'):
            if self.person.gender == 'm':
                back_rel_type = 'grandfather'
            else:
                back_rel_type = 'grandmother'
        elif self.type in ('great_grandfather', 'great_grandmother'):
            if self.person.gender == 'm':
                back_rel_type = 'great_grandson'
            else:
                back_rel_type = 'great_granddaughter'
        elif self.type in ('great_grandson', 'great_granddaughter'):
            if self.person.gender == 'm':
                back_rel_type = 'great_grandfather'
            else:
                back_rel_type = 'great_grandmother'
        elif self.type in ('father_in_low_m', 'mother_in_low_m'):
            back_rel_type = 'son_in_low'
        elif self.type == 'son_in_low':
            if self.person.gender == 'm':
                back_rel_type = 'father_in_low_m'
            else:
                back_rel_type = 'mother_in_low_m'
        elif self.type in ('father_in_low_f', 'mother_in_low_f'):
            back_rel_type = 'daughter_in_low'
        elif self.type == 'daughter_in_low':
            if self.person.gender == 'm':
                back_rel_type = 'father_in_low_f'
            else:
                back_rel_type = 'mother_in_low_f'
        elif self.type in ('uncle', 'aunt'):
            if self.person.gender == 'm':
                back_rel_type = 'nephew'
            else:
                back_rel_type = 'niece'
        elif self.type in ('nephew', 'niece'):
            if self.person.gender == 'm':
                back_rel_type = 'uncle'
            else:
                back_rel_type = 'aunt'

        if back_rel_type:
            # Автоматически ставить состояние "в браке"
            if back_rel_type in ('husband', 'wife'):
                self.person.married = True
                self.person.save()
                self.rel.married = True
                self.rel.save()
            # Если обратной связи нет, создать
            if not Relation.objects.filter(
                    rel=self.person, person=self.rel, type=back_rel_type):
                back_rel = Relation()
                back_rel.rel = self.person
                back_rel.person = self.rel
                back_rel.type = back_rel_type
                back_rel.save()

    class Meta:
        unique_together = ('person', 'rel', 'type')
        verbose_name = 'Родственник'
        verbose_name_plural = 'Родственники'


class Action(models.Model):
    """
    Активность в церкви: пасторское служение, малая группа,
    молитвенное служение и т.п.
    """
    name = models.CharField(
        null=False, blank=False, unique=True, max_length=256,
        verbose_name='Название'
    )
    periods = models.ManyToManyField(
        'Period',  blank=True,  related_name='actions',
        verbose_name='Периоды',
    )
    address = models.ForeignKey(
        'Address', null=True, blank=True, related_name='Активности',
        verbose_name='Адрес'
    )
    action_type = models.ForeignKey(
        'ActionType', on_delete=models.CASCADE, related_name='actions',
        null=True, blank=True,
        verbose_name='Тип активности'
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Примечания'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'
        ordering = ['name']


class ActionType(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Наименование'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип активности'
        verbose_name_plural = 'Типы активностей'


class Staff(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Должность в церкви'
    )

    def __str__(self):
        return self.name

    @classmethod
    def make_choices(cls):
        choices = [(s.id, s.name) for s in cls.objects.all()]
        choices.insert(0, (1000, 'Не важно'))
        return choices

    class Meta:
        verbose_name = 'Должность в церкви'
        verbose_name_plural = 'Должности в церкви'


class Role(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    @classmethod
    def make_choices(cls):
        choices = [(s.id, s.name) for s in cls.objects.all()]
        choices.insert(0, (1000, 'Не важно'))
        return choices

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class ActionRole(models.Model):
    """
    Участие в активности и опционально - роль в ней.
    Например, малая группа - лидер.
    """
    # TODO Remove it
    role = models.CharField(
        null=True, blank=True, max_length=256,
        verbose_name='Роль (устаревшее)'
    )
    charge = models.ForeignKey(
        'Role', on_delete=models.CASCADE, related_name='action_roles',
        null=True, blank=True,
        verbose_name='Роль'
    )
    action = models.ForeignKey(
        'Action', on_delete=models.CASCADE, related_name='roles',
        verbose_name='Активность'
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='actions',
        verbose_name='Профиль'
    )

    class Meta:
        unique_together = ('action', 'person')
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        preview = self.action.name
        if self.role:
            preview = '{} ({})'.format(preview, self.role.lower())
        return preview


class Event(models.Model):
    """
    События, такие как церковные курсы, день города, крещение и т.п.
    """
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Наименование'
    )
    started_at = models.DateTimeField(
        null=False, blank=False,
        verbose_name='Начало'
    )
    finished_at = models.DateTimeField(
        null=False, blank=False,
        verbose_name='Завершение'
    )
    people = models.ManyToManyField(
        'Person', related_name='events',
        verbose_name='Участники'
    )
    address = models.ForeignKey(
        'Address', null=True, blank=True, related_name='События',
        verbose_name='Адрес'
    )
    type = models.CharField(
        null=False, default='public', max_length=256, choices=(
            ('private', 'Личное'), ('public', 'Публичное')
        ),
        verbose_name='Публичность'
    )
    event_type = models.ForeignKey(
        'EventType', on_delete=models.CASCADE, related_name='events',
        null=True, blank=True,
        verbose_name='Тип события'
    )
    gallery = models.ForeignKey(
        Gallery, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Галерея', related_name='events'
    )

    def __str__(self):
        return '{}: {}'.format(str(self.started_at)[:10], self.name)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['started_at']


class Skill(models.Model):
    """
    Способности и духовные дары, такие как проповедь, рисование,
    игра на инструменте
    """
    name = models.CharField(
        null=False, blank=False, unique=True, max_length=256,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дары и таланты'
        verbose_name_plural = 'Дары и таланты'
        ordering = ['name']


class Period(models.Model):
    """
    Время на неделе, когда человек готов послужить: день недели и часы
    """
    dow = models.SmallIntegerField(
        null=False, default=0, choices=DOW_CHOICES,
        verbose_name='День недели'
    )
    time_from = models.TimeField(
        null=False, blank=False,
        verbose_name='Начало'
    )
    time_to = models.TimeField(
        null=False, blank=False,
        verbose_name='Завершение'
    )

    def __str__(self):
        return '{} с {} по {}'.format(
            DOW_CHOICES[self.dow][1], self.time_from, self.time_to
        )

    def clean(self):
        if self.time_from > self.time_to:
            raise ValidationError(
                'Время начала не может быть позже времени завершения'
            )

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
        ordering = ['dow', 'time_from']


class EventType(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=256,
        verbose_name='Наименование'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип событий'
        verbose_name_plural = 'Типы событий'
