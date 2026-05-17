from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .forms import ContactForm


def build_social_links():
    links = [
        {
            "label": "GitHub",
            "icon": "ri-github-fill",
            "url": settings.PORTFOLIO_GITHUB_URL,
        },
        {
            "label": "LinkedIn",
            "icon": "ri-linkedin-fill",
            "url": settings.PORTFOLIO_LINKEDIN_URL,
        },
        {
            "label": "Email",
            "icon": "ri-mail-line",
            "url": f"mailto:{settings.PORTFOLIO_EMAIL}" if settings.PORTFOLIO_EMAIL else "",
        },
        {
            "label": "Twitter",
            "icon": "ri-twitter-x-fill",
            "url": settings.PORTFOLIO_TWITTER_URL,
        },
        {
            "label": "WhatsApp",
            "icon": "ri-whatsapp-line",
            "url": settings.PORTFOLIO_WHATSAPP_URL,
        },
        {
            "label": "Fiverr",
            "icon": "ri-briefcase-4-fill",
            "url": settings.PORTFOLIO_FIVERR_URL,
        },
        {
            "label": "ComeUp",
            "icon": "ri-store-2-fill",
            "url": settings.PORTFOLIO_COMEUP_URL,
        },
    ]
    return [link for link in links if link["url"]]


def build_projects():
    return [
        {
            "emoji": "🍽️",
            "image": "",
            "title": "Plateforme Multi-Restaurants",
            "description": (
                "Application web complète permettant la gestion de plusieurs "
                "restaurants avec système de réservations en ligne et tableau "
                "de bord administrateur."
            ),
            "tags": ["Django", "MySQL", "REST API", "Bootstrap"],
            "links": [
                {"label": "GitHub", "icon": "ri-github-fill", "url": "https://github.com/esdyol/"},
            ],
        },
        {
            "emoji": "🏫",
            "image": "images/Gestion_ecole.png",
            "title": "Plateforme Multi-école (Full-Stack)",
            "description": (
                "Application SaaS full-stack : API Django REST pour la gestion centralisée "
                "de plusieurs établissements scolaires (notes, paiements, tableaux de bord) "
                "et interface utilisateur React déployée sur Vercel."
            ),
            "tags": ["Django", "React", "PostgreSQL", "REST API", "SaaS", "Vercel"],
            "links": [
                {"label": "GitHub", "icon": "ri-github-fill", "url": "https://github.com/esdyol/"},
                {"label": "Voir le site", "icon": "ri-external-link-line", "url": "https://schoolhub-frontend.vercel.app"},
            ],
        },
        {
            "emoji": "💻",
            "image": "",
            "title": "Applications Desktop Tkinter",
            "description": (
                "Suite d'applications de bureau avec interfaces graphiques "
                "élégantes, connexion aux bases de données et système de "
                "validation avancé."
            ),
            "tags": ["Python", "Tkinter", "SQLite"],
            "links": [
                {"label": "GitHub", "icon": "ri-github-fill", "url": "https://github.com/esdyol/"},
            ],
        },
    ]


def build_context(form):
    return {
        "form": form,
        "profile_image": "images/profile-photo.webp",
        "social_links": build_social_links(),
        "projects": build_projects(),
    }


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Envoi de l'email via Brevo
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD and settings.PORTFOLIO_EMAIL:
                subject = f"Portfolio - Nouveau message : {contact.subject}"
                body = f"Nouveau message de : {contact.name} ({contact.email})\n\n{contact.message}"
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.PORTFOLIO_EMAIL],
                    fail_silently=True,
                )
            
            messages.success(request, "Votre message a bien été envoyé. Merci !")
            return redirect("/") 
        messages.error(request, "Le formulaire contient des erreurs.")
        return render(request, "base.html", build_context(form), status=400)

    form = ContactForm()
    return render(request, "base.html", build_context(form))


def custom_404(request, exception):
    return render(request, "404.html", status=404)
