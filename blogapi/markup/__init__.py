def render_markup(content, markup):
    renderer = __import__(markup, globals())
    return renderer.render(content, markup)

