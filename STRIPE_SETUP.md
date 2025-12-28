# Stripe Payment Gateway Setup

This project now includes Stripe payment integration. Follow these steps to set it up:

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `stripe` package (version 7.0.0).

## 2. Get Your Stripe API Keys

1. Sign up for a Stripe account at https://stripe.com
2. Go to the Stripe Dashboard: https://dashboard.stripe.com
3. Navigate to **Developers** > **API keys**
4. Copy your **Publishable key** and **Secret key**

## 3. Configure Stripe Keys

### Option A: Environment Variables (Recommended for Production)

Set these environment variables:
```bash
export STRIPE_PUBLISHABLE_KEY='pk_test_your_publishable_key_here'
export STRIPE_SECRET_KEY='sk_test_your_secret_key_here'
```

### Option B: Direct Configuration (For Development Only)

Edit `eCommerce/settings.py` and replace the placeholder values:
```python
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_actual_key_here'
STRIPE_SECRET_KEY = 'sk_test_your_actual_key_here'
```

## 4. Run Migrations

Create and apply the database migrations for the billing app:

```bash
python manage.py makemigrations billing
python manage.py migrate
```

## 5. Test the Integration

### Test Mode
- Use test API keys (they start with `pk_test_` and `sk_test_`)
- Use Stripe's test card numbers:
  - **Success**: 4242 4242 4242 4242
  - **Decline**: 4000 0000 0000 0002
  - Use any future expiry date and any 3-digit CVC

### Production Mode
- Replace test keys with live keys (they start with `pk_live_` and `sk_live_`)
- Update the keys in your production environment

## 6. Features Included

- ✅ Checkout page with Stripe Elements
- ✅ Secure payment processing
- ✅ Order management
- ✅ Payment history
- ✅ Order status tracking
- ✅ Cart clearing after successful payment

## 7. URLs

- Checkout: `/billing/checkout/`
- Payment Processing: `/billing/payment/`
- Payment Success: `/billing/payment/success/<order_id>/`
- Order History: `/billing/orders/`

## 8. Admin Interface

The billing models (BillingProfile, Order, Payment) are registered in the Django admin for easy management.

## Security Notes

⚠️ **Important**: Never commit your secret keys to version control. Always use environment variables in production.

## Support

For Stripe API documentation, visit: https://stripe.com/docs/api

