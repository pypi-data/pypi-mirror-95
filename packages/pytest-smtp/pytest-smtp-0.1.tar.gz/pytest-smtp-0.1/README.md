# pytest-smtp
A plugin for send email with pytest execution result once execution is completed

---

### How it works:

- Get execution details using  `pytest_terminal_summary()` hook
- Build html template
- Send's email for respective recipients

---

### How to use in project:

1. Install `pytest-smtp`

> Case 1: Using `setup.py` (clone repo and run command in root)
```
python setup.py install
```

> Case 2: Install from git (changes in master)
```
pip install git+https://github.com/txu2k8/pytest-smtp
```

2. Execute test's normally using options
Add SMTP_HOST, SMTP_USER,SMTP_PWD to ENV
```
export SMTP_HOST=<smtp-server>
export SMTP_USER=<your-email-user>
export SMTP_PWD=<your-password>
```
If you need smtp ssl or customize smtp port, add SMTP_PORT or SMTP_SSL to ENV
```
export SMTP_PORT=465
export SMTP_SSL=True
```
And run pytest with options `--send-email` and `--email-receivers=<email_addr>,<email_addr>`
```
pytest --send-email --email-to=a@gmail.com,b@hotmail.com
```

You can also config email receivers, subject, body and smtp info in pytest.ini
```
[pytest]
addopts = --send-email --html=report.html
email_to = a@126.com,b@outlook.com
email_subject = Pytest Report
email_attachments=test_a.py,report.html
```

Email options:
- --send-email: Send email when --send-email
- --email-to: Email receivers, comma-separated
- --smtp-host: SMTP host
- --smtp-port: SMTP port
- --smtp-user: SMTP user
- --smtp-pwd: SMTP password
- --smtp-ssl: Use smtp_ssl
- --email-subject: Email subject
- --email-body: Email content, support HTML
- --email-template: Email content template path
- --email-attachments: Email attachments, commn-separated

Email ini-options:

- --smtp_host: SMTP host
- --smtp_port: SMTP port
- --smtp_user: SMTP user
- --smtp_pwd: SMTP password
- --smtp_ssl: Use smtp_ssl
- --email_subject: Email subject
- --email_body: Email content, support HTML
- --email_to: Email receivers, comma-separated
- --email_template: Email content template path
- --email_attachments: Email attachments, commn-separated

> At least --send-email and --email-to or email_to are necessary
---

*Sample Report*

<img src="https://github.com/txu2k8/pytest-smtp/tree/main/docs/pytest_email.jpg" alt="pytest_email.jpg">

---

### What kind of information is shared?

Following test counts:
- Total
- Passed
- Failed
- Skipped
- Error
- XPassed
- XFailed
- Duration

Future: Failed test information

---

*Thanks for using pytest-smtp!*

If you have any questions / suggestions / comments on this, please feel free to reach me at

- Email: <a href="mailto:txu2008@outlook.com?Subject=Pytest-smtp%20Send%20Email" target="_blank">`txu2008@outlook.com`</a> 
- Blog: <a href="https://txu2008.github.io/" target="_blank">`txu2k8`</a>
- GitHub: <a href="https://github.com/txu2k8" target="_blank">`txu2k8`</a>

---
