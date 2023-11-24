from skywalking.trace.context import get_context
from skywalking import Layer, Component
from skywalking.trace.context import get_context
from skywalking.trace.tags import TagHttpMethod, TagHttpStatusCode, TagHttpParams
from skywalking.trace.carrier import Carrier

def Fg_trace(func):
    def wrapper(event, context):  
        carrier = Carrier()
        headers = event['headers']
        for item in carrier:
            if item.key.capitalize() == 'Sw8':
                item.val = headers['sw8']
            if item.key.capitalize() == 'Sw8-correlation':
                item.val = headers['sw8-correlation']
            if item.key.capitalize() in headers:
                item.val = headers[item.key.capitalize()]

        with get_context().new_entry_span(op=event['path'] or '/', carrier=carrier, inherit=Component.General) as span:
            span.layer = Layer.Http
            span.component = Component.General
            span.tag(TagHttpMethod('handler'))    
            span.tag(TagHttpParams(event['body']))
            resp = func(event, context)
            if resp['statusCode'] >= 400:
                span.error_occurred = True
            span.tag(TagHttpStatusCode(resp['statusCode']))
            return resp
    return wrapper