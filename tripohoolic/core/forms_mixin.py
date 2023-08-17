class DisabledFormMixin:
    disabled_fields = []
    fields = {}

    def _disable_fields(self):
        for field_name in self.disabled_fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['readonly'] = 'readonly'
