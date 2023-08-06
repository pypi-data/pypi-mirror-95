# django-crontab-manager

Manage crontab tasks on web. Update crontab file on system while changes made on manager. Work with django-crontab-agent.

## Install

```
pip install django-crontab-manager
```

## Usage

*settings.py*

```
INSTALLED_APPS = [
    'django_apiview',
    'django_fastadmin',
    'django_crontab_manager',
]
```

## Usage

1. Setup django-crontab-manager at server side. django-crontab-manager is a simple django application, include it in django project.
1. Install django-crontab-agent on all target linux server.

## Releases

### v0.1.13 2020/01/29

- First release.