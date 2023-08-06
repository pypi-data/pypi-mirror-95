
# django-excel-export

A Django library for exporting data.

Features:

- support xlsx, xls, docx

## How to install

```sh
$ pip install excel-exporter
```


## How to use

Export is achieved by subclassing ExportAdmin, which implements export as an admin action.

```python
# app/admin.py
from excel_exporter.admin import ExportAdmin

class PersonAdmin(ExportAdmin):
    list_display = ( 'name', 'address', 'date', 'image')
    export_fields = ('name', 'address', 'float', 'time', 'date', 'image')
    
```

![avatar](./images/person_export.png)

