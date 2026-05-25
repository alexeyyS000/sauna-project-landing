from wagtail.admin.panels import FieldPanel





class CodeMirrorPanel(FieldPanel):
    template = "custom_panels/code_mirror_panel.html"

    class Media:
        css = {"all": ["css/codemirror.css"]}
        js = [
            "js/codemirror/codemirror.js",
            "js/codemirror/htmlmixed.js",
            "js/codemirror/closetag.js",
        ]
