#from time import sleep
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from async_orm.chains import repickle_chain, AsyncOrmException

@csrf_exempt
def orm_execute(request):
    # FIXME: auth?
    if request.method != 'POST':
        raise Http404

    try:
        data = repickle_chain(request.raw_post_data)
        return HttpResponse(data)
    except AsyncOrmException, e:
        return HttpResponseBadRequest(str(e))
