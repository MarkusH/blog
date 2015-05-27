from docutils import nodes


class gallery_node(nodes.bullet_list):
    pass


class project_node(nodes.BackLinkable, nodes.Element):
    pass


class project_list(nodes.bullet_list):
    pass


class project_desc(nodes.list_item):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        nodes.list_item.__init__(self, *args, **kwargs)


class project_code(nodes.TextElement):
    label = 'Code'
    icon = 'icon-code-array'


class project_docs(nodes.TextElement):
    label = 'Documentation'
    icon = 'icon-file-document'


class project_download(nodes.TextElement):
    label = 'Download'
    icon = 'icon-download'


class project_homepage(nodes.TextElement):
    label = 'Homepage'
    icon = 'icon-link'


class project_license(nodes.TextElement):
    label = 'License'
    icon = 'icon-gavel'
