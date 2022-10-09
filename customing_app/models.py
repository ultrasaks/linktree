from django.db import models


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

    background = models.CharField(max_length=8, default='#15151E')
    font = models.CharField(max_length=8, default='#15151E')
    card = models.CharField(max_length=8, default='#15151E')
    
    button = models.CharField(max_length=8, default='#15151E')
    button_font = models.CharField(max_length=8, default='#15151E')
    button_hover = models.CharField(max_length=8, default='#15151E')
    button_click = models.CharField(max_length=8, default='#15151E')
    #TODO: продумать

    class Meta:
        db_table = 'ColorScheme'
        verbose_name = 'цветовая схема'
        verbose_name_plural = 'цветовые схемы'


