# 📧 Gmail SMTP Setup Guide - Quick Start

## 🎯 Goal
Enable HR Agent to send real emails to candidates with test results and login credentials.

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Enable 2-Step Verification (1 min)

1. Open: https://myaccount.google.com/security
2. Scroll to "How you sign in to Google"
3. Click **2-Step Verification**
4. Click **Get Started**
5. Follow prompts (verify phone, etc.)

### Step 2: Generate App Password (2 min)

1. Still in Google Account > Security
2. Click **2-Step Verification** again
3. Scroll down to **App passwords**
4. Click **App passwords**
5. Select app: **Mail**
6. Select device: **Other (Custom name)**
7. Type: `HR Agent`
8. Click **GENERATE**
9. **COPY** the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update .env File (1 min)

Open `.env` file in the HR_Agent folder and update:

```env
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=abcdefghijklmnop
```

**Example:**
```env
SENDER_EMAIL=john.work@gmail.com
SENDER_PASSWORD=xyzi wqpo lkjh mnbv
```

### Step 4: Restart Application (1 min)

```powershell
# Stop the current app (Ctrl+C in terminal)
# Start again:
& '.\.venv\Scripts\python.exe' -m streamlit run app.py
```

---

## ✅ Test Your Setup

1. Go to **Candidate Portal**
2. Upload a resume
3. Take the test (if accepted)
4. Pass the test (60%+ score)
5. Check your email inbox!

---

## 🔍 Troubleshooting

### Error: "Authentication failed"
❌ **Problem:** Wrong password
✅ **Solution:** Use the 16-character App Password, not your Gmail password

### Error: "SMTP AUTH extension not supported"
❌ **Problem:** 2-Step Verification not enabled
✅ **Solution:** Enable 2-Step Verification first, then generate App Password

### Error: "Email credentials not configured"
❌ **Problem:** .env file not updated
✅ **Solution:** Add SENDER_EMAIL and SENDER_PASSWORD to .env file

---

## 🔐 Security Notes

⚠️ **NEVER share your App Password**
⚠️ **NEVER commit .env file to Git**
⚠️ **Use a work/test Gmail account, not personal**

---

## 📝 Without Email Setup

The app works without email configuration!

- Test results still display on screen
- Credentials shown immediately after passing
- Email content is generated but not sent
- Warning message appears: "Email credentials not configured"

You can copy the email content manually and send it yourself.

---

## 🎓 What Happens When Configured?

### Candidate Passes Test:
✉️ **Email sent automatically** to candidate's Gmail
📋 **Subject:** "Congratulations! You've been selected for [Position]"
📄 **Content:** LLM-generated professional email with credentials

### Candidate Fails Test:
✉️ **Email sent automatically** to candidate's Gmail
📋 **Subject:** "Test Results for [Position] Position"
📄 **Content:** Professional thank you message with encouragement

---

## 🚀 Ready to Go!

Once configured, emails are sent automatically:
- ✅ Professional LLM-generated content
- ✅ Personalized with candidate name and score
- ✅ Includes credentials for passed candidates
- ✅ Logged in audit system

**No manual intervention needed!** 🎉

---

## 📞 Need Help?

If emails still don't work:

1. **Check Gmail account**:
   - 2-Step Verification enabled? ✓
   - App Password generated? ✓
   - Copied correctly to .env? ✓

2. **Check .env file**:
   ```env
   SENDER_EMAIL=correct-email@gmail.com  # Your Gmail
   SENDER_PASSWORD=16-char-app-password  # No spaces
   SMTP_SERVER=smtp.gmail.com            # Default
   SMTP_PORT=587                         # Default
   ```

3. **Restart the app** after changing .env

4. **Test with a simple test**:
   - Apply with a test resume
   - Take and pass the test
   - Check spam folder if email not in inbox

---

## ⏱️ Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Enable 2-Step Verification | 1 min |
| 2 | Generate App Password | 2 min |
| 3 | Update .env file | 1 min |
| 4 | Restart app | 1 min |
| **Total** | **Complete Setup** | **~5 min** |

---

Happy automating! 🤖✨
