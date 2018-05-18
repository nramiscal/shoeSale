from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# Create your models here.
class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []

        if len(form['fname']) < 2:
            errors.append("First name must be at least 2 characters.")
        if len(form['lname']) < 2:
            errors.append("Last name must be at least 2 characters.")
        if not form['email']:
            errors.append("Email required.")
        elif not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif User.objects.filter(email=form['email']):
             errors.append("Account already exists.")
        if len(form['password']) < 5:
            errors.append("Password must have at least 5 characters.")

        if len(errors) == 0:
            hash1 = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(fname=form['fname'], lname=form['lname'], email=form['email'], password=hash1)
            return (True, user)
        else:
            return (False, errors)

    def loginValidator(self, form):

        errors = []

        if not form['email']:
            errors.append("Email required.")
        elif not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif not User.objects.filter(email=form['email']):
             errors.append("Please register first")

        elif len(form['password']) < 5:
            errors.append("Password must have at least 5 characters.")
        else:
            user = User.objects.filter(email=form['email'])
            if not bcrypt.checkpw(form['password'].encode(), user[0].password.encode()):
                errors.append("Password does not match password in database.")

        if not errors:
            return (True, user[0])
        else:
            return (False, errors)


class ProductValidator(models.Manager):

    def productValidator(self, form, id):

        errors = []

        if not form['name']:
            errors.append("Name cannot be empty.")
        if not form['price']:
            errors.append("Price cannot be empty.")

        if not errors:
            product = Product.objects.create(name=form['name'], price=form['price'], seller_id=id)
            return (True, product)
        else:
            return (False, errors)


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __repr__(self):
        return "<User {}| {} {} | {}".format(self.id, self.fname, self.lname, self.email)

    objects = UserManager()



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    isSold = models.BooleanField(default=False)
    seller = models.ForeignKey(User, related_name="products")

    def __repr__(self):
        return "<Product {}| {} {} | {}".format(self.id, self.name, self.price, self.isSold)

    objects = ProductValidator()

class Sales(models.Model):
    product = models.ForeignKey(Product, related_name="sales_product")
    buyer = models.ForeignKey(User, related_name="sales_buyer")
    date_sold = models.DateTimeField(auto_now_add = True)
