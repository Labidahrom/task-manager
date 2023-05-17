class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields:
            self.fields[field].widget. \
                attrs.update({'class': 'form-control mb-3'})
