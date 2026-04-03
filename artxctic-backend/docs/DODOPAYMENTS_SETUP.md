# Dodopayments Setup Guide — Artxtic

## Prerequisites
- Dodopayments account (https://dodopayments.com)
- Backend deployed or running locally

## Step 1: Get API Keys

1. Log into Dodopayments (https://app.dodopayments.com)
2. **Settings → API Keys** — copy **Secret Key** and **Publishable Key**
3. **Settings → Webhooks** — copy or create a **Webhook Secret**

## Step 2: Configure `.env`

```env
DODOPAYMENTS_API_KEY=your-secret-key-here
DODOPAYMENTS_WEBHOOK_KEY=your-webhook-secret-here
DODOPAYMENTS_SUCCESS_URL=https://artxtic.com/payment-success
DODOPAYMENTS_CANCEL_URL=https://artxtic.com/payment-failure
```

For **test mode**, prefix with test key. Already configured for development.

## Step 3: Create Products in Dodopayments Dashboard

Go to **Products → Create** and create these subscription products:

| Plan | Monthly Price | Yearly Price | Notes |
|------|-------------|-------------|-------|
| Pro Monthly | $9.99/month | — | Copy Product ID |
| Pro Yearly | — | $99.00/year | Copy Product ID |
| Enterprise Monthly | $29.99/month | — | Copy Product ID |
| Enterprise Yearly | — | $299.00/year | Copy Product ID |

## Step 4: Update Seed Data

Replace the placeholder product IDs in `scripts/seed.py`:
```python
"dodopayments_plan_id": "your_real_product_id_here",
```

Then re-seed:
```bash
python scripts/seed.py
```

## Step 5: Configure Webhook Endpoint

1. In Dodopayments dashboard → **Webhooks → Create Endpoint**
2. URL: `https://yourdomain.com/api/v1/webhooks/dodopayments`
3. Events to subscribe:
   - `subscription.active`
   - `subscription.renewed`
   - `subscription.cancelled`
   - `subscription.expired`
   - `payment.failed`
4. Save and copy the webhook key to `.env`

## Step 6: Run Migration

```bash
alembic upgrade head
```

## Step 7: Test

```bash
# List plans
curl http://localhost:8000/api/v1/subscription/plans

# Create checkout (authenticated)
curl -X POST http://localhost:8000/api/v1/subscription/checkout \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"plan_id": "PLAN_ID", "billing_cycle": "monthly"}'
```

## Architecture

```
User → POST /checkout → Dodopayments Hosted Checkout
                              ↓ (payment success)
Dodopayments → POST /webhooks/dodopayments → subscription.active webhook
                              ↓
              Create/update Subscription record → Initialize UsageLimit
                              ↓
User → GET /subscription/current → See active plan + usage
```
