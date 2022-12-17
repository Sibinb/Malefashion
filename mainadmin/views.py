from django.shortcuts import render,redirect
from django.http.response import HttpResponse,JsonResponse
from user.models import AdminInfo,UserInfo,ProductInfo,Brand,Orderdetails,Coupon,Category
from .models import Cart
import uuid
import os
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from user.helpers import Sales

def admin(request):
    return redirect('admin_home')


def admin_users(request):
    if 'admin' in request.session :
        user=UserInfo.objects.all()
        return render(request,"admin_users.html",{"users":user})
    else:
        return redirect('admin_login')
    

def login(request):
     if request.method == "POST":
        Email=request.POST["email"]
        pasword=request.POST["password"]
        admin=AdminInfo.objects.filter(email=Email).all()
        if admin :
            for i in admin:
                pass1=i.password
            if pass1==pasword :
               request.session['admin']=True
               return redirect('admin_home')
            else:
                msg="Invalid password or username"
            return render(request,'admin_login.html',{'msg':msg})
        else:
            msg="Invalid password or username"
            return render(request,'admin_login.html',{'msg':msg})
    
     return render(request,"admin_login.html")
 
 
def block(request,p):
     user=UserInfo.objects.filter(id=p).all()
     for i in user:
         i.isblocked=1
         i.save()
     return JsonResponse({"page":"users"})
     
def unblock(request,po):
     user=UserInfo.objects.filter(id=po).all()
     for i in user:
         i.isblocked=0
         i.save()
     return JsonResponse({"page":"users"})
     

def admin_dashbord(request):
    if 'admin' in request.session :
        ord1 = Orderdetails.objects.all().aggregate(Sum('order_prd_price'))
        ords = Orderdetails.objects.all()
        usr  = UserInfo.objects.all()
        try:
            sum1 = int(ord1["order_prd_price__sum"])
        except:
            sum1=0
        items=[]
        for item in ords:
            if item.date.strftime("%Y-%m-%d") in items:
                continue
            else:
                dat=item.date.strftime("%Y-%m-%d")
                items.append(dat)
        datas={}
        for x in items:
            num=len(Orderdetails.objects.filter(date=x).all())
            datas[x]=num
        tot_ord=len(ords)
        tot_usr=len(usr)
        return render(request,'home.html',{"sum":sum1,"tot_ord":tot_ord,"tot_usr":tot_usr,"date":items,"data":datas})
    else:
        return redirect('admin_login')
    
def logout(request):
    if request.session:
        request.session.flush()
        return redirect('admin_login')
    else:
        return redirect('admin_home')
    
def admin_products(request):
    if 'admin' in request.session :
        prod=ProductInfo.objects.all()
        return render(request,'admin_products.html',{"products":prod})
    else:
        return redirect('admin_login')
    
    
@csrf_exempt
def admin_addproducts(request):
    if request.method=="POST":
        Product_Name=request.POST['Product_Name']
        Description=request.POST['Description']
        Product_Price=request.POST['Product_Price']
        category=request.POST['category']
        subcat=request.POST['subcat']
        brand=request.POST['brand']
        stock=request.POST['stock']
        id=uuid.uuid1()
        request.FILES['img1'].name=f"{id}.jpg"
        img1=request.FILES['img1']
        id=uuid.uuid1()
        request.FILES['img2'].name=f"{id}.jpg"
        img2=request.FILES['img2']
        id=uuid.uuid1()
        request.FILES['img3'].name=f"{id}.jpg"
        img3=request.FILES['img3']
        id=uuid.uuid1()
        request.FILES['img4'].name=f"{id}.jpg"
        img4=request.FILES['img4']
        cat=Category.objects.filter(pk=category).get()
        cat.tot_num=int(cat.tot_num)+1
        cat.save()
        product=ProductInfo(stock=stock,brand=brand,product_name=Product_Name,product_image1=img1,product_image2=img2,product_image3=img3,product_image4=img4, category_id_id=category,product_price=Product_Price,product_description=Description,subcategory=subcat)
        product.save()
        prod=ProductInfo.objects.all()
        return render(request,'admin_products.html',{"products":prod})
    brand=Brand.objects.all()
    cat_items=Category.objects.all()
    return render(request,'admin_addproduct.html',{'show':0,'brands':brand,"categry":cat_items})


def admin_editproducts(request,id):
    prod=ProductInfo.objects.filter(id=id).all()
    if request.method=="POST":
        prod1=ProductInfo.objects.filter(id=id).get()
        Product_Name=request.POST['Product_Name']
        Description=request.POST['Description']
        Product_Price=request.POST['Product_Price']
        category=request.POST['category']
        subcat=request.POST['subcat']
        
        try:
            img=request.FILES['img']
        except:
            img=""
              
        if img !="":
            id=uuid.uuid1()
            request.FILES['img'].name=f"{id}.jpg"
            img=request.FILES['img']
        else:
            img=prod1.product_image1
            
        prod1.product_name=Product_Name
        prod1.product_image1=img
        prod1.category_id_id=category
        prod1.product_price=Product_Price
        prod1.product_description=Description
        prod1.subcategory=subcat
        prod1.save()
        prodo=ProductInfo.objects.all()
        return render(request,'admin_products.html',{"products":prodo})
    cat_items=Category.objects.all()  
    return render(request,'admin_editproducts.html',{"products":prod,"categry":cat_items})
    
    
def admin_deleteproducts(request,id):
    prod1=ProductInfo.objects.filter(id=id).get()
    cat=Category.objects.filter(pk=prod1.category_id_id).get()
    cat.tot_num=int(cat.tot_num)-1
    cat.save()
    prod1.delete()
    prodo=ProductInfo.objects.all()
    return render(request,'admin_products.html',{"products":prodo})

def admin_brand(request):
    if request.method == "POST":
        name=request.POST['name']
        isfund=Brand.objects.filter(Name=name).all()
        if isfund:
            msg="This brand is already exists"
            return render(request,'admin_addproduct.html',{'show':1,"msg":msg})
        brand=Brand.objects.create(Name=name).save()
        return redirect('admin_addproducts')
    else:
        return render(request,'admin_addproduct.html',{'show':1})



def admin_oders(request):
    oder=Orderdetails.objects.all()
    return render(request,'admin_oders.html',{'products':oder})

def change_status(request):
    id = request.GET['id']
    value=request.GET['value']
    oder=Orderdetails.objects.filter(pk=id).get()
    if oder.payment_method=="COD":
        if value == "Delivered":
            oder.status=value
            oder.payment_status="Success"
            oder.save()
            return HttpResponse("done")
    oder.status=value
    oder.save()
    return HttpResponse("done")

def admin_orders_details(request,id):
    oder=Orderdetails.objects.filter(pk=id).get()
    return render(request,'admin_order_productdetails.html',{"orders":oder})

@csrf_exempt
def coupon(request,id):
    products=ProductInfo.objects.all()
    if int(id)==0:
        if request.method == "POST":
            Name=request.POST['name']
            discount=request.POST['discount']
            product=request.POST['product']
            coup=Coupon()
            coup.coupon_name=Name
            coup.offer=discount
            coup.save()
            pro=ProductInfo.objects.filter(pk=product).get()
            pro.offer_id_id=coup.pk
            pro.save()
            return JsonResponse({"done":"done"})
        return render(request,'coupon.html',{"products":products})
    else:
        cat=Category.objects.all()
        if request.method == "POST":
           Name=request.POST['name']
           discount=request.POST['discount']
           categ=request.POST['Category']
           coup=Coupon()
           coup.coupon_name=Name
           coup.offer=discount
           coup.save()
           pro=ProductInfo.objects.filter(category_id_id=categ).all()
           for i in pro:
               i.offer_id_id=coup.pk
               i.save()
           return HttpResponse("done")
        return render(request,'coupon.html',{"cat":1,"Category":cat})
    
def add_category(request):
    if request.method == "POST":
        Name=request.POST['name']
        isfound=Category.objects.filter(category_name=Name).all()
        if isfound:
            msg="This category is already exists"
            return render(request,'category_add.html',{"msg":msg})
        newcat=Category()
        newcat.category_name=Name
        newcat.offer_id=1
        newcat.save()
        msg="This category is successfully added"
        return render(request,'category_add.html',{"msg1":msg})
    return render(request,'category_add.html')


def admin_sales(request):
    try:
        id=int(request.GET['id'])
    except:
        id=0
    salesreport=[]
    mostSell={}
    product=ProductInfo.objects.all()
    for i in product:
        totprice=Orderdetails.objects.filter(order_prd_name=i.product_name).all().aggregate((Sum('order_prd_price')))
        totqnty=Orderdetails.objects.filter(order_prd_name=i.product_name).all().aggregate((Sum('order_prd_quantity')))
        sold=Orderdetails.objects.filter(order_prd_name=i.product_name).all().count()
        mostSell[i.pk]=int(sold)
        obj=Sales(i.product_name,totqnty["order_prd_quantity__sum"],i.product_price,totprice["order_prd_price__sum"],i.product_image1)
        salesreport.append(obj)
    if id == 1 :
        odr=Orderdetails.objects.all().aggregate((Sum('order_prd_quantity')))
        totpr=Orderdetails.objects.all().aggregate((Sum('order_prd_price')))
        max_key=max(mostSell,key=mostSell.get)
        min_key=min(mostSell,key=mostSell.get)
        mstSoldprd=ProductInfo.objects.get(pk=max_key)
        lstSoldprd=ProductInfo.objects.get(pk=min_key)
        context={
            "totoder":odr["order_prd_quantity__sum"],
            "totprc":totpr["order_prd_price__sum"],
            "mostsold":mstSoldprd.product_name,
            "leastsold":lstSoldprd.product_name,
            
        }
        return render(request,'summary.html',context)
    return render(request,'salesreport.html',{'products':salesreport})