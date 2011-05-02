from __future__ import absolute_import
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from slacker.postpone import proceed_pickled

@csrf_exempt
def slacker_execute(request):
    # FIXME: auth?

    if request.method != 'POST':
        raise Http404

    data = proceed_pickled(request.raw_post_data)
    return HttpResponse(data)
