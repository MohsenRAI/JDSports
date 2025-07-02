# Security Setup Guide

## Environment Variables

This project uses environment variables to securely store sensitive information like API keys. **Never commit API keys directly to your code.**

### Local Development Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file and add your actual API keys:**
   ```bash
   # Edit .env file
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

3. **The `.env` file is automatically ignored by git** (see `.gitignore`) so your keys won't be committed.

### Production Deployment (Vercel)

For production deployment on Vercel:

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following environment variables:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** Your actual OpenAI API key
   - **Environment:** Production (and Preview if needed)
   - **Name:** `FLASK_ENV`
   - **Value:** `production`
   - **Environment:** Production

### Other Deployment Platforms

For other platforms, set the environment variable according to their documentation:

- **Heroku:** Use `heroku config:set OPENAI_API_KEY=your_key FLASK_ENV=production`
- **Railway:** Add in the Variables section
- **Netlify:** Add in Site settings → Environment variables
- **AWS/GCP/Azure:** Use their respective secret management services

## Security Features Implemented

### 🔒 **API Key Security**
- Environment variables instead of hardcoded keys
- Automatic error if API key is missing
- Separate keys for development and production

### 🛡️ **Input Validation**
- File type validation (only image formats allowed)
- File size limits (10MB maximum)
- MIME type verification
- Path traversal protection
- Filename sanitization

### 🚫 **Production Security**
- Debug mode disabled in production
- Secure host binding (127.0.0.1 in production)
- Error message sanitization (no internal details exposed)
- Request timeouts to prevent hanging connections

### 🌐 **CORS Security**
- Specific origin allowlist
- Credentials disabled for security
- Limited headers and methods

### 📁 **File Security**
- Directory traversal prevention
- Path validation within allowed directories
- File extension and MIME type checking
- Empty file rejection

### Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore` for a reason
2. **Use different API keys** for development and production
3. **Rotate API keys regularly**
4. **Monitor API usage** to detect unauthorized access
5. **Use environment-specific keys** (dev, staging, prod)
6. **Keep dependencies updated** - Run `npm audit` and `pip check` regularly
7. **Use HTTPS in production** - Never use HTTP for sensitive data
8. **Implement rate limiting** - Prevent abuse of your APIs
9. **Log security events** - Monitor for suspicious activity
10. **Regular security audits** - Review code and dependencies

### Troubleshooting

If you get an error like "OPENAI_API_KEY environment variable is required":

1. Make sure you have a `.env` file in the `gazman-product-page` directory
2. Check that the file contains `OPENAI_API_KEY=your_key_here`
3. Restart your development server after adding the environment variable
4. For production, ensure the environment variable is set in your deployment platform

### Getting OpenAI API Keys

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key immediately (you won't be able to see it again)
5. Add it to your `.env` file or deployment platform

## Security Monitoring

### What to Monitor
- Unusual API usage patterns
- Failed authentication attempts
- Large file uploads
- Suspicious file types
- Error rate spikes
- Response time anomalies

### Recommended Tools
- **OpenAI Usage Dashboard** - Monitor API costs and usage
- **Vercel Analytics** - Track application performance
- **Sentry** - Error tracking and monitoring
- **LogRocket** - Session replay and debugging

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do NOT** create a public GitHub issue
2. Email security concerns privately
3. Include detailed steps to reproduce
4. Allow time for fixes before public disclosure

## Security Checklist

- [ ] API keys stored in environment variables
- [ ] `.env` files in `.gitignore`
- [ ] Debug mode disabled in production
- [ ] Input validation implemented
- [ ] File upload restrictions in place
- [ ] CORS properly configured
- [ ] Error messages sanitized
- [ ] Dependencies regularly updated
- [ ] HTTPS used in production
- [ ] Security headers implemented 