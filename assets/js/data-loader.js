
async function loadJson(path){
  const response = await fetch(path,{cache:'no-store'});
  if(!response.ok) throw new Error(`Unable to load ${path}: ${response.status}`);
  return response.json();
}
export async function loadApplicationData(){
  const app = await loadJson('data/config/app.json');
  const ribbon = await loadJson(app.data_files.ribbon);
  const treeIndex = await loadJson(app.data_files.tree_index);
  const treeEntries = await Promise.all(Object.entries(treeIndex).map(async ([key,path])=>[key,await loadJson(path)]));
  const [columns,records,sources,processedAssets,needSourceMap] = await Promise.all([
    loadJson(app.data_files.comparator_columns),
    loadJson(app.data_files.comparator_records),
    loadJson(app.data_files.source_inventory),
    loadJson(app.data_files.processed_assets),
    loadJson(app.data_files.need_source_map)
  ]);
  return {app,ribbon,trees:Object.fromEntries(treeEntries),columns,records,sources,processedAssets,needSourceMap};
}
