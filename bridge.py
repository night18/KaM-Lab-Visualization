import gi
import json
from itertools import groupby 

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, GLib, Gio
from gi.repository import WebKit2
from file_utils import F

class  ReloadView:
    jsonList = [];
    authorList = [];
    timeList = [];
    typeList = [];


    def __init__(self):
        window = Gtk.Window()
        window.connect('delete-event',Gtk.main_quit)

        self.view = WebKit2.WebView()
        self.view.get_settings().set_enable_developer_extras(True)
        self.view.get_context().get_security_manager().register_uri_scheme_as_cors_enabled("python")
        self.view.get_context().register_uri_scheme("python", self.visualizer_request, None, None)
        self.view.load_uri(F.uri_from_path("visualize.html"))
        

        window.add(self.view)
        window.resize(550,600)
        window.show_all()
        
    def visualizer_request(self, request, *args):
        print request
        request.finish(Gio.MemoryInputStream(), 0, "text/html")
        eval("self." + request.get_path())
    
    def js_function(self,function, param):
        print("js_function")
        self.view.run_javascript(function +"(" + json.dumps(param) + ")", None, None)
        
    def getJansFromKeyword(self, keyword):
        json_author = [];
        json_time = [];
        json_type = [];
        print("getJansFromKeyword")
        json_context = F.json_from_file("/home/wei/KaM-Lab-Visualization/hardcode/" + keyword + ".json")
        self.jsonList = json.loads(json_context)
        self.js_function("getJansFromKeyword",json_context)

        #for i in range(0,len(self.jsonList)):
        for d in self.jsonList:
            print d["uuid"]
            for key,value in d.iteritems():
                if key == "author":
                    json_author.append(value)
                if key == "time":
                    json_time.append(value)
                if key == "type":
                    json_type.append(value)
        self.authorList = [dict(name = key, value= len(list(group))) for key,group in groupby(sorted(json_author))]
        self.timeList = [dict(name = key, value= len(list(group))) for key,group in groupby(sorted(json_time))]
        self.typeList = [dict(name = key, value= len(list(group))) for key,group in groupby(sorted(json_type))]

    def getIdsFromCategory(self,category):
        print("getIdsFromCategory")
        if category == "author":
            showList = self.authorList
        elif category == "time":
            showList = self.timeList
        elif category == "type":
            showList = self.typeList
        self.js_function("getIdsFromCategory", json.dumps(showList))
        


if __name__ == "__main__":
    ReloadView()
    Gtk.main()


