from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.utils import timezone
from .models import News, Category
from .forms import ContactForm


def your_view(request):
    today = timezone.now()
    return render(request, 'news/base.html', {'today': today})


def news_list(request):
    new_list = News.published.all()  # Используем только опубликованные новости
    context = {
        "new_list": new_list
    }
    return render(request, "news/news_list.html", context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.PUBLISHED)
    context = {
        "news": news
    }
    return render(request, 'news/news_detail.html', context)

def home_page_view(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:5]
    local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[:1]
    local_news = News.published.all().filter(category__name="Mahalliy").order_by("publish_time")[1:6]

    context = {
        "news_list": news_list,
        "categories": categories,
        "local_one": local_one,
        "local_news": local_news
    }
    return render(request, 'news/home.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.errors)
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur!")
        return render(request, self.template_name, {'form': form})

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name="Mahalliy").order_by("publish_time")[1:6]
        context['xorij_xabarlari'] = News.published.all().filter(category__name="Xorij").order_by("publish_time")[1:6]
        context['sport_xabarlari'] = News.published.all().filter(category__name="Sport").order_by("publish_time")[1:6]
        context['texnologiya_xabarlari'] = News.published.all().filter(category__name="Texnologiya").order_by("publish_time")[1:6]
        return context

def error_page_view(request):
    return render(request, 'news/404.html', {})


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    success_url = reverse_lazy('news-list')
