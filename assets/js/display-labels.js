const GENERIC_EXACT=new Set([
  'case','cases','certification','certifications','classroom','product','products',
  'product specification','product specifications','specification','specifications',
  'continued','catalog','catalogue','index','catalog number index','part # description',
  'part number description','catalog item','item','items','typ typ','b typ','profiles'
]);
const GENERIC_PATTERNS=[
  /catalog(?:ue)?\s*(?:number)?\s*index/i,
  /product\s*specifications?/i,
  /part\s*#?\s*(?:number)?\s*description/i,
  /^continued\b/i,
  /^certifications?$/i,
  /^classroom$/i,
  /^case$/i,
  /^(?:[a-z]\s+)?typ(?:\s+[a-z]\s+typ)*$/i,
  /^catalog(?:ue)?$/i,
  /^products?$/i
];
export function cleanDisplayText(value=''){
  return String(value??'').replace(/\s+/g,' ').replace(/^[\s·•|:;,._-]+|[\s·•|:;,._-]+$/g,'').trim();
}
export function normalizeDisplayText(value=''){
  return cleanDisplayText(value).toLowerCase().replace(/[^a-z0-9]+/g,' ');
}
export function isLowInformationLabel(value=''){
  const text=cleanDisplayText(value), normalized=normalizeDisplayText(text);
  if(!text || text.length<2 || GENERIC_EXACT.has(normalized)) return true;
  if(GENERIC_PATTERNS.some(pattern=>pattern.test(text))) return true;
  if(!/[a-z0-9]/i.test(text)) return true;
  return false;
}
function compact(value,max=92){
  const text=cleanDisplayText(value);
  return text.length>max?`${text.slice(0,max-1).trim()}…`:text;
}
function meaningfulDescription(value=''){
  const text=cleanDisplayText(value);
  return text && !isLowInformationLabel(text) ? text : '';
}
export function treeDisplayLabel(node,{duplicate=false}={}){
  const original=cleanDisplayText(node?.label||'');
  if(!['product','service'].includes(node?.type)) return original;
  if(!duplicate && !isLowInformationLabel(original)) return original;
  const description=meaningfulDescription(node?.description||'');
  if(description) return compact(description);
  const id=node?.product_record_id||node?.source_uid||node?.id||'record';
  return `Review needed — ${compact(id,58)}`;
}
export function recordDisplayName(row={}){
  const original=cleanDisplayText(row.item_name||row.product_name||row.title||'');
  if(!isLowInformationLabel(original)) return original;
  const description=meaningfulDescription(row.description||row.spec_text||'');
  const model=cleanDisplayText(row.model_part_number||row.part_number||row.source_record_id||'');
  if(description) return compact(model && !description.includes(model)?`${description} — ${model}`:description,120);
  const source=cleanDisplayText(row.source_vendor||row.manufacturer||'Catalog record');
  const category=cleanDisplayText(row.category_original||row.category_group||'');
  return compact([source,category,model||row.record_id].filter(Boolean).join(' — '),120);
}
export function displayCellValue(row,column,formatCell){
  if(['item_name','product_name','title'].includes(column.field)) return recordDisplayName(row);
  return formatCell(row[column.field],column.type);
}
