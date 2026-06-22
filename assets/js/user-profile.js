
import {escapeHtml} from './utils.js';
export function renderUserProfile({state,store,selectedNode}){
  const p=state.userProfile;
  const field=(id,label,value,min=0,max=100)=>`<div class="profile-field"><label for="${id}">${escapeHtml(label)} <output>${value}</output></label><input id="${id}" data-profile-field="${id}" type="range" min="${min}" max="${max}" value="${value}"></div>`;
  const html=`<div class="workspace-card"><h2>User Profile Lens</h2><p>The profile changes how the selected need is assessed. It does not add duplicate branches to the needs TreeView.</p><div class="profile-form"><div class="profile-field"><label>Selected Need</label><strong>${escapeHtml(selectedNode.label)}</strong><p>${escapeHtml(selectedNode.description||'')}</p></div><div class="profile-field"><label for="profileLocation">Location / Standing</label><select id="profileLocation" data-profile-select="location"><option>Personal / Local</option><option>Municipal</option><option>Provincial / State</option><option>National</option><option>International</option></select></div><div class="profile-field"><label for="budget">Maximum Budget <output>${p.budget}</output></label><input id="budget" data-profile-field="budget" type="range" min="0" max="10000" step="100" value="${p.budget}"></div>${field('riskTolerance','Risk Tolerance',p.riskTolerance)}${field('priceWeight','Price Importance',p.priceWeight)}${field('fulfillmentWeight','Fulfillment Importance',p.fulfillmentWeight)}${field('durabilityWeight','Durability Importance',p.durabilityWeight)}${field('availabilityWeight','Availability Importance',p.availabilityWeight)}</div></div>`;
  queueMicrotask(()=>{
    document.querySelectorAll('[data-profile-field]').forEach(input=>input.addEventListener('input',()=>store.mutate(s=>s.userProfile[input.dataset.profileField]=Number(input.value))));
    const select=document.querySelector('[data-profile-select="location"]'); if(select){select.value=p.location;select.addEventListener('change',()=>store.mutate(s=>s.userProfile.location=select.value));}
  });
  return html;
}
