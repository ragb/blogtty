import creole, creole2html

def render(content, *args, ** kwargs):
    parser = creole.Parser(content)
    document = parser.parse()
    return creole2html.HtmlEmitter(document).emit()
