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

file = open("{}/.gitignore".format(dir), "w")
line = [
    ".vscode/\n",
    "*.log\n",
    ".pyc\n",
    "__pycache__/\n",
    "db-volumes/\n",
    "db.sqlite3\n",
    "dump.rdb\n",
]
file.writelines(line)
file.close()

run("mkdir templates", shell=True, cwd="{}/{}".format(dir, dir))
run("mkdir static", shell=True, cwd="{}/{}".format(dir, dir))
run("mkdir css", shell=True, cwd="{}/{}/static".format(dir, dir))
run("mkdir js", shell=True, cwd="{}/{}/static".format(dir, dir))
run("mkdir img", shell=True, cwd="{}/{}/static".format(dir, dir))

if len(sys.argv) == 3:
    #channels-setting
    if sys.argv[2] == "channels":
        file = open("{}/config/asgi.py".format(dir, dir), "w")
        line = [
            '"""\n',
            "ASGI config for config project.\n",
            "\n",
            "It exposes the ASGI callable as a module-level variable named ``application``.\n",
            "\n",
            "For more information on this file, see\n",
            "https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/\n",
            '"""\n',
            "\n",
            "import os\n",
            "\n",
            "from channels.auth import AuthMiddlewareStack\n",
            "from channels.routing import ProtocolTypeRouter, URLRouter\n",
            "from django.core.asgi import get_asgi_application\n",
            "import {}.routing\n".format(dir),
            "\n",
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\n",
            "\n",
            "application = ProtocolTypeRouter({\n",
            '    "http": get_asgi_application(),\n',
            '    "websocket": AuthMiddlewareStack(\n',
            '        URLRouter(\n',
            '            {}.routing.websocket_urlpatterns\n'.format(dir),
            '        )\n',
            '    ),\n',
            '})\n'
        ]

        file.writelines(line)
        file.close()

        file = open("{}/config/settings.py".format(dir), "r")
        line = file.readlines()
        line.insert(33, "    'channels',\n")
        newInsertLine = [
            "\n",
            "ASGI_APPLICATION = 'config.asgi.application'\n",
            "\n",
            "CHANNEL_LAYERS = {\n",
            "    'default': {\n",
            "        'BACKEND': 'channels_redis.core.RedisChannelLayer',\n",
            "        'CONFIG': {\n",
            "            'hosts': [('127.0.0.1', 6379)],\n",
            "        },\n",
            "    },\n",
            "}\n",
        ]
        
        file.close()

        file = open("{}/config/settings.py".format(dir), "w")
        file.writelines(line + newInsertLine)
        file.close()

        file = open("{}/{}/routing.py".format(dir, dir), "w")
        line = [
            "from django.urls import path\n",
            "\n",
            "from . import consumers\n",
            "\n",
            "websocket_urlpatterns = [\n",
            "    \n",
            "]\n",
        ]

        file.writelines(line)
        file.close()

        file = open("{}/{}/consumers.py".format(dir, dir), "w")
        line = [
            "from asgiref.sync import async_to_sync\n",
            "from channels.generic.websocket import WebsocketConsumer\n",
            "import json\n",
        ]

        file.writelines(line)
        file.close()