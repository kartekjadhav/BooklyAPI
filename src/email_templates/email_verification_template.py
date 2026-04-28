def generate_email_verification_template(username:str, verification_link:str):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Verify Your Email – Bookly</title>
        </head>
        <body style="margin:0;padding:0;background-color:#f5f3ff;font-family:'Georgia',serif;">

        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                style="background-color:#f5f3ff;padding:48px 16px;">
            <tr>
            <td align="center">

                <!-- Card -->
                <table width="580" cellpadding="0" cellspacing="0" border="0"
                    style="max-width:580px;width:100%;background:#ffffff;
                            border-radius:20px;overflow:hidden;
                            box-shadow:0 8px 48px rgba(99,71,255,0.12);
                            border:1px solid #ede9fe;">

                <!-- Top bar -->
                <tr>
                    <td style="height:5px;background:linear-gradient(90deg,#6347ff,#a78bfa,#38bdf8);"></td>
                </tr>

                <!-- Hero section -->
                <tr>
                    <td align="center"
                        style="background:linear-gradient(160deg,#1e1040 0%,#0f0f1a 100%);
                            padding:52px 48px 44px;">

                    <!-- Shield icon -->
                    <div style="width:72px;height:72px;margin:0 auto 24px;
                                background:linear-gradient(135deg,#6347ff22,#a78bfa22);
                                border:2px solid #6347ff55;border-radius:20px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:36px;line-height:72px;text-align:center;">
                        🔐
                    </div>

                    <h1 style="margin:0 0 10px;font-size:32px;font-weight:normal;
                                color:#f0eeff;letter-spacing:-0.5px;line-height:1.2;">
                        Verify Your Email
                    </h1>
                    <p style="margin:0;font-size:15px;color:#7c6fa0;line-height:1.6;">
                        One click and you're all set, <strong style="color:#a78bfa;">{ username }</strong>
                    </p>
                    </td>
                </tr>

                <!-- Body -->
                <tr>
                    <td style="padding:44px 48px 36px;">

                    <p style="margin:0 0 16px;font-size:16px;color:#3d3560;line-height:1.8;">
                        Thanks for signing up for <strong>Bookly</strong>. Please verify your
                        email address so we know it's really you.
                    </p>

                    <p style="margin:0 0 36px;font-size:15px;color:#7c6fa0;line-height:1.8;">
                        This link will expire in <strong style="color:#6347ff;">3 hour.</strong>
                        If you didn't create an account, you can safely ignore this email.
                    </p>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                        <tr>
                        <td align="center">
                            <a href="{ verification_link }"
                            style="display:inline-block;padding:16px 48px;
                                    background:linear-gradient(135deg,#6347ff,#a78bfa);
                                    color:#ffffff;font-size:16px;font-weight:bold;
                                    text-decoration:none;border-radius:12px;
                                    letter-spacing:0.5px;font-family:'Georgia',serif;
                                    box-shadow:0 4px 24px rgba(99,71,255,0.35);">
                            ✓ &nbsp; Verify My Email
                            </a>
                        </td>
                        </tr>
                    </table>

                    </td>
                </tr>

                <!-- Divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;background:linear-gradient(90deg,
                        transparent,#ede9fe,transparent);"></div>
                    </td>
                </tr>

                <!-- Link fallback -->
                <tr>
                    <td style="padding:28px 48px;">
                    <p style="margin:0 0 10px;font-size:13px;color:#9ca3af;">
                        Button not working? Copy and paste this link into your browser:
                    </p>
                    <p style="margin:0;font-size:12px;color:#6347ff;
                                word-break:break-all;line-height:1.6;">
                        {{ verification_link }}
                    </p>
                    </td>
                </tr>

                <!-- Divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;background:linear-gradient(90deg,
                        transparent,#ede9fe,transparent);"></div>
                    </td>
                </tr>

                <!-- Warning box -->
                <tr>
                    <td style="padding:28px 48px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                            style="background:#fff8f0;border-radius:10px;
                                    border-left:4px solid #f59e0b;overflow:hidden;">
                        <tr>
                        <td style="padding:16px 20px;">
                            <p style="margin:0;font-size:13px;color:#92400e;line-height:1.7;">
                            ⚠️ &nbsp;<strong>Never share this link</strong> with anyone.
                            Bookly will never ask for your verification link via chat or phone.
                            </p>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td align="center" style="padding:16px 48px 36px;">
                    <p style="margin:0 0 8px;font-size:13px;color:#c4b5fd;">
                        © 2026 Bookly · All rights reserved
                    </p>
                    <p style="margin:0;font-size:13px;color:#d1d5db;">
                        <a href="#" style="color:#a78bfa;text-decoration:none;">Unsubscribe</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#a78bfa;text-decoration:none;">Privacy Policy</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#a78bfa;text-decoration:none;">Help</a>
                    </p>
                    </td>
                </tr>

                <!-- Bottom bar -->
                <tr>
                    <td style="height:5px;background:linear-gradient(90deg,#38bdf8,#a78bfa,#6347ff);"></td>
                </tr>

                </table>
                <!-- /Card -->

            </td>
            </tr>
        </table>

        </body>
        </html>
    """