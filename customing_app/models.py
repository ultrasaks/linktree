from django.db import models
import re


class Profile(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=400)
    owner = models.ForeignKey('welcome_app.User', on_delete=models.CASCADE,)

    # image = models.ImageField(default='default.jpg', upload_to='profile_pics') #TODO: загрузка изображения
    #? Изображение конвертируется в jpeg/webp
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
    icon = models.CharField(max_length=100, default='link', verbose_name='иконка')
    url = models.CharField(max_length=400, verbose_name='ссылка')
    user_profile = models.ForeignKey('customing_app.Profile', on_delete=models.CASCADE, verbose_name='профиль')
    title = models.CharField(max_length=100, verbose_name='заголовок')
    position = models.IntegerField(verbose_name='позиция', null=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = Link.objects.filter(user_profile=self.user_profile).count()
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'Links'
        verbose_name = 'ссылку'
        verbose_name_plural = 'ссылки'


class ColorScheme(models.Model):
    owner = models.ForeignKey('customing_app.Profile', on_delete=models.CASCADE, blank=True, null=True)

    background = models.CharField(max_length=8, default='#172C38', verbose_name='background')
    font = models.CharField(max_length=8, default='#FFFFFF', verbose_name='font')
    card = models.CharField(max_length=8, default='#15151E', verbose_name='card')
    
    button = models.CharField(max_length=8, default='#172C38', verbose_name='button')
    button_shape = models.IntegerField(default=0) #0-2
    button_type = models.IntegerField(default=0) # 0-3
    button_font = models.CharField(max_length=8, default='#D0EEFF', verbose_name='button font')
    # button_hover = models.CharField(max_length=8, default='#1C3746', verbose_name='button hover')
    # button_click = models.CharField(max_length=8, default='#1272a5', verbose_name='button click')
    #TODO: продумать

    class Meta:
        db_table = 'ColorScheme'
        verbose_name = 'цветовую схему'
        verbose_name_plural = 'цветовые схемы'
    
    def __str__(self) -> str:
        return f'Схема {self.owner.name}'

    # def get_colors(self) -> list:
    #     return [self.background, self.font, self.card, self.button, self.button_hover, self.button_click, self.button_font]

    # def get_colors_plural (self) -> dict:
    #     return {'background': self.background, 'font': self.font, 'card': self.card, 'button': self.button, 
    #     'button_hover': self.button_hover, 'button_click': self.button_click, 'button_font': self.button_font}

    def check_color(self, color: str) -> bool:
        is_ok = re.search(r'^#[A-Fa-f0-9]{6}$', color)
        if is_ok is None:
            return False
        return True


def check_link_correct(link:str) -> bool:
    #TODO: перенести в более подходящее место
    link = link.replace('http://', '').replace('https://', '')
    is_ok = re.search(r'^[A-Za-z0-9_-]+\.[a-zA-Z]', link)
    if is_ok is None:
        return False
    return True
