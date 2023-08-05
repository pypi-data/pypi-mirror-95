# Django Cleanup Ignore Directories

This is an Extension of the django-cleanup project v4.0.0. This extension allows ignoring files in specified user directories from deletion.
The original project is this [one](https://pypi.org/project/django-cleanup/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Django Cleanup Ignore Directories.

```bash
django-cleanup-ignore-directories
```

## Configuration
In the settings.py file in your Django main app, add the below in the installed apps section:

```python
INSTALLED_APPS = [
    ...
    'django_cleanup_ignore_directories.apps.CleanupConfig',
    ...
]
```

Also in the settings.py file, you need to add the directories to be ignored as a python list as below.

```python
DJANGO_CLEANUP_IGNORE_DIRECTORIES = ['article_pics/default', 'default_pics']
```
Add this at the very bottom of your settings file.

## License
[MIT](https://choosealicense.com/licenses/mit/)