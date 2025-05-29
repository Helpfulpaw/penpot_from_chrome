document.addEventListener('DOMContentLoaded', () => {
  const exportButton = document.getElementById('export');
  if (!exportButton) return;

  exportButton.addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'export' }, () => {
        if (chrome.runtime.lastError) {
          console.error('Error sending message:', chrome.runtime.lastError);
        }
      });
    });
  });
});
