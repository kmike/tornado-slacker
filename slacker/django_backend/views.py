from __future__ import absolute_import

#from time import sleep
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from slacker.postpone import proceed_pickled, SlackerException

@csrf_exempt
def slacker_execute(request):
    # FIXME: auth?
    if request.method != 'POST':
        raise Http404

    # TODO: move boilerplate to process_pickled
    # TODO: exceptions should be pickled, returned and re-raised on client
    try:
        data = proceed_pickled(request.raw_post_data)
        return HttpResponse(data)
    except SlackerException, e:
        return HttpResponseBadRequest(str(e))
#    except Exception, e:
#        print e
#        raise
