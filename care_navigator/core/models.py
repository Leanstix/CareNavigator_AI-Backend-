from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Extend the default user model to include roles (e.g., patient or provider)
class User(AbstractUser):
    ROLES = (
        ('patient', 'Patient'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Override related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Custom related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Custom related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username


# Healthcare provider model
class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"


# Appointment model
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='appointments_as_provider')
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('completed', 'Completed')), default='pending')

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.provider.user.username} on {self.date}"
