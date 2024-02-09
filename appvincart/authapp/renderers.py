from rest_framework import renderers
import json


#it is helpful in front end in order to understand and differentiate from errors, as in registeration for empty blanks , though there was a error but it was not showing so.
class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data, accepted_media_type=None, renderer_context =None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)
            
        return response
    
class SuccessRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context =None):
        response_data = {"success" : data}  #        response_data = {"success" : data.get("message", "")}
        # if "redirect_url" in data:
        #     response_data["redirect_url"] = data["redirect_url"]
        return response_data