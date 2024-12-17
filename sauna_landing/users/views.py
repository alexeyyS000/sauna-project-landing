from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from telegrambot.tasks import send_notifications
from .forms import CallbackRequestForm


@csrf_exempt
def callback_request_view(request):
    if request.method == "POST":
        form = CallbackRequestForm(request.POST)
        if form.is_valid():
            back_call = form.save()
            name = form.cleaned_data.get("name")
            send_notifications.delay(back_call.id, name)
            return JsonResponse({"status": "success", "message": "Ваш запрос принят"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    return JsonResponse({"status": "error", "message": "Неверный метод запроса"})
