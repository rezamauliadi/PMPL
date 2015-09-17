from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the-only-list-in-the-world/')	
	return render(request, 'home.html')

def view_list(request):
	items = Item.objects.all()
	
	komentar = 'oh tidak'
	if items.count() == 0:
		komentar = 'yey, waktunya berlibur'
	elif items.count() < 5:
		komentar = 'sibuk tapi santai'
	
	return render(request, 'list.html', {'items': items, 'komentarhtml': komentar})
