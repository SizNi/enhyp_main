(()=>{function e(e,t,a,s){Object.defineProperty(e,t,{get:a,set:s,enumerable:!0,configurable:!0})}var t=globalThis.parcelRequireda87,a=t.register;a("gmyca",function(a,s){Object.defineProperty(a.exports,"__esModule",{value:!0,configurable:!0}),e(a.exports,"default",()=>l);var r=t("7ZQJ3"),i=t("lUrVZ"),l={template:`
    <div class="l-fx l-ai-bl">
      <h4 class="fblHead"></h4>
      <div class="fblPanel l-fx">
          <div class="fblDec"></div>
          <span class="fblCount"></span>
          <div class="fblInc"></div>
      </div>
    </div>
    <div class="fblCollection"></div>`,nodes(){return{fblHead:{_text:()=>`${this.param.target.heading}`},fblCount:{_text:()=>`${this.deliver(this.proxy._values,[...this.param.path,"length"])??0}`},fblDec:{component:{src:r.default,params:{size:"mini",options:{icon:"-"}},proxies:{disabled:()=>this.deliver(this.proxy._values,[...this.param.path,"length"])===(this.param.target.collection.minlength||0)},methods:{action:()=>{this.method.remove({path:this.param.path}),this.method.error({key:[...this.param.path,this.deliver(this.proxy._values,[...this.param.path,"length"])].join("_"),value:!1})}}}},fblInc:{component:{src:r.default,params:{size:"mini",options:{icon:"+"}},proxies:{disabled:()=>this.deliver(this.proxy._values,[...this.param.path,"length"])===(this.param.target.collection.maxlength||100)},methods:{action:()=>{this.method.add({target:this.param.target,path:this.param.path})}}}},fblCollection:{component:{src:i.default,iterate:()=>this.deliver(this.proxy._values,this.param.path),params:{name:this.param.name,target:this.param.target,path:(e,t)=>[...this.param.path,t]}}}}},loaded(){let e=this.options.inputs;this.options.props={params:{name:{},target:{},path:{}},proxies:{_values:{store:e.params.name}},methods:{add:{store:e.params.name},remove:{store:e.params.name},error:{store:e.params.name}}}}}}),a("lUrVZ",function(a,s){e(a.exports,"default",()=>l);var r=t("buET6"),i=t("eVNf3"),l={template:`
    <div class="fblContent">
      <div class="fblElements"></div>
      <div class="fblChildren"></div>
    </div>`,nodes(){return{fblContent:{dataset:()=>{let e=this.param.path.at(-1);return"number"==typeof e?{index:e+1}:{}}},fblElements:{component:{induce:()=>this.param.target.elements,src:r.default,params:{elements:this.param.target.elements,name:this.param.name,path:this.param.path,error:this.param.target.error||"",disabled:this.param.target.disabled}}},fblChildren:{component:{src:i.default,iterate:()=>this.param.target.children,induce:()=>!this.param.target.hidden||this.execute({_values:this.proxy._values,path:this.param.path,direction:this.param.target.hidden,exclude:this.exclude}),params:{name:this.param.name,target:e=>e,path:this.param.path}}}}},loaded(){let e=this.options.inputs;this.options.props={params:{name:{},target:{},path:{}},proxies:{_values:{store:e.params.name}}}},created(){// if (!this.deliver(this.proxy._values, this.param.path)) this.method.set({ path: this.param.path, value: {} })
// this.param.target.elements?.forEach(el => {
//   const fullPath = [...this.param.path, el.name]
//   if (!this.deliver(this.proxy._values, fullPath)) this.method.set({ path: fullPath, value: el.value ?? el.default ?? null })
// })
}}}),a("buET6",function(a,s){e(a.exports,"default",()=>i);var r=t("kZ1CG"),i={template:`
    <div class="lstForm">
      <div class="lstFormErr"></div>
      <div class="lstEls l-fx"></div>
    </div>`,params:{errors:[]},proxies:{error:""},nodes(){return{lstForm:{_class:{brError:()=>this.proxy.error}},lstEls:{component:{src:r.default,iterate:()=>this.param.elements,params:{element:e=>e,name:this.param.name,path:this.param.path,size:"medium",disabled:this.param.disabled},methods:{error:(e,t)=>{this.param.errors[e]=t;let a=Object.values(this.param.errors).includes(!0);this.proxy.error=a?this.param.error:"",this.method.error({key:this.param.path.join("_"),value:a})}}}},lstFormErr:{textContent:()=>this.proxy.error}}},methods:{transit(e,t,a){let s=this.param.elements.findIndex(t=>t.name===e);this.node.lstEls.children[s]?.method.transit(t,a)}},loaded(){let e=this.options.inputs;this.options.props={params:{name:{},elements:{type:"Array"},path:{},error:{default:""},disabled:{}},methods:{error:{store:e.params.name}}}}}}),a("kZ1CG",function(t,a){e(t.exports,"default",()=>s);var s={template:`
    <div>
      <div class="lstEl"></div>
    </div>`,proxies:{hidden:!1},params:{fullPath:[],changed:!1},nodes(){return{lstEl:{hidden:()=>this.proxy.hidden,style:()=>({flexBasis:`calc((100% - (11 * var(--xs)))/12 * ${this.param.element.column} + ${this.param.element.column-1} * var(--xs))`}),component:{induce:()=>this.elements[this.param.element.component],src:this.elements[this.param.element.component],proxies:{value:()=>{let e=this.param.element.binding,t=this.deliver(this.proxy._values,this.param.fullPath);return e&&!this.param.changed&&(t=this.execute({_values:this.proxy._values,path:this.param.path,value:t,direction:e,exclude:this.exclude}),this.method.set({path:this.param.fullPath,value:t})),this.param.changed=!1,t},disabled:()=>this.param.element.disabled||this.param.disabled,error:()=>{let{validation:e,required:t}=this.param.element,a=this.deliver(this.proxy._values,this.param.fullPath),s=e&&!this.execute({_values:this.proxy._values,path:this.param.path,value:a,direction:e,exclude:this.exclude}),r=s||t&&(!a||Array.isArray(a)&&!a.length);return this.method.error(this.param.element.name,r),r}},params:{size:this.param.size,name:this.param.element.name,type:this.param.element.type,text:this.param.element.text,options:this.param.element},methods:{change:e=>{this.param.changed=!0,this.method.set({path:this.param.fullPath,value:"number"===this.param.element.type?Number(e):e})},action:(e,t)=>this.method.action({name:e,value:t}),validated:e=>this.method.error(e)}}}}},methods:{hidden(e){this.proxy.hidden=e},transit(e,t){this.node.lstEl.method[e]&&this.node.lstEl.method[e](t)}},loaded(){let e=this.options.inputs;this.options.props={params:{name:{},element:{},size:{},path:{},disabled:{}},proxies:{_values:{store:e.params.name}},methods:{set:{store:e.params.name},action:{store:e.params.name},error:{}}}},created(){this.proxy.hidden=this.param.element.hidden,this.param.fullPath=[...this.param.path,this.param.element.name]}}})})();