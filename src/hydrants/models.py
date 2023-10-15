from django.db import models

class TechnicalConditionChoices(models.TextChoices):
    """
    Choices for technical condition.
    """
    DEFECTIVE = "несправний", "Несправний"
    SERVICEABLE = "справний", "Справний"
    OFFSET = "зміщений", "Зміщений"


class TypeHydrantChoices(models.TextChoices):
    """
    Choices for type hydrants.
    """
    STREET = "вулиичний", "Вуличний"
    THE_OBJECT = "об'єктовий", "Об'єктовий"


class TypeLocationChoices(models.TextChoices):
    """
    Choices for type locations.
    """
    UNDERGROUND = "підземний", "Підземний"
    above_the_ground = "надземний", "Надземний"


class TypeWaterNetworkChoices(models.TextChoices):
    """
    Choices for type water network.
    """
    K = "K", "K",
    T = "T", "T"


class TypeDiameterChoices(models.IntegerChoices):
    """
    Choices for type diameter.
    """
    DIAMETER_20 = 20, '20'
    DIAMETER_40 = 40, '40'
    DIAMETER_50 = 50, '50'
    DIAMETER_65 = 65, '65'
    DIAMETER_70 = 70, '70'
    DIAMETER_75 = 75, '75'
    DIAMETER_76 = 76, '76'
    DIAMETER_80 = 80, '80'
    DIAMETER_86 = 86, '86'
    DIAMETER_100 = 100, '100'
    DIAMETER_102 = 102, '102'
    DIAMETER_110 = 110, '110'
    DIAMETER_120 = 120, '120'
    DIAMETER_125 = 125, '125'
    DIAMETER_150 = 150, '150'
    DIAMETER_160 = 160, '160'
    DIAMETER_175 = 175, '175'
    DIAMETER_180 = 180, '180'
    DIAMETER_200 = 200, '200'
    DIAMETER_219 = 219, '219'
    DIAMETER_222 = 222, '222'
    DIAMETER_225 = 225, '225'
    DIAMETER_250 = 250, '250'
    DIAMETER_273 = 273, '273'
    DIAMETER_300 = 300, '300'
    DIAMETER_315 = 315, '315'
    DIAMETER_320 = 320, '320'
    DIAMETER_325 = 325, '325'
    DIAMETER_350 = 350, '350'
    DIAMETER_400 = 400, '400'
    DIAMETER_500 = 500, '500'
    DIAMETER_600 = 600, '600'


class Hydrant(models.Model):
    """
    Model for hydrants.
    """

    technical_condition = models.CharField(
        max_length=10,
        choices=TechnicalConditionChoices.choices,
        default=TechnicalConditionChoices.SERVICEABLE,
        verbose_name="Технічний стан"
    )
    type_hydrant = models.CharField(
        max_length=10,
        choices=TypeHydrantChoices.choices,
        default=TypeHydrantChoices.STREET,
        verbose_name="Тип гідранта"
    )
    type_location = models.CharField(
        max_length=10,
        choices=TypeLocationChoices.choices,
        default=TypeLocationChoices.UNDERGROUND,
        verbose_name="Вид розташування"
    )

    type_water_network = models.CharField(
        max_length=1,
        choices=TypeWaterNetworkChoices.choices,
        null=True,
        verbose_name="Тип водомережі"
    )
    type_diameter = models.IntegerField(
        choices=TypeDiameterChoices.choices,
        verbose_name="Тип діаметра"
    )
    address = models.CharField(max_length=1024, verbose_name="Прив'язка до адреси")
    description = models.TextField(verbose_name="Опис")
    coordinates = models.CharField(max_length=256, unique=True, verbose_name="Координати розташування")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    image = models.ImageField(verbose_name="Фото", upload_to="hydrants/images/", blank=True, null=True)

    owner = models.ForeignKey(
        "Owner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hydrants",
        verbose_name="Балансоутримувач"
    )

    subdivision = models.ForeignKey(
        "Subdivision",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subdivision_hydrants",
        verbose_name="Підрозділ"
    )

    class Meta:
        """
        Set custom verbose name.
        """

        verbose_name = "Гідрант"
        verbose_name_plural = "Гідрант"

    def __str__(self):
        """
        Representation str object.
        """
        return self.address


class Subdivision(models.Model):
    """
    Model for subdivisions
    """
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name="Назва підрозділу"
    )

    class Meta:
        """
        Set custom verbose name.
        """

        verbose_name = "Підрозділ"
        verbose_name_plural = "Підрозділ"

    def __str__(self):
        """
        Representation str object.
        """
        return self.name


class Owner(models.Model):
    """
    Model for owner hydrants
    """
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name="Назва балансоутримувача"
    )

    class Meta:
        """
        Set custom verbose name.
        """

        verbose_name = "Балансоутримувач"
        verbose_name_plural = "Балансоутримувач"

    def __str__(self):
        """
        Representation str object.
        """
        return self.name

