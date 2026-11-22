/* Gold Berlin — GitHub Pages data layer: reads data.json (written by the scheduled tasks) */
(function(){
  window.__RO=true;
  var cache=null, subs=[], CLAUDE_URL='https://claude.ai/artifact/KNRjhdAwiUc4yZW9JXuwgd';
  function snap(name){var arr=(cache&&cache[name])||[];return{size:arr.length,empty:!arr.length,docs:arr.map(function(d){var c={};for(var k in d)if(k!=='_id')c[k]=d[k];return{id:d._id,exists:true,data:function(){return c;}};}),docChanges:function(){return[];},metadata:{fromCache:false}};}
  function emit(){subs.forEach(function(s){try{s.cb(snap(s.name));}catch(e){}});}
  var busy=false;
  function getJ(u){return fetch(u+'?t='+Date.now(),{cache:'no-store'}).then(function(r){if(r.status===404)return null;if(!r.ok)throw new Error('http '+r.status);return r.json();});}
  function load(){ if(busy)return; busy=true;
    getJ('data.json').then(function(idx){ idx=idx||{months:[]}; var ms=idx.months||[];
        return Promise.all(ms.map(function(m){return Promise.all([getJ('data/prices-'+m+'.json'),getJ('data/spot-'+m+'.json')]);})).then(function(parts){
          var P=[],S=[]; parts.forEach(function(x){P=P.concat(x[0]||[]);S=S.concat(x[1]||[]);});
          var j={updated:idx.updated,prices:P,spot:S,alerts:idx.alerts||[],notifications:idx.notifications||[]};
          var sig=JSON.stringify([j.updated,P.length,S.length,(S[S.length-1]||{}).ts,(P[P.length-1]||{}).ts,j.alerts.length,j.notifications.length]);
          var changed=!cache||cache.__sig!==sig; j.__sig=sig; cache=j; if(changed) emit(); });
      })
      .catch(function(e){subs.forEach(function(s){if(s.err&&!cache)try{s.err(e);}catch(x){}});})
      .then(function(){busy=false;});
  }
  function col(name){var q={orderBy:function(){return q;},limit:function(){return q;},where:function(){return q;},
      onSnapshot:function(cb,err){var s={name:name,cb:cb,err:err};subs.push(s);if(cache)setTimeout(function(){cb(snap(name));},0);else load();return function(){subs=subs.filter(function(x){return x!==s;});};},
      doc:function(id){return ref(name+'/'+id);}};return q;}
  function ro(){var e=new Error('read_only');e.code='read_only';return Promise.reject(e);}
  function ref(){return{set:ro,update:ro,delete:ro,onSnapshot:function(cb){setTimeout(function(){cb({exists:false,data:function(){}});},0);return function(){};}};}
  window.claude={use:function(n){return Promise.resolve(n==='db'?{collection:col,doc:ref}:null);}};
  setInterval(load,5*60*1000);
  document.addEventListener('visibilitychange',function(){if(!document.hidden)load();});
  window.addEventListener('focus',load); window.addEventListener('pageshow',load);
  document.addEventListener('DOMContentLoaded',function(){
    var b=document.getElementById('f-save'); if(!b)return;
    var g=b.closest('.group'), sh=g&&g.previousElementSibling;
    if(g){g.style.display='none';}
    var note=document.createElement('div'); note.className='group';
    note.innerHTML='<div class="cell plain" style="display:block;padding:16px"><div style="font-weight:700;margin-bottom:6px">Add or change alerts</div><div class="s" style="white-space:normal;color:#8e8e93;font-size:.86rem;line-height:1.45;margin-bottom:12px">Alerts are saved in the Claude version of the app. Open it to add, switch off or delete an alert — they show up here automatically.</div><a class="btn fill" data-noi18n-href href="'+CLAUDE_URL+'" target="_blank" rel="noopener" style="display:block;text-align:center;text-decoration:none">Open in Claude</a></div>';
    if(g&&g.parentNode) g.parentNode.insertBefore(note,g.nextSibling);
    var st=document.createElement('style'); st.textContent='#a-list .toggle,#a-list .del{display:none!important}'; document.head.appendChild(st);
  });
})();
