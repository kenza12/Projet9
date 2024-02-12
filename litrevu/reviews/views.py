
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Ticket
from .forms import ReviewForm, ReviewFormWithoutTicket
from ticket.forms import TicketForm
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect
from django.urls import reverse


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'


class CreateReviewWithTicketView(LoginRequiredMixin, View):
    template_name = 'reviews/create_review_with_ticket.html'

    def get(self, request):
        ticket_form = TicketForm()
        review_form = ReviewFormWithoutTicket()
        return render(request, self.template_name, {
            'ticket_form': ticket_form,
            'review_form': review_form
        })

    def post(self, request):
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewFormWithoutTicket(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('review_list')
        return render(request, self.template_name, {
            'ticket_form': ticket_form,
            'review_form': review_form
        })


class CreateReviewForTicketView(LoginRequiredMixin, View):
    template_name = 'reviews/create_review_for_ticket.html'

    def get(self, request, *args, **kwargs):
        ticket_id = request.GET.get('ticket_id')
        if not ticket_id:
            return HttpResponseRedirect(reverse('feed'))

        ticket = get_object_or_404(Ticket, pk=ticket_id)
        review_form = ReviewForm(initial={'ticket': ticket})
        return render(request, self.template_name, {
            'form': review_form,
            'ticket': ticket
        })

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')
        else:
            print("FORM NOT VALID **************")
            for field, errors in review_form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
        return render(request, self.template_name, {
            'form': review_form
        })


class UpdateReviewView(LoginRequiredMixin, View):
    template_name = 'reviews/update_review.html'

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        form = ReviewForm(instance=review)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
        return render(request, self.template_name, {'form': form})

class DeleteReviewView(LoginRequiredMixin, View):
    template_name = 'reviews/delete_review.html'

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        return render(request, self.template_name, {'review': review})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        review.delete()
        return redirect('review_list')