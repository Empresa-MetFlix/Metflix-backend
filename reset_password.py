import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from core.models import User

# Deletar usuario antigo (se existir)
User.objects.filter(email='arthurlanznaster@gmail.com').delete()
print("Usuarios antigos deletados")

# Criar usuario manualmente (SEM cpf e nome, USAR name)
user = User(
    email='arthurlanznaster@gmail.com',
    name='Arthur Lanznaster',  # ✅ É 'name', não 'nome'
    is_superuser=True,
    is_staff=True,
    is_active=True
)

# Definir senha
user.set_password('Lanz2006')
user.save()

print(f"✅ Usuario criado: {user.email}")
print(f"👤 Nome: {user.name}")
print(f"🔑 Senha: Lanz2006")
print(f"👑 Superuser: {user.is_superuser}")
print(f"🔐 Teste senha: {user.check_password('Lanz2006')}")

print("\n🚀 Agora inicie o Django e teste no frontend:")
print("   python manage.py runserver")
