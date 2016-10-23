import gi
import json

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, GLib, Gio
from gi.repository import WebKit2
from file_utils import F

class  ReloadView:
    def __init__(self):
        window = Gtk.Window()
        window.connect('delete-event',Gtk.main_quit)

        self.view = WebKit2.WebView()
        self.view.get_settings().set_enable_developer_extras(True)
        self.view.get_context().get_security_manager().register_uri_scheme_as_cors_enabled("python")
        self.view.get_context().register_uri_scheme("python", self.visualizer_request, None, None)
        self.view.load_uri(F.uri_from_path("visualize.html"))
        

        window.add(self.view)
        window.resize(500,850)
        window.show_all()
        
    def visualizer_request(self, request, *args):
        print request
        request.finish(Gio.MemoryInputStream(), 0, "text/html")
        eval("self." + request.get_path())
    
    def js_function(self,function, param):
        print("js_function")
        self.view.run_javascript(function +"(" + json.dumps(param) + ")", None, None)
        
    def getJansFromKeyword(self, keyword):
        print("getJansFromKeyword")
        self.js_function("getJansFromKeyword",F.json_from_file("/home/chunwei/KaM-Lab-Visualization/hardcode/" + keyword + ".json"))
        
    def getCategory(self,keyword):
        print("getCategory")
        self.js_function("getCategory", (F.json_from_file("/home/chunwei/KaM-Lab-Visualization/hardcode/category")).split(","))

    def getIdsFromCategory(self,category):
        print("getIdsFromCategory")
        self.js_function("getIdsFromCategory", F.json_from_file("/home/chunwei/KaM-Lab-Visualization/hardcode/" + category+".json"))
        


if __name__ == "__main__":
    ReloadView()
    Gtk.main()


