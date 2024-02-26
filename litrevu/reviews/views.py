from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Ticket
from .forms import ReviewForm, ReviewFormWithoutTicket
from ticket.forms import TicketForm
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse


class CreateReviewWithTicketView(LoginRequiredMixin, View):
    """
    Cette vue affiche et traite les formulaires pour créer un nouveau ticket et une critique associée.
    """
    template_name = "reviews/create_review_with_ticket.html"

    def get(self, request):
        """
        Gère la requête GET pour afficher les formulaires de ticket et de critique.

        Args:
            request: L'objet HttpRequest.

        Returns:
            HttpResponse: Rendu de la page avec les formulaires de ticket et de critique.
        """

        ticket_form = TicketForm()
        review_form = ReviewFormWithoutTicket()
        return render(request, self.template_name, {"ticket_form": ticket_form, "review_form": review_form})

    def post(self, request):
        """
        Gère la requête POST pour soumettre et enregistrer un nouveau ticket et une critique.

        Args:
            request: L'objet HttpRequest.

        Returns:
            HttpResponse: Redirige vers la liste des posts ou renvoie la page avec des erreurs.
        """

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

            return redirect("ticket_list")
        else:
            return render(request, self.template_name, {"ticket_form": ticket_form, "review_form": review_form})


class CreateReviewForTicketView(LoginRequiredMixin, View):
    """
    Vue pour créer une critique pour un ticket existant.
    """

    template_name = "reviews/create_review_for_ticket.html"

    def get(self, request, *args, **kwargs):
        """
        Affiche le formulaire de critique pour un ticket spécifié.

        Args:
            request: L'objet HttpRequest.

        Returns:
            HttpResponse: Rendu de la page avec le formulaire de critique.
        """

        ticket_id = request.GET.get("ticket_id")
        if not ticket_id:
            return HttpResponseRedirect(reverse("feed"))

        ticket = get_object_or_404(Ticket, pk=ticket_id)
        review_form = ReviewForm(initial={"ticket": ticket})
        return render(request, self.template_name, {"form": review_form, "ticket": ticket})

    def post(self, request, *args, **kwargs):
        """
        Traite la soumission du formulaire de critique.

        Args:
            request: L'objet HttpRequest.

        Returns:
            HttpResponse: Redirige vers la liste des posts ou affiche les erreurs.
        """

        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("ticket_list")
        else:
            for field, errors in review_form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
        return render(request, self.template_name, {"form": review_form})


class UpdateReviewView(LoginRequiredMixin, View):
    """
    Gère l'affichage et la soumission du formulaire de mise à jour d'une critique existante.
    """

    template_name = "reviews/update_review.html"

    def get(self, request, pk):
        """
        Affiche le formulaire de mise à jour pour une critique spécifiée.

        Args:
            request: L'objet HttpRequest.
            pk (int): L'identifiant de la critique à mettre à jour.

        Returns:
            HttpResponse: Rendu de la page avec le formulaire de mise à jour.
        """

        review = get_object_or_404(Review, pk=pk, user=request.user)
        ticket = review.ticket  # Récupérer le ticket associé à la critique
        form = ReviewForm(instance=review)
        return render(request, self.template_name, {"form": form, "ticket": ticket})

    def post(self, request, pk):
        """
        Traite la soumission du formulaire de mise à jour de la critique.

        Args:
            request: L'objet HttpRequest.
            pk (int): L'identifiant de la critique à mettre à jour.

        Returns:
            HttpResponse: Redirige vers la liste des posts ou affiche les erreurs.
        """

        review = get_object_or_404(Review, pk=pk, user=request.user)
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("ticket_list")
        return render(request, self.template_name, {"form": form, "ticket": review.ticket})


class DeleteReviewView(LoginRequiredMixin, View):
    """
    Gère l'affichage de la confirmation de suppression et la suppression effective d'une critique existante.
    """

    template_name = "reviews/delete_review.html"

    def get(self, request, pk):
        """
        Affiche la page de confirmation de suppression pour une critique spécifiée.

        Args:
            request: L'objet HttpRequest.
            pk (int): L'identifiant de la critique à supprimer.

        Returns:
            HttpResponse: Rendu de la page de confirmation de suppression.
        """

        review = get_object_or_404(Review, pk=pk, user=request.user)
        return render(request, self.template_name, {"review": review})

    def post(self, request, pk):
        """
        Effectue la suppression de la critique spécifiée.

        Args:
            request: L'objet HttpRequest.
            pk (int): L'identifiant de la critique à supprimer.

        Returns:
            HttpResponse: Redirige vers la liste des posts après suppression.
        """

        review = get_object_or_404(Review, pk=pk, user=request.user)
        review.delete()
        return redirect("ticket_list")
