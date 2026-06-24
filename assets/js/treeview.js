import {escapeHtml,countTreeNodes,findTreeNode,walkTree} from './utils.js';
import {normalizeDisplayText,treeDisplayLabel} from './display-labels.js';
const icons={orientation:'⌂','sector-link':'◦',sector:'◉',category:'▣',class:'◇',brick:'▦','sector-root':'◉','priority-tree':'↓',need:'◆','fulfillment-class':'◇',records:'▤','record-class':'□','market-class':'⇄',classification:'▣','classification-system':'▦',model:'▦','model-object':'□','simulation-class':'△','data-reference':'◫','source-library':'☷','source-filter':'◫','processed-assets':'▤','finance-class':'◇','public-class':'⌂','public-data':'▤','classification-node':'▦'};
const INSPECTABLE=new Set(['model-object','record-class','classification-node','data-reference']);
function ownText(node){return [node.label,node.meta,node.description,node.source_uid,node.product_record_id].filter(Boolean).join(' ').toLowerCase()}
function siblingCounts(children=[]){const counts=new Map();children.forEach(child=>{const key=normalizeDisplayText(child.label);counts.set(key,(counts.get(key)||0)+1)});return counts}
export function createTreeView({container,countElement,filterElement,contextElement,expandButton,collapseButton,trees,store}){
  const expanded=state=>new Set(state.expandedBySector[state.sector]||[]),currentTree=state=>trees[state.sector]||trees.home;
  function render(state){
    const root=currentTree(state),selectedId=state.selectedNodeBySector[state.sector]||root.id,open=expanded(state),filter=(state.treeFilter||'').toLowerCase().trim();
    countElement.textContent=`${countTreeNodes(root).toLocaleString()} nodes · ${(root.product_count||0).toLocaleString()} linked records`;
    const matchCache=new Map();function branchMatches(node){if(!filter)return true;if(matchCache.has(node.id))return matchCache.get(node.id);const result=ownText(node).includes(filter)||(node.children||[]).some(branchMatches);matchCache.set(node.id,result);return result}
    const lines=[];
    function branch(node,depth=0,duplicates=new Map()){
      if(!branchMatches(node))return;
      const has=(node.children||[]).length>0,isOpen=open.has(node.id)||Boolean(filter),selected=node.id===selectedId,duplicate=(duplicates.get(normalizeDisplayText(node.label))||0)>1;
      const displayLabel=treeDisplayLabel(node,{duplicate}),count=node.product_count?`<span class="product-count">${Number(node.product_count).toLocaleString()}</span>`:'';
      const tooltip=[node.label,node.description].filter(Boolean).join(' — ');
      lines.push(`<div class="tree-node"><div class="tree-line ${selected?'selected':''}" data-node-id="${node.id}" title="${escapeHtml(tooltip)}" style="padding-left:${depth*2}px"><span class="tree-toggle">${has?(isOpen?'−':'▸'):'·'}</span><span class="tree-icon">${icons[node.type]||'□'}</span>${node.priority_rank?`<span class="priority-rank">${String(node.priority_rank).padStart(2,'0')}</span>`:''}<span class="tree-label">${escapeHtml(displayLabel)}</span>${count}<span class="tree-meta">${escapeHtml(node.meta||node.type||'')}</span></div>`);
      if(has&&isOpen){lines.push('<div class="tree-children">');const counts=siblingCounts(node.children);node.children.forEach(child=>branch(child,depth+1,counts));lines.push('</div>')}lines.push('</div>');
    }
    branch(root);container.innerHTML=lines.join('');
    const result=findTreeNode(root,selectedId),selected=result?.node||root;
    contextElement.innerHTML=`<b>Tree:</b> ${escapeHtml(root.label)}<br><b>Selected:</b> ${escapeHtml(treeDisplayLabel(selected))}<br><b>Priority:</b> ${selected.priority_rank||'—'}<br><b>Linked records:</b> ${(selected.product_count||0).toLocaleString()}<br><b>Tool:</b> ${escapeHtml(state.tool)}`;
    container.querySelectorAll('.tree-line').forEach(line=>line.addEventListener('click',event=>{const id=line.dataset.nodeId,found=findTreeNode(root,id)?.node;store.mutate(s=>{const sector=s.sector,arr=new Set(s.expandedBySector[sector]||[]);if(event.target.classList.contains('tree-toggle')&&(found?.children||[]).length){arr.has(id)?arr.delete(id):arr.add(id);s.expandedBySector[sector]=[...arr]}else if(found?.type==='sector-link'&&found.sector){s.sector=found.sector;s.inspectorOpen=false;s.selectedRecordId=null;s.selectedRecordNeedId=null}else{s.selectedNodeBySector[sector]=id;if((found?.children||[]).length)arr.add(id);s.expandedBySector[sector]=[...arr];s.datagrid.page=1;s.datagrid.search='';s.selectedRecordId=null;s.selectedRecordNeedId=null;s.inspectorOpen=INSPECTABLE.has(found?.type)}})}));
  }
  filterElement.addEventListener('input',()=>store.mutate(s=>s.treeFilter=filterElement.value));expandButton.addEventListener('click',()=>store.mutate(s=>{const ids=[];walkTree(currentTree(s),n=>{if((n.children||[]).length)ids.push(n.id)});s.expandedBySector[s.sector]=ids}));collapseButton.addEventListener('click',()=>store.mutate(s=>s.expandedBySector[s.sector]=[currentTree(s).id]));store.subscribe(render);render(store.get());
}
