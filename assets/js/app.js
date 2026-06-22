
import {loadApplicationData} from './data-loader.js';
import {store} from './state.js';
import {createRibbon} from './ribbon.js';
import {createTreeView} from './treeview.js';
import {createWorkspace} from './workspace.js';
import {createInspector} from './inspector.js';
import {createBottomDock} from './event-bus.js';
import {attachPersistence} from './persistence.js';

async function start(){
  try{
    const data=await loadApplicationData();
    document.getElementById('appTitle').textContent=data.app.title;
    document.getElementById('appSubtitle').textContent=data.app.subtitle;
    const defaultColumns=data.columns.filter(c=>c.default_visible).map(c=>c.field);
    store.mutate(s=>{if(!s.datagrid.visibleColumns.length)s.datagrid.visibleColumns=defaultColumns;});
    attachPersistence(store);
    createRibbon(document.getElementById('contextRibbon'),data.ribbon,store);
    createTreeView({container:document.getElementById('treeView'),countElement:document.getElementById('treeNodeCount'),filterElement:document.getElementById('treeFilter'),contextElement:document.getElementById('treeContext'),expandButton:document.getElementById('expandTree'),collapseButton:document.getElementById('collapseTree'),trees:data.trees,store});
    createWorkspace({viewport:document.getElementById('workspaceViewport'),breadcrumb:document.getElementById('workspaceBreadcrumb'),actions:document.getElementById('workspaceActions'),trees:data.trees,columns:data.columns,records:data.records,sources:data.sources,processedAssets:data.processedAssets,store});
    createInspector({container:document.getElementById('inspectorBody'),exportButton:document.getElementById('exportSelection'),trees:data.trees,store});
    createBottomDock({summary:document.getElementById('summaryDock'),event:document.getElementById('eventDock'),evidence:document.getElementById('evidenceDock'),trees:data.trees,sources:data.sources,processedAssets:data.processedAssets,store});
  }catch(error){
    console.error(error);
    document.getElementById('workspaceViewport').innerHTML=`<div class="empty-state"><div><h2>Unable to load modular data</h2><p>${error.message}</p><p>Open this project through GitHub Pages or run <code>serve_local.bat</code>.</p></div></div>`;
  }
}
start();
