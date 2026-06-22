const initial={
  sector:'home',scope:'personal',overlay:'law-rights',tool:'swimlane',
  selectedNodeBySector:{home:'economy-home',human:'human-needs',market:'market-exchange',business:'business-commercial',finance:'finance-capital',public:'public-government'},
  expandedBySector:{home:['economy-home'],human:['human-consumer','human-needs'],market:['market-exchange'],business:['business-commercial'],finance:['finance-capital'],public:['public-government']},
  treeFilter:'',
  datagrid:{visibleColumns:[],sorts:[{field:'need_rank',direction:'asc'},{field:'need_match_score',direction:'desc'},{field:'risk',direction:'desc'}],columnsOpen:false,search:'',page:1,pageSize:100},
  userProfile:{budget:2500,location:'Personal / Local',riskTolerance:45,priceWeight:60,fulfillmentWeight:90,durabilityWeight:65,availabilityWeight:70},
  events:[{level:'ok',text:'19,009 linked English product and service records loaded into the modular Human tree and Comparator datagrid.'}],
  evidence:[{level:'ok',text:'Tree selection filters the datagrid; datagrid row selection returns to the exact product or service tree node.'}]
};
class Store{constructor(value){this.value=structuredClone(value);this.listeners=new Set()}get(){return this.value}update(patch){this.value={...this.value,...patch};this.emit()}mutate(fn){fn(this.value);this.emit()}subscribe(fn){this.listeners.add(fn);return()=>this.listeners.delete(fn)}emit(){this.listeners.forEach(fn=>fn(this.value))}}
export const store=new Store(initial);
