
export function escapeHtml(value=''){
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
export function downloadJson(filename, value){
  const blob = new Blob([JSON.stringify(value,null,2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download=filename; a.click();
  setTimeout(()=>URL.revokeObjectURL(url),500);
}
export function walkTree(root, fn, path=[]){
  fn(root,path);
  (root.children||[]).forEach(child=>walkTree(child,fn,[...path,root]));
}
export function findTreeNode(root,id,path=[]){
  if(!root) return null;
  if(root.id===id) return {node:root,path:[...path,root]};
  for(const child of root.children||[]){ const found=findTreeNode(child,id,[...path,root]); if(found) return found; }
  return null;
}
export function countTreeNodes(root){ let count=0; walkTree(root,()=>count++); return count; }
export function formatCell(value,type){
  if(value===null || value===undefined || value==='') return '';
  if(type==='currency') return typeof value==='number' ? new Intl.NumberFormat('en-CA',{style:'currency',currency:'CAD',maximumFractionDigits:0}).format(value) : value;
  return String(value);
}
