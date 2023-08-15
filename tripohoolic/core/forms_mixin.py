class DisabledFormMixin:
    disabled_fields = ()
    fields = {}

    def _disable_fields(self):
        if self.disabled_fields == '__all__':
            fields = self.disabled_fields
        else:
            fields = self.disabled_fields

        # fields = self.disabled_fields if self.disabled_fields != '__all__' else self.fields.keys()

        for field_name in fields:
            if field_name in self.disabled_fields:
                field = self.fields[field_name]
                # field.widget.attrs['disabled'] = 'disabled'
                field.widget.attrs['readonly'] = 'readonly'