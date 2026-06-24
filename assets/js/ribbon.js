import {escapeHtml} from './utils.js';
export function createRibbon(container,ribbonConfig,store){
  function render(state){
    container.innerHTML=ribbonConfig.rows.map(row=>`<div class="ribbon-row"><div class="ribbon-label">${escapeHtml(row.label)}</div><div class="ribbon-buttons">${row.items.map(item=>`<button class="context-button ${state[row.id]===item.id?'active':''}" data-row="${row.id}" data-id="${item.id}">${escapeHtml(item.label)}</button>`).join('')}</div></div>`).join('');
    container.querySelectorAll('.context-button').forEach(button=>button.addEventListener('click',()=>{const row=button.dataset.row,id=button.dataset.id;store.mutate(state=>{state[row]=id;state.inspectorOpen=false;state.selectedRecordId=null;state.selectedRecordNeedId=null;if(row==='sector'&&!state.selectedNodeBySector[id])state.selectedNodeBySector[id]=id})}));
  }
  store.subscribe(render);render(store.get());
}
