// "Signed in as NAME · Switch" in the header bar of every page that has a .who slot.
(async () => {
  const slot = document.querySelector('.who');
  if (!slot) return;
  const me = await (await fetch('/api/me')).json();
  if (!me.name) { slot.innerHTML = '<a href="/login">Sign in</a>'; return; }
  const name = document.createElement('strong'); name.textContent = me.name;
  const sw = document.createElement('a'); sw.href = '#'; sw.textContent = 'Switch';
  sw.onclick = async (e) => { e.preventDefault(); await fetch('/api/logout', { method: 'POST' }); location.href = '/login?next=' + encodeURIComponent(location.pathname); };
  slot.replaceChildren('Signed in as ', name, ' · ', sw);
})();
