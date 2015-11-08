from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
	alllist = List.objects.all()
	totalAllLists = alllist.count()
	totalList = Item.objects.count()
		
	komentar = 'oh tidak'
	if totalList == 0:
		komentar = 'yey, waktunya berlibur'
	elif totalList < 5:
		komentar = 'sibuk tapi santai'
		
	return render(request, 'home.html', {'totalAllLists': totalAllLists, 'thelists': alllist, 'komentarhtml': komentar, 'jumlah': totalList})
	

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None

	if request.method == 'POST':
		try:
			item = Item.objects.create(text=request.POST['item_text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			item.delete()
			error = "You can't have an empty list item"

	set_of_list = list_.item_set.all()
	total = set_of_list.count()
	alllist = List.objects.all()
	
	komentar = 'oh tidak'
	if total == 0:
		komentar = 'yey, waktunya berlibur'
	elif total < 5:
		komentar = 'sibuk tapi santai'
		
	return render(request, 'list.html', {'thelists': alllist, 'list': list_, 'komentarhtml': komentar, "error": error})
	
def new_list(request):
	list_ = List.objects.create()
	item = Item.objects.create(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"

		alllist = List.objects.all()
		totalAllLists = alllist.count()
		totalList = Item.objects.count()
			
		komentar = 'oh tidak'
		if totalList == 0:
			komentar = 'yey, waktunya berlibur'
		elif totalList < 5:
			komentar = 'sibuk tapi santai'

		return render(request, 'home.html', {'totalAllLists': totalAllLists, 'thelists': alllist, "error": error, 'komentarhtml': komentar, 'jumlah': totalList})
	return redirect(list_)
