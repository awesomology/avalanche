from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
# import requests
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def notify_purchase_intent(request):
    try:
        data = json.loads(request.body)
        product = data.get('product', {})
        user_info = data.get('user', {})
        
        # Extract all product details including size, quantity, timestamp
        product_name = product.get('name', 'N/A')
        product_price = product.get('price', 'N/A')
        product_brand = product.get('brand', 'N/A')
        product_url = product.get('url', 'N/A')
        product_size = product.get('size', 'Not specified')
        product_quantity = product.get('quantity', 1)
        product_total = product.get('totalPrice', 'N/A')
        inquiry_time = product.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Build HTML email for better formatting
        # Simpler table-based HTML for maximum email client compatibility
        html_message = f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: white; margin: 20px auto; border-radius: 10px;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #DAA520; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                                <h1 style="color: white; margin: 0;">🛍️ NEW PURCHASE INTENT</h1>
                            </td>
                        </tr>
                        
                        <!-- Product Details -->
                        <tr>
                            <td style="padding: 20px;">
                                <h2 style="color: #DAA520; margin: 0 0 15px 0;">📦 PRODUCT INFORMATION</h2>
                                <table width="100%" cellpadding="5" cellspacing="0" border="0">
                                    <tr>
                                        <td width="120" style="font-weight: bold;">Name:</td>
                                        <td>{product_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Brand:</td>
                                        <td>{product_brand}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Price:</td>
                                        <td>₦{product_price}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Quantity:</td>
                                        <td>{product_quantity}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Size:</td>
                                        <td>{product_size}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Total:</td>
                                        <td style="color: #DAA520; font-weight: bold;">{product_total}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Link:</td>
                                        <td><a href="{product_url}" style="color: #DAA520;">Click Here</a></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Customer Info -->
                        <tr>
                            <td style="padding: 20px; background-color: #f9f9f9;">
                                <h2 style="color: #DAA520; margin: 0 0 15px 0;">👤 CUSTOMER INFORMATION</h2>
                                <table width="100%" cellpadding="5" cellspacing="0" border="0">
                                    <tr>
                                        <td width="120" style="font-weight: bold;">Time:</td>
                                        <td>{inquiry_time}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Device:</td>
                                        <td>{user_info.get('userAgent', 'N/A')[:50]}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Platform:</td>
                                        <td>{user_info.get('platform', 'N/A')}</td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: bold;">Referrer:</td>
                                        <td>{user_info.get('referrer', 'Direct visit')}</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 20px; text-align: center; font-size: 12px; color: #666;">
                                <p>This is an automated notification from Avalanche Store.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """
        
        # Build detailed notification message for admins
        text_message = f"""
        🔔 *NEW PURCHASE INTENTION* 🔔
        
        ════════════════════════
        📦 *PRODUCT INFORMATION*
        ════════════════════════
        • Name: {product_name}
        • Brand: {product_brand}
        • Price: ₦{product_price}
        • Quantity: {product_quantity}
        • Size: {product_size}
        • Total: {product_total}
        • Link: {product_url}
        
        ════════════════════════
        👤 *CUSTOMER INFORMATION*
        ════════════════════════
        • Time: {inquiry_time}
        • Device: {user_info.get('userAgent', 'N/A')[:100]}
        • Platform: {user_info.get('platform', 'N/A')}
        • Language: {user_info.get('language', 'N/A')}
        • Screen Size: {user_info.get('screenSize', 'N/A')}
        • Timezone: {user_info.get('timezone', 'N/A')}
        • Referrer: {user_info.get('referrer', 'N/A')}
        
        ════════════════════════
        📋 *ACTION REQUIRED*
        ════════════════════════
        Please contact this potential customer immediately!
        
        ---
        This is an automated notification from Avalanche Store.
        """
        
        # Send emails to all admins
        email_sent = False
        for admin_email in settings.ADMIN_EMAILS:
            if admin_email:  # Only send if email exists
                try:
                    # Create email with both HTML and plain text
                    email = EmailMultiAlternatives(
                        subject=f"🛍️ Purchase Intent - {product_name}",
                        body=text_message,  # Plain text version
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[admin_email],
                    )
                    email.attach_alternative(html_message, "text/html")  # HTML version
                    email.send(fail_silently=False)
                    email_sent = True
                    logger.info(f"Email sent successfully to {admin_email}")
                except Exception as e:
                    logger.error(f"Failed to send email to {admin_email}: {str(e)}")
        
        return JsonResponse({
            'status': 'success',
            'email_sent': email_sent
            }, status=200)
        
    except Exception as e:
        print(f"Notification error: {e}")
        logger.error(f"Notification error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def send_whatsapp_notification(phone_number, message):
    """Send WhatsApp notification using WhatsApp Business API or third-party service"""
    
    # Option 1: Using WhatsApp Cloud API (Meta)
    # You'll need to set up WhatsApp Business API
    WHATSAPP_TOKEN = getattr(settings, 'WHATSAPP_TOKEN', '')
    WHATSAPP_PHONE_ID = getattr(settings, 'WHATSAPP_PHONE_ID', '')
    
    if WHATSAPP_TOKEN and WHATSAPP_PHONE_ID:
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message[:1500]}  # WhatsApp message limit
        }
        try:
            requests.post(url, headers=headers, json=data, timeout=5)
        except:
            pass
    
    # Option 2: Using Twilio WhatsApp API
    # TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    # TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    # TWILIO_WHATSAPP_NUMBER = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', '')
    
    # Option 3: Using a webhook to a custom service
    # Or simply log to database for manual review


def send_telegram_notification(message):
    """Send notification to Telegram bot"""
    TELEGRAM_BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message[:4000],
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, json=data, timeout=5)
        except:
            pass