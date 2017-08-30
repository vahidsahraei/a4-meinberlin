import datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import widgets as form_widgets
from django.template.loader import render_to_string
from django.utils.timezone import localtime


class DateTimeInput(form_widgets.SplitDateTimeWidget):
    def __init__(self, time_label='', time_default=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_label = time_label
        self.time_default = time_default or datetime.time(hour=0, minute=0)

    class Media:
        js = (
            staticfiles_storage.url('datepicker.js'),
        )
        css = {'all': [
            staticfiles_storage.url('datepicker.css'),
        ]}

    def render(self, name, value, attrs=None):
        date_attrs = self.build_attrs(attrs)
        date_attrs.update({
            'class': 'datepicker',
            'placeholder': self.widgets[0].format_value(datetime.date.today()),
            'id': attrs['id'] + '_date'
        })
        time_attrs = self.build_attrs(attrs)
        time_attrs.update({
            'class': 'timepicker',
            'placeholder': self.widgets[1].format_value(
                self.get_default_time()),
            'id': attrs['id'] + '_time'
        })

        if isinstance(value, datetime.datetime):
            value = localtime(value)
            date = value.date()
            time = value.time()
        else:
            # value's just a list in case of an error
            date = value[0] if value else None
            time = value[1] if value else None

        return render_to_string(
            'meinberlin_datetimefield/datetime_input.html', {
                'date': self.widgets[0].render(
                    name + '_0',
                    date,
                    date_attrs
                ),
                'time': self.widgets[1].render(
                    name + '_1',
                    time,
                    time_attrs
                ),
                'time_label': {
                    'label': self.time_label,
                    'id_for_label': attrs['id'] + '_time'
                },
            })

    def id_for_label(self, id_):
        if id_:
            id_ += '_date'
        return id_

    def get_default_time(self):
        time_widget = self.widgets[1]

        if not self.time_default:
            return time_widget.format_value(datetime.time(hour=0, minute=0))
        elif isinstance(self.time_default, (datetime.time, datetime.datetime)):
            return time_widget.format_value(self.time_default)
        else:
            return self.time_default
