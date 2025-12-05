<script>
  import { onMount } from 'svelte';

  const STORAGE_KEY = 'hackathon-questionnaire-responses';

  // 100 Questions organized by category
  const questionCategories = [
    {
      name: "Problem & Purpose",
      icon: "🎯",
      questions: [
        "What specific problem are you trying to solve?",
        "Who experiences this problem most acutely?",
        "How do people currently solve this problem?",
        "What makes existing solutions inadequate?",
        "Why does this problem matter to you personally?",
        "What would the world look like if this problem was solved?",
        "How often does this problem occur for your target users?",
        "What is the cost (time, money, frustration) of this problem?",
        "Is this a problem you've experienced yourself?",
        "What triggered you to think about this problem?"
      ]
    },
    {
      name: "Target Users",
      icon: "👥",
      questions: [
        "Who is your primary user?",
        "What does a typical day look like for your user?",
        "What are your user's biggest frustrations?",
        "What tools does your user already use?",
        "How tech-savvy is your target user?",
        "Where do your users spend time online?",
        "What would make your user's life 10x easier?",
        "How would you find 10 users to test your idea?",
        "What language does your user use to describe this problem?",
        "What would convince your user to try something new?"
      ]
    },
    {
      name: "Solution Approach",
      icon: "💡",
      questions: [
        "In one sentence, what does your solution do?",
        "What is the core insight behind your approach?",
        "Why hasn't this been built before?",
        "What's the simplest version that could work?",
        "What makes your approach unique?",
        "What existing technology can you leverage?",
        "What's the hardest technical challenge?",
        "What assumptions are you making?",
        "How will users discover your solution?",
        "What's the 'aha moment' for users?"
      ]
    },
    {
      name: "MVP & Scope",
      icon: "🎪",
      questions: [
        "What's the ONE feature you must demo?",
        "What features can you cut and still have value?",
        "What can you fake/mock for the demo?",
        "What's your 2-hour version?",
        "What's your 8-hour version?",
        "What would you add with unlimited time?",
        "What's the riskiest part to build first?",
        "Can you describe the MVP in 3 bullet points?",
        "What's the minimum data you need?",
        "What can you hardcode for now?"
      ]
    },
    {
      name: "Technical Stack",
      icon: "🛠️",
      questions: [
        "What languages/frameworks do you know best?",
        "What sponsor technologies could you use?",
        "What APIs would accelerate development?",
        "Do you need a backend? Why?",
        "Do you need a database? What kind?",
        "What's the deployment plan?",
        "What's your testing strategy?",
        "What could cause technical failure?",
        "Do you need real-time features?",
        "What third-party services can you leverage?"
      ]
    },
    {
      name: "AI & Data",
      icon: "🤖",
      questions: [
        "What role could AI play in your solution?",
        "What data would you need to train a model?",
        "Could you use a pre-trained model?",
        "What would you use an LLM for?",
        "What prompts would your system need?",
        "How would you handle AI errors/hallucinations?",
        "Is AI essential or just nice-to-have?",
        "What's the fallback if AI doesn't work?",
        "How would you evaluate AI output quality?",
        "What's the cost of AI API calls?"
      ]
    },
    {
      name: "Team & Skills",
      icon: "👨‍💻",
      questions: [
        "What's each team member's strongest skill?",
        "What skills are you missing?",
        "How will you divide the work?",
        "Who will handle the presentation/demo?",
        "How will you communicate during the hackathon?",
        "What's your backup plan if someone gets stuck?",
        "Who has experience with the sponsor tech?",
        "What can each person learn from this project?",
        "How will you resolve disagreements?",
        "Who is responsible for the final submission?"
      ]
    },
    {
      name: "Time Management",
      icon: "⏰",
      questions: [
        "What's your hour-by-hour plan?",
        "When will you stop coding and start polishing?",
        "What's your deadline for a working prototype?",
        "When will you practice the demo?",
        "What will you do in the last hour?",
        "What's your sleep/break strategy?",
        "What's your 'emergency pivot' time?",
        "When will you commit to the final approach?",
        "What tasks can be parallelized?",
        "What's blocking progress right now?"
      ]
    },
    {
      name: "Presentation & Demo",
      icon: "🎤",
      questions: [
        "What's your opening hook?",
        "Can you demo the core value in 60 seconds?",
        "What story will you tell?",
        "What visuals will support your pitch?",
        "What questions might judges ask?",
        "How will you show impact/metrics?",
        "What's your backup if the demo fails?",
        "Who is your ideal judge persona?",
        "What makes your demo memorable?",
        "How will you end with a strong close?"
      ]
    },
    {
      name: "Competition & Differentiation",
      icon: "🏆",
      questions: [
        "What sponsor prizes are you targeting?",
        "What do winning projects usually have?",
        "How will you stand out from other teams?",
        "What's your unfair advantage?",
        "What's innovative about your approach?",
        "How does this align with sponsor goals?",
        "What would make a judge remember you?",
        "What category does your project fit?",
        "How will you demonstrate technical depth?",
        "What risks are you taking that others won't?"
      ]
    }
  ];

  // Flatten questions with IDs
  let allQuestions = [];
  let questionIndex = 0;
  questionCategories.forEach(cat => {
    cat.questions.forEach(q => {
      allQuestions.push({
        id: questionIndex++,
        category: cat.name,
        icon: cat.icon,
        text: q
      });
    });
  });

  // Responses state
  let responses = {};
  let searchQuery = '';
  let filterCategory = 'all';
  let showOnlyAnswered = false;
  let showOnlyUnanswered = false;

  // Load from localStorage
  onMount(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        responses = JSON.parse(saved);
      } catch (e) {
        responses = {};
      }
    }
  });

  // Save to localStorage on change
  function saveResponses() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(responses));
  }

  // Export as text
  function exportAsText() {
    let text = "# Hackathon Questionnaire Responses\n";
    text += `# Exported: ${new Date().toLocaleString()}\n\n`;

    questionCategories.forEach(cat => {
      text += `\n## ${cat.icon} ${cat.name}\n${'='.repeat(40)}\n\n`;
      cat.questions.forEach((q, i) => {
        const qId = allQuestions.find(aq => aq.text === q && aq.category === cat.name)?.id;
        const answer = responses[qId] || '';
        text += `Q: ${q}\n`;
        text += `A: ${answer || '(not answered)'}\n\n`;
      });
    });

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `hackathon-questionnaire-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  // Import from text
  function importFromText() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const text = await file.text();
      const lines = text.split('\n');

      let currentQuestion = null;
      let currentAnswer = [];

      for (const line of lines) {
        if (line.startsWith('Q: ')) {
          // Save previous answer
          if (currentQuestion !== null) {
            const qObj = allQuestions.find(q => q.text === currentQuestion);
            if (qObj) {
              responses[qObj.id] = currentAnswer.join('\n').trim();
            }
          }
          currentQuestion = line.substring(3);
          currentAnswer = [];
        } else if (line.startsWith('A: ')) {
          const answerStart = line.substring(3);
          if (answerStart !== '(not answered)') {
            currentAnswer.push(answerStart);
          }
        } else if (currentQuestion && !line.startsWith('#') && !line.startsWith('=')) {
          currentAnswer.push(line);
        }
      }

      // Save last answer
      if (currentQuestion !== null) {
        const qObj = allQuestions.find(q => q.text === currentQuestion);
        if (qObj) {
          responses[qObj.id] = currentAnswer.join('\n').trim();
        }
      }

      responses = { ...responses };
      saveResponses();
    };
    input.click();
  }

  // Clear all
  function clearAll() {
    if (confirm('Clear all responses? This cannot be undone.')) {
      responses = {};
      saveResponses();
    }
  }

  // Filter questions
  $: filteredQuestions = allQuestions.filter(q => {
    if (filterCategory !== 'all' && q.category !== filterCategory) return false;
    if (searchQuery && !q.text.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    if (showOnlyAnswered && !responses[q.id]?.trim()) return false;
    if (showOnlyUnanswered && responses[q.id]?.trim()) return false;
    return true;
  });

  // Stats
  $: answeredCount = allQuestions.filter(q => responses[q.id]?.trim()).length;
  $: progress = Math.round((answeredCount / allQuestions.length) * 100);
</script>

<div class="questionnaire">
  <header class="q-header">
    <div class="q-title">
      <h1>💭 100 Questions</h1>
      <p>Think through your hackathon project</p>
    </div>
    <div class="q-actions">
      <button on:click={exportAsText} title="Export as text file">📥 Export</button>
      <button on:click={importFromText} title="Import from text file">📤 Import</button>
      <button on:click={clearAll} class="danger" title="Clear all responses">🗑️ Clear</button>
    </div>
  </header>

  <div class="q-progress">
    <div class="progress-bar">
      <div class="progress-fill" style="width: {progress}%"></div>
    </div>
    <span class="progress-text">{answeredCount} / {allQuestions.length} answered ({progress}%)</span>
  </div>

  <div class="q-filters">
    <input
      type="text"
      placeholder="Search questions..."
      bind:value={searchQuery}
      class="search-input"
    />
    <select bind:value={filterCategory}>
      <option value="all">All Categories</option>
      {#each questionCategories as cat}
        <option value={cat.name}>{cat.icon} {cat.name}</option>
      {/each}
    </select>
    <label class="filter-checkbox">
      <input type="checkbox" bind:checked={showOnlyUnanswered} on:change={() => showOnlyAnswered = false} />
      Unanswered
    </label>
    <label class="filter-checkbox">
      <input type="checkbox" bind:checked={showOnlyAnswered} on:change={() => showOnlyUnanswered = false} />
      Answered
    </label>
  </div>

  <div class="q-list">
    {#each filteredQuestions as question (question.id)}
      <div class="q-item" class:answered={responses[question.id]?.trim()}>
        <div class="q-item-header">
          <span class="q-number">#{question.id + 1}</span>
          <span class="q-category">{question.icon} {question.category}</span>
        </div>
        <div class="q-text">{question.text}</div>
        <textarea
          placeholder="Type your thoughts here..."
          bind:value={responses[question.id]}
          on:input={saveResponses}
          rows="2"
        ></textarea>
      </div>
    {/each}

    {#if filteredQuestions.length === 0}
      <div class="no-results">
        <p>No questions match your filters</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .questionnaire {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .q-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
  }

  .q-title h1 {
    font-size: 1.25rem;
    margin: 0;
  }

  .q-title p {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 0.25rem 0 0;
  }

  .q-actions {
    display: flex;
    gap: 0.5rem;
  }

  .q-actions button {
    padding: 0.5rem 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 0.8rem;
  }

  .q-actions button:hover {
    background: var(--border-color);
    color: var(--text-primary);
  }

  .q-actions button.danger:hover {
    background: var(--danger);
    border-color: var(--danger);
    color: white;
  }

  .q-progress {
    padding: 0.75rem 1.5rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .progress-bar {
    flex: 1;
    height: 8px;
    background: var(--bg-tertiary);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--accent);
    transition: width 0.3s ease;
  }

  .progress-text {
    font-size: 0.75rem;
    color: var(--text-muted);
    white-space: nowrap;
  }

  .q-filters {
    display: flex;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    flex-wrap: wrap;
    align-items: center;
  }

  .search-input {
    flex: 1;
    min-width: 200px;
    padding: 0.5rem 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 0.85rem;
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent);
  }

  .q-filters select {
    padding: 0.5rem 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 0.85rem;
  }

  .filter-checkbox {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.8rem;
    color: var(--text-secondary);
    cursor: pointer;
  }

  .filter-checkbox input {
    cursor: pointer;
  }

  .q-list {
    flex: 1;
    overflow-y: auto;
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .q-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    transition: border-color 0.2s;
  }

  .q-item.answered {
    border-left: 3px solid var(--accent);
  }

  .q-item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .q-number {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 600;
  }

  .q-category {
    font-size: 0.7rem;
    color: var(--text-muted);
    background: var(--bg-tertiary);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }

  .q-text {
    font-size: 0.95rem;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
    font-weight: 500;
  }

  .q-item textarea {
    width: 100%;
    padding: 0.75rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 0.85rem;
    resize: vertical;
    min-height: 60px;
    font-family: inherit;
  }

  .q-item textarea:focus {
    outline: none;
    border-color: var(--accent);
  }

  .q-item textarea::placeholder {
    color: var(--text-muted);
  }

  .no-results {
    text-align: center;
    padding: 3rem;
    color: var(--text-muted);
  }
</style>
