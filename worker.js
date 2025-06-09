export default {
  async fetch(request) {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get('url');
    if (!url) {
      const html = `<!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <title>TikTok Downloader</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 2rem; }
            #status { color: red; margin-top: 1rem; }
          </style>
        </head>
        <body>
          <h1>TikTok Downloader</h1>
          <input type="text" id="url" size="50" placeholder="Enter TikTok link" />
          <button id="download">Get Download Link</button>
          <p id="status"></p>
          <script>
            const btn = document.getElementById('download');
            const status = document.getElementById('status');
            btn.addEventListener('click', async () => {
              const link = document.getElementById('url').value.trim();
              if (!link) {
                status.textContent = 'Please enter a TikTok link';
                return;
              }
              status.textContent = 'Fetching...';
              try {
                const res = await fetch('?url=' + encodeURIComponent(link));
                const data = await res.json();
                if (data.download) {
                  window.location = data.download;
                } else {
                  status.textContent = data.error || 'Unexpected response';
                }
              } catch (err) {
                status.textContent = err.message;
              }
            });
          </script>
        </body>
      </html>`;
      return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' },
      });
    }
    try {
      const apiUrl = 'https://tikwm.com/api/?url=' + encodeURIComponent(url);
      const apiRes = await fetch(apiUrl);
      if (!apiRes.ok) {
        throw new Error('API request failed');
      }
      const data = await apiRes.json();
      if (data.code !== 0) {
        throw new Error(data.msg || 'API returned error');
      }
      const downloadUrl = data.data && data.data.play;
      if (!downloadUrl) {
        throw new Error('Download URL not found');
      }
      return new Response(JSON.stringify({ download: downloadUrl }), {
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }
  },
};
