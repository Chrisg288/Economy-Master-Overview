export function createProductRepository(productIndex){
  const files=new Map(productIndex.files.map(file=>[file.need_id,file]));
  const cache=new Map();
  async function loadJson(path){const response=await fetch(path,{cache:'no-store'});if(!response.ok)throw new Error(`Unable to load ${path}: ${response.status}`);return response.json()}
  async function loadFileSpec(file){const paths=Array.isArray(file.paths)?file.paths:[file.path];const parts=await Promise.all(paths.filter(Boolean).map(loadJson));return parts.flat()}
  async function loadNeed(needId){if(!needId)return[];if(cache.has(needId))return cache.get(needId);const file=files.get(needId);if(!file)return[];const promise=loadFileSpec(file);cache.set(needId,promise);return promise}
  async function loadAll(){const parts=await Promise.all([...files.keys()].map(loadNeed));return parts.flat()}
  async function recordsForNode(node){
    if(!node)return[];
    const f=node.filter||{};
    let records;
    const needId=node.need_id||f.need_id;
    if(f.all_products||node.role==='priority-tree'||node.id==='human-consumer')records=await loadAll();
    else if(needId)records=await loadNeed(needId);
    else return[];
    if(f.category_group_id||node.type==='brick')return records.filter(r=>r.category_group_id===(f.category_group_id||node.id));
    if(f.fulfillment_id||node.role==='fulfillment-class')return records.filter(r=>r.fulfillment_id===(f.fulfillment_id||node.id));
    if(f.need_id||node.role==='need')return records.filter(r=>r.need_id===(f.need_id||node.need_id));
    return records;
  }
  async function recordById(needId,recordId){if(!recordId)return null;const records=needId?await loadNeed(needId):await loadAll();return records.find(r=>r.record_id===recordId)||null}
  async function recordForNode(node){const rows=await recordsForNode(node);return rows[0]||null}
  return{index:productIndex,loadNeed,loadAll,recordsForNode,recordForNode,recordById,cachedNeeds:()=>[...cache.keys()]};
}
