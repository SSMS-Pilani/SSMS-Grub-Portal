import os


def add_user():
	a=User.objects.get_or_create(username="r",password="rango123",is_superuser=True)
	

# Start execution here!
if __name__ == '__main__':
	print "Starting Vk hwing population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
	from django.contrib.auth.models import User
	add_user()
