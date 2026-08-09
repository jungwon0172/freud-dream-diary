/* ============================================================
   쿠키 동의 배너 — Google AdSense 광고 쿠키 고지
   ============================================================ */
(function(){
  const KEY = 'freud-dream-cookie-consent';

  function getChoice(){
    try{ return window.localStorage.getItem(KEY); }
    catch(e){ return null; }
  }
  function setChoice(v){
    try{ window.localStorage.setItem(KEY, v); }catch(e){}
  }

  function render(){
    if(getChoice()) return;

    const bar = document.createElement('div');
    bar.id = 'cookie-consent-bar';
    bar.innerHTML = `
      <div class="cc-inner">
        <p class="cc-text">이 사이트는 Google AdSense 광고 게재를 위해 쿠키를 사용합니다. 자세한 내용은 <a href="${(location.pathname.includes('/theory/') ? '../' : '')}privacy.html">개인정보처리방침</a>에서 확인하실 수 있습니다.</p>
        <div class="cc-actions">
          <button class="btn small ghost" id="cc-decline">필수만 허용</button>
          <button class="btn small" id="cc-accept">모두 허용</button>
        </div>
      </div>
    `;
    document.body.appendChild(bar);

    document.getElementById('cc-accept').addEventListener('click', () => {
      setChoice('all');
      bar.remove();
    });
    document.getElementById('cc-decline').addEventListener('click', () => {
      setChoice('essential');
      bar.remove();
    });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', render);
  }else{
    render();
  }
})();
