from django.db import models
import re


class Profile(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=400)
    owner = models.ForeignKey('welcome_app.User', on_delete=models.CASCADE,)

    # image = models.ImageField(default='default.jpg', upload_to='profile_pics') #TODO: загрузка изображения
    
    colors = models.ForeignKey('customing_app.ColorScheme', on_delete=models.CASCADE, blank=True, null=True)
    #TODO: статистика

    def __str__(self) -> str:
        return self.name

    def short_body(self) -> str:
        if len(self.about) > 200:
            return f'{self.about[:450]}...'
        return self.about
    
    def get_links(self):
        return Link.objects.filter(user_profile=self)
    

    class Meta:
        db_table = 'Profiles'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Link(models.Model):
    icon = models.CharField(max_length=100, default='link')
    url = models.CharField(max_length=400)
    user_profile = models.ForeignKey('customing_app.Profile', on_delete=models.CASCADE,)
    title = models.CharField(max_length=100)
    solid = models.BooleanField(default=False) #! кнопка

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = 'Links'
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'


class ColorScheme(models.Model):
    owner = models.ForeignKey('customing_app.Profile', on_delete=models.CASCADE, blank=True, null=True)

    background = models.CharField(max_length=8, default='#172C38')
    font = models.CharField(max_length=8, default='#FFFFFF')
    card = models.CharField(max_length=8, default='#15151E')
    
    button = models.CharField(max_length=8, default='#172C38')
    button_font = models.CharField(max_length=8, default='#D0EEFF')
    button_hover = models.CharField(max_length=8, default='#1C3746')
    button_click = models.CharField(max_length=8, default='#1272a5;')
    #TODO: продумать

    class Meta:
        db_table = 'ColorScheme'
        verbose_name = 'цветовую схему'
        verbose_name_plural = 'цветовые схемы'
    
    def __str__(self) -> str:
        return f'Схема {self.owner.name}'

    def get_colors(self) -> list:
        return [self.background, self.font, self.card, self.button, self.button_hover, self.button_click, self.button_font]

    def check_color(self, color: str) -> bool:
        is_ok = re.search(r'^#[A-Fa-f0-9]{6}$', color)
        if is_ok is None:
            return False
        return True
