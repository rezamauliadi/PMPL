from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
	alllist = List.objects.all()
	totalList = Item.objects.count()
		
	komentar = 'oh tidak'
	if totalList == 0:
		komentar = 'yey, waktunya berlibur'
	elif totalList < 5:
		komentar = 'sibuk tapi santai'
		
	return render(request, 'home.html', {'thelists': alllist, 'komentarhtml': komentar, 'jumlah': totalList})
	

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	
	set_of_list = list_.item_set.all()
	total = set_of_list.count()
	
	komentar = 'oh tidak'
	if total == 0:
		komentar = 'yey, waktunya berlibur'
	elif total < 5:
		komentar = 'sibuk tapi santai'
		
	return render(request, 'list.html', {'list': list_, 'komentarhtml': komentar})
	
def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))
