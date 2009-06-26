import wikimarkup

def render(content, *args, **kwargs):
    return wikimarkup.parse(content, *args, **kwargs)
