// Vercel Edge Cron Trigger: Dispatches GitHub Actions Workflows with 0-jitter precision
// Bypasses GitHub's flaky internal cron queue and requires zero GCP billing accounts.

const GH_REPO = process.env.GITHUB_REPO || 'alexkingston1993/the-bull-print';
const GH_TOKEN = process.env.GITHUB_PAT_TOKEN || process.env.GITHUB_TOKEN || '';

module.exports = async function handler(req, res) {
  // Verify Cron caller or authorized request
  const authHeader = req.headers['authorization'];
  const cronSecret = process.env.CRON_SECRET;
  
  if (cronSecret && authHeader !== `Bearer ${cronSecret}` && req.headers['x-admin-key'] !== process.env.ADMIN_DASHBOARD_PASS) {
    // If CRON_SECRET is configured, enforce security
    return res.status(401).json({ error: 'Unauthorized cron dispatch request.' });
  }

  const { workflow = 'daily_longtail_seo.yml', ref = 'main' } = req.query;

  if (!GH_TOKEN) {
    return res.status(500).json({ error: 'Missing GITHUB_TOKEN or GITHUB_PAT_TOKEN in environment.' });
  }

  const url = `https://api.github.com/repos/${GH_REPO}/actions/workflows/${workflow}/dispatches`;

  try {
    const dispatchRes = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${GH_TOKEN}`,
        Accept: 'application/vnd.github.v3+json',
        'User-Agent': 'TheBullPrint-EdgeCron/1.0',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ref }),
    });

    if (dispatchRes.status === 204) {
      console.log(`[+] Successfully triggered ${workflow} via Edge Cron.`);
      return res.status(200).json({
        success: true,
        workflow,
        ref,
        timestamp: new Date().toISOString(),
        message: 'Dispatched to GitHub Actions with 0-jitter precision.'
      });
    } else {
      const errBody = await dispatchRes.text();
      console.error(`[-] Failed to dispatch ${workflow}:`, dispatchRes.status, errBody);
      return res.status(dispatchRes.status).json({
        error: `GitHub API error: ${dispatchRes.status}`,
        details: errBody
      });
    }
  } catch (err) {
    console.error('Edge cron error:', err);
    return res.status(500).json({ error: 'Internal edge cron error: ' + err.message });
  }
};
