from wx import Platform

from Consts import FormatTypes

from WikidPad.lib.pwiki.StringOps import colorDescToRgbTuple


if Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'heading4': 10,
              'heading3': 11,
              'heading2': 12,
              'heading1': 12
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Consolas', #'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 10,
              'heading4': 10,
              'heading3': 11,
              'heading2': 12,
              'heading1': 12
             }


if Platform == '__WXMSW__':
    INTHTML_FONTSIZES = (7, 8, 10, 12, 16, 22, 30)

elif Platform == '__WXMAC__':
    INTHTML_FONTSIZES = (9, 12, 14, 18, 24, 30, 36)

else:
    INTHTML_FONTSIZES = (10, 12, 14, 16, 19, 24, 32)
    INTHTML_FONTSIZES = (10, 10, 10, 10, 10, 12, 14)


def getStyles(styleFaces, config):
    # Read colors from config
    colPlaintext = config.get("main", "editor_plaintext_color", "#000000")
    colLink      = config.get("main", "editor_link_color",      "#0000BB")
    colAttribute = config.get("main", "editor_attribute_color", "#555555")

    # Check validity
    if colorDescToRgbTuple(colPlaintext) is None:
        colPlaintext = "#000000"
    if colorDescToRgbTuple(colLink) is None:
        colLink = "#0000BB"
    if colorDescToRgbTuple(colAttribute) is None:
        colAttribute = "#555555"

    # Add colors to dictionary:
    styleFaces = styleFaces.copy()
    styleFaces.update({"colPlaintext":       colPlaintext,
                       "colLink":            colLink,
                       "colAttribute":       colAttribute,
                       "darkgreen":          "#269900",
                       "grey":               "#707070",
                       "bordeaux":           "#940000"})   #5D7EDF

         # fore:#0000BB,face:Consolas,size:10

    return [(FormatTypes.Default,
             "face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.WikiWord,
             "fore:%(grey)s,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.AvailWikiWord,
             "fore:%(colLink)s,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.Bold,
             "fore:%(colPlaintext)s,bold,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.Italic,
             "fore:%(colPlaintext)s,italic,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.Heading4,
             "fore:%(bordeaux)s,bold,face:%(mono)s,size:%(heading4)d" % styleFaces),
            (FormatTypes.Heading3,
             "fore:%(bordeaux)s,bold,face:%(mono)s,size:%(heading3)d" % styleFaces),
            (FormatTypes.Heading2,
             "fore:%(bordeaux)s,bold,face:%(mono)s,size:%(heading2)d" % styleFaces),
            (FormatTypes.Heading1,
             "fore:%(bordeaux)s,bold,face:%(mono)s,size:%(heading1)d" % styleFaces),
            (FormatTypes.Url,
             "fore:%(colLink)s,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.Script,
             "fore:%(colAttribute)s,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.Attribute,
             "bold,fore:%(colAttribute)s,face:%(mono)s,size:%(size)d" % styleFaces),
            (FormatTypes.ToDo,
             "fore:%(darkgreen)s,bold,face:%(mono)s,size:%(size)d" % styleFaces)]