from random import choice
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
import json
import datetime
from .forms import SignUpForm, QuestionForm, AnswerForm, ChallengeAnswerForm
from .utils import cartData, guestOrder
import asyncio
from .sendmessage import send_single_message

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def signup_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form':form})

	return render(request, 'signup.html', {'form':form})


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    category_id = request.GET.get('category')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'store.html', {'products' : products, 'cartItems': cartItems, 'categories': categories})



def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']          
        
    return render(request, 'cart.html', {'items': items, 'order': order, 'cartItems': cartItems})


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, 'checkout.html', {'items': items, 'order': order, 'cartItems': cartItems})
        


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    Address.objects.create(
            customer = customer,
            order = order,
            street = data['shipping']['street'],
            city = data['shipping']['city'],
            postal_code = data['shipping']['postal_code'],
        )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # Serialize the order items into a list of dictionaries
    order_items = [
        {
            "product_name": item.product.name,
            "quantity": item.quantity,
        }
        for item in OrderItem.objects.filter(order=order)
    ]

    address = Address.objects.get(order=order)

    # Construct the message content as a dictionary
    message_content = {
        "order_id": order.id,
        "customer_name": order.customer.name,
        "customer_email": order.customer.email,
        "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
        "address": {
            "street": address.street,
            "city": address.city,
            "postal_code": address.postal_code,
        },
        "order_items": order_items,
    }

    # Serialize the message content to JSON
    order_json = json.dumps(message_content)

    asyncio.run(send_single_message(order_json))


    return JsonResponse('Payment complete', safe=False)

@login_required
def forum(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user to the question
            question.save()
            return redirect('forum')  # Redirect to the forum page after successfully creating the question
    else:
        form = QuestionForm()
    
    return render(request, 'forum.html', {'questions': questions, 'form': form})

@login_required
def question(request, id):
    question = Question.objects.get(pk=id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user  # Assign the current user to the answer
            answer.question = question
            answer.save()
            return redirect('question', id=id)  # Redirect back to the same question page after submitting the answer
    else:
        form = AnswerForm()

    return render(request, 'question.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def challenge(request):
    current_date = datetime.date.today()
    print("Current Date:", current_date)

    # Get challenges with the current date
    challenges = Challenge.objects.filter(date=current_date)
    print("Challenges for Today:", challenges)

    if challenges:
        # Choose a random challenge from the list
        selected_challenge = choice(challenges)
        print("Selected Challenge:", selected_challenge)
        # Store the selected challenge's ID in the session
        request.session['selected_challenge_id'] = selected_challenge.id
    else:
        selected_challenge = None

    if request.method == 'POST':
        form = ChallengeAnswerForm(request.POST)
    else:
        form = ChallengeAnswerForm()

    return render(request, 'challenge.html', {'challenge': selected_challenge, 'form': form})
