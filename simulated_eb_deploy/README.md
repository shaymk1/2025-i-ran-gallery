# In 2025, I Ran — Gallery & Blog

Welcome to **In 2025, I Ran**, a Django-powered web application for sharing running stories, race galleries, and personal achievements. This project features a modern blog, photo gallery, social media sharing, email subscriptions, and more.

---

## Features

- 🏃 **Blog & Gallery:** Share stories and race photos with rich content.
- 🏷️ **Tags & Search:** Easily find posts by tags or keywords.
- 📬 **Email Subscriptions:** Readers can subscribe via email (powered by Brevo).
- 🔗 **Social Media Sharing:** Share posts to Twitter, Facebook, WhatsApp, or Email.
- 📰 **RSS Feed:** Stay updated with the latest posts via RSS.
- 🗺️ **Sitemap:** SEO-friendly sitemap for search engines.
- 📈 **Google Analytics:** Integrated for traffic monitoring.
- 🛡️ **Security:** Secure authentication, password reset, and session management.

- 📧 **Contact Form:** Easy way for readers to reach out.

---

## Tech Stack

- **Backend:** Django 4.x
- **Frontend:** Bootstrap 5, Font Awesome
- **Database:** SQLite (dev), PostgreSQL/MySQL (prod recommended)
- **Media Storage:** AWS S3 (via django-storages)
- **Email:** Brevo (Sendinblue) API
- **Deployment:** AWS Elastic Beanstalk (or any WSGI-compatible host)

---

## Setup & Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/2025-i-ran-gallery.git
    cd 2025-i-ran-gallery
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Copy `.env.example` to `.env` and fill in your secrets (SECRET_KEY, DB credentials, AWS keys, BREVO_API_KEY, etc.).

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Collect static files:**
    ```bash
    python manage.py collectstatic
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

---

## Deployment

- Ready for deployment on AWS Elastic Beanstalk or any WSGI-compatible host.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` and production environment variables.
- Use `python manage.py collectstatic` before deploying.

---

## Folder Structure

```
2025-i-ran-gallery/
│
├── app/                # Main Django app (views, models, templates)
├── core/               # Project settings and configuration
├── static/             # Global static files
├── media/              # Uploaded media files (S3 in production)
├── templates/          # Base templates
├── requirements.txt
├── .env.example
├── manage.py
└── README.md
```

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Brevo (Sendinblue)](https://www.brevo.com/)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
- [Sentry](https://sentry.io/)

---

**Happy running and sharing!**