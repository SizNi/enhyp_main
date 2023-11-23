var e;(0,(e=globalThis.parcelRequireda87).register)("5DlNz",function(t,s){Object.defineProperty(t.exports,"__esModule",{value:!0,configurable:!0}),Object.defineProperty(t.exports,"default",{get:()=>a,set:void 0,enumerable:!0,configurable:!0});var a={template:`
  <label class="lstCheckbox">
    <input type="checkbox" class="lstCheckboxInp">
    <span class="lstCheckmark"></span>
    <span class="lstCheckboxText"></span>
  </label>`,directives:{_attr:e("1L9sq")._attr},props:{proxies:{value:{},disabled:{},error:{}},params:{size:{default:"small"},text:{}},methods:{change:{}}},nodes(){return{lstCheckbox:{_attr:{size:this.param.size}},lstCheckboxInp:{checked:()=>this.proxy.value,onchange:e=>{this.proxy.value=e.target.checked,this.method.change&&this.method.change(e.target.checked)}},lstCheckboxText:{_text:()=>this.param.text??""}}},methods:{set(e){this.proxy.value=e}}}});