/* ============================================================
   꿈해몽 검색 — 클라이언트 사이드 필터링
   window.DREAM_SYMBOLS (assets/dream-data.js)를 사용합니다.
   ============================================================ */
(function(){
  function ready(fn){
    if(document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function(){
    const input = document.getElementById('dream-search');
    const resultsBox = document.getElementById('search-results');
    if(!input || !resultsBox || !window.DREAM_SYMBOLS) return;

    function matches(sym, q){
      if(sym.title.includes(q)) return true;
      if(sym.aliases.some(a => a.includes(q))) return true;
      if(sym.category.includes(q)) return true;
      return false;
    }

    function render(q){
      if(!q){
        resultsBox.innerHTML = '';
        resultsBox.style.display = 'none';
        return;
      }
      const found = window.DREAM_SYMBOLS.filter(s => matches(s, q)).slice(0, 8);
      resultsBox.style.display = 'block';
      if(found.length === 0){
        resultsBox.innerHTML = '<div class="empty-state">검색 결과가 없습니다. 다른 표현으로 검색해보세요.</div>';
        return;
      }
      resultsBox.innerHTML = found.map(s => `
        <a class="entry" style="display:block; margin-bottom:10px;" href="dream/${s.slug}.html">
          <div class="entry-head"><span class="entry-date">${s.category}</span></div>
          <p class="entry-text" style="font-family:var(--font-display); font-size:17px; margin-top:6px;">${s.title} 해몽</p>
          <p class="small" style="margin:4px 0 0;">${s.summary}</p>
        </a>
      `).join('');
    }

    input.addEventListener('input', () => render(input.value.trim()));

    // URL에 ?q=검색어 가 있으면 자동 검색
    const params = new URLSearchParams(location.search);
    const initial = params.get('q');
    if(initial){
      input.value = initial;
      render(initial.trim());
    }
  });
})();
