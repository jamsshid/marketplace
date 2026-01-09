Project Structure

smart_marketplace/
├── core/                       # Sozlamalar
│   ├── settings/               # settings.py
│   ├── celery.py               # Celery konfiguratsiyasi
│   └── urls.py                 # Asosiy routing + Swagger
├── apps/                       
│   ├── users/                  # Auth & Profile
│   ├── products/               # Catalog & Inventory
│   ├── orders/                 # Cart & Checkout
│   ├── analytics/              # Statistics & Reporting
│   └── payments/               # Payment Gateway Integration
├── services/                   # Tashqi API va og'ir mantiqlar (Stripe, Email)
├── docker/                     # Dockerfile va Nginx config
├── .env.example                # Muhit o'zgaruvchilari namunasi
├── docker-compose.yml
└── manage.py

