#Copyright (c) 2009 - Rui Batista <rui.batista@ist.utl.pt>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""wikicreole 1.0 plugin

See spec at 
http://www.wikicreole.org/wiki/Creole1.0#section-Creole1.0-ImageInline

"""

import creole, creole2html

def render(content, *args, ** kwargs):
    parser = creole.Parser(content.encode('utf8', 'ignore'))
    document = parser.parse()
    return creole2html.HtmlEmitter(document).emit()
