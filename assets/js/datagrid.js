
import {escapeHtml,formatCell} from './utils.js';
function compare(a,b,type){
  if(type==='number'||type==='currency'){ const x=Number(a??Number.POSITIVE_INFINITY),y=Number(b??Number.POSITIVE_INFINITY);return x-y; }
  return String(a??'').localeCompare(String(b??''),undefined,{numeric:true,sensitivity:'base'});
}
export function renderDatagrid({state,store,columns,rows,title='Comparator Datagrid',description=''}){
  const availableFields=new Set(columns.map(c=>c.field));
  let visibleFields=state.datagrid.visibleColumns.filter(field=>availableFields.has(field));
  if(!visibleFields.length){ visibleFields=columns.filter(c=>c.default_visible!==false).map(c=>c.field); state.datagrid.visibleColumns=visibleFields; }
  const visible=columns.filter(c=>visibleFields.includes(c.field));
  const activeSorts=state.datagrid.sorts.filter(sort=>availableFields.has(sort.field));
  if(activeSorts.length!==state.datagrid.sorts.length) state.datagrid.sorts=activeSorts;
  const sorted=[...rows].sort((a,b)=>{for(const sort of activeSorts){const col=columns.find(c=>c.field===sort.field);const result=compare(a[sort.field],b[sort.field],col?.type);if(result)return sort.direction==='asc'?result:-result;}return 0;});
  const html=`<div class="workspace-card"><div class="grid-toolbar"><div class="grid-toolbar-left"><div><h2>${escapeHtml(title)}</h2><p>${escapeHtml(description)}</p></div></div><div class="grid-toolbar-right"><button class="action-button" data-action="columns">Columns</button><button class="action-button" data-action="clear-sort">Clear Sort</button></div></div><div class="column-panel ${state.datagrid.columnsOpen?'open':''}">${columns.map(c=>`<label class="column-option"><input type="checkbox" data-column="${c.field}" ${state.datagrid.visibleColumns.includes(c.field)?'checked':''}> ${escapeHtml(c.label)}</label>`).join('')}</div><div class="data-grid-wrap"><table class="data-grid"><thead><tr>${visible.map(c=>{const index=state.datagrid.sorts.findIndex(s=>s.field===c.field);const mark=index>=0?`<span class="sort-index">${index+1}${state.datagrid.sorts[index].direction==='asc'?'▲':'▼'}</span>`:'';return `<th data-sort-field="${c.field}">${escapeHtml(c.label)}${mark}</th>`}).join('')}</tr></thead><tbody>${sorted.map(row=>`<tr>${visible.map(c=>`<td>${escapeHtml(formatCell(row[c.field],c.type))}</td>`).join('')}</tr>`).join('')}</tbody></table></div></div>`;
  queueMicrotask(()=>{
    document.querySelector('[data-action="columns"]')?.addEventListener('click',()=>store.mutate(s=>s.datagrid.columnsOpen=!s.datagrid.columnsOpen));
    document.querySelector('[data-action="clear-sort"]')?.addEventListener('click',()=>store.mutate(s=>s.datagrid.sorts=[]));
    document.querySelectorAll('[data-column]').forEach(box=>box.addEventListener('change',()=>store.mutate(s=>{const set=new Set(s.datagrid.visibleColumns);box.checked?set.add(box.dataset.column):set.delete(box.dataset.column);s.datagrid.visibleColumns=[...set];})));
    document.querySelectorAll('[data-sort-field]').forEach(th=>th.addEventListener('click',event=>store.mutate(s=>{const field=th.dataset.sortField;let sorts=event.shiftKey?[...s.datagrid.sorts]:[];const i=sorts.findIndex(x=>x.field===field);if(i>=0)sorts[i]={field,direction:sorts[i].direction==='asc'?'desc':'asc'};else sorts.push({field,direction:'asc'});s.datagrid.sorts=sorts;})));
  });
  return html;
}
