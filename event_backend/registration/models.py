from django.db import models

class Visitor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    vk_link = models.URLField(blank=True, verbose_name="Ссылка на ВК")
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
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    vk_link = models.URLField(blank=True, verbose_name="Ссылка на ВК")
    reason = models.TextField(blank=True, verbose_name="Причина")
    
    class Meta:
        verbose_name = "Черный список"
        verbose_name_plural = "Черный список"
        unique_together = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
