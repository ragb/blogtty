"""
textile markup plugin

You will need the pytextile library from
http://pytextile.sourceforge.net
"""


import textile

def render(content, *args, **kwargs):
    return textile.Textiler(content).process()
