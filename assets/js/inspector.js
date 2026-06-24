import {escapeHtml,findTreeNode,downloadJson} from './utils.js';
import {recordDisplayName,treeDisplayLabel} from './display-labels.js';
export function createInspector({panel,container,closeButton,exportButton,trees,products,store}){
  let current=null,currentRecord=null,token=0;
  function row(label,value){return `<tr><td>${escapeHtml(label)}</td><td>${escapeHtml(value??'')}</td></tr>`}
  function setOpen(open){panel.classList.toggle('open',open);panel.setAttribute('aria-hidden',open?'false':'true')}
  async function render(state){
    if(!state.inspectorOpen){setOpen(false);return}
    const myToken=++token,tree=trees[state.sector]||trees.home;
    current=findTreeNode(tree,state.selectedNodeBySector[state.sector]||tree.id)?.node||tree;
    currentRecord=state.selectedRecordId?await products.recordById(state.selectedRecordNeedId,state.selectedRecordId):null;
    if(myToken!==token)return;
    setOpen(true);
    const displayName=currentRecord?recordDisplayName(currentRecord):treeDisplayLabel(current);
    const badge=currentRecord?(currentRecord.record_kind==='service'?'SERVICE':'PRODUCT'):(current.type||'object').toUpperCase();
    const recordRows=currentRecord?[row('Record ID',currentRecord.record_id),row('Need Path',currentRecord.need_path),row(currentRecord.record_kind==='service'?'Service':'Product',recordDisplayName(currentRecord)),row('Original Label',currentRecord.item_name),row('Manufacturer',currentRecord.manufacturer||'—'),row('Model / Part',currentRecord.model_part_number||'—'),row('Source',currentRecord.source_vendor),row('Source Record',currentRecord.source_record_id),row('Status',currentRecord.record_status),row('Availability',currentRecord.availability),row('Risk',currentRecord.risk),row('Risk Type',currentRecord.risk_type),row('Updated / Year',currentRecord.last_updated||currentRecord.catalog_year),row('Historical Cost',currentRecord.total_cost==null?'—':`${currentRecord.total_cost} ${currentRecord.currency}`),row('Evidence',currentRecord.evidence)].join(''):'';
    container.innerHTML=`<div class="inspector-title"><span class="status-badge">${escapeHtml(badge)}</span><h3>${escapeHtml(displayName)}</h3><span class="status-badge">${escapeHtml(state.sector)}</span><span class="status-badge">${escapeHtml(state.tool)}</span></div><div class="inspector-actions"><button class="compact-button">NEW</button><button class="compact-button">OPEN</button><button class="compact-button">EDIT</button><button class="compact-button">SAVE</button></div><div class="inspector-actions"><button class="compact-button">SIMULATE</button><button class="compact-button">ASSESS</button><button class="compact-button">DOCUMENT</button><button class="compact-button">COMPARE</button></div><div class="module-note">TreeView remains at the selected sector/category/class/brick. Datagrid rows are records, not TreeView leaves.</div><h4>IDENTITY</h4><table class="property-table">${row('Tree Node',treeDisplayLabel(current))}${row('Tree Class',current.type||'')}${row('Sector',state.sector)}${row('Scope',state.scope)}${row('Overlay',state.overlay)}${row('Tool',state.tool)}${row('Priority',current.priority_rank||'—')}${row('Linked Records',(current.product_count||0).toLocaleString())}${row('Description',current.description||'')}${recordRows}</table>`;
  }
  closeButton.addEventListener('click',()=>store.mutate(s=>s.inspectorOpen=false));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&store.get().inspectorOpen)store.mutate(s=>s.inspectorOpen=false)});
  exportButton.addEventListener('click',()=>current&&downloadJson('selected-economy-object.json',currentRecord?{tree_node:current,record:currentRecord}:current));
  store.subscribe(render);render(store.get());
}
