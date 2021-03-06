import os
import re

class F:
    @staticmethod
    def slurp(uri):
        filename = F.path_from_uri(uri)
        text = ""
        with open(filename) as file:
            text = file.read()
        return text

    @staticmethod
    def dump(filename, string):
        with open(filename, "w") as file:
            file.write(string)

    @staticmethod
    def uri_from_path(path):
        return "file://" + os.path.abspath(path)

    @staticmethod
    def path_from_uri(uri):
        return re.sub("file://", "", uri)
    
    @staticmethod
    def json_from_file(filename):
        with open(filename,'r') as content_file:
            content = content_file.read()
        return content



