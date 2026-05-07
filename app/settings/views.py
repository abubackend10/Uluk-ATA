from django.shortcuts import render, redirect
from app.settings.models import Settings, OurHistory, Statistic, HistoryFeature, News, Testimonial, Gallery, ContactMessage, Reservation, Category, Dish
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField, Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    site_settings = Settings.objects.first()
    our_history = OurHistory.objects.prefetch_related('features').first()
    popular_dishes = Dish.objects.filter(is_popular=True)[:6]
    context = {
        'site_settings': site_settings,
        'our_history': our_history,
        'statistics': Statistic.objects.all(),
        'news_list': News.objects.filter(is_published=True)[:3],
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('-created_at'),
        'popular_dishes': popular_dishes,
    }
    return render(request, 'index.html', context)

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not phone or not message:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля (Имя, Телефон, Сообщение).')
            return redirect('contacts')

        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )
        
        if email:
            try:
                send_mail(
                    subject='Спасибо за ваше сообщение - Uluk-Ata Restaurant',
                    message=f'Здравствуйте, {name}!\n\nМы получили ваше сообщение и свяжемся с вами в ближайшее время по номеру {phone}.\n\nВаше сообщение:\n"{message}"\n\nС уважением,\nКоманда Uluk-Ata Restaurant',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Ошибка отправки email: {e}")

        messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return redirect('contacts')
    
    return render(request, 'contacts.html')

def gallery(request):
    context = {
        'gallery_items': Gallery.objects.all().order_by('created_at'),
    }
    return render(request, 'gallery.html', context)


def menu(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    
    today = timezone.now().date()
    
    is_new_q = Q(is_new=True) & (Q(new_until_date__isnull=True) | Q(new_until_date__gte=today))
    is_promo_q = Q(is_promotion=True) & (Q(promotion_end_date__isnull=True) | Q(promotion_end_date__gte=today)) & Q(discount_price__isnull=False)

    dishes = Dish.objects.select_related('category').annotate(
        sort_priority=Case(
            When(is_new_q & is_promo_q, then=Value(1)),
            When(is_new_q, then=Value(2)),
            When(is_promo_q, then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by('sort_priority', 'title')

    current_category = None
    if category_slug and category_slug.lower() != 'all':
        current_category = Category.objects.filter(slug=category_slug).first()
        if current_category:
            dishes = dishes.filter(category=current_category)

    context = {
        'categories': categories,
        'dishes': dishes,
        'current_category': current_category,
        'active_category': category_slug.lower() if category_slug else 'all',
    }
    return render(request, 'menu.html', context)

def reservation(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        guests = request.POST.get('guests', '').strip()
        occasion = request.POST.get('occasion', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not name or not phone or not date or not time or not guests:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля для бронирования.')
            return redirect('reservation')

        Reservation.objects.create(
            name=name, phone=phone, date=date, time=time,
            guests=guests, occasion=occasion, comment=comment
        )
        
        site_settings = Settings.objects.first()
        if site_settings and site_settings.email:
            try:
                send_mail(
                    subject=f'Новая бронь: {name} на {date} {time}',
                    message=f'Новая бронь столика!\n\nИмя: {name}\nТелефон: {phone}\nДата: {date}\nВремя: {time}\nГостей: {guests}\nПовод: {occasion}\nКомментарий: {comment}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[site_settings.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Ошибка отправки email: {e}")
                
        messages.success(request, 'Ваша заявка принята! Мы свяжемся с вами в ближайшее время для подтверждения бронирования.')
        return redirect('reservation')
        
    return render(request, 'reservation.html')

def reviews(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        rating = request.POST.get('rating', '').strip()
        text = request.POST.get('text', '').strip()

        if not name or not text or not rating:
            messages.error(request, 'Пожалуйста, укажите имя, оценку и текст отзыва.')
            return redirect('reviews')

        Testimonial.objects.create(
            name=name,
            rating=rating,
            text=text
        )
        messages.success(request, 'Спасибо! Ваш отзыв отправлен на модерацию и скоро появится на сайте.')
        return redirect('reviews')
        
    return render(request, 'reviews.html')

def news_list(request):
    context = {
        'news_all': News.objects.filter(is_published=True),
    }
    return render(request, 'news_list.html', context)
