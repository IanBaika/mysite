from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from .models import Dish, Cart, CartContent
from .forms import SearchForm, LoginForm, RegisterForm, EditForm, ImageForm, DishEditForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required

def add_dish(request):
    some_dish = Dish(title='рамен2')
    some_dish.save()


def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditForm(instance=request.user)
    return render(request, 'registration/login.html', {'form': form,
                                          'submit_text': 'Изменить',
                                          'auth_header': 'Изменение профиля'})


def view_dishes(request):
    all_dishes = Dish.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = request.POST.get('search')
            all_dishes = all_dishes.filter(title=search)
    else:
        form = SearchForm()

    return render(request, 'base.html',
                  {'dishes': all_dishes, 'form': form, 'user': request.user})


def dish_edit(request):
    if request.method == 'GET':
        disheditform = DishEditForm.get(pk=this_object_id)
        if disheditform.is_valid():
            disheditform.save()
            return redirect('/')
    else:
        disheditform = DishEditForm(pk=this_object_id)
    return render(request, 'dishedit.html', {'form': disheditform,
                                             'submit_text': 'Изменить',
                                             'auth_header': 'Изменение блюда', })


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'registration/edit.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
        return render(request, 'registration/edit.html', {'form': form})


class MasterView(View):

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()
        return cart


class HomeView(MasterView):
    all_dishes = Dish.objects.all()

    def get(self, request):
        form = SearchForm()
        return render(request, 'base.html',
                      {'dishes': self.all_dishes, 'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid() and search:
            search_vector = SearchVector('title',
                                         'description',
                                         'categories__title',
                                         'company__title', )
            self.all_dishes = self.all_dishes.annotate(search=search_vector).filter(search=search)
        else:
            form = SearchForm()
        return render(request, 'base.html',
                      {'dishes': self.all_dishes, 'form': form, 'user': request.user})


@login_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/login.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # if request.GET and 'next' in request.GET:
                #     return redirect(request.GET['next'])
                return redirect('/')
            else:
                form.add_error('login', 'Bad login or password')
                form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form })


def logout_view(request):
    logout(request)
    return redirect('/')


class CartView(MasterView):
    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'cart.html', context)

    def post(self, request):
        dish = Dish.objects.get(id=request.POST.get('dish_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        # get_or_create - найдет обьект, если его нет в базе, то создаст
        # первый параметр - обьект, второй - булевое значение которое сообщает создан ли обьект
        # если обьект создан, то True, если он уже имеется в базе, то False
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=dish)
        cart_content.qty = quantity
        cart_content.save()
        response = self.get_cart_records(cart, redirect('/#dish-{}'.format(dish.id)))
        return response
