
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from functools import partial
from gbm.utils import GMapsExtractor
from .tasks import scrap_data1
from .tasks import add


def index(request):
    if request.method == 'POST':
        x = int(request.POST.get('x', 0))
        y = int(request.POST.get('y', 0))
        result = add.delay(x, y)
        return JsonResponse({'task_id': result.id})

    return render(request, 'home.html')

def home(request):
    return render(request,'home.html')

 

# Example usage in a view
def some_view(request):
    keyword_list = []
    
    if request.method == 'POST':
        get_keyword = request.POST.get('keyword', '')
        for line in get_keyword.split('\n'):
            line = line.strip()
            if line and line not in keyword_list:
                keyword_list.append(line)
        if not keyword_list:
            return HttpResponse('Please fill keyword list!', 'Please fill keyword list!')
        
        task = scrap_data1(keyword_list)
        # You can now use task.id to track the task status
        return JsonResponse({'task_id': "task created"}, status=202)
    return render(request, 'home.html')


def ui_on_error(msg):
        return "error"

def on_task_finished():
    print("Task finished")

def fetch_gbm_data(request):
    if request.method == 'POST':
        #if request.GET.get('status') == 'start':
        keyword_list = []
        get_keyword = request.POST.get('keyword', '')
        for line in get_keyword.split('\n'):
            line = line.strip()
            if line and line not in keyword_list:
                keyword_list.append(line)
        if not keyword_list:
            return HttpResponse('Please fill keyword list!', 'Please fill keyword list!')
        print("keyword_list================", keyword_list)
        working_thread = GMapsExtractor(keyword_list=keyword_list)
        #working_thread.error.connect(ui_on_error)
        #working_thread.task_finished.connect(on_task_finished)
        working_thread.start()
        print("task completed")
        return HttpResponse('task completed')
