from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q, F, Value, Func, Count,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import  Avg, Max, Min, Sum

from django.contrib.contenttypes.models import ContentType

from store.models import Product, Customer, Order, OrderItem,Collection
from tags.models import TaggedItem

# Create your views here.

#@transaction.atomic() #全部函数都用事务
def say_hello(request):
    # try:
    #     product = Product.objects.get(pk=1)
    # except ObjectDoesNotExist:
    #     pass
    
    # 以下方式代替上面的try None
    # product = Product.objects.filter(pk=0).first()
    
    # 1、filter where条件
    # exists = Product.objects.filter(pk=0).exists() # 返回真假
    # queryset = Order.objects.filter(pk=1)   #Orders placed by customer with id = 1

    # queryset = Product.objects.filter(unit_price__gte=20) #gte是大于等于，gt是大于，lte是小于等于，lt是小于
    # queryset = Product.objects.filter(unit_price__range=(20,30)) # between 20 and 30
    
    
    # queryset = Product.objects.filter(title__contains="coffee") # like '%coffee%' #contains不分大小写，icontains区分大小写
    # queryset = Product.objects.filter(last_update__year=2021)  # between ''2021-01-01 00:00:00''' AND '''2021-12-31 23:59:59.999999'''
    # queryset = Product.objects.filter(description__isnull=True)  # is null
    # queryset = Customer.objects.filter(email__endswith='.com') # LIKE '%.com' Customers with .com accounts
    # queryset =    #Collections that don’t have a featured product
    # queryset = Product.objects.filter(inventory__lt=10)  #Products with low inventory (less than 10)
    
    # 2、complex lookups    
    # queryset = Product.objects.filter(unit_price__gt=20, inventory__lt=10) # unit_price > 20 and inventory < 10; AND条件
    # queryset = Product.objects.filter(unit_price__gt=20).filter(inventory__lt=10) # AND条件
    # queryset = Product.objects.filter(Q(unit_price__gt=20) | Q(inventory__lt=10)) # OR是|, AND是&,  Q() 用于复杂查询 ~Q() 用于取反查询 
    # queryset = Product.objects.filter(inventory=F('unit_price')) #Products with inventory equal to unit price F()用于字段比较
    # queryset =  Product.objects.filter(inventory=F("collection__id"))  #Product where the product’s collection id matches the inventory
    
    # sorting -  order by
    # queryset = Product.objects.filter(collection__id=3).order_by("title").reverse()  #ascending order by title 默认顺序, -title is descending order倒序，reverse也是倒序
    # limit 
    # prodcut = Product.objects.earliest("unit_price") #earliest是最早的，latest是最晚的, first是排在第一的，last是排在最后的；需要可以比较的类型，比如时间，数字，字符串
    # return render(request, "home.html", {"name": "Harley", "product": prodcut})
    
    # limiting 0,1,2,3,4 
    # queryset = Product.objects.order_by("unit_price")[:1] #limit 1
    # product  = Product.objects.order_by("unit_price")[0] #同limit 1，但这个写法只有1个结果，无法迭代
    #queryset = Product.objects.all()[:5]  #limit to 5 results
    # 5,6,7,8,9
    # queryset = Product.objects.all()[5:10]  #offset by 5 results
    
    
    
    # selecting fields 联合查询
    # only specific fields, 用values()方法返回指定字段
    # queryset = Product.objects.filter(collection__id=3).values("title", "collection__title")  #select title and collection title; inner join '' on 'store_collection'.'id' = 'store_product'.'collection_id' where 'store_product'.'collection_id' = 3
    # queryset = Product.objects.all().values('title', 'collection__title')  #select title and collection title，返回{}; inner join '' on 'store_collection'.'id' = 'store_product'.'collection_id'
    # queryset = Product.objects.all().values_list('title', 'collection__title')  #select title and collection title，返回()turple
    # queryset = Product.objects.only('title', 'collection__title')  #select title and collection title，only()方法返回dictionay object; select 'store_product'.'id', 'store_product'.'title', 'store_product'.'collection_id'from 'store_product'
    
    #找出所有orderitem里面的product_id，然后再找出product
    # queryset = Product.objects.filter(id__in=OrderItem.objects.values("product_id").distinct()) #values()方法返回instance,
    
    
    # excercize: be odered products and sort them by title
    # queryset = OrderItem.objects.values("product_id").distinct() #values()方法返回instance,
    # queryset = Product.objects.filter(id__in=queryset).order_by("title")
    
    # deferring fields for otmiization
    # queryset = Product.objects.defer("id", "title") #尽量少用
    
    # 关系查询
    # queryset = Product.objects.filter(collection__id=3)
    
    
    # select_related 优化效率
    # selected related objects， one relationship 一对多关系
    # queryset = Product.objects.all() # 如果模版要显示关联字段，那么效率低 查询多1000次
    # queryset = Product.objects.select_related("collection").all() # 效率高 先inner join后查询
    # queryset = Product.objects.select_related("collection__collection").all() # 效率高 先inner join后查询 外键的外键
    
    # prefetch_related objects， many relationship 多对多关系
    # queryset = Product.objects.prefetch_related("promotions").all() # 效率高 先join后查询   
    
    #结合上面
    # queryset = Product.objects.prefetch_related("promotions").select_related('collection').all() 
    
    #exercise: get the last 5 orders with their customer and items (incl product)
    # queryset = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5].select_related("id") #customer是父级，只有一个，用select_related, orderitem_set表示orderitem是子级，有多个，相反用用prefetch_related
    # result = Product.objects.aggregate(Count("id")) # 默认输出 {'id__count': 1000}
    
    
    #aggregate 聚合函数
    # result = Product.objects.aggregate(
        # count = Count("id"), # 输出 {'count': 1000}
        # min_price = Min("unit_price"), # 输出 {'min_price': 1.00}
        # ) 
        
    #annoatate 注释的意思 主要是创建一些字段
    # queryset = Product.objects.annotate(new_id = Value(True)) # annotate给对象添加了一个新的字段，不能是bool，否则要用value转化 
    # queryset = Product.objects.annotate(new_id = F("id") + 1) # annotate给对象添加了一个新的字段，用F()函数转化为str ; select id + 1 as new_id from store_product
    
    # queryset = Customer.objects.annotate(
    #     full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT') # annotate给对象添加了一个新的字段，而且用Func()函数调用concat函数连接full_name; 
    # )
    #作用同上
    # queryset = Customer.objects.annotate(
    #    full_name = Concat(('first_name'), Value(' '), ('last_name')) # annotate给对象添加了一个新的字段，而且用Func()函数调用concat函数连接full_name; 
    #    )
    # queryset = Customer.objects.annotate(
    #     orders_count = Count("order") # annotate给对象添加了一个新的字段，求订单数量；order有个外键是customer，但是不能用order_set反向查询orders, 只能先left join和group by，然后count（自动实现）
    #     )
    # discounted_price = ExpressionWrapper(F("unit_price") * 0.8, output_field=DecimalField()) # ExpressionWrapper是一个表达式，用于计算折扣价，output_field=DecimalField()是指定输出的数据类型
    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price
    #     )
    
    # querying generic relationships, 适用 content-type类型
    # content_type = ContentType.objects.get_for_model(Product) # 获取product的content_type的id,在django_content_type表里面
    # queryset = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=1) # 通过content_type和object_id来查询taggeditem;setect_related('tag')是为了优化查询效率，因为taggeditem有一个外键是tag，如果不用select_related('tag')，那么会查询1000次taggeditem，然后再查询1000次tag，这样效率很低，用了select_related('tag')，就会先查询taggeditem，然后再查询tag，这样效率高很多
    
    
    #自定义一个objects.get_tags_for的方法，custom manager，实现上面content_type的功能
    #在models文件里面定义一个manager, 在模型里面实例化这个manager，然后就可以用这个manager的方法了
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)
    
    #queryset的缓存
    
    # create objects
    # prodduct和collection都有外键，collection有一个featured_product外键，指向product；而某一部份的product则是同一个collection
    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # #collection.featured_product_id = 1  #和上面那句作用是一样的
    # collection.save()
    #collection = Collection.objects.create(title="Video Games", featured_product_id=1) #和上面那句作用是一样的
    
    # update objects
    # collection = Collection(pk=11) #这种方式容易发生问题，如果title没有设置，那么title就会被设置为null
    # collection.title = "Games"
    # collection.featured_product = None
    # collection.save()
    #collection = Collection.objects.filter(pk=11).update(featured_product=None) #这种方式不会发生问题，如果title没有设置，那么title就不会被更新
    
    #delete objects
    # collection = Collection(pk=11)
    # collection.delete()
    # Collection.objects.filter(id__gt=10).delete() #删除id大于10的collection
    
    #transactions
    #保存一个订单和一个item，如果有一个失败，那么都不保存
    with transaction.atomic(): #将以下代码放在事务里面
        order = Order()
        order.customer = Customer(pk=1)
        order.save()
        
        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
        
    # raw sql
    
    return render(request, "home.html", {"name": "Harley"})
