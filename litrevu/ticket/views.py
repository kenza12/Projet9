from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket
from .forms import TicketForm
from reviews.models import Review
from utils import get_stars



class TicketListView(LoginRequiredMixin, View):
    """
    Display a list of tickets and reviews related to the user.
    """

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews_to_user_tickets = Review.objects.filter(ticket__user=request.user)
        user_reviews = Review.objects.filter(user=request.user)

        # Ajouter les étoiles aux reviews
        for review in reviews_to_user_tickets:
            review.stars_str = ''.join(['★' if star else '☆' for star in get_stars(review.rating)])

        for review in user_reviews:
            review.stars_str = ''.join(['★' if star else '☆' for star in get_stars(review.rating)])

        context = {
            'tickets': tickets,
            'reviews_to_user_tickets': reviews_to_user_tickets,
            'user_reviews': user_reviews
        }

        return render(request, 'ticket/ticket_list.html', context)


class CreateTicketView(LoginRequiredMixin, View):
    """
    Create a new ticket.
    
    Extends the View class and uses LoginRequiredMixin to ensure only authenticated
    users can access this view.
    """

    def get(self, request):
        """
        Handle GET requests and present a form to create a new ticket.

        Args:
            request (HttpRequest): The incoming request object.

        Returns:
            HttpResponse: Rendered HTML response with the ticket creation form.
        """
        form = TicketForm()
        return render(request, 'ticket/create_ticket.html', {'form': form})

    def post(self, request):
        """
        Handle POST requests to create a new ticket.

        Args:
            request (HttpRequest): The incoming request object with submitted form data.

        Returns:
            HttpResponse: Redirect to the ticket list on successful creation or 
                          render the form again with errors.
        """
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)  # don't save the ticket in DB
            ticket.user = request.user  # add connected user
            ticket.save()  # save the ticket
            return redirect('ticket_list')
        else:
            return render(request, 'ticket/create_ticket.html', {'form': form})

class UpdateTicketView(LoginRequiredMixin, View):
    template_name = 'ticket/update_ticket.html'

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        form = TicketForm(instance=ticket)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
        return render(request, self.template_name, {'form': form})

class DeleteTicketView(LoginRequiredMixin, View):
    template_name = 'ticket/delete_ticket.html'

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        ticket.delete()
        return redirect('ticket_list')