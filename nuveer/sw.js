/* Nuveer app — offline copy of the site. Photos have content-hashed names, so they never go stale. */
const VERSION = "v204";
const CACHE = 'nuveer-' + VERSION;
const FILES = ["./", "index.html", "manifest.webmanifest", "img/0092d38c61b62d.jpg", "img/026a93299ecb53.jpg", "img/036c9d6ec128ca.jpg", "img/0479d1cbc9ef93.jpg", "img/04ca3d5178e769.jpg", "img/05c5b0ef5d2cb1.jpg", "img/05ecefd46fc112.jpg", "img/05f8d63e1e4829.jpg", "img/06f5050211a783.jpg", "img/06f94df1970076.jpg", "img/0856658b0b2190.jpg", "img/086b87b8ecc725.jpg", "img/08ab8acb6d09a8.jpg", "img/0a3aa1e5100572.jpg", "img/0b731c8517f609.jpg", "img/0c24a4c5066679.jpg", "img/0d168f63017fd7.jpg", "img/0d9338b5ea84ce.jpg", "img/107e6c6e308e18.jpg", "img/10a32772f78733.jpg", "img/13001d357f68b7.jpg", "img/131ef27b43787d.jpg", "img/17a0c0e491c1eb.jpg", "img/17ecb832b08271.jpg", "img/182b54a175b01d.jpg", "img/187714b9e84ba2.jpg", "img/18805170539e5b.jpg", "img/1ba019236e2ae9.jpg", "img/1caa5cbfdb51fb.jpg", "img/1cfc800646a08f.jpg", "img/1d20ffd36a050e.jpg", "img/1de408a705dca2.jpg", "img/1e4593852976b7.jpg", "img/1ee3f176ba0de2.jpg", "img/2088031694ec90.jpg", "img/22b49dde282ad4.jpg", "img/2319bd20f7745f.jpg", "img/238b52fd78b05e.jpg", "img/2417b54a5cc83a.jpg", "img/24ac3224e59807.jpg", "img/25ae060680e810.jpg", "img/270963a395ae7c.jpg", "img/272737db8803cd.jpg", "img/274d2419915c0b.jpg", "img/2832ef8f25b71a.jpg", "img/28e241cd80c0d0.jpg", "img/295358e2011a2a.jpg", "img/29b2abbda75096.jpg", "img/2a4ec0351804d6.jpg", "img/2beb934b9cb881.jpg", "img/2c27f7eb3a50fe.jpg", "img/2c871908525330.jpg", "img/2d0393dfe7a3fe.jpg", "img/2d2302ceea8329.jpg", "img/2e68f0338a9671.jpg", "img/2e8390d5ff915d.jpg", "img/30020631e49e57.jpg", "img/31b6e5d2b362da.jpg", "img/31ce874c0defd4.jpg", "img/32a10f58f55d1e.jpg", "img/36005d02067246.jpg", "img/366d4c60f0fbea.jpg", "img/36991a183286d8.jpg", "img/37c96ed87872a0.jpg", "img/380ef8672c87d0.jpg", "img/388079110f6953.jpg", "img/389572af18d261.jpg", "img/38a947148d13df.jpg", "img/390b9fc1e20082.jpg", "img/39230a43040a15.jpg", "img/394624ea7f8cd0.jpg", "img/39d4053880d870.jpg", "img/3a2f049c3c1bdc.jpg", "img/3a5061c5849e3c.jpg", "img/3ba7f7697e039e.jpg", "img/3bed3e0ae70261.jpg", "img/3cfa32aa13bf86.jpg", "img/3e0dd748421a2a.jpg", "img/3f5bd60ad3061b.jpg", "img/407862a276b1a4.jpg", "img/407989d332988a.jpg", "img/40e27a0db5f945.jpg", "img/42013eb54ddfdf.jpg", "img/4264cab762b262.jpg", "img/44fed480f909a8.jpg", "img/45cb053d03498f.jpg", "img/45dc5daf1d0424.jpg", "img/4612f79765835c.jpg", "img/4653d61b739423.jpg", "img/47249ca37f67a2.jpg", "img/47f0c372fb4ce6.jpg", "img/492697f65f353f.jpg", "img/4aef2fc04c174d.jpg", "img/4b006dae3ad15f.jpg", "img/4b0de46ff130e4.jpg", "img/4b395f09f7cd78.jpg", "img/4c8a07414efe27.jpg", "img/4cc02bf81683bc.jpg", "img/4cd26343645158.jpg", "img/4d56a4ba8f1dfd.jpg", "img/4df3f75a818e8f.jpg", "img/4e75b281951d5b.jpg", "img/500658a3f13c52.jpg", "img/50321a3618cce4.jpg", "img/50d27b72a7d77c.jpg", "img/5157ab8d89cdd3.jpg", "img/51bf509efcfdd2.jpg", "img/5252543ed27f8d.jpg", "img/5411591260d14a.jpg", "img/554b324a654882.jpg", "img/5598d132ff3d01.jpg", "img/55fc5333be56b9.jpg", "img/568ac52eb82af3.jpg", "img/57c8afa3f92ebb.jpg", "img/5967c7d9f542b6.jpg", "img/596a4e39a14e8b.jpg", "img/5bbff736f4b9a4.jpg", "img/5bf3be4f361991.jpg", "img/5de41f73d2e8af.jpg", "img/5e11c765a48224.jpg", "img/5e309be8d152f5.jpg", "img/5e3845443dc857.jpg", "img/5ee1283f382e45.jpg", "img/62005a38183219.jpg", "img/62e89118927122.jpg", "img/6402773f43b8d4.jpg", "img/643c76f277294d.jpg", "img/65015a50774c1b.jpg", "img/65f0c8611cae1b.jpg", "img/67846b6dd0824a.jpg", "img/67a1e4ad68e600.jpg", "img/67b0fa9742e5d1.jpg", "img/67b83c1b4fef20.jpg", "img/6840b8fb3fc1e6.jpg", "img/696e1c12507a4d.jpg", "img/6aab834e406848.jpg", "img/6b861ab81ab32d.jpg", "img/6c6743cf607ba9.jpg", "img/6c6c0102d58c79.jpg", "img/6d0ae151215427.jpg", "img/6d257d05105bfd.jpg", "img/71640b286d8ad7.jpg", "img/71f26775fe0dbd.jpg", "img/7254bff1fc7438.jpg", "img/7434b2df372b6d.jpg", "img/74ab5c80aeed71.jpg", "img/750d8b81078509.jpg", "img/756fee09e60185.jpg", "img/7627ed53b35394.jpg", "img/76e9e5c0c27bdf.jpg", "img/78f1b167edab95.jpg", "img/7988d27afc0e92.jpg", "img/7a1f79d6a99a8e.jpg", "img/7ae37063795006.jpg", "img/7b3f86c4eb46bc.jpg", "img/7b980bcfb1ff01.jpg", "img/7ced67ee594d63.jpg", "img/7e3136d1e76b36.jpg", "img/7e33f4874eef84.jpg", "img/801c02f7e6bd65.jpg", "img/80d70a4a16595c.jpg", "img/8172ad26fd4de4.jpg", "img/8271a10656cb97.jpg", "img/831e9aa38109e4.jpg", "img/841db491b7d446.jpg", "img/852bb03557da32.jpg", "img/85af56e99f456b.jpg", "img/87900a6ed2cf25.jpg", "img/881c80e18c00ec.jpg", "img/8852be43bea1fc.jpg", "img/88b1a842a38da7.jpg", "img/88fbbcf2d62584.jpg", "img/89e6ae05420d76.jpg", "img/8a8eaba5696be1.jpg", "img/8ca0ef616d00fa.jpg", "img/8cf551fba761ed.jpg", "img/8d69cceda080ec.jpg", "img/8dd0db68294bd2.jpg", "img/8e37316b005e1c.jpg", "img/8fc48bdaa4091f.jpg", "img/8fff273c65fc18.jpg", "img/9130d2456d6959.jpg", "img/91cc0f2975485b.jpg", "img/930234ac1e0aac.jpg", "img/9339169ffd5131.jpg", "img/9345e4189c2eb8.jpg", "img/934f17c9d65cc0.jpg", "img/93b2e67857e4ce.jpg", "img/93d2840cf7e3f7.jpg", "img/94528ccd497b2b.jpg", "img/95dc0dbdd8be72.jpg", "img/97a5f6df7c2474.jpg", "img/98a1ea3554372b.jpg", "img/98a8ad5aedb3a9.jpg", "img/98aaa68fffe359.jpg", "img/98cc87455efa5b.jpg", "img/98ec4aa280b8c7.jpg", "img/9a806b4174d9f2.jpg", "img/9de26394ec7380.jpg", "img/9de7ae367f0aa9.jpg", "img/9ef455a6585fa8.jpg", "img/a1092c219bf4c2.jpg", "img/a131a52dd32615.jpg", "img/a35201b5498551.jpg", "img/ab643c8542044c.jpg", "img/ae44bab3673235.jpg", "img/aeefa84d30ea8d.jpg", "img/b0f1626073d97c.jpg", "img/b2a6d1121c177a.jpg", "img/b327cc783e495f.jpg", "img/b437044ae436a1.jpg", "img/b52ecab56e334e.jpg", "img/b5ac10e76f77ba.jpg", "img/b64e5a4684401f.jpg", "img/b6a9b48c0353e7.jpg", "img/b6b834fb5ead6b.jpg", "img/b6e72686cc93a9.jpg", "img/b7d4b6095714de.jpg", "img/b8690ca721d2fb.jpg", "img/b95f34dca9435b.jpg", "img/bc6b4cc38f62f9.jpg", "img/be35bd02d0688b.jpg", "img/bf53a57741960d.jpg", "img/bfcaecc3060b38.jpg", "img/bfefafcae48518.jpg", "img/c091519baa894d.jpg", "img/c1858d6f0a6bec.jpg", "img/c3ee687556e9ec.jpg", "img/c4605b3e041bf2.jpg", "img/c497dd07f6472e.jpg", "img/c4b249520254d1.jpg", "img/c5e6c3923093f4.jpg", "img/c65e1cf104ae6d.jpg", "img/c68869c3058058.jpg", "img/c7528a94170084.jpg", "img/c76291dddc6cb8.jpg", "img/cb6a53dfe125ae.jpg", "img/cd539a1baa8bf8.jpg", "img/cd7e4f188da140.jpg", "img/cddfd01654c4ae.jpg", "img/ce5d3a178f64f8.jpg", "img/ceb3b6ddaf59fd.jpg", "img/cf2644581378f6.jpg", "img/d06af612e65f5c.jpg", "img/d1f29887334e0e.jpg", "img/d31ee33b085691.jpg", "img/d3a8b964214a39.jpg", "img/d48ddb5c4d8cd0.jpg", "img/d5241c36ee685f.jpg", "img/d537b9ffa2f371.jpg", "img/d6fbba7382d011.jpg", "img/d75f76870a9471.jpg", "img/d89b5031ad3e72.jpg", "img/dc0e1fa8602bae.jpg", "img/dcafc796c0b032.jpg", "img/dceb37be1ed0cc.jpg", "img/dd0be96575e9fa.jpg", "img/ddd034322e8801.jpg", "img/de4b2c1c837760.jpg", "img/de690fe76d10c2.jpg", "img/deb62988945484.jpg", "img/e24493f0a1f64b.jpg", "img/e26e3e981f42c2.jpg", "img/e392ba94a54962.jpg", "img/e4d947db82a688.jpg", "img/e5556e5442ff42.jpg", "img/e633bc006a0f08.jpg", "img/e79e9a0432cd96.jpg", "img/e7bf2700bb2fce.jpg", "img/e7d2abd0d8bbf1.jpg", "img/e80d2a80de870c.jpg", "img/ea4a6668df1e6b.jpg", "img/ecd243779c39fd.jpg", "img/ed13b96501d599.jpg", "img/ed1e585c43f599.jpg", "img/ed2b640f3ea664.jpg", "img/ed62108ccc484c.jpg", "img/ee5167b2d37bec.jpg", "img/ee56c284faf50a.jpg", "img/f002bdc24c2f7b.jpg", "img/f0055ae528b2f4.jpg", "img/f2539ff64292bc.jpg", "img/f328a2754573ab.jpg", "img/f384fc1daf7d78.jpg", "img/f3ca0b48bfed8a.jpg", "img/f44fb44fa68760.jpg", "img/f49334892808c8.jpg", "img/f4f0b6cfc0a011.jpg", "img/f5160e077958d1.jpg", "img/f5ea14d0d57743.jpg", "img/f843643e864dc7.jpg", "img/f8a4e5e6f5268e.jpg", "img/f8fdae4db1d8f9.jpg", "img/f958836d7674f0.jpg", "img/f9d68c60335b5b.jpg", "img/fa7a405de53c3d.jpg", "img/faa2cfb79ea09b.jpg", "img/fab144c6686c72.jpg", "img/fabcb0fb6d069b.jpg", "img/fb9486292fc193.jpg", "img/fc1054bc53e03a.jpg", "img/fd7e4ecbb4d8dc.jpg", "img/fe23b95f17f030.jpg", "img/fec4765a8f5c83.jpg", "icons/apple-touch-icon-120.png", "icons/apple-touch-icon-152.png", "icons/apple-touch-icon-167.png", "icons/apple-touch-icon-180.png", "icons/apple-touch-icon.png", "icons/icon-1024.png", "icons/icon-192.png", "icons/icon-512-maskable.png", "icons/icon-512.png"];
const FONT_CSS = ["https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap", "https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500&display=swap"];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    // reuse photos already on the phone from the previous version, fetch only what is new
    const old = (await caches.keys()).filter(k => k.startsWith('nuveer-') && k !== CACHE);
    for (const f of FILES) {
      let hit = null;
      if (f.startsWith('img/') || f.startsWith('icons/')) for (const k of old) { hit = await (await caches.open(k)).match(f); if (hit) break; }
      if (hit) await c.put(f, hit); else await c.add(new Request(f, {cache: 'reload'}));
    }
    // the site's Google fonts, so text looks the same offline (best effort)
    for (const u of FONT_CSS) {
      try {
        const r = await fetch(u, {mode: 'cors'}); if (!r.ok) continue;
        const css = await r.clone().text(); await c.put(u, r);
        for (const m of css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)) {
          try { const f = await fetch(m[1], {mode: 'cors'}); if (f.ok) await c.put(m[1], f); } catch (_) {}
        }
      } catch (_) {}
    }
  })());
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('nuveer-') && k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // the page: try the network first (to pick up a new version), fall back to the copy on the phone
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 4000);
        const r = await fetch(req, {signal: ctl.signal, cache: 'no-store'}); clearTimeout(t);
        if (r.ok) { const c = await caches.open(CACHE); c.put('index.html', r.clone()); }
        return r;
      } catch (_) { return (await caches.match('index.html')) || (await caches.match('./')) || Response.error(); }
    })());
    return;
  }
  // photos, icons, fonts: from the phone first, network only if missing
  if (url.origin === location.origin || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith((async () => {
      const hit = await caches.match(req, {ignoreSearch: url.origin === location.origin}); if (hit) return hit;
      try { const r = await fetch(req); if (r.ok || r.type === 'opaque') { const c = await caches.open(CACHE); c.put(req, r.clone()); } return r; }
      catch (_) { return Response.error(); }
    })());
  }
});
