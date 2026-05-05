from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Settings(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название сайта')
    description = models.TextField(max_length=500, verbose_name='Описание сайта')
    logo = models.ImageField(upload_to='settings/', verbose_name='Логотип сайта', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', verbose_name='Фавикон (иконка сайта)', blank=True, null=True, help_text="Изображение для иконки сайта (например, .ico, .png). Рекомендуется 32x32 или 64x64 пикселя.")
    hero_image = models.ImageField(upload_to='settings/', verbose_name='Фон главного экрана', blank=True, null=True)
    facebook = models.URLField(max_length=250, verbose_name='Ссылка на Facebook')
    instagram = models.URLField(max_length=250, verbose_name='Ссылка на Instagram')
    tikTok = models.URLField(max_length=250, verbose_name='Ссылка на TikTok')
    whatsapp = models.CharField(max_length=250, verbose_name='Номер WhatsApp', blank=True, null=True, help_text="Введите номер без '+' и пробелов, например: 996555212293")
    address = models.CharField(max_length=250, verbose_name='Адрес')
    map_link = models.TextField(verbose_name='Ссылка на карту (iframe src)', help_text="Используйте только атрибут src из кода вставки Google Maps (начинается с https://www.google.com/maps/embed...)")
    phone_number = models.CharField(max_length=250, verbose_name='Телефон')
    delivery_phone = models.CharField(max_length=250, verbose_name='Номер для доставки', blank=True, null=True)
    email = models.EmailField(max_length=250, verbose_name='Электронная почта')
    working_hours = models.TextField(max_length=500, verbose_name='Часы работы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '01) Основные настройки'
        verbose_name_plural = '01) Основные настройки'

class Statistic(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название показателя')
    value = models.CharField(max_length=50, verbose_name='Значение (например, 50+)')
    icon = models.CharField(max_length=100, verbose_name='Иконка (FontAwesome класс)', help_text="Используйте fa-solid для обычных иконок (напр. fa-solid fa-bowl-food) или fa-brands для соцсетей. Поиск: fontawesome.com/search?m=free")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '03) Статистика'
        verbose_name_plural = '03) Статистика'

class OurHistory(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    description = models.TextField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='history_images/', verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '02) История'
        verbose_name_plural = '02) История'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=False, verbose_name='Slug (для фильтра на сайте)', help_text="Используется для фильтрации. Заполняется автоматически из названия (латиницей).")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '06) Категории'
        verbose_name_plural = '06) Категории'
        ordering = ['name']

class HistoryFeature(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок особенности', default='')
    description = models.CharField(max_length=250, verbose_name='Описание особенности')
    history = models.ForeignKey(OurHistory, on_delete=models.CASCADE, related_name='features', verbose_name="История")
    icon = models.CharField(max_length=100, verbose_name='Иконка (FontAwesome)', help_text="Для обычных: fa-solid fa-leaf. Для брендов: fa-brands fa-bluetooth. Поиск free иконок на fontawesome.com")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Особенность истории'
        verbose_name_plural = 'Особенности истории'

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name='Категория блюда')
    title = models.CharField(max_length=30, verbose_name='Название блюда')
    description = models.TextField(max_length=100, verbose_name='Описание блюда')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    image = models.ImageField(upload_to='dish_images/', verbose_name='Изображение блюда')
    is_popular = models.BooleanField(default=False, verbose_name='Отображать на главной странице')
    is_new = models.BooleanField(default=False, verbose_name='Новое')
    is_promotion = models.BooleanField(default=False, verbose_name='Акция')
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена по акции', blank=True, null=True)
    new_until_date = models.DateField(verbose_name='Новое до даты', blank=True, null=True, help_text="Блюдо будет отображаться как 'Новое' до этой даты.")
    promotion_end_date = models.DateField(verbose_name='Дата окончания акции', blank=True, null=True)

    @property
    def is_promo_active(self):
        if not self.is_promotion:
            return False
        if self.promotion_end_date and self.promotion_end_date < timezone.now().date():
            return False
        return self.discount_price is not None

    @property
    def is_new_active(self):
        if not self.is_new:
            return False
        if self.new_until_date and self.new_until_date < timezone.now().date():
            return False
        return True
    def get_display_price(self):
        if self.is_promo_active and self.discount_price is not None:
            return self.discount_price
        return self.price

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '07) Блюда'
        verbose_name_plural = '07) Блюда'

class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок новости')
    description = models.TextField(verbose_name='Описание новости')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение (16:9)')
    date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    promotion_end_date = models.DateField(verbose_name='Дата окончания акции', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '04) Новости'
        verbose_name_plural = '04) Новости'
        ordering = ['-date']

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя клиента')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveIntegerField(default=5, verbose_name='Рейтинг (1-5)')
    is_active = models.BooleanField(default=False, verbose_name='Отображать на главной')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Отзыв от {self.name}"

    class Meta:
        verbose_name = '05) Отзывы'
        verbose_name_plural = '05) Отзывы'

class Gallery(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок (название локации или события)')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '08) Галерея'
        verbose_name_plural = '08) Галерея'

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
    ]
    name = models.CharField(max_length=100, verbose_name='Имя отправителя')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    message = models.TextField(verbose_name='Сообщение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return f"Сообщение от {self.name} ({self.phone})"

    class Meta:
        verbose_name = '10) Сообщения'
        verbose_name_plural = '10) Сообщения'

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    guests = models.IntegerField(verbose_name='Количество гостей')
    occasion = models.CharField(max_length=100, verbose_name='Повод', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Бронь: {self.name} на {self.date} {self.time}"

    class Meta:
        verbose_name = '09) Бронирования'
        verbose_name_plural = '09) Бронирования'