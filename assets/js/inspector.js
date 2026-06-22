
import {escapeHtml,findTreeNode,downloadJson} from './utils.js';
export function createInspector({container,exportButton,trees,store}){
  let current=null;
  function render(state){
    const tree=trees[state.sector]||trees.home; current=findTreeNode(tree,state.selectedNodeBySector[state.sector]||tree.id)?.node||tree;
    container.innerHTML=`<div class="inspector-title"><span class="status-badge">${escapeHtml((current.type||'object').toUpperCase())}</span><h3>${escapeHtml(current.label)}</h3><span class="status-badge">${escapeHtml(state.sector)}</span><span class="status-badge">${escapeHtml(state.tool)}</span></div><div class="inspector-actions"><button class="compact-button">NEW</button><button class="compact-button">OPEN</button><button class="compact-button">EDIT</button><button class="compact-button">SAVE</button></div><div class="inspector-actions"><button class="compact-button">SIMULATE</button><button class="compact-button">ASSESS</button><button class="compact-button">DOCUMENT</button><button class="compact-button">COMPARE</button></div><div class="module-note">Standard activity layer: every category should support New, Open, Edit, Save, Simulate, Assess and Document.</div><h4>IDENTITY</h4><table class="property-table"><tr><td>Name</td><td>${escapeHtml(current.label)}</td></tr><tr><td>Class</td><td>${escapeHtml(current.type||'')}</td></tr><tr><td>Sector</td><td>${escapeHtml(state.sector)}</td></tr><tr><td>Scope</td><td>${escapeHtml(state.scope)}</td></tr><tr><td>Overlay</td><td>${escapeHtml(state.overlay)}</td></tr><tr><td>Tool</td><td>${escapeHtml(state.tool)}</td></tr><tr><td>Priority</td><td>${current.priority_rank||'—'}</td></tr><tr><td>Description</td><td>${escapeHtml(current.description||'')}</td></tr></table>`;
  }
  exportButton.addEventListener('click',()=>current&&downloadJson('selected-economy-object.json',current));
  store.subscribe(render); render(store.get());
}
