/**
 * Family Fork - Main JavaScript
 * Shared utilities and interactions
 */

// Adjust servings with automatic ingredient scaling
function adjustServings(delta) {
  const baseServings = parseInt(document.getElementById('base-servings').value);
  const currentCount = document.getElementById('serving-count');
  let newServings = parseInt(currentCount.textContent) + delta;
  
  // Constrain between 1 and 10
  newServings = Math.max(1, Math.min(10, newServings));
  currentCount.textContent = newServings;
  
  // Scale ingredients
  const ratio = newServings / baseServings;
  document.querySelectorAll('.ingredient-qty').forEach(qty => {
    const base = parseFloat(qty.dataset.base);
    const scaledQty = (base * ratio).toFixed(2).replace(/\.?0+$/, '');
    qty.textContent = scaledQty + ' ' + qty.dataset.unit;
  });
}

// Timer functionality
function startTimer(minutes) {
  const seconds = minutes * 60;
  let remaining = seconds;
  
  const timerDisplay = document.createElement('div');
  timerDisplay.className = 'timer-display';
  timerDisplay.textContent = formatTime(remaining);
  
  const countdown = setInterval(() => {
    remaining--;
    timerDisplay.textContent = formatTime(remaining);
    
    if (remaining <= 0) {
      clearInterval(countdown);
      playNotification();
      timerDisplay.textContent = 'Time\'s up! ✓';
    }
  }, 1000);
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function playNotification() {
  // Simple audio notification (beep)
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  
  oscillator.connect(gain);
  gain.connect(audioContext.destination);
  
  oscillator.frequency.value = 800;
  oscillator.type = 'sine';
  
  gain.gain.setValueAtTime(0.3, audioContext.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
  
  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + 0.5);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeFeatures();
});

function initializeFeatures() {
  bindGenerateButtons();
  console.log('Family Fork initialized');
}

function bindGenerateButtons() {
  document.querySelectorAll('.generate-recipe-btn').forEach(button => {
    button.addEventListener('click', async () => {
      await generateRecipe(button);
    });
  });
}

async function generateRecipe(button) {
  const buttons = Array.from(document.querySelectorAll('.generate-recipe-btn'));
  const originalStates = buttons.map(btn => ({ btn, text: btn.textContent, disabled: btn.disabled }));

  buttons.forEach(btn => {
    btn.disabled = true;
    btn.textContent = 'Generating…';
  });

  try {
    const response = await fetch('/api/generate', { method: 'POST' });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Unable to generate recipe.');
    }

    if (!data.job_id) {
      throw new Error('Missing generation job ID.');
    }

    const result = await pollJobStatus(data.job_id);

    if (result.recipe && result.recipe.id) {
      window.location.href = `/recipe/${result.recipe.id}`;
      return;
    }

    window.location.reload();
  } catch (error) {
    alert(error.message || 'Failed to generate a recipe.');
    originalStates.forEach(state => {
      state.btn.disabled = state.disabled;
      state.btn.textContent = state.text;
    });
  }
}

async function pollJobStatus(jobId) {
  const maxAttempts = 90;
  const pollInterval = 2000;
  let attempts = 0;

  while (attempts < maxAttempts) {
    const response = await fetch(`/api/job/${jobId}`);
    const data = await response.json();

    if (data.status === 'done') {
      return data;
    }

    if (data.status === 'error') {
      throw new Error(data.error || 'Recipe generation failed.');
    }

    await new Promise(resolve => setTimeout(resolve, pollInterval));
    attempts += 1;
  }

  throw new Error('Recipe generation is taking too long. Please refresh the page and try again.');
}

// Smooth scroll utility
function smoothScroll(element) {
  element.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Local storage utilities
const Storage = {
  set: (key, value) => localStorage.setItem('ff_' + key, JSON.stringify(value)),
  get: (key) => {
    const item = localStorage.getItem('ff_' + key);
    return item ? JSON.parse(item) : null;
  },
  remove: (key) => localStorage.removeItem('ff_' + key),
  clear: () => localStorage.clear()
};
