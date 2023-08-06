# django-morris
A hexadecimal color field with a preview.

## Installation
- Run `pip install django-morris`
- Add `morris` to `settings.INSTALLED_APPS`
- Run `python manage.py collectstatic`
- Restart your application server

## Usage
### Models
Just add a color field to your models like this:

```python
from django.db import models
from morris.fields import HexColorField

class MyModel(model.Model):
    color = HexColorField()
```

## Credits
*Heavily* inspired from
[django-colorfield](https://github.com/fabiocaccamo/django-colorfield). If you
need a color picker you should use `django-colorfield` instead of this package.

## License
Released under [MIT License](LICENSE.txt).
