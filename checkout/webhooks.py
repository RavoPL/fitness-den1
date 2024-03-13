from django.conf import settings
import logging
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    logging.info(1)

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, wh_secret
        )
        logging.info(2)
    except ValueError as e:
        # Invalid payload
        logging.info('payload')
        logging.info(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logging.info('signature')
        logging.info(e)
        return HttpResponse(status=400)
    except Exception as e:
        logging.info('generic')
        logging.info(e)
        return HttpResponse(content=e, status=400)
    logging.info(3)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)
    logging.info(4)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }
    logging.info(5)

    # Get the webhook type from Stripe
    event_type = event['type']
    logging.info(6)

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)
    logging.info(7)

    # Call the event handler with the event
    response = event_handler(event)
    logging.info(8)
    return response