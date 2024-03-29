from django.db import models
import re

LINK_REGEX = r'^[A-Za-z0-9_-]+\.[a-zA-Z]'
COLOR_REGEX = r'^#[A-Fa-f0-9]{6}$'
RADIUSES = ('0', '.5', '1.5',)
AVA_RADIUSES = ('0', '10', '25', '50')
ADDITIONAL_CSS_BTNS = (
    '',
    r'background:transparent;outline:{OUTLINE} 2px solid;',
    r'box-shadow: 0px 3px 6px rgba({SHADOW_RGB}, 0.15);',
    r'box-shadow: 5px 5px 0px {SHADOW};transition-duration: 0s;}.button:hover {transform: translate(2px, 2px);box-shadow: 3px 3px 0px {SHADOW}' #outline:{OUTLINE} 2px solid;
)
BTN_BASE = r'.button:hover{transform: scale(1.05);}.button{background:{BTN};color:{BTN_FONT};font-weight:600;padding:.75rem 1rem;border-radius:{RADIUS}rem;cursor:pointer;display:flex;justify-content:center;align-items:center;box-sizing:border-box;transition:transform .15s ease-out;border-color:transparent;text-decoration:none;margin-bottom:1rem;{ADDITIONAL}}'
class Profile(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=400)
    owner = models.ForeignKey('welcome_app.User', on_delete=models.CASCADE,)

    image = models.ImageField(upload_to='media', null=True)
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

    # card = models.CharField(max_length=8, default='#15151E', verbose_name='card')
    
    avatar_shape = models.IntegerField(default=3) #1-4
    button_shape = models.IntegerField(default=1) #1-3
    button_type = models.IntegerField(default=1) # 1-4
    
    button_font = models.CharField(max_length=8, default='#D0EEFF', verbose_name='button font')
    background = models.CharField(max_length=8, default='#172C38', verbose_name='background')
    font = models.CharField(max_length=8, default='#FFFFFF', verbose_name='font')
    button = models.CharField(max_length=8, default='#172C38', verbose_name='button')
    outline = models.CharField(max_length=8, default='#172C38', verbose_name='outline')
    shadow = models.CharField(max_length=8, default='#FFFFFF', verbose_name='shadow')

    font_name = models.ForeignKey('customing_app.Font', on_delete=models.CASCADE, blank=True, null=True)



    class Meta:
        db_table = 'ColorScheme'
        verbose_name = 'цветовую схему'
        verbose_name_plural = 'цветовые схемы'
    
    def __str__(self) -> str:
        return f'Схема {self.owner.name}'
    
    def set_color(self, color_id:str, color_hash:str):
        if self.check_color(color_hash):
            color_id = color_id.replace('-color-input', '')
            match color_id:
                case "shadow":
                    self.shadow = color_hash
                case "button":
                    self.button = color_hash
                case "outline":
                    self.outline = color_hash
                case "button-text":
                    self.button_font = color_hash
                case "font":
                    self.font = color_hash
                case "background":
                    self.background = color_hash
                case _:
                    return False
            self.save()
            return True
        return False
            
    def set_font(self, font):
        font_id = int(font.split('_')[1])
        font = Font.objects.filter(id=font_id).first()
        if font is not None:
            self.font_name = font
            self.save()
            return True
        return False

    def get_button_css(self) -> str:
        baza = BTN_BASE.replace(r'{ADDITIONAL}', ADDITIONAL_CSS_BTNS[self.button_type-1])
        baza = baza.replace(r'{BTN}', self.button)
        baza = baza.replace(r'{BTN_FONT}', self.button_font)
        baza = baza.replace(r'{SHADOW}', self.shadow)
        baza = baza.replace(r'{OUTLINE}', self.outline)
        baza = baza.replace(r'{RADIUS}', RADIUSES[self.button_shape-1])
        if self.button_type == 3:
            baza = baza.replace(r'{SHADOW_RGB}', hex_to_rgb(self.shadow))
        return baza

    def get_ava_radius(self) -> str:
        return AVA_RADIUSES[self.avatar_shape]

    def get_font(self):
        if self.font_name is not None:
            return self.font_name.gfont()
        return Font.objects.first().gfont()
    
    def name_font(self):
        if self.font_name is not None:
            return self.font_name.name
        return Font.objects.first().name
    
    def img_font(self):
        if self.font_name is not None:
            return self.font_name.img_name
        return Font.objects.first().img_name

    def check_color(self, color: str) -> bool:
        is_ok = re.search(COLOR_REGEX, color)
        if is_ok is None:
            return False
        return True

class Font(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название шрифта')
    img_name = models.CharField(max_length=40, verbose_name='картинка')

    def __str__(self) -> str:
        return f'Шрифт {self.name}'
    
    def as_json(self) -> tuple:
        return [self.id, self.name, self.img_name]
    
    def gfont(self):
        return self.name.title().replace(' ', '+')

    class Meta:
        db_table = 'Fonts'
        verbose_name = 'шрифт'
        verbose_name_plural = 'шрифты'


def add_fonts():
    "Создаёт модели шрифтов, запускать если их нет"
    with open("font_pic_generator/font_list.txt", "r") as file:
        font_list = file.read().splitlines()
    for font in font_list:
        new_font = Font()
        new_font.name = font.title()
        new_font.img_name = font.replace(' ', "_")
        new_font.save()


def get_fonts():
    unsorted = tuple(font.as_json() for font in Font.objects.all())
    return tuple(unsorted[i:i+2] for i in range(0, len(unsorted), 2))


def hex_to_rgb(hex_code:str):
    hex_code = hex_code.lstrip('#')
    return str(tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))[1:-1]


def check_link_correct(link:str) -> bool:
    #TODO: перенести в более подходящее место
    link = link.replace('http://', '').replace('https://', '')
    is_ok = re.search(LINK_REGEX, link)
    if is_ok is None:
        return False
    return True
