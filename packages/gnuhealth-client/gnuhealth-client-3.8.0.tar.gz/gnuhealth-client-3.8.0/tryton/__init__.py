# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import gi
import locale

SERVER_VERSION = "5.0.0"

# Load the latest patchset version
with open('../version') as f:
    __version__ = f.read()

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_foreign('cairo')
try:
    gi.require_version('GtkSpell', '3.0')
except ValueError:
    pass

try:
    # Import earlier otherwise there is a segmentation fault on MSYS2
    import goocalendar
except ImportError:
    pass

if not hasattr(locale, 'localize'):
    def localize(formatted, grouping=False, monetary=False):
        if '.' in formatted:
            seps = 0
            parts = formatted.split('.')
            if grouping:
                parts[0], seps = locale._group(parts[0], monetary=monetary)
            decimal_point = locale.localeconv()[
                monetary and 'mon_decimal_point' or 'decimal_point']
            formatted = decimal_point.join(parts)
            if seps:
                formatted = locale._strip_padding(formatted, seps)
        else:
            seps = 0
            if grouping:
                formatted, seps = locale._group(formatted, monetary=monetary)
            if seps:
                formatted = locale._strip_padding(formatted, seps)
        return formatted
    setattr(locale, 'localize', localize)
