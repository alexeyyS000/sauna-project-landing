from django import forms
from wagtail.blocks import RawHTMLBlock
from wagtail.admin.staticfiles import versioned_static

class CodeMirrorWidget(forms.Textarea):
    class Media:
        js = [
            versioned_static("home/static/codemirror.js"),
            # versioned_static("path/to/htmlmixed.js"),
            # versioned_static("path/to/xml.js"),
            # versioned_static("path/to/css.js"),
            # versioned_static("path/to/javascript.js"),
        ]
        css = {
            'all': [
                versioned_static("path/to/codemirror.css"),
            ]
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'codemirror-textarea'})

class CodeMirrorHTMLBlock(RawHTMLBlock):
    def get_prep_value(self, value):
        return super().get_prep_value(value)

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CodeMirrorWidget()
        super().__init__(*args, **kwargs)
