export function createProductRepository(productIndex){
  const files=new Map(productIndex.files.map(file=>[file.need_id,file]));
  const cache=new Map();
  async function loadJson(path){const response=await fetch(path,{cache:'no-store'});if(!response.ok)throw new Error(`Unable to load ${path}: ${response.status}`);return response.json()}
  async function loadFileSpec(file){const paths=Array.isArray(file.paths)?file.paths:[file.path];const parts=await Promise.all(paths.filter(Boolean).map(loadJson));return parts.flat()}
  async function loadNeed(needId){if(!needId)return[];if(cache.has(needId))return cache.get(needId);const file=files.get(needId);if(!file)return[];const promise=loadFileSpec(file);cache.set(needId,promise);return promise}
  async function loadAll(){const parts=await Promise.all([...files.keys()].map(loadNeed));return parts.flat()}
  async function recordsForNode(node){if(!node)return[];const f=node.filter||{};let records;if(f.all_products||node.type==='priority-tree'||node.id==='human-consumer')records=await loadAll();else if(node.need_id)records=await loadNeed(node.need_id);else return[];if(f.record_id||node.product_record_id)return records.filter(r=>r.record_id===(f.record_id||node.product_record_id));if(f.page_id)return records.filter(r=>r.page_id===f.page_id);if(f.category_group_id)return records.filter(r=>r.category_group_id===f.category_group_id);if(f.fulfillment_id||node.type==='fulfillment-class')return records.filter(r=>r.fulfillment_id===(f.fulfillment_id||node.id));if(f.need_id||node.type==='need')return records.filter(r=>r.need_id===(f.need_id||node.need_id));return records}
  async function recordForNode(node){const rows=await recordsForNode(node);return rows[0]||null}
  return{index:productIndex,loadNeed,loadAll,recordsForNode,recordForNode,cachedNeeds:()=>[...cache.keys()]};
}
