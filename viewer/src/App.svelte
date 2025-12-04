<script>
  import { marked } from 'marked';
  import { onMount } from 'svelte';

  // File definitions with metadata
  const files = [
    { id: 'sponsor_combinations', name: 'Tool Combinations (330 ideas)', path: 'sponsor_combinations_ideas.md', category: 'Ideas', icon: '🔗' },
    { id: 'ics_combinations', name: 'ICS Combinations (60 ideas)', path: 'ics_combinations_ideas.md', category: 'Ideas', icon: '📅' },
    { id: 'ar_tools', name: 'AR Tools (65 ideas)', path: 'ar_tools_combinations_ideas.md', category: 'Ideas', icon: '👓' },
    { id: 'local_ai_100', name: '100 Local AI Uses (4GB)', path: '100_local_ai_usecases_4gb.md', category: 'Ideas', icon: '💻' },
    { id: 'free_hackathon', name: 'Free Hackathon Ideas', path: 'free_hackathon_ideas.md', category: 'Ideas', icon: '💡' },
    { id: 'local_ai_guide', name: 'Local AI Guide', path: 'local_ai_guide.md', category: 'Guides', icon: '🤖' },
    { id: 'free_tier', name: 'Free Tier Services', path: 'free_tier_services.md', category: 'Guides', icon: '🆓' },
    { id: 'hackathon_platforms', name: 'Hackathon Platforms', path: 'hackathon_platforms_guide.md', category: 'Guides', icon: '🏆' },
    { id: 'sponsor_matrix', name: 'Sponsor Matrix', path: 'sponsor_combinations_matrix.md', category: 'Reference', icon: '📊' },
    { id: 'template_merging', name: 'Template Merging', path: 'template_merging_guide.md', category: 'Reference', icon: '📝' },
  ];

  const categories = [...new Set(files.map(f => f.category))];

  let openPanels = [];
  let fileContents = {};
  let loading = {};
  let searchQuery = '';
  let sidebarCollapsed = false;

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

  // Toggle panel
  function togglePanel(file) {
    const index = openPanels.findIndex(p => p.id === file.id);
    if (index >= 0) {
      openPanels = openPanels.filter(p => p.id !== file.id);
    } else {
      openPanels = [...openPanels, file];
      loadFile(file);
    }
  }

  // Close panel
  function closePanel(fileId) {
    openPanels = openPanels.filter(p => p.id !== fileId);
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

  // Open all files
  function openAll() {
    files.forEach(file => {
      if (!openPanels.find(p => p.id === file.id)) {
        openPanels = [...openPanels, file];
        loadFile(file);
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
      <h1>📚 Sponsor Prep</h1>
      <button class="collapse-btn" on:click={() => sidebarCollapsed = !sidebarCollapsed}>
        {sidebarCollapsed ? '→' : '←'}
      </button>
    </div>

    {#if !sidebarCollapsed}
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
                  on:click={() => togglePanel(file)}
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
  </aside>

  <!-- Main Content -->
  <main class="content">
    {#if openPanels.length === 0}
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
          {#each openPanels as panel}
            <button
              class="tab"
              class:active={openPanels[0]?.id === panel.id}
              on:click={() => {
                openPanels = [panel, ...openPanels.filter(p => p.id !== panel.id)];
              }}
            >
              <span>{panel.icon} {panel.name}</span>
              <span class="close" on:click|stopPropagation={() => closePanel(panel.id)}>×</span>
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
        {#each openPanels as panel (panel.id)}
          <div class="panel">
            <div class="panel-header">
              <span class="panel-title">{panel.icon} {panel.name}</span>
              <button class="close-btn" on:click={() => closePanel(panel.id)}>×</button>
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
