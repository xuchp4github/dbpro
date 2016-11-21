from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from .query import *
import os
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload(request):
    thumb = []
    if(request.method == 'POST'):       
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            pho = Photo(image=form.cleaned_data['image'])
            pho.save()
            raw,thumb = query(pho.image)
            rawstr = ','.join(raw)
            thumbstr = ','.join(thumb)
            context = {'raw':raw, 'thumb':thumb}
            with open(os.getcwd()+'/imgsearch/static/imgUrl', 'w') as fp:
                for item in thumb:
                    fp.write(str(item)+"\n")
        else:
            return HttpResponse('allow only allow POST')
    else:
        with open(os.getcwd()+'/imgsearch/static/imgUrl', 'r') as fp:
            for line in fp.readlines():
                thumb.append(line.strip())
   
    after_range_num = 9
    before_range_num = 9
    try:
        page=int(request.GET.get('page','1'))
        if page < 1:
            page=1
    except ValueError:
        page=1
    paginator = Paginator(thumb,12)
    try:
        winloglist = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        winloglist = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]
    total_page = paginator.num_pages
    return render(request, 'gallery.html', locals())
    
#    

def test(request):
    return render(request, 'test.html')
