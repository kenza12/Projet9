from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket
from .forms import TicketForm
from reviews.models import Review
from utils import get_stars
from itertools import chain


class TicketListView(LoginRequiredMixin, View):
    """Display a list of tickets and reviews related to the user."""

    def get(self, request):
        # Retrieve tickets created by the currently logged-in user, sorted by creation time.
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")

        # Retrieve reviews left by the currently logged-in user on their own tickets, sorted by creation time.
        reviews_to_user_tickets = Review.objects.filter(ticket__user=request.user, user=request.user).order_by("-time_created")

        # Retrieve reviews created by the currently logged-in user but exclude those left on their own tickets, sorted by creation time.
        user_reviews = (
            Review.objects.filter(user=request.user).exclude(ticket__user=request.user).order_by("-time_created")
        )

        # Function to annotate posts with types and stars
        def annotate_posts(posts, post_type):
            for post in posts:
                post.type = post_type
                if hasattr(post, "rating"):
                    post.stars_str = "".join(["★" if star else "☆" for star in get_stars(post.rating)])
            return posts

        # Annotating each type of post
        annotated_tickets = annotate_posts(tickets, "ticket")
        annotated_reviews_to_user_tickets = annotate_posts(reviews_to_user_tickets, "review_to_user_ticket")
        annotated_user_reviews = annotate_posts(user_reviews, "user_review")

        # Merging tickets and reviews into a single sorted list
        all_posts = sorted(
            chain(annotated_tickets, annotated_reviews_to_user_tickets, annotated_user_reviews),
            key=lambda post: post.time_created,
            reverse=True,
        )

        return render(request, "ticket/ticket_list.html", {"all_posts": all_posts})


class CreateTicketView(LoginRequiredMixin, View):
    """Create a new ticket."""

    def get(self, request):
        """Handle GET requests and present a form to create a new ticket.

        Args:
            request (HttpRequest): The incoming request object.

        Returns:
            HttpResponse: Rendered HTML response with the ticket creation form.
        """
        form = TicketForm()
        return render(request, "ticket/create_ticket.html", {"form": form})

    def post(self, request):
        """Handle POST requests to create a new ticket.

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
            return redirect("ticket_list")
        else:
            return render(request, "ticket/create_ticket.html", {"form": form})


class UpdateTicketView(LoginRequiredMixin, View):
    """View for updating an existing ticket."""

    template_name = "ticket/update_ticket.html"

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        form = TicketForm(instance=ticket)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_list")
        return render(request, self.template_name, {"form": form})


class DeleteTicketView(LoginRequiredMixin, View):
    """View for deleting an existing ticket."""

    template_name = "ticket/delete_ticket.html"

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        return render(request, self.template_name, {"ticket": ticket})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        ticket.delete()
        return redirect("ticket_list")
