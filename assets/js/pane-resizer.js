const STORAGE_KEY='economy-master-tree-width-v03';
export function attachTreePaneResizer({grid,resizer,defaultWidth=367,minWidth=280,maxWidth=720}){
  if(!grid||!resizer)return;
  const clamp=value=>Math.max(minWidth,Math.min(maxWidth,Math.min(window.innerWidth*.46,value)));
  const apply=value=>{const width=clamp(Number(value)||defaultWidth);grid.style.setProperty('--tree-panel-width',`${width}px`);resizer.setAttribute('aria-valuenow',String(Math.round(width)));return width};
  let width=apply(localStorage.getItem(STORAGE_KEY)||defaultWidth),startX=0,startWidth=width,dragging=false;
  const stop=()=>{if(!dragging)return;dragging=false;resizer.classList.remove('dragging');localStorage.setItem(STORAGE_KEY,String(width));document.body.style.userSelect='';document.body.style.cursor=''};
  resizer.addEventListener('pointerdown',event=>{dragging=true;startX=event.clientX;startWidth=parseFloat(getComputedStyle(grid).getPropertyValue('--tree-panel-width'))||width;resizer.setPointerCapture(event.pointerId);resizer.classList.add('dragging');document.body.style.userSelect='none';document.body.style.cursor='col-resize'});
  resizer.addEventListener('pointermove',event=>{if(!dragging)return;width=apply(startWidth+event.clientX-startX)});
  resizer.addEventListener('pointerup',stop);resizer.addEventListener('pointercancel',stop);
  resizer.addEventListener('dblclick',()=>{width=apply(defaultWidth);localStorage.setItem(STORAGE_KEY,String(width))});
  resizer.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home'].includes(event.key))return;event.preventDefault();if(event.key==='Home')width=apply(defaultWidth);else width=apply(width+(event.key==='ArrowRight'?10:-10));localStorage.setItem(STORAGE_KEY,String(width))});
  resizer.setAttribute('aria-valuemin',String(minWidth));resizer.setAttribute('aria-valuemax',String(maxWidth));resizer.setAttribute('aria-valuenow',String(Math.round(width)));
}
