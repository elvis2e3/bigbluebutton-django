#! /bin/bash
echo "====== Iniciar Migracion de la Base de Datos ========"
python manage.py makemigrations
python manage.py migrate
echo "======= Fin de Migracion de la Base de Datos ========"
echo "                  <========>"
echo "============== Crendo grupos o roles ================"
python manage.py crear_roles
echo "========= Fin del creado de grupos o roles =========="
echo "                  <========>"
echo "========= Crendo usuario Admin por defecto =========="
python manage.py crear_usuario_admin
echo "=========== Fin del creado usuario Admin ============"