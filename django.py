from subprocess import run
import sys

if len(sys.argv) == 1:
    raise Exception("Usage:python3 django.py YOUR_APP_NAME")

dir = sys.argv[1]
run("mkdir {}".format(dir), shell=True)
run("django-admin startproject config {}".format(dir), shell=True)
run("python3 manage.py startapp {}".format(dir, dir), shell=True, cwd=dir)

file = open("{}/config/settings.py".format(dir), "r")
line = file.readlines()
line.insert(39, "    '{}',\n".format(dir))
line[106] = "LANGUAGE_CODE = 'ja'\n"
line[108] = "TIME_ZONE = 'Asia/Tokyo'\n" 
file.close()

file = open("{}/config/settings.py".format(dir), "w")
file.writelines(line)
file.close()

file = open("{}/config/urls.py".format(dir), "r")
line = file.readlines()
line[16] = "from django.urls import path, include"
line.insert(20, "    path('',include('{}.urls')),\n".format(dir))
file.close()

file = open("{}/config/urls.py".format(dir), "w")
file.writelines(line)
file.close()

file = open("{}/{}/urls.py".format(dir, dir), "w")
line = [
    "from django.urls import path\n",
    "from . import views\n",
    "\n",
    "urlpatterns = []\n",
]

file.writelines(line)
file.close()

run("mkdir templates", shell=True, cwd="{}/{}".format(dir, dir))
run("mkdir static", shell=True, cwd="{}/{}".format(dir, dir))
run("mkdir css", shell=True, cwd="{}/{}/static".format(dir, dir))
run("mkdir js", shell=True, cwd="{}/{}/static".format(dir, dir))
run("mkdir ", shell=True, cwd="{}/{}/static".format(dir, dir))
