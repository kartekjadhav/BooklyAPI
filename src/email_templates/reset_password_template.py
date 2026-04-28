def generate_reset_password_template(reset_link: str):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Reset Your Password – Bookly</title>
        </head>
        <body style="margin:0;padding:0;background-color:#0d0d1a;font-family:'Georgia',serif;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                style="background-color:#0d0d1a;padding:48px 16px;">
            <tr>
            <td align="center">

                <!-- Card -->
                <table width="560" cellpadding="0" cellspacing="0" border="0"
                    style="max-width:560px;width:100%;background:#0f0f1f;
                            border-radius:20px;overflow:hidden;
                            border:1px solid #1e1e3a;
                            box-shadow:0 0 80px rgba(239,68,68,0.08),
                                        0 0 40px rgba(99,71,255,0.08);">

                <!-- Top accent bar -->
                <tr>
                    <td style="height:5px;
                            background:linear-gradient(90deg,#ef4444,#f97316,#eab308);"></td>
                </tr>

                <!-- Header -->
                <tr>
                    <td align="center"
                        style="padding:52px 48px 40px;
                            background:linear-gradient(180deg,#1a0a0a 0%,#0f0f1f 100%);">

                    <!-- Icon circle -->
                    <div style="width:80px;height:80px;margin:0 auto 28px;
                                border-radius:50%;
                                background:linear-gradient(135deg,#ef444422,#f9731622);
                                border:2px solid #ef444455;
                                font-size:36px;line-height:80px;text-align:center;">
                        🔑
                    </div>

                    <h1 style="margin:0 0 12px;font-size:30px;font-weight:normal;
                                color:#fff1f0;letter-spacing:-0.5px;line-height:1.2;">
                        Password Reset Request
                    </h1>
                    <p style="margin:0;font-size:15px;color:#7c6fa0;line-height:1.6;">
                        Hey, we have received a request to reset your password.
                    </p>
                    </td>
                </tr>

                <!-- Divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;
                                background:linear-gradient(90deg,transparent,#ef444433,transparent);">
                    </div>
                    </td>
                </tr>

                <!-- Body -->
                <tr>
                    <td style="padding:40px 48px 36px;">
                    <p style="margin:0 0 12px;font-size:15px;color:#c4b8e8;line-height:1.8;">
                        Click the button below to reset your password.
                        This link is valid for only
                        <strong style="color:#f97316;">15 minutes.</strong>
                    </p>
                    <p style="margin:0 0 36px;font-size:14px;color:#5a5480;line-height:1.8;">
                        If you did not request a password reset, please ignore this email.
                        Your password will remain unchanged.
                    </p>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tr>
                        <td align="center">
                            <a href="{ reset_link }"
                            style="display:inline-block;padding:16px 52px;
                                    background:linear-gradient(135deg,#ef4444,#f97316);
                                    color:#ffffff;font-size:16px;font-weight:bold;
                                    text-decoration:none;border-radius:12px;
                                    letter-spacing:0.5px;font-family:'Georgia',serif;
                                    box-shadow:0 4px 24px rgba(239,68,68,0.35);">
                            🔒 &nbsp; Reset My Password
                            </a>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- Divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;
                                background:linear-gradient(90deg,transparent,#1e1e3a,transparent);">
                    </div>
                    </td>
                </tr>

                <!-- Link fallback -->
                <tr>
                    <td style="padding:28px 48px;">
                    <p style="margin:0 0 10px;font-size:13px;color:#5a5480;">
                        Button not working? Paste this link in your browser:
                    </p>
                    <p style="margin:0;font-size:12px;color:#ef4444;
                                word-break:break-all;line-height:1.7;">
                        { reset_link }
                    </p>
                    </td>
                </tr>

                <!-- Divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;
                                background:linear-gradient(90deg,transparent,#1e1e3a,transparent);">
                    </div>
                    </td>
                </tr>

                <!-- Warning box -->
                <tr>
                    <td style="padding:28px 48px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                            style="background:#1a0a0a;border-radius:10px;
                                    border-left:4px solid #ef4444;overflow:hidden;">
                        <tr>
                        <td style="padding:18px 20px;">
                            <p style="margin:0 0 6px;font-size:13px;
                                    color:#fca5a5;font-weight:bold;">
                            ⚠️ Didn't request this?
                            </p>
                            <p style="margin:0;font-size:13px;color:#7c6fa0;line-height:1.7;">
                            Someone may have entered your email by mistake.
                            Your account is safe — no changes have been made.
                            You can safely ignore this email.
                            </p>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td align="center" style="padding:16px 48px 36px;">
                    <p style="margin:0 0 8px;font-size:13px;color:#3d3560;">
                        © 2026 Bookly · All rights reserved
                    </p>
                    <p style="margin:0;font-size:13px;">
                        <a href="#" style="color:#6347ff;text-decoration:none;">Unsubscribe</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#6347ff;text-decoration:none;">Privacy Policy</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#6347ff;text-decoration:none;">Help</a>
                    </p>
                    </td>
                </tr>

                <!-- Bottom accent bar -->
                <tr>
                    <td style="height:5px;
                            background:linear-gradient(90deg,#eab308,#f97316,#ef4444);">
                    </td>
                </tr>

                </table>
                <!-- /Card -->

            </td>
            </tr>
        </table>

        </body>
        </html>
    """