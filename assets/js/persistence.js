
export function attachPersistence(store){
  const key='economy-master-modular-rebuild-v0.1';
  try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved)store.mutate(s=>Object.assign(s,saved));}catch{}
  store.subscribe(state=>{try{localStorage.setItem(key,JSON.stringify(state));}catch{}});
}
