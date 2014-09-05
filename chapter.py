"""
Represents a chapter, which is a collection of slides, together with sound
transitions.  Each slide is of type 'Slide'.
"""

from collections import namedtuple
from xml.dom import minidom

# Has a path to a picture and/or sound file
# If one of them is None, it means the slide represents a transition of the
# other, which the one given by None remains the same.
#
# Example: ('blah1.jpg', None) means transition the picture to blah1.jpg, but
# keep the current running sound the same.
Slide = namedtuple("Slide", "picture sound")

class Chapter(object):
    """
    Represents a collection of slides, which are defined in an XML file
    """
    def __init__(self, script_path):
        """
        Args:
            script_path: path to an XML file defining this chapter.  See
            example.xml
        """
        self.script_path = script_path
        self.slides = []
        self.reload()

    def reload(self):
        """
        (Re)instantiates this chapter from it's script_file
        """
        self.slides = []

        xmld = minidom.parse(self.script_path)
        chapters = xmld.getElementsByTagName('Chapter')

        assert len(chapters) == 1, "Script file does not contain 1 chapter"

        scenes = chapters[0].getElementsByTagName('Scene')

        assert len(scenes) > 0, "Not much point in having a chapter with " \
                "no scenes, eh?"

        for scene in scenes:
            photos = scene.getElementsByTagName('Photo')
            sound = scene.getAttribute('sound')

            if not photos:
                self.slides.append(Slide(None, sound))
                continue

            first_photo = True
            for photo in photos:
                photo_path = photo.getAttribute('path')
                if first_photo:
                    self.slides.append(Slide(photo_path, sound))
                    first_photo = False
                else:
                    self.slides.append(Slide(photo_path, None))

    def __iter__(self):
        """
        Returns an interator over this instance's slides
        """
        return self.slides.__iter__()
