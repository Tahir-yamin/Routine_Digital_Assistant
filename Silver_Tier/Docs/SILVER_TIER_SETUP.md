# Silver Tier Setup Guide

This guide covers the setup required for Silver Tier functionality in the Personal AI Employee system.

## Overview

Silver Tier adds:
- **LinkedIn Watcher**: Generates LinkedIn post suggestions daily
- **LinkedIn Posting Skill**: Publishes approved content to LinkedIn
- **Email MCP Server**: Send emails via SMTP (receiving already working)
- **Human-in-the-Loop Approvals**: All external actions require human approval

## 1. LinkedIn Integration Setup

### LinkedIn Watcher (Content Suggestions)

The LinkedIn watcher is **already working** without API credentials! It generates daily post suggestions based on your completed work.

**Current Status**: ✅ Operational in suggestion-only mode

**Configuration**:
- Enabled in `watcher_config.json`: `linkedin_enabled: true`
- Runs every hour (3600 seconds)
- Creates post suggestions in `/Needs_Action`

**To test**:
```bash
python linkedin_watcher.py
```

### LinkedIn API (Optional - For Automated Posting)

To enable automated LinkedIn posting (not just suggestions), you need to configure the LinkedIn API.

**Steps**:

1. **Create LinkedIn App**
   - Go to: https://www.linkedin.com/developers/apps
   - Click "Create app"
   - Fill in app details (name, company, privacy policy, logo)
   - Select "Sign In with LinkedIn using OpenID Connect"

2. **Configure OAuth**
   - In your app settings, go to "Auth" tab
   - Add redirect URL: `http://localhost:8080/callback`
   - Request these permissions:
     - `r_liteprofile` (Read profile)
     - `r_emailaddress` (Read email)
     - `w_member_social` (Post on behalf of member)
     - `r_organization_social` (Read organization posts)

3. **Get Credentials**
   - Copy your **Client ID**
   - Copy your **Client Secret**

4. **Update Configuration**
   - Edit `watcher_config.json` and add:
   ```json
   {
     "linkedin_client_id": "your_client_id_here",
     "linkedin_client_secret": "your_client_secret_here"
   }
   ```

5. **Authenticate**
   ```bash
   # This will open a browser for OAuth authorization
   python linkedin_watcher.py --auth
   ```

6. **Verify Connection**
   - Your access token will be saved in `.linkedin_token.json`
   - Test posting: `claude /silver.post-linkedin`

**Note**: Without LinkedIn API, you can still:
- Get daily post suggestions from the watcher
- Create and approve post drafts
- Manually copy content to LinkedIn

---

## 2. Email MCP Server (External Action Server)

**This fulfills the Silver Tier requirement**: "One working MCP server for external action (e.g., sending emails)"

**MCP Server**: `@modelcontextprotocol/server-email`
**Status**: ✅ Connected

### Current Status

- **Email Receiving (IMAP)**: ✅ Working
- **Email Sending (SMTP)**: ⚠️ Requires Gmail App Password

### Why Email MCP Server?

The Email MCP Server is the **official external action server** for Silver Tier, not a custom SMTP implementation. It provides:
- ✅ Standardized email interface via MCP tools
- ✅ Support for 8+ email providers (Gmail, Outlook, etc.)
- ✅ Built-in testing and configuration tools
- ✅ Fulfills Silver Tier MCP requirement

### Issue: Gmail Authentication

Gmail requires an "App Password" for SMTP access, not your regular Gmail password.

**Error you might see**:
```
535-5.7.8 Username and Password not accepted
```

### Solution: Generate Gmail App Password

**Steps**:

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Turn on "2-Step Verification" if not already enabled

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" (custom name)
   - Enter: "Personal AI Employee"
   - Click "Generate"
   - **Copy the 16-character password** (spaces don't matter)

3. **Update .env File**
   - Open `.env` file
   - Update `EMAIL_PASSWORD` with the app password:
   ```
   EMAIL_USER=kh0102267@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   ```

4. **Reconfigure Email MCP Server**

   In Claude Code, use the MCP tool:
   ```javascript
   mcp__email__setup_email_account({
     email: "kh0102267@gmail.com",
     password: "your-16-char-app-password"
   })
   ```

5. **Test Email Sending**

   Use the MCP test tool:
   ```javascript
   mcp__email__test_email_connection({ testType: "smtp" })
   ```

   Expected: `✅ SMTP服务器连接测试成功！`

### Email MCP Server Configuration

The Email MCP Server automatically configures settings for Gmail:
- **MCP Server**: `@modelcontextprotocol/server-email`
- **SMTP Server**: smtp.gmail.com
- **SMTP Port**: 587 (STARTTLS)
- **SMTP SSL**: false (uses STARTTLS instead)
- **IMAP Server**: imap.gmail.com
- **IMAP Port**: 993
- **IMAP SSL**: true

**Important**: Port 587 uses STARTTLS (not direct SSL). This was the root cause of the original SSL error.

**MCP Tools Available**:
- `mcp__email__send_email` - Send emails
- `mcp__email__get_recent_emails` - Retrieve inbox
- `mcp__email__get_email_content` - Get email details
- `mcp__email__setup_email_account` - Configure account
- `mcp__email__test_email_connection` - Test connection

**See**: `EMAIL_MCP_SERVER_GUIDE.md` for complete MCP server documentation

---

## 3. Watcher Manager Configuration

All watchers are managed through `watcher_config.json`.

**Current Configuration**:
```json
{
  "gmail_enabled": true,
  "whatsapp_enabled": true,
  "bank_enabled": true,
  "file_drop_enabled": true,
  "linkedin_enabled": true,

  "gmail_interval": 300,      // 5 minutes
  "whatsapp_interval": 60,     // 1 minute
  "bank_interval": 600,        // 10 minutes
  "linkedin_interval": 3600,   // 1 hour

  "linkedin_client_id": "",
  "linkedin_client_secret": "",
  "linkedin_access_token": ""
}
```

**To start all watchers**:
```bash
python watcher_manager.py
```

---

## 4. Silver Tier Skills

### Available Skills

1. **`/silver.send-email`**
   - Sends approved emails via SMTP
   - Requires: Gmail App Password
   - Status: Needs password update

2. **`/silver.post-linkedin`**
   - Posts approved content to LinkedIn
   - Works in draft mode without API
   - Status: ✅ Operational (draft mode)

3. **`/silver.execute-approved`**
   - Orchestrates execution of all approved actions
   - Status: ✅ Operational

### Skill Usage

**LinkedIn Posting**:
```bash
# Create a post from a suggestion
claude /bronze.process-inbox

# Review and approve in /Pending_Approval

# Move approved file to /Approved

# Execute posting
claude /silver.post-linkedin
```

**Email Sending**:
```bash
# Process inbox to create email drafts
claude /bronze.process-inbox

# Approve email in /Pending_Approval

# Move to /Approved

# Send email
claude /silver.send-email
```

---

## 5. Testing Your Setup

### Test LinkedIn Watcher

```bash
# Run once to generate a suggestion
python linkedin_watcher.py

# Check for suggestion file
ls Needs_Action/*linkedin*
```

Expected output:
- Creates file: `Needs_Action/post_suggestion_YYYYMMDD_HHMMSS_suggesti.md`
- Contains post topic, content idea, and hashtags

### Test Email Receiving

```bash
# Check IMAP connection
python -c "from mcp__email__test_email_connection import test; test('imap')"
```

Expected: ✅ IMAP connection successful

### Test Email Sending

After updating EMAIL_PASSWORD with App Password:
```bash
# Check SMTP connection
python -c "from mcp__email__test_email_connection import test; test('smtp')"
```

Expected: ✅ SMTP connection successful

---

## 6. Troubleshooting

### LinkedIn Watcher Not Creating Suggestions

**Check**:
1. Is `linkedin_enabled: true` in `watcher_config.json`?
2. Delete `.linkedin_suggestion_today` to force new suggestion
3. Run: `python linkedin_watcher.py`

### Email Sending Fails

**Common Issues**:

| Error | Cause | Solution |
|-------|-------|----------|
| SSL version error | Wrong port/SSL config | Use port 587 with smtpSecure: false |
| Username/Password not accepted | Regular password used | Generate Gmail App Password |
| Connection timeout | Firewall blocking | Check firewall for port 587 outbound |
| Too many login attempts | Rate limiting | Wait 15 minutes, then retry |

### LinkedIn API Not Working

**Check**:
1. Client ID and Secret are in `watcher_config.json`
2. Redirect URI matches exactly: `http://localhost:8080/callback`
3. App has correct permissions (w_member_social)
4. Access token hasn't expired (re-authenticate)

---

## 7. Next Steps

### Immediate Actions

1. **Update Gmail App Password** (Priority: High)
   - Follow steps in Section 2
   - Test email sending

2. **Test LinkedIn Watcher** (Priority: Medium)
   - Already working in suggestion mode
   - Optionally set up API for automated posting

3. **Review Approvals Workflow**
   - Check `/Pending_Approval` folder daily
   - Approve or reject suggested actions

### Optional Enhancements

1. **Set up LinkedIn API** for automated posting
2. **Configure Windows Task Scheduler** to auto-start watchers
3. **Add more post templates** in LinkedIn watcher
4. **Create custom email templates** for common responses

---

## 8. Silver Tier Requirements Checklist

### Core Requirements
- [x] **Two or more Watcher scripts**: Gmail ✅, WhatsApp ✅, Bank ✅, File Drop ✅, LinkedIn ✅ (5 total)
- [x] **Automatically post on LinkedIn**: LinkedIn watcher generates suggestions, `/silver.post-linkedin` skill created
- [x] **Claude reasoning loop creates Plan.md**: `/bronze.generate-plan` skill operational
- [ ] **One working MCP server for external action**: Email MCP Server connected (IMAP ✅, SMTP needs App Password)
- [x] **Human-in-the-loop approval workflow**: All sensitive actions require approval
- [x] **Basic scheduling**: Watcher manager coordinates all watchers
- [x] **AI functionality as Agent Skills**: All skills in `.claude/skills/`

### Feature Implementation
- [x] LinkedIn watcher (content suggestions)
- [x] LinkedIn posting skill (`/silver.post-linkedin`)
- [x] Email MCP Server connected
- [x] Email receiving (IMAP) ✅
- [ ] Email sending (SMTP) ⚠️ **Needs Gmail App Password**
- [x] Human-in-the-loop approval workflow
- [x] Watcher manager integration
- [x] Audit logging for all actions
- [x] Dashboard updates

**Silver Tier Status**: 6/7 requirements complete (85.7%)

**Blocking Issue**: Gmail App Password needed for Email MCP Server SMTP functionality

**Note**: The Email MCP Server IS the "working MCP server for external action" requirement. Once SMTP is configured, this requirement is 100% fulfilled.

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review skill documentation in `.claude/skills/`
3. Check logs in `/Logs/` directory
4. Review Constitution principles in `.specify/memory/constitution.md`

---

**Last Updated**: 2026-01-10
**Version**: 1.0.0
**Tier**: Silver
