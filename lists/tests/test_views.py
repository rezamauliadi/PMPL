from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		
		self.assertEqual(response.content.decode(), expected_html)
		
		
class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')
	
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')
		
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

#-------------------- unit tests for tutorial ----------------------------#

	def test_tutorial2_for_comment_yeywaktunyaberlibur(self):
		list_ = List()
		list_.save()
		
		request = HttpRequest()
		response = view_list(request, list_.id)
		response2 = home_page(request)
		
		self.assertIn('yey, waktunya berlibur', response.content.decode())
		self.assertIn('0', response2.content.decode())
		
	def test_tutorial2_for_comment_sibuktapisantai(self):
		list_ = List()
		list_.save()
		
		Item.objects.create(text='itemey 1', list=list_)
		
		request = HttpRequest()
		response = view_list(request, list_.id)
		response2 = home_page(request)
		
		self.assertIn('sibuk tapi santai', response.content.decode())
		self.assertIn('sibuk tapi santai', response2.content.decode())
		self.assertIn('1', response2.content.decode())
		
	def test_tutorial2_for_comment_ohtidak(self):
		list_ = List()
		list_.save()
		
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)
		Item.objects.create(text='itemey 3', list=list_)
		Item.objects.create(text='itemey 4', list=list_)
		Item.objects.create(text='itemey 5', list=list_)
		
		request = HttpRequest()
		response = view_list(request, list_.id)
		response2 = home_page(request)
		
		self.assertIn('oh tidak', response.content.decode())
		self.assertIn('5', response2.content.decode())

#-------------------- end of unit tests for tutorial ----------------------------#

class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,), 
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
		
	def test_redirects_after_POST(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,), 
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new', 
			data={'item_text': 'A new list item'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new', 
			data={'item_text': 'A new list item'}
		)
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
		
	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)
		
	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
