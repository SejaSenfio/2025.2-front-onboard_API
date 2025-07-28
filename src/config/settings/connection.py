from corsheaders.defaults import default_headers

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1", "https://*.senfio.com.br"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

APPEND_SLASH = False

WSGI_APPLICATION = "config.wsgi.application"

SESSION_TIMEOUT = 60 * 10

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

CORS_ALLOW_HEADERS = default_headers + ("content-disposition",)

CORS_EXPOSE_HEADERS = [
    "Content-Disposition",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d+)?$",
    r"^https:\/\/.*\.senfio\.com\.br$",
]

CORS_ALLOW_ALL_ORIGINS = False
