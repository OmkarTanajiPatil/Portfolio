# Email Configuration Guide

Your portfolio website is now set up with email functionality, but you need to configure it to actually send emails.

## Current Status
✅ **Contact form works** - Messages are saved to database  
✅ **SendGrid integration ready** - Code is written and configured  
❌ **Email sending needs setup** - Requires email credentials  

## Option 1: SendGrid Setup (Recommended)

SendGrid is already integrated! To enable email sending:

### 1. Create SendGrid Account
- Go to [sendgrid.com](https://sendgrid.com)
- Sign up for free account (100 emails/day free)
- Verify your account

### 2. Get API Key
- Login to SendGrid dashboard
- Go to Settings > API Keys
- Create new API key with "Mail Send" permissions
- Copy the API key (you already added this to Replit Secrets)

### 3. Verify Sender Email
- Go to Settings > Sender Authentication
- Verify a sender email address (your email)
- This is required by SendGrid

### 4. Add Email Addresses to Replit Secrets
Add these two secrets in your Replit project:

```
SENDER_EMAIL=your-verified-email@domain.com
RECIPIENT_EMAIL=your-email@domain.com
```

- `SENDER_EMAIL`: Must be verified in SendGrid
- `RECIPIENT_EMAIL`: Where you want to receive contact form messages

### 5. Test Email Functionality
Once configured, test by:
1. Submit contact form on your website
2. Check that you receive email notification
3. Verify message is saved in admin panel

## Option 2: Gmail SMTP (Alternative)

If you prefer Gmail instead of SendGrid, you can:

1. Remove SendGrid and use Flask-Mail with Gmail
2. Set these environment variables:
   - `MAIL_USERNAME`: your Gmail address
   - `MAIL_PASSWORD`: Gmail app password (not regular password)
   - `MAIL_DEFAULT_SENDER`: your Gmail address

## Testing

You can test the contact form functionality:

1. **Database Storage**: Always works - check `/admin` to see stored messages
2. **Email Sending**: Works once email configuration is complete

## Current Behavior

- ✅ All messages are saved to database
- ✅ Admin panel shows all messages
- 🔄 Email sending shows "Message saved!" until email is configured
- ✅ Once configured, shows "Thank you for your message!" and sends email

## Need Help?

The contact form is fully functional for collecting messages. Email notifications are optional but recommended for getting instant alerts when someone contacts you.