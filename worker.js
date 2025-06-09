export default {
  async fetch(request) {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get('url');
    if (!url) {
      return new Response(JSON.stringify({ error: 'Missing url parameter' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
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
