chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'export') {
    // TODO: Implement export logic
    console.log('Export to Penpot triggered');
  }
});
