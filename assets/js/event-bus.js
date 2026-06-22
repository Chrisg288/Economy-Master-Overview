
import {escapeHtml,countTreeNodes,findTreeNode} from './utils.js';
export function createBottomDock({summary,event,evidence,trees,sources,processedAssets,products,store}){
  function render(state){
    const tree=trees[state.sector]||trees.home, selected=findTreeNode(tree,state.selectedNodeBySector[state.sector]||tree.id)?.node||tree;
    summary.innerHTML=`<span class="ok">TREE</span> ${countTreeNodes(tree)} nodes &nbsp; | &nbsp; <span class="ok">SOURCES</span> ${sources.length} &nbsp; | &nbsp; <span class="ok">RECORDS</span> ${products.index.record_count.toLocaleString()} &nbsp; | &nbsp; <span class="ok">SELECTED</span> ${escapeHtml(selected.label)}`;
    event.innerHTML=state.events.map(e=>`<span class="${e.level}">●</span> ${escapeHtml(e.text)}`).join('<br>');
    evidence.innerHTML=state.evidence.map(e=>`<span class="${e.level}">✓</span> ${escapeHtml(e.text)}`).join('<br>')+`<br><span class="ok">✓</span> ${processedAssets.length} processed-asset entries retained.`;
  }
  store.subscribe(render); render(store.get());
}
