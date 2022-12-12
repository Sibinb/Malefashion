from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import UserInfo, ProductInfo, Adress, Orderdetails, Category, Coupon_details, Coupon, Brand
from mainadmin.models import Cart, Wishlist
from user import helpers
from passlib.hash import pbkdf2_sha256
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def login(request):
    if 'islogedin' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = UserInfo.objects.filter(email=email).get()
            except:
                user = None

            if user:
                if user.isblocked:
                    msg = "Your account is blocked"
                    return render(request, 'user_login.html', {"msg1": msg})
                if pbkdf2_sha256.verify(password, user.password):
                    request.session['islogedin'] = True
                    request.session['user_id'] = user.id
                    userid = request.session['user_id']
                    total = len(Cart.objects.filter(user_id=userid).all())
                    request.session['value'] = total
                    return redirect("home")
                else:
                    msg = "Email or Password is incorrect"
                    return render(request, 'user_login.html', {"msg1": msg})
            else:
                msg = "Email or Password is incorrect"
                return render(request, 'user_login.html', {"msg1": msg})

        return render(request, 'user_login.html')


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST["username"]
        email = request.POST['email']
        mobile = request.POST["mobile"]
        password = request.POST["password"]
        confirm = request.POST['confirm']
        isfound = UserInfo.objects.filter(email=email).all()
        if isfound:
            msg = "Email is already taken.Try another email"
            return render(request, 'user_registration.html', {"msg": msg})
        if password == confirm:
            eny_password = pbkdf2_sha256.encrypt(
                password, rounds=12000, salt_size=32)
            user = UserInfo()
            user.Name = name
            user.username = username
            user.email = email
            user.mobileno = mobile
            user.password = eny_password
            helpers.user1 = user
            request.session['phone'] = mobile
            helpers.otp = helpers.sendotp(mobile)
            return redirect('otp')
        else:
            msg = "Passwords are not matching.Try again"
            return render(request, 'user_registration.html', {"msg": msg})

    return render(request, 'user_registration.html')


def otp(request):
    phone = request.session['phone']
    if request.method == 'POST':
        get_otp = request.POST['otp']
        otp1 = str(helpers.otp)
        if get_otp == otp1:
            helpers.user1.save()
            msg = "Registration succsesfully completed..."
            helpers.user1 = {}
            helpers.otp = 0
            return render(request, 'user_login.html', {"msg": msg})
        else:
            msg = "otp is incorrect"
            return render(request, 'otp.html', {'msg': msg})
    return render(request, 'otp.html', {'phone': phone})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def home(request):
    product = ProductInfo.objects.all()
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        wsh_list = Wishlist.objects.filter(user_id=userid).all()
        items = []
        for i in wsh_list:
            items.append(i.wishlist_prd_id_id)
        user = UserInfo.objects.filter(id=userid).get()
        return render(request, 'index.html', {"products": product, "user": user, "item": items})
    else:
        return render(request, 'index.html', {"products": product, "guest_user": True})


@csrf_exempt
def user_profile(request):
    userid = request.session['user_id']
    user = UserInfo.objects.filter(id=userid).get()

    if request.method == "POST":
        if user.mobileno != int(request.POST['mobile']):
            if not helpers.send:
                request.session["otp"] = helpers.sendotp(
                    request.POST['mobile'])
                helpers.send = True
                return JsonResponse({"otp": "true"})
            else:
                if request.session['otp'] == int(request.POST['otp']):
                    helpers.send = False
                    return JsonResponse({"done": "do"})
                else:
                    return JsonResponse({"otp_error": "true"})
        try:
            img = request.FILES['img']
        except:
            img = user.profile_pic
        user.profile_pic = img
        user.Name = request.POST['name']
        user.email = request.POST['email']
        user.mobileno = request.POST['mobile']
        user.username = request.POST['username']
        user.save()
        return JsonResponse({"hello": "helo"})
    return render(request, 'user_profile.html', {"user": user})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def shop(request):
    prod = ProductInfo.objects.all()
    length = len(prod)
    p = Paginator(prod, 9)
    page = request.GET.get('page')
    product = p.get_page(page)
    brand_stats = Brand.objects.all()
    category_stats = Category.objects.all()
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        wsh_list = Wishlist.objects.filter(user_id=userid).all()
        items = []
        for i in wsh_list:
            items.append(i.wishlist_prd_id_id)
        user = UserInfo.objects.filter(id=userid).get()
        context = {"products": product, "user": user, "item": items,
                   "len": length, "cat_stats": category_stats, "brand_stats": brand_stats}
        return render(request, 'shop.html', context)
    else:
        return render(request, 'shop.html', {"products": product, "guest_user": True, "len": length, "cat_stats": category_stats, "brand_stats": brand_stats})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def sortshop(request, type, name):
    req = str(request.build_absolute_uri())
    category_stats = Category.objects.all()
    brand_stats = Brand.objects.all()
    if type == "c":
        cat = Category.objects.filter(category_name=name).get()
        prod = ProductInfo.objects.filter(category_id=cat.pk).all()
        length = len(prod)
        if length == 0:
            msg="No matching result found"
        else:
            msg=""
        p = Paginator(prod, 9)
        page = request.GET.get('page')
        product = p.get_page(page)
        if 'islogedin' in request.session:
            return render(request, 'shop.html', {"products": product, "len": length, "cat_stats": category_stats, "brand_stats": brand_stats,"msg":msg})
        else:
            return render(request, 'shop.html', {"products": product, "guest_user": True, "len": length, "cat_stats": category_stats, "brand_stats": brand_stats,"msg":msg})
    elif type == "b" :
        prod = ProductInfo.objects.filter(brand=name).all()
        length = len(prod)
        if length == 0:
            msg="No matching result found"
        else:
            msg=""
        p = Paginator(prod, 9)
        page = request.GET.get('page')
        product = p.get_page(page)
        if 'islogedin' in request.session:
            return render(request, 'shop.html', {"products": product, "req": req, "cat_stats": category_stats, "len": length, "brand_stats": brand_stats,"msg":msg})
        else:
            return render(request, 'shop.html', {"products": product, "guest_user": True, "req": req, "cat_stats": category_stats, "len": length, "brand_stats": brand_stats,"msg":msg})
    else:
        name_int=int(name)
        name_int2=name_int+500
        if name_int == 2500:
          prod = ProductInfo.objects.filter(product_price__gte=name_int)
        elif name_int == 1:
            prod=ProductInfo.objects.order_by("product_price").all()
        elif name_int == 1001:
            prod = ProductInfo.objects.filter(product_price__gte=1000)
        else:
            prod = ProductInfo.objects.filter(product_price__gte=name_int,product_price__lte=name_int2)
        length = len(prod)
        if length == 0:
            msg="No matching result found"
        else:
            msg=""
        p = Paginator(prod, 9)
        page = request.GET.get('page')
        product = p.get_page(page)
        if 'islogedin' in request.session:
            return render(request, 'shop.html', {"products": product, "req": req, "cat_stats": category_stats, "len": length, "brand_stats": brand_stats,"msg":msg})
        else:
            return render(request, 'shop.html', {"products": product, "guest_user": True, "req": req, "cat_stats": category_stats, "len": length, "brand_stats": brand_stats,"msg":msg})

@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def logout(request):
    if 'islogedin' in request.session:
        del request.session['islogedin']
        del request.session['user_id']
        return redirect('home')
    else:
        return redirect('home')


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def details(request, type):
    pro = ProductInfo.objects.filter(id=type).all()
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        user = UserInfo.objects.filter(id=userid).get()
        return render(request, 'product_details.html', {"product": pro, "user": user})
    return render(request, 'product_details.html', {"product": pro, "guest_user": True})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def cart(request):
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        products = Cart.objects.filter(user_id=userid).all()
        userid = request.session['user_id']
        user = UserInfo.objects.filter(id=userid).get()
        ord = Cart.objects.filter(user_id=userid).all(
        ).aggregate(Sum('cart_total_price'))
        sum = ord["cart_total_price__sum"]
        if sum == None:
            sum = 0
        return render(request, 'cart.html', {"products": products, "total_price": sum, "user": user})
    return redirect('login')


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def add_cart(request):
    prd_id = request.GET['id']
    userid = request.session['user_id']
    state = int(request.GET['st'])
    prd = ProductInfo.objects.get(id=prd_id)
    try:
        product = Cart.objects.filter(
            user_id=userid, cart_prd_id_id=prd_id).get()
    except:
        product = None

    if product:
        if state == 1:
            wsh = Wishlist.objects.filter(
                user_id=userid, wishlist_prd_id_id=prd_id).get()
            wsh.delete()
            prd.save()
            total = len(Cart.objects.filter(user_id=userid).all())
            request.session['value'] = total
        return HttpResponse("cart")
    else:
        if state == 1:
            wsh = Wishlist.objects.filter(
                user_id=userid, wishlist_prd_id_id=prd_id).get()
            wsh.delete()
            prd.wishlist = 0
            prd.save()
            total = len(Cart.objects.filter(user_id=userid).all())
            request.session['value'] = total
        cart_prd = Cart()
        cart_prd.cart_prd_quantity = 1
        cart_prd.cart_prd_id_id = prd_id
        cart_prd.cart_total_price = prd.product_price
        cart_prd.user_id = request.session['user_id']
        cart_prd.save()
    total = len(Cart.objects.filter(user_id=userid).all())
    request.session['value'] = total
    return HttpResponse("cart")


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def remove_frm_cart(request):
    _id = request.GET['id']
    userid = request.session['user_id']
    product = Cart.objects.filter(user_id=userid, cart_prd_id=_id).get()
    product.delete()
    total = len(Cart.objects.filter(user_id=userid).all())
    request.session['value'] = total
    return HttpResponse("cart")


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def quant_add(request):
    _id = request.GET['id']
    userid = request.session['user_id']
    quant = request.GET['quant']
    product = Cart.objects.filter(user_id=userid, cart_prd_id_id=_id).get()
    if quant == 0:
        product.delete()
    else:
        product.cart_prd_quantity = quant
        product.cart_total_price = int(
            product.cart_prd_quantity)*int(product.cart_prd_id.product_price)
        product.save()
        prodo_qun = product.cart_prd_quantity
        prodo_price = product.cart_total_price
        ord = Cart.objects.filter(user_id=userid).all(
        ).aggregate(Sum('cart_total_price'))
        sum = ord["cart_total_price__sum"]
    total = len(Cart.objects.filter(user_id=userid).all())
    request.session['value'] = total
    return JsonResponse({"prodo_qun": prodo_qun, "prodo_price": prodo_price, "total_price": sum})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def wishlist(request):
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        user = UserInfo.objects.filter(id=userid).get()
        userid = request.session['user_id']
        products = Wishlist.objects.filter(user_id=userid)
        return render(request, 'wishlist.html', {"products": products, "user": user})
    return redirect('login')


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def add_to_wishlist(request):
    prd_id = request.GET['id']
    userid = request.session['user_id']
    prd = ProductInfo.objects.get(id=prd_id)
    try:
        product = Wishlist.objects.filter(
            user_id=userid, wishlist_prd_id=prd_id).get()
    except:
        product = None

    if product:
        prd.wlist = 0
        prd.save()
        product.delete()
        return HttpResponse(0)
    else:
        wsh_prd = Wishlist()
        prd.wlist = 1
        wsh_prd.user_id = request.session['user_id']
        wsh_prd.wishlist_prd_id_id = prd_id
        prd.save()
        wsh_prd.save()
    return HttpResponse(1)


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def checkout(request, id):
    if 'islogedin' in request.session:
        userid = request.session['user_id']
        user = UserInfo.objects.filter(id=userid).get()
        adress = Adress.objects.filter(userid=userid).all()
        lists = Cart.objects.filter(user_id=userid).all()
        try:
            prd = Cart.objects.all()
        except:
            prd = None
        obj = {}
        for i in prd:
            if int(i.cart_prd_id.offer_id_id) > 1:
                id = i.cart_prd_id.offer_id_id
                obj[id] = f"{i.cart_prd_id.offer_id.coupon_name}-{i.cart_prd_id.offer_id.offer}%Off "

        ord1 = Cart.objects.filter(user_id=userid).all(
        ).aggregate(Sum('cart_total_price'))
        sum1 = ord1["cart_total_price__sum"]
        if sum1 is None:
            sum1 = 0
        ido = int(id)
        if ido == 1:
            adress = None
        return render(request, 'checkout.html', {"lists": lists, "total": sum1, "adress": adress, "user": user, "obj": obj})
    return redirect('login')


def Placeorder(request, id):
    userid = request.session['user_id']
    _id = int(id)
    if _id == 2:
        od = Orderdetails.objects.filter(
            user_id=userid, ord_id=helpers.dat).all()
        for item in od:
            item.payment_status = "success"
            item.save()
        request.session['value'] = 0
        cart = Cart.objects.filter(user_id=userid).all()
        cart_updt_stock = ProductInfo.objects.all()
        for val in cart:
            num = int(val.cart_prd_quantity)
            for val2 in cart_updt_stock:
                if val.cart_prd_id_id == val2.pk:
                    val2.stock = int(val2.stock)-num
                    val2.save()
        helpers.cart.delete()
        return HttpResponse("confirm")
    payment_method = request.POST['payment-method']
    val = request.POST['address']
    if payment_method == "COD":
        if _id == 1:
            if request.method == "POST":
                addr = Adress.objects.filter(userid=userid, pk=val).get()
                cart = Cart.objects.filter(user_id=userid).all()
                x = datetime.datetime.now()
                try:
                    value = helpers.generateRazorpay(10000, 1)
                    generated_id = value['id']
                except:
                    generated_id = 000000000+int(len(cart))*838
                date = f"{x.year}-{x.month}-{x.day}"
                for item in cart:
                    oder = Orderdetails()
                    oder.address_id = addr.pk
                    oder.order_prd_name = item.cart_prd_id.product_name
                    oder.order_prd_quantity = item.cart_prd_quantity
                    oder.order_prd_price = item.cart_total_price
                    oder.date = date
                    oder.payment_method = payment_method
                    oder.status = "Placed"
                    oder.payment_status = "Pending"
                    oder.ord_id = generated_id
                    oder.user_id = userid
                    oder.order_prd_image = item.cart_prd_id.product_image1
                    oder.save()
                request.session['value'] = 0
                cart_updt_stock = ProductInfo.objects.all()
                for val in cart:
                    num = int(val.cart_prd_quantity)
                    for val2 in cart_updt_stock:
                        if val.cart_prd_id_id == val2.pk:
                            val2.stock = int(val2.stock)-num
                            val2.save()
                cart.delete()
                return JsonResponse({"cod": True})

        else:
            if request.method == "POST":
                name = request.POST['name']
                lastname = request.POST['lastname']
                country = request.POST['country']
                _address = request.POST['address']
                state = request.POST['state']
                postcode = request.POST['postcode']
                phone = request.POST['phone']
                email = request.POST['email']
                city = request.POST['city']
                address = Adress()
                address.Name = name
                address.Lastname = lastname
                address.Country = country
                address.State = state
                address.Postcode = postcode
                address.mobileno = phone
                address.email = email
                address.City = city
                address.userid = userid
                address.Address = _address
                address.save()
                adr_id = address.pk
                addr = Adress.objects.filter(userid=userid, pk=adr_id).get()
                cart = Cart.objects.filter(user_id=userid).all()
                x = datetime.datetime.now()
                try:
                    value = helpers.generateRazorpay(10000, 1)
                    generated_id = value['id']
                except:
                    generated_id = 000000000+int({x.day})*834
                date = f"{x.year}-{x.month}-{x.day}"
                for item in cart:
                    oder = Orderdetails()
                    oder.address_id = addr.pk
                    oder.order_prd_name = item.cart_prd_id.product_name
                    oder.order_prd_quantity = item.cart_prd_quantity
                    oder.order_prd_price = item.cart_total_price
                    oder.date = date
                    oder.payment_method = payment_method
                    oder.status = "Placed"
                    oder.payment_status = "Pending"
                    oder.ord_id = generated_id
                    oder.user_id = userid
                    oder.order_prd_image = item.cart_prd_id.product_image1
                    oder.save()
                request.session['value'] = 0
                cart_updt_stock = ProductInfo.objects.all()
                for val in cart:
                    num = int(val.cart_prd_quantity)
                    for val2 in cart_updt_stock:
                        if val.cart_prd_id_id == val2.pk:
                            val2.stock = int(val2.stock)-num
                            val2.save()
                cart.delete()
                return JsonResponse({"cod": True})
    elif payment_method == "online payment":
        if _id == 1:
            if request.method == "POST":
                addr = Adress.objects.filter(userid=userid, pk=val).get()
                cart = Cart.objects.filter(user_id=userid).all()
                x = datetime.datetime.now()
                date = f"{x.year}-{x.month}-{x.day}"
                ord1 = Cart.objects.filter(user_id=userid).all(
                ).aggregate(Sum('cart_total_price'))
                sum1 = int(ord1["cart_total_price__sum"])*100
                try:
                    value = helpers.generateRazorpay(sum1, 1)
                    helpers.dat = value['id']
                except:
                    print("error is here")
                for item in cart:
                    oder = Orderdetails()
                    oder.address_id = addr.pk
                    oder.order_prd_name = item.cart_prd_id.product_name
                    oder.order_prd_quantity = item.cart_prd_quantity
                    oder.order_prd_price = item.cart_total_price
                    oder.date = date
                    oder.payment_method = payment_method
                    oder.ord_id = helpers.dat
                    oder.payment_status = "pending"
                    oder.status = "Placed"
                    oder.user_id = userid
                    oder.order_prd_image = item.cart_prd_id.product_image1
                    oder.save()
                ord1 = Cart.objects.filter(user_id=userid).all(
                ).aggregate(Sum('cart_total_price'))
                sum1 = int(ord1["cart_total_price__sum"])*100
                helpers.cart = cart
                details = {"name": addr.Name,
                           "adress": addr.Address, "num": addr.mobileno}
                return JsonResponse({"res": value, "addr": details, "cod": False})
        else:
            if request.method == "POST":
                name = request.POST['name']
                lastname = request.POST['lastname']
                country = request.POST['country']
                _address = request.POST['address']
                state = request.POST['state']
                postcode = request.POST['postcode']
                phone = request.POST['phone']
                email = request.POST['email']
                city = request.POST['city']
                payment_method = request.POST['payment-method']
                address = Adress()
                address.Name = name
                address.Lastname = lastname
                address.Country = country
                address.State = state
                address.Postcode = postcode
                address.mobileno = phone
                address.email = email
                address.City = city
                address.userid = userid
                address.Address = _address
                address.save()
                adr_id = address.pk
                addr = Adress.objects.filter(userid=userid, pk=adr_id).get()
                cart = Cart.objects.filter(user_id=userid).all()
                x = datetime.datetime.now()
                date = f"{x.year}-{x.month}-{x.day}"
                ord1 = Cart.objects.filter(user_id=userid).all(
                ).aggregate(Sum('cart_total_price'))
                sum1 = int(ord1["cart_total_price__sum"])*100
                value = helpers.generateRazorpay(sum1, 1)
                helpers.dat = value['id']
                for item in cart:
                    oder = Orderdetails()
                    oder.address_id = addr.pk
                    oder.order_prd_name = item.cart_prd_id.product_name
                    oder.order_prd_quantity = item.cart_prd_quantity
                    oder.order_prd_price = item.cart_total_price
                    oder.date = date
                    oder.payment_method = payment_method
                    oder.ord_id = helpers.dat
                    oder.payment_status = "pending"
                    oder.status = "Placed"
                    oder.user_id = userid
                    oder.order_prd_image = item.cart_prd_id.product_image1
                    oder.save()
                helpers.cart = cart
                details = {"name": addr.Name,
                           "adress": addr.Address, "num": addr.mobileno}
                return JsonResponse({"res": value, "addr": details, "cod": False})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def oders(request):
    userid = request.session['user_id']
    user = UserInfo.objects.filter(id=userid).get()
    oder = Orderdetails.objects.filter(
        user_id=userid).order_by('date').reverse().all()
    return render(request, 'oders.html', {"products": oder, "user": user})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def view_oders(request, id):
    userid = request.session['user_id']
    user = UserInfo.objects.filter(id=userid).get()
    oder = Orderdetails.objects.filter(pk=id).get()
    price = int(oder.order_prd_price)/int(oder.order_prd_quantity)
    return render(request, 'order_products_details.html', {'od': oder, "user": user, "price": price})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def cancelorder(request):
    id = request.GET['id']
    order = Orderdetails.objects.filter(pk=id).get()
    order.status = "cancelled"
    order.save()
    return HttpResponse("oders")


@csrf_exempt
def test(request):
    pro = ProductInfo.objects.filter(product_name__contains="a").all()
    pro1 = ProductInfo.objects.filter(product_name__contains="a").all()
    lis = []
    for p in pro:
        lis.append(p)
    for p in pro1:
        lis.append(p)
    se = set(lis)
    return HttpResponse("done")


def confirm(request):
    return render(request, 'confirm.html')


def apply_coupon(request):
    id = int(request.GET['id'])
    userid = request.session['user_id']
    ord1 = Cart.objects.filter(user_id=userid).all(
    ).aggregate(Sum('cart_total_price'))
    sum1 = int(ord1["cart_total_price__sum"])

    if id == 1:
        coup1 = request.GET['coup']
        try:
            coup2 = Coupon.objects.filter(coupon_name=coup1).get()
        except:
            return JsonResponse({"error": "Coupon not found"})
        coup = coup2.pk
    else:
        coup = request.GET['coup']
    try:
        used = Coupon_details.objects.filter(
            user_id=userid, coupon_id=coup).get()
    except:
        used = None
    if used:
        return JsonResponse({"error": "Coupon is already redeemed"})
    cup = Coupon.objects.filter(pk=coup).get()
    sum2 = sum1*int(cup.offer)/100
    coup_det = Coupon_details()
    x = datetime.datetime.now()
    date = f"{x.year}-{x.month}-{x.day}"
    coup_det.coupon_id = coup
    coup_det.user_id = userid
    coup_det.date = date
    coup_det.save()
    cart = Cart.objects.filter(user_id=userid).all()
    lenv = len(cart)
    got_price = sum2/lenv
    for i in cart:
        i.cart_total_price = i.cart_total_price-got_price
        i.save()
    ord3 = Cart.objects.filter(user_id=userid).all(
    ).aggregate(Sum('cart_total_price'))
    sum3 = int(ord3["cart_total_price__sum"])
    return JsonResponse({"tot": sum3, "sum": sum2})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def returnorder(request):
    if 'islogedin' in request.session:
        id = request.GET['id']
        order = Orderdetails.objects.filter(pk=id).get()
        order.status = "Returned"
        order.save()
        return HttpResponse("oders")
    return redirect('login')


def searched(request):
    if request.method == "POST":
        category_stats = Category.objects.all()
        content = request.POST["search"].capitalize()
        if 'islogedin' in request.session:
            userid = request.session['user_id']
            user = UserInfo.objects.filter(id=userid).get()
        pro1 = ProductInfo.objects.filter(product_name__contains=content).all()
        pro2 = ProductInfo.objects.filter(
            product_price__contains=content).all()
        pro3 = ProductInfo.objects.filter(subcategory__contains=content).all()
        pro4 = ProductInfo.objects.filter(brand__contains=content).all()
        lis = []
        for p in pro1:
            lis.append(p)
        for p in pro2:
            lis.append(p)
        for p in pro3:
            lis.append(p)
        for p in pro4:
            lis.append(p)
        pro = set(lis)
        prod = list(pro)
        length = len(prod)
        p = Paginator(prod, 9)
        page = request.GET.get('page')
        product = p.get_page(page)
        if len(pro) == 0:
            msg = "No matching results found"
            if 'islogedin' in request.session:
                return render(request, 'shop.html', {"products": product, "user": user, "msg": msg, "cat_stats": category_stats})
            else:
                return render(request, 'shop.html', {"products": product, "msg": msg, "cat_stats": category_stats})
        if 'islogedin' in request.session:
            wsh_list = Wishlist.objects.filter(user_id=userid).all()
            items = []
            for i in wsh_list:
                items.append(i.wishlist_prd_id_id)
        if 'islogedin' in request.session:
            return render(request, 'shop.html', {"products": product, "user": user, "item": items, "len": length, "cat_stats": category_stats})
        else:
            return render(request, 'shop.html', {"products": product, "guest_user": True, "len": length, "cat_stats": category_stats})


@cache_control(no_cache=True, must_revaliddate=True, no_store=True)
def remove_frm_wishlist(request):
    _id = request.GET['id']
    userid = request.session['user_id']
    product = Wishlist.objects.filter(
        user_id=userid, wishlist_prd_id_id=_id).get()
    product.delete()
    return HttpResponse("wishlist")
