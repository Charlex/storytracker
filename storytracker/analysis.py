import os
import gzip
import copy
import storytracker
from bs4 import BeautifulSoup


def open_archive_filepath(path):
    """
    Accepts a file path and returns an ArchivedURL object ready for analysis
    """
    # Split the file extension from the name
    name = os.path.basename(path)
    name, ext = os.path.splitext(name)
    # Extract the URL and timestamp from the file name
    url, timestamp = storytracker.reverse_archive_filename(name)
    # If it is gzipped, then open it that way
    if ext == '.gz':
        obj = gzip.open(path)
    # Otherwise handle it normally
    else:
        obj = open(path, "rb")
    return ArchivedURL(url, timestamp, obj.read())


def open_archive_directory(path):
    """
    Accepts a directory path and returns an ArchivedURLSet ready for analysis
    """
    # Make sure it's a directory
    if not os.path.isdir(path):
        raise ValueError("Path must be a directory")

    # Loop through the directory and pull the data
    urlset = ArchivedURLSet([])
    for root, dirs, files in os.walk(path):
        for name in files:
            path = os.path.join(root, name)
            obj = open_archive_filepath(path)
            urlset.append(obj)

    # Pass it back out
    return urlset


class ArchivedURL(object):
    """
    An URL's archived HTML response with tools for analysis
    """
    def __init__(self, url, timestamp, html):
        self.url = url
        self.timestamp = timestamp
        self.html = html
        self.soup = BeautifulSoup(html)

    @property
    def hyperlinks(self):
        """
        Parse all of the hyperlinks from the HTML
        """
        link_list = []
        for a in self.soup.findAll("a", {"href": True}):
            obj = Hyperlink(a["href"])
            link_list.append(obj)
        return link_list


class ArchivedURLSet(list):
    """
    A list of archived URLs sorted by their timestamp
    """
    def __init__(self, obj_list):
        # Create a list to put objects after we've checked them out
        safe_list = []
        for obj in obj_list:

            # Verify that the user is trying to add an ArchivedURL object
            if not isinstance(obj, ArchivedURL):
                raise TypeError("Only ArchivedURL objects can be added")

            # Check if the object is already in the list
            if obj in safe_list:
                raise ValueError("This object is already in the list")

            # Add to safe list
            safe_list.append(obj)

        # Do the normal list start up
        super(ArchivedURLSet, self).__init__(obj_list)

    def append(self, obj):
        # Verify that the user is trying to add an ArchivedURL object
        if not isinstance(obj, ArchivedURL):
            raise TypeError("Only ArchivedURL objects can be added")

        # Check if the object is already in the list
        if obj in [o for o in list(self.__iter__())]:
            raise ValueError("This object is already in the list")

        # If it's all true, append it.
        super(ArchivedURLSet, self).append(copy.copy(obj))


class Hyperlink(object):
    """
    A hyperlink extracted from an archived URL with tools for analysis
    """
    def __init__(self, href):
        self.href = href
