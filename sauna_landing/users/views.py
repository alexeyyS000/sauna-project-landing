from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CallbackRequestForm

@csrf_exempt
def callback_request_view(request):
    if request.method == "POST":
        form = CallbackRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Ваш запрос принят"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    return JsonResponse({"status": "error", "message": "Неверный метод запроса"})
