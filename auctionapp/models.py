from django.db import models
from datetime import datetime


from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)

# Inheriting from AbstractUser
# Creating users here and giving them specific proppreties.


class CustomManager(BaseUserManager):
    def create_user(self, email, password, **extraFields):
        extraFields.setdefault('is_staff', False)
        extraFields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            **extraFields,
            password=password

        )

        # if not extraFields.get("is_superuser") and extraFields.get('is_staff'):
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extraFields):
        extraFields.setdefault('is_superuser', True)
        extraFields.setdefault('is_staff', True)
        user = self.create_user(
            email=self.normalize_email(email),
            **extraFields,
            password=password
        )

        # if extraFields.get("is_staff") and extraFields.get("is_superuser"):

        return user


class Account(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    profileImage = models.ImageField(
        null=True, blank=True, default="../static/images/defaultImage.svg")
    dOB = models.DateField()
    phoneNumber = models.IntegerField(blank=True, null=True)
    addressLine1 = models.CharField(max_length=200, blank=True)
    addressLine2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    # Users have to login with email
    USERNAME_FIELD = 'email'

    # Admins login with Username?
    REQUIRED_FIELDS = ['profileImage', 'username', 'first_name', 'last_name', 'dOB',
                       'phoneNumber', 'addressLine1', 'addressLine2', 'city', 'postcode', 'country']
    objects = CustomManager()
    # pass

    # Do not need to specify the type of the self parameter.
    # The self parameter is a reference to the instance of the class that the method is being called on, and it does not have a fixed type.
    def __str__(self) -> str:
        return self.email

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'profileImage': self.profileImage.url,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dOB': self.dOB,
            'phoneNumber': self.phoneNumber,
            'addressLine1': self.addressLine1,
            'addressLine2': self.addressLine2,
            'city': self.city,
            'postcode': self.postcode,
            'country': self.country,
        }


class Item(models.Model):
    OTHER = "OTHER"
    SPORTS = "SP"
    TECHNOLOGY = "TECH"
    CLOTHES = "CLTH"
    KITCHEN = "KIT"
    ITEM_TAGS_CHOICES = [
        (SPORTS, 'Sports'),
        (TECHNOLOGY, 'Technology'),
        (CLOTHES, 'Clothes'),
        (KITCHEN, 'Kitchen'),
        (OTHER, 'Other'),
    ]
    item_tag = models.CharField(
        max_length=10, choices=ITEM_TAGS_CHOICES, default=OTHER)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    active = models.BooleanField(default=True, blank=True, null=True)
    description = models.TextField()
    startingPrice = models.DecimalField(decimal_places=2, max_digits=10)
    pictureOfItem = models.ImageField()
    startDateTimeItem = models.DateTimeField()
    endDateTimeItem = models.DateTimeField()

    # Do not need to specify the type of the self parameter.
    # The self parameter is a reference to the instance of the class that the method is being called on, and it does not have a fixed type.
    def __str__(self) -> str:
        return self.title

    def to_dict(self) -> dict[str]:
        model_dict = self.user.username
        userId = self.user.id
        currentDateTime = datetime.now()
        currentDateTime = currentDateTime.replace(tzinfo=None)
        endDateTimeItem = self.endDateTimeItem.replace(tzinfo=None)
        if currentDateTime > endDateTimeItem:
            self.active = False

        return {
            'id': self.id,
            'item_tag': self.item_tag,
            'user_id': userId,
            'active': self.active,
            'user': model_dict,
            'pictureOfItem': self.pictureOfItem.url,
            'title': self.title,
            'description': self.description,
            'startingPrice': self.startingPrice,
            'startDateTimeItem': self.startDateTimeItem,
            'endDateTimeItem': self.endDateTimeItem,
        }


class Bid(models.Model):
    # userFK
    userIDFK = models.ForeignKey(Account, on_delete=models.CASCADE)
    # ItemFK
    itemIDFK = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidAmount = models.DecimalField(decimal_places=2, max_digits=10)
    dateTimeBids = models.DateTimeField()

    # Do not need to specify the type of the self parameter.
    # The self parameter is a reference to the instance of the class that the method is being called on, and it does not have a fixed type.
    def __str__(self) -> str:
        return str(self.itemIDFK)

    def to_dict(self) -> dict[str]:
        return {
            'bidAmount': self.bidAmount,
            'user': self.userIDFK.username,
            'dateTimeBids': self.dateTimeBids
        }


class Question(models.Model):
    userFK = models.ForeignKey(Account, on_delete=models.CASCADE)
    itemFK = models.ForeignKey(Item, on_delete=models.CASCADE)
    questionText = models.TextField()
    dateTimeOfQuestion = models.DateTimeField()

    # Do not need to specify the type of the self parameter.
    # The self parameter is a reference to the instance of the class that the method is being called on, and it does not have a fixed type.
    def __str__(self) -> str:
        return str(self.questionText)

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'questionText': self.questionText,
            'user': self.userFK.username,
            'dateTimeOfQuestion': self.dateTimeOfQuestion
        }


class Answer(models.Model):
    questionFK = models.OneToOneField(Question, on_delete=models.CASCADE)
    answerText = models.TextField()
    dateTimeOfAnswer = models.DateTimeField()

    # Do not need to specify the type of the self parameter.
    # The self parameter is a reference to the instance of the class that the method is being called on, and it does not have a fixed type.
    def __str__(self) -> str:
        return str(self.questionFK)

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'questionID': self.questionFK.id,
            'answerText': self.answerText,
            'dateTimeOfAnswer': self.dateTimeOfAnswer
        }
