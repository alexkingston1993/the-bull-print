export default function handler(req, res) {
  const { code, state, error, error_description } = req.query;

  if (error) {
    return res.status(400).send(`
      <!DOCTYPE html>
      <html>
        <head><title>TikTok Authorization Failed</title></head>
        <body style="background:#090D14;color:#EF4444;font-family:sans-serif;padding:40px;text-align:center;">
          <h2>Authorization Failed</h2>
          <p>${error_description || error}</p>
        </body>
      </html>
    `);
  }

  return res.status(200).send(`
    <!DOCTYPE html>
    <html>
      <head><title>The Bull Print // TikTok Authorized</title></head>
      <body style="background:#090D14;color:#F8FAFC;font-family:sans-serif;padding:40px;text-align:center;">
        <h2 style="color:#10B981;">✓ TikTok Creator Account Connected!</h2>
        <p style="color:#94A3B8;">Authorization code received. The Bull Print Automator is now ready to publish.</p>
        <div style="background:#111827;border:1px solid #1F2937;border-radius:8px;display:inline-block;padding:12px 20px;margin-top:20px;font-family:monospace;color:#38BDF8;">
          auth_code: ${code ? code.slice(0, 16) + '...' : 'none'}
        </div>
      </body>
    </html>
  `);
}
