from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from .models import Review
from django.views import View # Bazı görünüm ayarlarını genişletmek için
from django.views.generic.base import TemplateView # Daha spesifik özel bir görünüm için
from django.views.generic import ListView, DetailView # Listeler için özel template 
# from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView


# Create your views here.

# def review(request):
# #   if request.method == 'POST':
# #     entered_username = request.POST['username']

# #     # if entered_username == "":
# #     if entered_username == "" and len(entered_username) >= 100:
# #       return render(request, "reviews/review.html", {
# #         "has_error": True
# #       })
# #     print(entered_username)
# #     return HttpResponseRedirect("/thank-you")
    
#     if request.method == 'POST':
#         existing_model = Review.objects.get(pk=1)
#         form = ReviewForm(request.POST, instance=existing_model) # instance=existing_model

#         if form.is_valid():
#             # print(form.cleaned_data)
#             # review = Review(
#             #     user_name=form.cleaned_data['user_name'],
#             #     review_text=form.cleaned_data['review_text'],
#             #     rating=form.cleaned_data['rating'])
#             # review.save()
#             form.save()
#             return HttpResponseRedirect("/thank-you")

#     else:
#         form = ReviewForm()

#     return render(request, "reviews/review.html", {
#         "form": form
#     })

class ReviewView(CreateView):
    # form_class = ReviewForm
    model = Review
    # fields = '__all__'
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


# # class ReviewView(View):
# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = "reviews/review.html"
#     success_url = "/thank-you"

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


    # def get(self, request):
    #     form = ReviewForm()

    #     return render(request, "reviews/review.html", {
    #         "form": form
    #     })

    # def post(self, request):
    #     form = ReviewForm(request.POST)

    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect("/thank-you")
        
    #     return render(request, "reviews/review.html", {
    #         "form": form
    #     })



# def thank_you(request):
#     return render(request, "reviews/thank_you.html")

class ThankYouView(TemplateView):
    # def get(self, request):
    #     return render(request, "reviews/thank_you.html")
    template_name = "reviews/thank_you.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This works!"
        return context
    
# class ReviewsListView(TemplateView):
#     template_name = "reviews/review_list.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         reviews = Review.objects.all()
#         context["reviews"] = reviews
#         return context
    
class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__gt=4)
    #     return data

    
# class SingleReviewView(TemplateView):
#     template_name = "reviews/single_review.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         review_id = kwargs["id"]
#         # reviews = Review.objects.all()
#         selected_review = Review.objects.get(pk=review_id)
#         # context["reviews"] = reviews
#         context["review"] = selected_review
#         return context
    
class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        # if "favorite_review" in request.session:
        #     favorite_id = request.session["favorite_review"]
        # else:
        #     favorite_id = None
        # favorite_id = request.session["favorite_review"]
        favorite_id = request.session.get("favorite_review")
        # context["is_favorite"] = favorite_id == loaded_review.id # True
        context["is_favorite"] = favorite_id == str(loaded_review.id) #"1"
        return context

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        # fav_review = Review.objects.get(pk=review_id)
        # request.session["favorite_review"] = fav_review
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)