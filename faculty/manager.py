from django.contrib.auth.base_user import BaseUserManager
import random

#manager to manage custom user model
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("email is required")
        
        email= self.normalize_email(email)
        user= self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superAdmin', True)
        # extra_fields.setdefault('fid', f"SADMIN{random.randint(1, 99):02d}")
        extra_fields.setdefault('name', "System Admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super user must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        
        return self.create_user(email, password, **extra_fields)