/**
 * Cloudflare Edge Notes App
 * Showcases: Workers Builds + D1
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Initialize D1 database
      if (path === '/api/init') {
        await env.DB.exec(`
          CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        `);
        return jsonResponse({ message: 'Database initialized' }, corsHeaders);
      }

      // List notes
      if (path === '/api/notes' && request.method === 'GET') {
        const { results } = await env.DB.prepare(
          'SELECT * FROM notes ORDER BY updated_at DESC'
        ).all();
        return jsonResponse(results, corsHeaders);
      }

      // Create note
      if (path === '/api/notes' && request.method === 'POST') {
        const { title, content } = await request.json();
        const { success, meta } = await env.DB.prepare(
          'INSERT INTO notes (title, content) VALUES (?, ?)'
        ).bind(title, content).run();

        return jsonResponse({
          id: meta.last_row_id,
          title,
          content,
          message: 'Note created'
        }, corsHeaders);
      }

      // Get single note
      if (path.startsWith('/api/notes/') && request.method === 'GET') {
        const id = path.split('/').pop();
        const note = await env.DB.prepare(
          'SELECT * FROM notes WHERE id = ?'
        ).bind(id).first();

        if (!note) {
          return jsonResponse({ error: 'Note not found' }, corsHeaders, 404);
        }
        return jsonResponse(note, corsHeaders);
      }

      // Update note
      if (path.startsWith('/api/notes/') && request.method === 'PUT') {
        const id = path.split('/').pop();
        const { title, content } = await request.json();

        await env.DB.prepare(
          'UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
        ).bind(title, content, id).run();

        return jsonResponse({ id, title, content, message: 'Note updated' }, corsHeaders);
      }

      // Delete note
      if (path.startsWith('/api/notes/') && request.method === 'DELETE') {
        const id = path.split('/').pop();
        await env.DB.prepare('DELETE FROM notes WHERE id = ?').bind(id).run();
        return jsonResponse({ message: 'Note deleted' }, corsHeaders);
      }

      // Serve HTML UI
      if (path === '/' || path === '/index.html') {
        return new Response(getHTML(), {
          headers: { 'Content-Type': 'text/html' }
        });
      }

      return jsonResponse({ error: 'Not found' }, corsHeaders, 404);

    } catch (error) {
      return jsonResponse({ error: error.message }, corsHeaders, 500);
    }
  }
};

function jsonResponse(data, corsHeaders, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders
    }
  });
}

function getHTML() {
  return `<!DOCTYPE html>
<html>
<head>
  <title>Edge Notes</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; }
    body { font-family: system-ui; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
    h1 { color: #f38020; }
    .note-form { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
    textarea { height: 100px; resize: vertical; }
    button { background: #f38020; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    button:hover { background: #e5721a; }
    .note { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .note h3 { margin: 0 0 10px 0; }
    .note p { color: #666; margin: 0; }
    .note-actions { margin-top: 10px; }
    .note-actions button { background: #666; margin-right: 5px; padding: 5px 10px; }
    .note-actions button.delete { background: #dc3545; }
    .badge { background: #f38020; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; }
  </style>
</head>
<body>
  <h1>Edge Notes <span class="badge">Cloudflare D1</span></h1>

  <div class="note-form">
    <input type="text" id="title" placeholder="Note title">
    <textarea id="content" placeholder="Note content..."></textarea>
    <button onclick="saveNote()">Save Note</button>
  </div>

  <div id="notes"></div>

  <script>
    async function loadNotes() {
      const res = await fetch('/api/notes');
      const notes = await res.json();
      document.getElementById('notes').innerHTML = notes.map(note => \`
        <div class="note">
          <h3>\${note.title}</h3>
          <p>\${note.content || 'No content'}</p>
          <small style="color: #999">Updated: \${new Date(note.updated_at).toLocaleString()}</small>
          <div class="note-actions">
            <button onclick="deleteNote(\${note.id})" class="delete">Delete</button>
          </div>
        </div>
      \`).join('');
    }

    async function saveNote() {
      const title = document.getElementById('title').value;
      const content = document.getElementById('content').value;
      if (!title) return alert('Title required');

      await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content })
      });

      document.getElementById('title').value = '';
      document.getElementById('content').value = '';
      loadNotes();
    }

    async function deleteNote(id) {
      if (!confirm('Delete this note?')) return;
      await fetch(\`/api/notes/\${id}\`, { method: 'DELETE' });
      loadNotes();
    }

    // Initialize DB and load notes
    fetch('/api/init').then(() => loadNotes());
  </script>
</body>
</html>`;
}
