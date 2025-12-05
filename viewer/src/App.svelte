<script>
  import { marked } from 'marked';
  import { onMount } from 'svelte';
  import Questionnaire from './Questionnaire.svelte';

  // App mode: 'docs' or 'questionnaire'
  let appMode = 'docs';

  // Configure marked to generate heading IDs for anchor links
  const renderer = new marked.Renderer();
  renderer.heading = function(text, level) {
    // Generate slug from heading text (GitHub-style)
    const slug = text.toLowerCase()
      .replace(/<[^>]*>/g, '')           // Remove HTML tags
      .replace(/[^\w\s-]/g, '')          // Remove special chars except hyphens
      .replace(/\s+/g, '-')              // Replace spaces with hyphens
      .replace(/--+/g, '-')              // Replace multiple hyphens with single
      .trim();
    return `<h${level} id="${slug}">${text}</h${level}>`;
  };
  marked.setOptions({ renderer });

  // File definitions with metadata
  let files = [
    // Ideas
    { id: 'sponsor_combinations', name: 'Tool Combinations (455 ideas)', path: 'sponsor_combinations_ideas.md', category: 'Ideas', icon: '🔗' },
    { id: 'local_ai_100', name: '100 Local AI Uses (4GB)', path: '100_local_ai_usecases_4gb.md', category: 'Ideas', icon: '💻' },
    { id: 'free_hackathon', name: 'Free Hackathon Ideas', path: 'free_hackathon_ideas.md', category: 'Ideas', icon: '💡' },
    { id: 'ics_combinations', name: 'ICS Tool Combinations', path: 'ics_combinations_ideas.md', category: 'Ideas', icon: '🏭' },
    { id: 'ar_combinations', name: 'AR Tool Combinations', path: 'ar_tools_combinations_ideas.md', category: 'Ideas', icon: '👓' },

    // Guides
    { id: 'local_ai_guide', name: 'Local AI Guide', path: 'local_ai_guide.md', category: 'Guides', icon: '🤖' },
    { id: 'free_tier', name: 'Free Tier Services', path: 'free_tier_services.md', category: 'Guides', icon: '🆓' },
    { id: 'hackathon_platforms', name: 'Hackathon Platforms', path: 'hackathon_platforms_guide.md', category: 'Guides', icon: '🏆' },
    { id: 'github_free_tools', name: 'GitHub Free Tools', path: 'github_free_tools_guide.md', category: 'Guides', icon: '🐙' },
    { id: 'ai_video_generation', name: 'AI Video Generation', path: 'ai_video_generation_guide.md', category: 'Guides', icon: '🎬' },

    // AI Agents
    { id: 'headless_ai_coders', name: 'Headless AI + GitHub Actions', path: 'headless_ai_coders_github_actions.md', category: 'AI Agents', icon: '⚡' },
    { id: 'autonomous_agents', name: 'Autonomous Coding Agents', path: 'autonomous_coding_agents.md', category: 'AI Agents', icon: '🤖' },

    // Resources
    { id: 'huggingface_gradio', name: 'HuggingFace & Gradio', path: 'huggingface_gradio_resources.md', category: 'Resources', icon: '🤗' },
    { id: 'hackathon_company', name: 'Company Resources', path: 'hackathon_company_resources.md', category: 'Resources', icon: '🏢' },
    { id: 'hackathon_project', name: 'Project Ideas', path: 'hackathon_project_ideas.md', category: 'Resources', icon: '💼' },

    // Reference
    { id: 'sponsor_matrix', name: 'Sponsor Matrix', path: 'sponsor_combinations_matrix.md', category: 'Reference', icon: '📊' },
    { id: 'template_merging', name: 'Template Merging', path: 'template_merging_guide.md', category: 'Reference', icon: '📝' },
    { id: 'sponsor_updates', name: 'Sponsor Updates', path: 'sponsor_updates_tracking.md', category: 'Reference', icon: '📋' },
  ];

  // Category order for display
  const categoryOrder = ['Ideas', 'Guides', 'AI Agents', 'Resources', 'Reference'];
  $: categories = categoryOrder.filter(cat => files.some(f => f.category === cat));

  let openPanels = [];
  let fileContents = {};
  let loading = {};
  let searchQuery = '';
  let sidebarCollapsed = false;
  let instanceCounter = 0;
  let refreshing = false;

  // Refresh file contents (clear cache and reload)
  async function refreshFiles() {
    refreshing = true;
    fileContents = {};
    // Reload any currently open panels
    for (const panel of openPanels) {
      await loadFile(panel);
    }
    refreshing = false;
  }

  // Load file content
  async function loadFile(file) {
    if (fileContents[file.id]) return;

    loading[file.id] = true;
    try {
      const response = await fetch(`./docs/${file.path}`);
      const text = await response.text();
      fileContents[file.id] = marked(text);
    } catch (error) {
      fileContents[file.id] = `<p style="color: var(--danger)">Error loading file: ${error.message}</p>`;
    }
    loading[file.id] = false;
  }

  // Open panel (allows multiple instances of same file)
  function openPanel(file) {
    instanceCounter++;
    const panelInstance = { ...file, instanceId: `${file.id}_${instanceCounter}` };
    openPanels = [...openPanels, panelInstance];
    loadFile(file);
  }

  // Close panel by instance ID
  function closePanel(instanceId) {
    openPanels = openPanels.filter(p => p.instanceId !== instanceId);
  }

  // Filter files by search
  $: filteredFiles = files.filter(f =>
    f.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Group files by category
  $: groupedFiles = categories.reduce((acc, cat) => {
    acc[cat] = filteredFiles.filter(f => f.category === cat);
    return acc;
  }, {});

  // Open all files (one instance each)
  function openAll() {
    files.forEach(file => {
      if (!openPanels.find(p => p.id === file.id)) {
        openPanel(file);
      }
    });
  }

  // Close all files
  function closeAll() {
    openPanels = [];
  }

  // Layout modes
  let layoutMode = 'grid'; // 'grid', 'columns', 'tabs'
</script>

<div class="app">
  <!-- Sidebar -->
  <aside class="sidebar" class:collapsed={sidebarCollapsed}>
    <div class="sidebar-header">
      <h1>{appMode === 'docs' ? '📚' : '💭'} Sponsor Prep</h1>
      <button class="collapse-btn" on:click={() => sidebarCollapsed = !sidebarCollapsed}>
        {sidebarCollapsed ? '→' : '←'}
      </button>
    </div>

    {#if !sidebarCollapsed}
      <div class="mode-toggle">
        <button class:active={appMode === 'docs'} on:click={() => appMode = 'docs'}>
          📚 Docs
        </button>
        <button class:active={appMode === 'questionnaire'} on:click={() => appMode = 'questionnaire'}>
          💭 100 Questions
        </button>
      </div>
    {/if}

    {#if !sidebarCollapsed && appMode === 'docs'}
      <div class="search-box">
        <input
          type="text"
          placeholder="Search files..."
          bind:value={searchQuery}
        />
      </div>

      <div class="sidebar-actions">
        <button on:click={openAll}>Open All</button>
        <button on:click={closeAll}>Close All</button>
        <button on:click={refreshFiles} class:refreshing disabled={refreshing}>
          {refreshing ? '...' : '↻'}
        </button>
      </div>

      <div class="layout-toggle">
        <button class:active={layoutMode === 'grid'} on:click={() => layoutMode = 'grid'}>Grid</button>
        <button class:active={layoutMode === 'columns'} on:click={() => layoutMode = 'columns'}>Columns</button>
        <button class:active={layoutMode === 'tabs'} on:click={() => layoutMode = 'tabs'}>Tabs</button>
      </div>

      <nav class="file-list">
        {#each categories as category}
          {#if groupedFiles[category]?.length > 0}
            <div class="category">
              <h3>{category}</h3>
              {#each groupedFiles[category] as file}
                <button
                  class="file-item"
                  class:active={openPanels.find(p => p.id === file.id)}
                  on:click={() => openPanel(file)}
                >
                  <span class="icon">{file.icon}</span>
                  <span class="name">{file.name}</span>
                </button>
              {/each}
            </div>
          {/if}
        {/each}
      </nav>

      <div class="sidebar-footer">
        <div class="stats">
          <span>{openPanels.length} / {files.length} open</span>
        </div>
      </div>
    {/if}

    {#if !sidebarCollapsed && appMode === 'questionnaire'}
      <div class="sidebar-info">
        <p>Answer questions to think through your hackathon project.</p>
        <p class="hint">Responses auto-save to browser storage.</p>
      </div>
    {/if}
  </aside>

  <!-- Main Content -->
  <main class="content">
    {#if appMode === 'questionnaire'}
      <Questionnaire />
    {:else if openPanels.length === 0}
      <div class="empty-state">
        <div class="empty-icon">📄</div>
        <h2>No files open</h2>
        <p>Select files from the sidebar to view them here</p>
        <button class="primary-btn" on:click={openAll}>Open All Files</button>
      </div>
    {:else if layoutMode === 'tabs'}
      <!-- Tabs Layout -->
      <div class="tabs-layout">
        <div class="tabs-header">
          {#each openPanels as panel (panel.instanceId)}
            <button
              class="tab"
              class:active={openPanels[0]?.instanceId === panel.instanceId}
              on:click={() => {
                openPanels = [panel, ...openPanels.filter(p => p.instanceId !== panel.instanceId)];
              }}
            >
              <span>{panel.icon} {panel.name}</span>
              <span class="close" on:click|stopPropagation={() => closePanel(panel.instanceId)}>×</span>
            </button>
          {/each}
        </div>
        <div class="tab-content">
          {#if openPanels[0]}
            {#if loading[openPanels[0].id]}
              <div class="loading">Loading...</div>
            {:else}
              <div class="markdown-content">
                {@html fileContents[openPanels[0].id] || ''}
              </div>
            {/if}
          {/if}
        </div>
      </div>
    {:else}
      <!-- Grid/Columns Layout -->
      <div class="panels-container" class:columns={layoutMode === 'columns'}>
        {#each openPanels as panel (panel.instanceId)}
          <div class="panel">
            <div class="panel-header">
              <span class="panel-title">{panel.icon} {panel.name}</span>
              <button class="close-btn" on:click={() => closePanel(panel.instanceId)}>×</button>
            </div>
            <div class="panel-content">
              {#if loading[panel.id]}
                <div class="loading">Loading...</div>
              {:else}
                <div class="markdown-content">
                  {@html fileContents[panel.id] || ''}
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </main>
</div>

<style>
  .app {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }

  /* Sidebar */
  .sidebar {
    width: 280px;
    min-width: 280px;
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    transition: all 0.2s ease;
  }

  .sidebar.collapsed {
    width: 50px;
    min-width: 50px;
  }

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
  }

  .sidebar-header h1 {
    font-size: 1.1rem;
    font-weight: 600;
    white-space: nowrap;
  }

  .collapsed .sidebar-header h1 {
    display: none;
  }

  .collapse-btn {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 1.2rem;
    padding: 0.25rem;
  }

  .mode-toggle {
    display: flex;
    padding: 0.5rem 0.75rem;
    gap: 0.25rem;
    border-bottom: 1px solid var(--border-color);
  }

  .mode-toggle button {
    flex: 1;
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.15s ease;
  }

  .mode-toggle button:hover {
    background: var(--border-color);
  }

  .mode-toggle button.active {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
  }

  .sidebar-info {
    padding: 1rem;
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.5;
  }

  .sidebar-info .hint {
    margin-top: 0.75rem;
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  .search-box {
    padding: 0.75rem;
  }

  .search-box input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 0.875rem;
  }

  .search-box input:focus {
    outline: none;
    border-color: var(--accent);
  }

  .sidebar-actions {
    display: flex;
    gap: 0.5rem;
    padding: 0 0.75rem 0.75rem;
  }

  .sidebar-actions button {
    flex: 1;
    padding: 0.4rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 0.75rem;
  }

  .sidebar-actions button:hover {
    background: var(--border-color);
    color: var(--text-primary);
  }

  .sidebar-actions button.refreshing {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .layout-toggle {
    display: flex;
    gap: 0.25rem;
    padding: 0 0.75rem 0.75rem;
  }

  .layout-toggle button {
    flex: 1;
    padding: 0.35rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 0.7rem;
  }

  .layout-toggle button.active {
    background: var(--accent);
    border-color: var(--accent);
    color: white;
  }

  .file-list {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
  }

  .category {
    margin-bottom: 1rem;
  }

  .category h3 {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    padding: 0.5rem;
    margin-bottom: 0.25rem;
  }

  .file-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.5rem 0.75rem;
    background: none;
    border: none;
    border-radius: 6px;
    color: var(--text-secondary);
    cursor: pointer;
    text-align: left;
    font-size: 0.85rem;
    transition: all 0.15s ease;
  }

  .file-item:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }

  .file-item.active {
    background: var(--accent);
    color: white;
  }

  .file-item .icon {
    font-size: 1rem;
  }

  .file-item .name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .sidebar-footer {
    padding: 0.75rem;
    border-top: 1px solid var(--border-color);
  }

  .stats {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: center;
  }

  /* Main Content */
  .content {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
  }

  .empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
  }

  .empty-state h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
  }

  .empty-state p {
    margin-bottom: 1.5rem;
  }

  .primary-btn {
    padding: 0.75rem 1.5rem;
    background: var(--accent);
    border: none;
    border-radius: 6px;
    color: white;
    font-weight: 500;
    cursor: pointer;
  }

  .primary-btn:hover {
    background: var(--accent-hover);
  }

  /* Panels Container */
  .panels-container {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1px;
    background: var(--border-color);
    overflow: hidden;
  }

  .panels-container.columns {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-rows: 100%;
  }

  .panel {
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
    overflow: hidden;
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .panel-title {
    font-weight: 500;
    font-size: 0.9rem;
  }

  .close-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 1.25rem;
    line-height: 1;
    padding: 0.25rem;
  }

  .close-btn:hover {
    color: var(--danger);
  }

  .panel-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
  }

  /* Tabs Layout */
  .tabs-layout {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .tabs-header {
    display: flex;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    overflow-x: auto;
  }

  .tab {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: none;
    border: none;
    border-right: 1px solid var(--border-color);
    color: var(--text-secondary);
    cursor: pointer;
    white-space: nowrap;
    font-size: 0.85rem;
  }

  .tab:hover {
    background: var(--bg-tertiary);
  }

  .tab.active {
    background: var(--bg-primary);
    color: var(--text-primary);
    border-bottom: 2px solid var(--accent);
  }

  .tab .close {
    color: var(--text-muted);
    font-size: 1rem;
  }

  .tab .close:hover {
    color: var(--danger);
  }

  .tab-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
  }

  /* Loading */
  .loading {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100px;
    color: var(--text-muted);
  }
</style>
