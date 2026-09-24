
const ta=document.getElementById('problem');
const fileInput=document.getElementById('image');
const prev=document.getElementById('prev');
// 이미지 클립보드 → file input 주입 + 미리보기 (공통)
function applyImage(blob){
  if(!blob) return false;
  const file=new File([blob],'pasted_'+Date.now()+'.png',{type:blob.type||'image/png'});
  const dt=new DataTransfer(); dt.items.add(file);
  try{ fileInput.files=dt.files; }catch(err){ /* 일부 브라우저는 files 대입 불가 → 미리보기만 */ }
  const url=URL.createObjectURL(blob);
  prev.src=url; prev.style.display='block';
  const pz=document.getElementById('pastezone');
  pz.textContent='✅ 이미지가 붙여넣어졌어요. 그대로 생성하면 됩니다.';
  pz.style.color='#3ddc97';
  return true;
}
// 경로 1: Ctrl+V (대부분 동작하나 포커스/보안 제약 있음)
document.addEventListener('paste',e=>{
  const cd=(e.clipboardData||window.clipboardData);
  if(!cd) return;
  let blob=null, foundText=false;
  if(cd.items){ for(const it of cd.items){
    if(it.type&&it.type.indexOf('image')===0){ blob=it.getAsFile(); if(blob) break; }
    else if(it.kind==='string') foundText=true;
  }}
  if(!blob&&cd.files&&cd.files.length){ for(const f of cd.files){ if(f.type&&f.type.indexOf('image')===0){ blob=f; break; } } }
  if(blob){ e.preventDefault(); applyImage(blob); }
});
// 경로 2: 📋 버튼 → 공식 Clipboard API (가장 확실, 권한 허용 시)
async function pasteFromClipboard(){
  const pz=document.getElementById('pastezone');
  if(!navigator.clipboard||!navigator.clipboard.read){
    pz.textContent='이 브라우저는 클립보드 읽기를 지원하지 않아요. 대신 🖼️ 갤러리 선택을 쓰세요.';
    pz.style.color='#ff6b6b'; return;
  }
  try{
    const items=await navigator.clipboard.read();
    for(const item of items){
      const type=item.types.find(t=>t.startsWith('image/'));
      if(type){ const blob=await item.getType(type); applyImage(blob); return; }
    }
    pz.textContent='클립보드에 이미지가 없어요. 캡처 후 다시 눌러주세요.';
    pz.style.color='#ffd166';
  }catch(err){
    pz.textContent='클립보드 접근이 차단됐어요. 브라우저가 권한을 물으면 "허용"을 누르세요. (또는 🖼️ 갤러리 선택)';
    pz.style.color='#ff6b6b';
  }
}
// 기존 파일 선택 시에도 미리보기
fileInput.addEventListener('change',()=>{
  if(fileInput.files&&fileInput.files[0]){prev.src=URL.createObjectURL(fileInput.files[0]);prev.style.display='block';}
});
// 경로 3: 드래그앤드롭 (클립보드 의존 없음 — 파일을 직접 끌어다 놓기)
const pz=document.getElementById('pastezone');
['dragover','dragenter'].forEach(ev=>pz.addEventListener(ev,e=>{e.preventDefault();pz.style.borderColor='#3ddc97';}));
['dragleave','drop'].forEach(ev=>pz.addEventListener(ev,e=>{e.preventDefault();pz.style.borderColor='#3a4566';}));
pz.addEventListener('drop',e=>{
  const dt=e.dataTransfer; if(!dt||!dt.files||!dt.files.length) return;
  for(const f of dt.files){ if(f.type.indexOf('image')===0){ applyImage(f); return; } }
});
// 📱 갤러리 / 카메라 선택 버튼
function pickImage(useCamera){
  const fi=document.getElementById('image');
  if(useCamera){ fi.setAttribute('capture','environment'); }
  else { fi.removeAttribute('capture'); }
  fi.value='';  // 같은 파일 재선택 허용
  fi.click();
}
// 생성 버튼 → 대기 오버레이 표시 (실제 제출은 그대로 진행)
document.getElementById('frm').addEventListener('submit',()=>{
  document.getElementById('loading').classList.add('show');
});
// 15초마다 완성된 퀴즈 확인 → 배너 표시 (최근 10분 내 것만)
function checkDone(){
  fetch('/done.json').then(r=>r.json()).then(d=>{
    const items=(d.items||[]).filter(it=>{
      const ts=it.ts||0;
      return (Date.now()/1000 - ts) < 600;  // 10분 이내
    });
    const box=document.getElementById('doneBox');
    const list=document.getElementById('doneList');
    if(items.length){
      box.style.display='block';
      list.innerHTML=items.map(it=>
        `<div>📄 <a href="/board/${it.slug}">${it.title}</a>`+
        ` <span style="color:#9aa6c0;font-size:.8rem"> — ${it.time}</span></div>`).join('');
      // 3개 초과면 스크롤, 3개 이하면 자동 높이
      box.style.maxHeight = items.length > 3 ? '300px' : 'none';
      box.style.overflowY = items.length > 3 ? 'auto' : 'visible';
    } else {
      box.style.display='none';
    }
  }).catch(()=>{});
}
// 중복 안내 팝업: 기존 풀이로 이동
(function(){const p=new URLSearchParams(location.search);const g=p.get('goto');
if(g){const m=document.getElementById('dupModal');document.getElementById('dupLink').href='/board/'+g;
m.style.display='block';setTimeout(()=>{location.href='/board/'+g;},2200);}})();
checkDone(); setInterval(checkDone, 15000);

