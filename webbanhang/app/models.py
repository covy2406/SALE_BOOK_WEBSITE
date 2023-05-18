from django.db import models
import uuid
import datetime
# Code  Model Trọng

class Persons(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=20,unique=True)
    Address = models.CharField(max_length=300)
    DateOfBirth = models.DateField(default=datetime.date.today)
    Password = models.CharField(max_length=20)
    Status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.Id} {self.Name} {self.Phone} {self.Address} {self.DateOfBirth}  {self.Password}"

class Categories(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Id} {self.Name}"
    
class Books(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=300)
    Author = models.CharField(max_length=100)
    Language = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    CategoryId = models.ForeignKey(Categories, on_delete=models.PROTECT)
    PublishDate = models.DateField(default=datetime.date.today)
    Status = models.BooleanField(default=False)
    Price = models.IntegerField()
    EntryPrice = models.IntegerField()
    Quantity = models.IntegerField()
    Image = models.ImageField(upload_to='images')
    Description = models.CharField(max_length=1000)
    SellNumber= models.IntegerField(default=0)
    # Time = models.DateTimeField(default=datetime.date.today.now)

    def __str__(self):
        return f"{self.Id} {self.Name} {self.Author} {self.Language} {self.Country} {self.CategoryId} {self.PublishDate} {self.Status} {self.Price} {self.EntryPrice} {self.Quantity} {self.Image} {self.Description}"
    
class Carts(models.Model):
    Id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PersonId = models.ForeignKey(Persons, on_delete=models.PROTECT)
    BookId = models.ForeignKey(Books, on_delete=models.PROTECT)
    Quantity = models.IntegerField()

    def __str__(self):
        return f"{self.Id} {self.PersonId} {self.BookId} {self.Quantity}"
