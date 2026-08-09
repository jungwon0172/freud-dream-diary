/* ============================================================
   프로이트 꿈 일기 — 저장 로직
   localStorage 사용, 접근 불가 환경(일부 미리보기 등)에서는
   메모리 폴백으로 동작합니다. (배너로 사용자에게 고지)
   ============================================================ */

(function(){
  const STORAGE_KEY = 'freud-dream-entries-v1';
  let memoryFallback = false;
  let memoryStore = [];

  function storageAvailable(){
    try{
      const t = '__test__';
      window.localStorage.setItem(t, '1');
      window.localStorage.removeItem(t);
      return true;
    }catch(e){
      return false;
    }
  }

  const hasStorage = storageAvailable();
  if(!hasStorage) memoryFallback = true;

  function loadEntries(){
    if(memoryFallback) return memoryStore.slice();
    try{
      const raw = window.localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    }catch(e){
      return [];
    }
  }

  function saveEntries(entries){
    if(memoryFallback){
      memoryStore = entries;
      return;
    }
    try{
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
    }catch(e){
      // 저장 실패 시 메모리로 전환
      memoryFallback = true;
      memoryStore = entries;
    }
  }

  function uid(){
    return 'd' + Date.now().toString(36) + Math.random().toString(36).slice(2,7);
  }

  window.DreamJournal = {
    isMemoryFallback: () => memoryFallback,
    all: loadEntries,
    add(entry){
      const entries = loadEntries();
      entries.unshift(Object.assign({
        id: uid(),
        createdAt: new Date().toISOString()
      }, entry));
      saveEntries(entries);
      return entries;
    },
    remove(id){
      const entries = loadEntries().filter(e => e.id !== id);
      saveEntries(entries);
      return entries;
    },
    stats(){
      const entries = loadEntries();
      const tagCount = {};
      const emotionCount = {};
      entries.forEach(e => {
        (e.tags||[]).forEach(t => { tagCount[t] = (tagCount[t]||0) + 1; });
        if(e.emotion) emotionCount[e.emotion] = (emotionCount[e.emotion]||0) + 1;
      });
      const topTag = Object.entries(tagCount).sort((a,b)=>b[1]-a[1])[0];
      const topEmotion = Object.entries(emotionCount).sort((a,b)=>b[1]-a[1])[0];
      return {
        total: entries.length,
        topTag: topTag ? topTag[0] : null,
        topTagCount: topTag ? topTag[1] : 0,
        topEmotion: topEmotion ? topEmotion[0] : null,
        topEmotionCount: topEmotion ? topEmotion[1] : 0
      };
    }
  };
})();
