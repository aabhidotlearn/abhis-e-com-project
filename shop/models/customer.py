from django.db import models

#create your models her
class Customer(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=200)


    #chercking if email is existing or not
    def isexist(self):
        return Customer.objects.filter(email__iexact=self.email).exists()

    #to check email id is matching or not
    @staticmethod
    def getemail(email):
        return Customer.objects.filter(email__iexact=email).first()
