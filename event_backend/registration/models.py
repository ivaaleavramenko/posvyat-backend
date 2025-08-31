from django.db import models

class Visitor(models.Model):
    # Существующие поля остаются как есть
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    vk_link = models.URLField(blank=True, verbose_name="Ссылка на ВК")
    
    # Новые поля - все с null=True и blank=True временно
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="Пол"
    )
    
    # Учебная информация - временно nullable
    university = models.CharField(max_length=200, blank=True, null=True, verbose_name="ВУЗ")
    faculty = models.CharField(max_length=200, blank=True, null=True, verbose_name="Факультет")
    program = models.CharField(max_length=200, blank=True, null=True, verbose_name="Направление")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Курс")
    group = models.CharField(max_length=50, blank=True, null=True, verbose_name="Группа")
    
    TRANSFER_CHOICES = [
        ('need', 'Нужен'),
        ('not_need', 'Не нужен'),
    ]
    transfer = models.CharField(
        max_length=10,
        choices=TRANSFER_CHOICES,
        blank=True,
        null=True,
        verbose_name="Трансфер"
    )
    
    # Дополнительная информация
    health_issues = models.TextField(blank=True, verbose_name="Проблемы по здоровью")
    allergies = models.TextField(blank=True, verbose_name="Аллергия")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class EventWave(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название волны")
    max_capacity = models.IntegerField(verbose_name="Максимальное количество участников")
    current_count = models.IntegerField(default=0, verbose_name="Текущее количество")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Волна мероприятия"
        verbose_name_plural = "Волны мероприятий"
    
    def __str__(self):
        return f"{self.name} ({self.current_count}/{self.max_capacity})"

class BlackList(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null = True, verbose_name="Отчество")
    vk_link = models.URLField(blank=True, verbose_name="Ссылка на ВК")
    reason = models.TextField(blank=True, verbose_name="Причина")
    
    class Meta:
        verbose_name = "Черный список"
        verbose_name_plural = "Черный список"
        unique_together = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
