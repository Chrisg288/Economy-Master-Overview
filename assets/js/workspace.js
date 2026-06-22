
import {escapeHtml,findTreeNode} from './utils.js';
import {renderDatagrid} from './datagrid.js';
import {renderUserProfile} from './user-profile.js';
function polar(cx,cy,r,angle){const rad=(angle-90)*Math.PI/180;return{x:cx+r*Math.cos(rad),y:cy+r*Math.sin(rad)}}
function arcPath(cx,cy,r,start,end){const a=polar(cx,cy,r,end),b=polar(cx,cy,r,start),large=end-start<=180?0:1;return `M ${cx} ${cy} L ${b.x} ${b.y} A ${r} ${r} 0 ${large} 1 ${a.x} ${a.y} Z`}
function homeView(state,store){
  const sectors=[['human','HUMAN / CONSUMER','#fff8bd'],['public','PUBLIC / GOVERNMENT','#f5b26f'],['finance','FINANCE / CAPITAL','#76a4d8'],['business','BUSINESS / COMMERCIAL','#b4a5c9'],['market','MARKET / EXCHANGE','#8ce6b1']];
  const cx=310,cy=230,r=175,start=-36;
  const wedges=sectors.map((s,i)=>{const a=start+i*72,b=a+72,mid=(a+b)/2,pos=polar(cx,cy,110,mid);return `<g class="wheel-sector ${state.sector===s[0]?'active':''}" data-sector-id="${s[0]}"><path d="${arcPath(cx,cy,r,a,b)}" fill="${s[2]}" stroke="#173c50" stroke-width="1.5"></path><text x="${pos.x}" y="${pos.y-7}" class="wheel-label">${s[1].split(' / ')[0]}</text><text x="${pos.x}" y="${pos.y+12}" class="wheel-label">${s[1].split(' / ')[1]||''}</text></g>`}).join('');
  const html=`<div class="home-layout"><div class="home-canvas"><svg class="home-wheel" viewBox="0 0 620 470" role="img" aria-label="Five-sector economy orientation wheel">${wedges}<circle cx="${cx}" cy="${cy}" r="55" fill="#fff" stroke="#173c50" stroke-width="2"></circle><text x="${cx}" y="${cy-4}" class="wheel-label">ECONOMY</text><text x="${cx}" y="${cy+15}" class="wheel-label">HOME</text></svg></div><div class="home-notes"><div class="workspace-card"><h3>Start here</h3><p>Select a sector wedge or ribbon sector. The selected Tool remains independently controlled.</p></div><div class="workspace-card"><h3>Human / Consumer</h3><p>Uses a survival-priority needs tree, from most important need to least important want.</p></div><div class="workspace-card"><h3>Comparator</h3><p>Datagrid mode lets the user choose columns and sort options to determine value and fulfillment.</p></div></div></div>`;
  queueMicrotask(()=>document.querySelectorAll('[data-sector-id]').forEach(g=>g.addEventListener('click',()=>store.mutate(s=>s.sector=g.dataset.sectorId))));
  return html;
}
function needsView(selectedNode){return `<div class="needs-layout"><div class="priority-diagram"><div class="title">LIST USER<br>WANTS / NEEDS</div><div>MOST IMPORTANT</div><div class="arrow">↓</div><div class="tree-word">HIERARCHICAL<br>TREEVIEW</div><div class="arrow">↓</div><div>LEAST IMPORTANT</div></div><div><div class="workspace-card"><h2>${escapeHtml(selectedNode.label)}</h2><p>This is a need-first navigation path, not a product-category dump.</p><p><strong>Priority:</strong> ${selectedNode.priority_rank||'Tree root'}</p><p><strong>Purpose:</strong> ${escapeHtml(selectedNode.description||'Select a branch to identify what can fulfill the user need.')}</p></div><div class="info-grid"><div class="info-tile"><h4>Identify</h4><p>Find the user need quickly.</p></div><div class="info-tile"><h4>Map</h4><p>Map catalogs, offers and evidence to that need.</p></div><div class="info-tile"><h4>Compare</h4><p>Sort relevant options by selected value columns.</p></div></div></div></div>`}
function genericView(selectedNode,state){return `<div class="workspace-card"><h2>${escapeHtml(selectedNode.label)}</h2><p>${escapeHtml(selectedNode.description||'Modular workspace view for the selected node.')}</p><div class="info-grid"><div class="info-tile"><h4>Sector</h4><p>${escapeHtml(state.sector)}</p></div><div class="info-tile"><h4>Scope</h4><p>${escapeHtml(state.scope)}</p></div><div class="info-tile"><h4>Overlay</h4><p>${escapeHtml(state.overlay)}</p></div></div></div>`}
function sourceLibraryView({selectedNode,sources,processedAssets,state,store}){
  const filter=selectedNode.filter?.source_group;
  const filtered=filter?sources.filter(s=>s.source_group===filter):sources;
  const counts={catalog:sources.filter(s=>s.source_group==='catalog').length,official:sources.filter(s=>s.source_group==='official').length,reference:sources.filter(s=>s.source_group==='reference').length,target:sources.filter(s=>s.source_group==='target').length};
  const sourceCols=[{field:'uid',label:'UID',type:'text',default_visible:true},{field:'title',label:'Source',type:'text',default_visible:true},{field:'vendor',label:'Vendor',type:'text',default_visible:true},{field:'source_type',label:'Type',type:'text',default_visible:true},{field:'domain',label:'Domain',type:'text',default_visible:true},{field:'status',label:'Status',type:'text',default_visible:true},{field:'priority',label:'Priority',type:'text',default_visible:true},{field:'recommended_path',label:'Repository Path',type:'text',default_visible:false}];
  return `<div class="source-summary"><div class="source-stat"><strong>${sources.length}</strong>Compiled sources</div><div class="source-stat"><strong>${counts.catalog}</strong>Catalogs</div><div class="source-stat"><strong>${counts.official}</strong>Official/open data</div><div class="source-stat"><strong>${processedAssets.length}</strong>Processed assets</div></div>${renderDatagrid({state,store,columns:sourceCols,rows:filtered,title:selectedNode.label,description:'Source inventory is separate from the Human needs tree. It supports the tree without replacing it.'})}`;
}
export function createWorkspace({viewport,breadcrumb,actions,trees,columns,records,sources,processedAssets,store}){
  function selected(state){const tree=trees[state.sector]||trees.home;return findTreeNode(tree,state.selectedNodeBySector[state.sector]||tree.id)||{node:tree,path:[tree]};}
  function actionBar(state,node){
    const common=[['Add Tree Node',''],['Grid Proposal',''],['Delete Local Node','danger'],['Add Object',''],['Workspace Editor',''],['PDCA Checks',''],['Export Workspace','success'],['Import Workspace',''],['Shared Data Sample',''],['Edit Object',''],['Save Local','success'],['Raise VRQ','warning'],['Clear Selection','']];
    actions.innerHTML=common.map(([label,cls])=>`<button class="action-button ${cls}">${label}</button>`).join('');
  }
  function render(state){
    const {node,path}=selected(state); breadcrumb.textContent=path.map(n=>n.label).join(' / '); actionBar(state,node);
    if(state.sector==='home' && state.tool==='swimlane'){viewport.innerHTML=homeView(state,store);return;}
    if(node.type==='source-library'||node.type==='source-filter'){viewport.innerHTML=sourceLibraryView({selectedNode:node,sources,processedAssets,state,store});return;}
    if(node.type==='processed-assets'){
      const assetCols=[{field:'name',label:'Processed Asset',type:'text',default_visible:true},{field:'repo_path',label:'Repository Path',type:'text',default_visible:true},{field:'status',label:'Status',type:'text',default_visible:true},{field:'artifact',label:'Package',type:'text',default_visible:true}];
      viewport.innerHTML=renderDatagrid({state,store,columns:assetCols,rows:processedAssets,title:'Processed GitHub Assets',description:'Known processed packages and repository paths from prior work.'});return;
    }
    if(state.tool==='datagrid'||state.tool==='compare-transact'){
      const needId=node.need_id||((node.type==='priority-tree')?null:node.id.startsWith('need-')?node.id:null);
      const filtered=needId?records.filter(r=>r.need_id===needId):records;
      viewport.innerHTML=renderDatagrid({state,store,columns,rows:filtered,title:state.tool==='compare-transact'?'Compare / Transact Datagrid':'Comparator Datagrid',description:'Choose visible columns. Click a header for primary sort; Shift-click adds secondary sort.'});return;
    }
    if(state.tool==='user-profile'){viewport.innerHTML=renderUserProfile({state,store,selectedNode:node});return;}
    if(node.type==='priority-tree'||node.type==='need'||node.type==='fulfillment-class'){viewport.innerHTML=needsView(node);return;}
    if(state.tool==='model'){viewport.innerHTML=`<div class="workspace-card"><h2>Model</h2><p>Plan objects, flows, requirements and records for ${escapeHtml(node.label)}.</p><div class="module-note">MODEL → SIMULATE → ASSESS → COMPARE / TRANSACT → RECORD → IMPROVE</div></div>`;return;}
    if(state.tool==='simulate'){viewport.innerHTML=`<div class="workspace-card"><h2>Simulate</h2><p>Scenario, demand, capacity, cost, time and risk testing for ${escapeHtml(node.label)}.</p></div>`;return;}
    if(state.tool==='assess'){viewport.innerHTML=`<div class="workspace-card"><h2>Assess</h2><p>Value, evidence, capability, risk and credit assessment for ${escapeHtml(node.label)}.</p></div>`;return;}
    if(state.tool==='objects-definitions'){viewport.innerHTML=`<div class="workspace-card"><h2>Objects / Definitions</h2><p>Class-aware object authoring and schema definitions for ${escapeHtml(node.label)}.</p></div>`;return;}
    viewport.innerHTML=genericView(node,state);
  }
  store.subscribe(render); render(store.get());
}
