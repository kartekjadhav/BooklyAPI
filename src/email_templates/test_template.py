def generate_template(username:str, message:str):
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Welcome to Bookly</title>
        </head>
        <body style="margin:0;padding:0;background-color:#0a0a0f;font-family:'Georgia',serif;">

        <!-- Outer wrapper -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0"
                style="background-color:#0a0a0f;padding:48px 16px;">
            <tr>
            <td align="center">

                <!-- Card -->
                <table width="600" cellpadding="0" cellspacing="0" border="0"
                    style="max-width:600px;width:100%;background-color:#0f0f1a;
                            border-radius:16px;overflow:hidden;
                            border:1px solid #1e1e3a;
                            box-shadow:0 0 80px rgba(99,71,255,0.15);">

                <!-- Top accent bar -->
                <tr>
                    <td style="height:4px;background:linear-gradient(90deg,#6347ff,#a78bfa,#38bdf8);"></td>
                </tr>

                <!-- Header -->
                <tr>
                    <td align="center" style="padding:52px 48px 36px;">
                    <!-- Logo mark -->
                    <div style="display:inline-block;background:linear-gradient(135deg,#6347ff,#38bdf8);
                                border-radius:14px;padding:14px 20px;margin-bottom:28px;">
                        <span style="font-size:26px;font-weight:bold;color:#fff;
                                    letter-spacing:3px;font-family:'Georgia',serif;">
                        BOOKLY
                        </span>
                    </div>

                    <!-- Divider dots -->
                    <div style="margin-bottom:28px;">
                        <span style="display:inline-block;width:5px;height:5px;border-radius:50%;
                                    background:#6347ff;margin:0 3px;"></span>
                        <span style="display:inline-block;width:5px;height:5px;border-radius:50%;
                                    background:#a78bfa;margin:0 3px;"></span>
                        <span style="display:inline-block;width:5px;height:5px;border-radius:50%;
                                    background:#38bdf8;margin:0 3px;"></span>
                    </div>

                    <h1 style="margin:0 0 12px;font-size:36px;font-weight:normal;
                                color:#f0eeff;letter-spacing:-0.5px;line-height:1.2;">
                        Hello, {username} 👋
                    </h1>
                    <p style="margin:0;font-size:16px;color:#7c6fa0;letter-spacing:0.3px;">
                        Your account is ready. Welcome aboard.
                    </p>
                    </td>
                </tr>

                <!-- Glowing divider -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;background:linear-gradient(90deg,
                        transparent,#6347ff55,#a78bfa88,#6347ff55,transparent);"></div>
                    </td>
                </tr>

                <!-- Main message body -->
                <tr>
                    <td style="padding:40px 48px;">
                    <p style="margin:0 0 20px;font-size:16px;line-height:1.8;color:#c4b8e8;">
                        { message }
                    </p>
                    <p style="margin:0 0 32px;font-size:15px;line-height:1.8;color:#7c6fa0;">
                        We're thrilled to have you here. Explore your library, track your reads,
                        and discover your next favourite book — all in one place.
                    </p>

                    <!-- CTA Button -->
                    <table cellpadding="0" cellspacing="0" border="0">
                        <tr>
                        <td align="center"
                            style="background:linear-gradient(135deg,#6347ff,#a78bfa);
                                    border-radius:10px;padding:1px;">
                            <a href="#"
                            style="display:inline-block;padding:14px 36px;
                                    background:#0f0f1a;border-radius:9px;
                                    color:#a78bfa;font-size:15px;
                                    text-decoration:none;letter-spacing:1px;
                                    font-family:'Georgia',serif;">
                            Open Your Library →
                            </a>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- Stats strip -->
                <tr>
                    <td style="padding:0 48px 40px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0"
                            style="background:#13132a;border-radius:12px;
                                    border:1px solid #1e1e3a;overflow:hidden;">
                        <tr>
                        <!-- Stat 1 -->
                        <td align="center" style="padding:24px 16px;
                            border-right:1px solid #1e1e3a;">
                            <div style="font-size:28px;font-weight:bold;
                                        color:#a78bfa;margin-bottom:4px;">10K+</div>
                            <div style="font-size:12px;color:#5a5480;
                                        letter-spacing:1px;text-transform:uppercase;">Books</div>
                        </td>
                        <!-- Stat 2 -->
                        <td align="center" style="padding:24px 16px;
                            border-right:1px solid #1e1e3a;">
                            <div style="font-size:28px;font-weight:bold;
                                        color:#38bdf8;margin-bottom:4px;">500+</div>
                            <div style="font-size:12px;color:#5a5480;
                                        letter-spacing:1px;text-transform:uppercase;">Authors</div>
                        </td>
                        <!-- Stat 3 -->
                        <td align="center" style="padding:24px 16px;">
                            <div style="font-size:28px;font-weight:bold;
                                        color:#6347ff;margin-bottom:4px;">50K+</div>
                            <div style="font-size:12px;color:#5a5480;
                                        letter-spacing:1px;text-transform:uppercase;">Readers</div>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <!-- Bottom accent -->
                <tr>
                    <td style="padding:0 48px;">
                    <div style="height:1px;background:linear-gradient(90deg,
                        transparent,#1e1e3a,transparent);"></div>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td align="center" style="padding:32px 48px 40px;">
                    <p style="margin:0 0 8px;font-size:13px;color:#3d3560;">
                        You're receiving this because you signed up at Bookly.
                    </p>
                    <p style="margin:0;font-size:13px;color:#3d3560;">
                        <a href="#" style="color:#6347ff;text-decoration:none;">Unsubscribe</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#6347ff;text-decoration:none;">Privacy Policy</a>
                        &nbsp;·&nbsp;
                        <a href="#" style="color:#6347ff;text-decoration:none;">Help</a>
                    </p>
                    <p style="margin:16px 0 0;font-size:11px;color:#2a2545;letter-spacing:2px;
                                text-transform:uppercase;">
                        © 2026 Bookly · Made with ♥
                    </p>
                    </td>
                </tr>

                <!-- Bottom accent bar -->
                <tr>
                    <td style="height:4px;background:linear-gradient(90deg,#38bdf8,#a78bfa,#6347ff);"></td>
                </tr>

                </table>
                <!-- /Card -->

            </td>
            </tr>
        </table>

        </body>
        </html>
    """