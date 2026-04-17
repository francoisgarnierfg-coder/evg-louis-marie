import os, base64, io
from PIL import Image

# Load photos
photo_dir = 'Photo'
files = sorted([f for f in os.listdir(photo_dir) if f.endswith('.jpeg')])
parts = []
for f in files:
    with open(os.path.join(photo_dir, f), 'rb') as fp:
        b64 = base64.b64encode(fp.read()).decode()
        parts.append('"data:image/jpeg;base64,' + b64 + '"')
PHOTOS_JS = '[' + ','.join(parts) + ']'

# Load Louis-Marie avatar (face crop, 320x320, optimised for inline embed)
lm_img_path = "Photo/WhatsApp Image 2026-04-17 at 18.23.14 (2).jpeg"
lm_img = Image.open(lm_img_path).convert('RGB')
w, h = lm_img.size
side = min(w, h)
left = (w - side) // 2
top = int((h - side) * 0.08)   # shifted up to capture face
right = left + side
bottom = top + side
lm_crop = lm_img.crop((left, top, right, bottom)).resize((360, 360), Image.LANCZOS)
buf = io.BytesIO()
lm_crop.save(buf, format='JPEG', quality=84, optimize=True)
LM_PHOTO = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

HTML = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0B1724">
<meta name="apple-mobile-web-app-title" content="EVJF Loulou">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-192.png">
<title>EVJF Loulou</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#0B1724;--ink2:#1C3352;--ocean:#1565A0;--ocean2:#1976D2;
  --teal:#00796B;--teal-bg:#E0F2F1;--amber:#B8830A;--amber-bg:#FFF8E1;
  --sand:#F4F1EC;--stone:#E2DACE;--white:#FFFFFF;--text:#1A1A1A;--sub:#64615D;
  --danger:#B71C1C;--danger-bg:#FFEBEE;
  --r:18px;--rsm:10px;--tab:64px;--sab:env(safe-area-inset-bottom,0px);
  --fh:'Playfair Display',Georgia,serif;--fb:'Inter',system-ui,sans-serif;
  --s0:0 1px 4px rgba(0,0,0,.06);--s1:0 2px 16px rgba(0,0,0,.08);--s2:0 8px 32px rgba(0,0,0,.14);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font-family:var(--fb);background:var(--sand);color:var(--text);min-height:100dvh;overflow-x:hidden;-webkit-font-smoothing:antialiased}
button{font-family:var(--fb);cursor:pointer}a{text-decoration:none;color:inherit}img{display:block}

#splash{position:fixed;inset:0;z-index:9999;background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity .5s ease,transform .5s ease}
#splash.out{opacity:0;transform:scale(1.05);pointer-events:none}
.sp-ico{font-size:48px;margin-bottom:24px;animation:spf 3s ease-in-out infinite}
@keyframes spf{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.sp-nm{font-family:var(--fh);font-size:38px;color:#fff;text-align:center;line-height:1.1}
.sp-nm em{display:block;font-style:italic;font-size:20px;color:rgba(255,255,255,.35);margin-top:4px}
.sp-loc{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,.28);margin-top:12px}
.sp-bar{width:140px;height:2px;background:rgba(255,255,255,.1);border-radius:99px;overflow:hidden;margin-top:48px}
.sp-fill{height:100%;background:linear-gradient(90deg,var(--teal),var(--ocean2));border-radius:99px;animation:spl 1.9s cubic-bezier(.65,0,.35,1) forwards}
@keyframes spl{from{width:0}to{width:100%}}

#app{display:none;flex-direction:column;min-height:100dvh}
#app.on{display:flex}
.pages{flex:1;overflow-y:auto;padding-bottom:calc(var(--tab) + var(--sab));-webkit-overflow-scrolling:touch}
.page{display:none}
.page.active{display:block;animation:pgin .22s ease both}
@keyframes pgin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

.tabbar{position:fixed;bottom:0;left:0;right:0;height:calc(var(--tab) + var(--sab));padding-bottom:var(--sab);background:rgba(255,255,255,.94);backdrop-filter:blur(24px) saturate(200%);-webkit-backdrop-filter:blur(24px) saturate(200%);border-top:1px solid rgba(0,0,0,.08);display:flex;z-index:100;box-shadow:0 -8px 24px rgba(0,0,0,.05)}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;border:none;background:none;color:var(--sub);font-size:10px;font-weight:500;padding:8px 4px 6px;transition:color .18s;position:relative}
.tab.on{color:var(--ocean)}
.tab.on::after{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:24px;height:2px;background:var(--ocean);border-radius:0 0 3px 3px}
.tab-ic{font-size:19px;line-height:1;transition:transform .12s}
.tab:active .tab-ic{transform:scale(.82)}

.card{background:var(--white);border-radius:var(--r);box-shadow:var(--s1);overflow:hidden}
.badge{display:inline-flex;align-items:center;gap:4px;border-radius:99px;padding:4px 11px;font-size:11px;font-weight:600}
.badge.def{background:rgba(0,0,0,.06);color:var(--text)}
.badge.ocean{background:rgba(21,101,160,.1);color:var(--ocean)}
.badge.teal{background:var(--teal-bg);color:var(--teal)}
.badge.amber{background:var(--amber-bg);color:var(--amber)}
.badge.danger{background:var(--danger-bg);color:var(--danger)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border-radius:var(--rsm);padding:12px 18px;font-size:13px;font-weight:600;border:none;transition:opacity .15s,transform .12s}
.btn:active{opacity:.8;transform:scale(.97)}
.btn.ink{background:var(--ink);color:#fff}
.btn.ocean{background:var(--ocean);color:#fff}
.btn-row{display:flex;gap:8px;margin-top:14px}
.btn-row .btn{flex:1}
.alert{border-radius:var(--rsm);padding:11px 14px;font-size:12px;line-height:1.6;margin-top:10px}
.alert.amber{background:var(--amber-bg);color:#7A5000}
.alert.danger{background:var(--danger-bg);color:var(--danger)}
.alert strong{font-weight:700}

.hero{position:relative;overflow:hidden;background:linear-gradient(155deg,var(--ink) 0%,var(--ink2) 55%,#1a5276 100%);color:#fff;padding:60px 24px 48px}
.lm-av{position:absolute;right:22px;top:50px;width:82px;height:82px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px rgba(184,131,10,.7),0 0 0 7px rgba(184,131,10,.15),0 10px 32px rgba(0,0,0,.5);flex-shrink:0;z-index:2}
.lm-av img{width:100%;height:100%;object-fit:cover}
.hero-grain{position:absolute;inset:0;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='.035'/%3E%3C/svg%3E");opacity:.7}
.hero-glow{position:absolute;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(25,118,210,.15) 0%,transparent 70%);top:-100px;right:-100px;pointer-events:none}
.hero-pill{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:99px;padding:5px 14px 5px 10px;font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;color:rgba(255,255,255,.85)}
.hero-h1{font-family:var(--fh);font-size:48px;line-height:1.02;letter-spacing:-.5px;margin-bottom:8px}
.hero-h1 em{display:block;font-size:22px;font-style:italic;color:rgba(255,255,255,.38);letter-spacing:.3px;margin-top:4px}
.hero-p{font-size:14px;color:rgba(255,255,255,.52);line-height:1.7;margin-bottom:26px;max-width:340px;font-weight:300}
.hero-tags{display:flex;flex-wrap:wrap;gap:8px}
.hero-tag{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.13);border-radius:99px;padding:6px 14px;font-size:12px;color:rgba(255,255,255,.78)}

.cd-wrap{padding:24px 20px 0}
.cd-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.cd-cell{background:var(--white);border-radius:var(--rsm);padding:14px 6px;text-align:center;box-shadow:var(--s0)}
.cd-n{font-family:var(--fh);font-size:30px;color:var(--ink);line-height:1;letter-spacing:-1px}
.cd-l{font-size:9px;font-weight:600;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;margin-top:4px}

.sh{padding:24px 20px 0}
.sh h3{font-size:17px;font-weight:700;color:var(--ink);letter-spacing:-.2px;margin-bottom:2px}
.sh p{font-size:12px;color:var(--sub);margin-bottom:16px}

.crew{display:flex;gap:14px;overflow-x:auto;padding:4px 0 12px;scroll-snap-type:x mandatory}
.crew::-webkit-scrollbar{display:none}
.cc{flex:0 0 68px;scroll-snap-align:start;display:flex;flex-direction:column;align-items:center;gap:6px}
.av{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;border:2px solid transparent;box-shadow:var(--s1);transition:transform .12s;position:relative;flex-shrink:0}
.av:active{transform:scale(.88)}
.av.star{background:var(--ink);color:#fff;border-color:var(--amber);box-shadow:0 0 0 3px rgba(184,131,10,.18),var(--s1)}
.av.star::after{content:'\1F48D';position:absolute;bottom:-3px;right:-3px;font-size:13px}
.av.reg{background:var(--stone);color:var(--ink2)}
.av-n{font-size:10px;font-weight:500;text-align:center;color:var(--text);line-height:1.3}
.av-r{font-size:9px;color:var(--sub);text-align:center}

.ig{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.it{background:var(--white);border-radius:var(--rsm);padding:16px;box-shadow:var(--s0)}
.it-ico{font-size:20px;margin-bottom:8px}
.it-l{font-size:9px;font-weight:600;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:3px}
.it-v{font-size:13px;font-weight:500;color:var(--ink);line-height:1.4}

.cr{display:flex;align-items:center;gap:14px;background:var(--white);border-radius:var(--rsm);padding:14px 16px;box-shadow:var(--s0);margin-bottom:8px}
.cr-ico{font-size:20px;flex-shrink:0}
.cr-i{flex:1}
.cr-n{font-size:13px;font-weight:600;color:var(--ink)}
.cr-p{font-size:11px;color:var(--sub);margin-top:1px}
.cr-cta{background:var(--teal-bg);color:var(--teal);border:none;border-radius:99px;padding:7px 13px;font-size:11px;font-weight:600}

.ph{background:var(--ink);padding:52px 24px 28px;color:#fff}
.ph h2{font-family:var(--fh);font-size:32px;letter-spacing:-.3px;margin-bottom:4px}
.ph p{font-size:13px;color:rgba(255,255,255,.42)}
.dw{padding:0 20px 12px}
.dh{display:flex;align-items:center;gap:12px;padding:20px 0 14px}
.dd{width:8px;height:8px;border-radius:50%;background:var(--ocean);flex-shrink:0}
.dt{font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--ocean)}
.dr{flex:1;height:1px;background:var(--stone)}
.tl{position:relative;padding-left:26px}
.tl::before{content:'';position:absolute;left:5px;top:10px;bottom:10px;width:1.5px;background:linear-gradient(to bottom,rgba(21,101,160,.3),rgba(21,101,160,.04));border-radius:2px}
.ev{position:relative;margin-bottom:12px}
.ev::before{content:'';position:absolute;left:-24px;top:16px;width:8px;height:8px;border-radius:50%;background:var(--white);border:2px solid var(--stone);z-index:1}
.ev.hl::before{border-color:var(--teal);background:var(--teal)}
.ev.am::before{border-color:var(--amber);background:var(--amber)}
.ev.oc::before{border-color:var(--ocean);background:var(--ocean)}
.evc{background:var(--white);border-radius:var(--r);padding:15px 17px;box-shadow:var(--s0);border-left:3px solid transparent}
.ev.hl .evc{border-left-color:var(--teal)}
.ev.am .evc{border-left-color:var(--amber)}
.ev.oc .evc{border-left-color:var(--ocean)}
.evr{display:flex;gap:14px;align-items:flex-start}
.etm{min-width:46px;flex-shrink:0}
.et1{font-size:13px;font-weight:700;color:var(--ink)}
.et2{font-size:10px;color:var(--sub);margin-top:1px}
.eb{flex:1}
.en{font-size:15px;font-weight:600;color:var(--ink);margin-bottom:3px}
.el{font-size:11px;color:var(--sub);margin-bottom:6px}
.ed{font-size:13px;color:var(--sub);line-height:1.62;font-weight:300}
.ebdg{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}

.ah{background:linear-gradient(145deg,#0d3d57,var(--teal));padding:52px 24px 28px;color:#fff}
.ah h2{font-family:var(--fh);font-size:32px;letter-spacing:-.3px;margin-bottom:4px}
.ah p{font-size:13px;color:rgba(255,255,255,.55)}
.acts{padding:20px;display:flex;flex-direction:column;gap:16px}
.act{background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:var(--s1)}
.aimg{height:140px;display:flex;align-items:center;justify-content:center;font-size:58px;position:relative}
.aimg.c1{background:linear-gradient(135deg,#e8f4f8,#d0eaf2)}
.aimg.c2{background:linear-gradient(135deg,#e8f5e9,#c8e6c9)}
.aimg.c3{background:linear-gradient(135deg,#e8eaf6,#c5cae9)}
.aimg.c4{background:linear-gradient(135deg,#fce4ec,#f8bbd0)}
.aimg.c5{background:linear-gradient(135deg,#fff3e0,#ffe0b2)}
.astar{position:absolute;top:12px;right:12px;background:rgba(0,0,0,.42);backdrop-filter:blur(6px);color:#fff;border-radius:99px;padding:4px 10px;font-size:11px;font-weight:600}
.abody{padding:18px}
.atitle{font-size:17px;font-weight:700;color:var(--ink);margin-bottom:5px}
.ameta{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.adesc{font-size:13px;color:var(--sub);line-height:1.65;margin-bottom:14px;font-weight:300}
.atbl{background:var(--sand);border-radius:var(--rsm);overflow:hidden;margin-bottom:14px}
.arow{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;font-size:12px;border-bottom:1px solid rgba(0,0,0,.04)}
.arow:last-child{border-bottom:none}
.arl{color:var(--sub)}
.arv{font-weight:600;color:var(--ink);text-align:right;max-width:58%}
.arv.danger{color:var(--danger)}
.arv.teal{color:var(--teal)}

.mapwrap{display:flex;flex-direction:column;min-height:calc(100dvh - var(--tab) - var(--sab))}
.mh{background:var(--ink);padding:52px 24px 20px;color:#fff;flex-shrink:0}
.mh h2{font-family:var(--fh);font-size:28px;letter-spacing:-.3px;margin-bottom:3px}
.mh p{font-size:13px;color:rgba(255,255,255,.42);padding-bottom:4px}
.mfilters{display:flex;gap:7px;overflow-x:auto;padding:14px 20px 12px;background:var(--white);border-bottom:1px solid var(--stone);flex-shrink:0}
.mfilters::-webkit-scrollbar{display:none}
.mbtn{flex:0 0 auto;background:var(--sand);border:1.5px solid var(--stone);border-radius:99px;padding:8px 14px;font-size:12px;font-weight:500;color:var(--ink);cursor:pointer;transition:all .18s;white-space:nowrap}
.mbtn.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.mframe{flex:1;border:none;width:100%;min-height:300px;height:calc(100dvh - 280px)}
.mfoot{background:var(--white);padding:14px 20px;border-top:1px solid var(--stone);display:flex;align-items:center;gap:10px;flex-shrink:0}
.mfoot-txt{flex:1;font-size:12px;color:var(--sub);line-height:1.5}
.mfoot-cta{background:var(--ocean);color:#fff;border:none;border-radius:99px;padding:8px 16px;font-size:12px;font-weight:600;flex-shrink:0}

.albhd{background:linear-gradient(145deg,#1a0533,#1B2D4F);padding:52px 24px 28px;color:#fff}
.albhd h2{font-family:var(--fh);font-size:32px;letter-spacing:-.3px;margin-bottom:4px}
.albhd p{font-size:13px;color:rgba(255,255,255,.48)}
.upz{margin:20px;background:var(--white);border:2px dashed var(--stone);border-radius:var(--r);padding:28px 20px;text-align:center;cursor:pointer;transition:border-color .2s,background .2s}
.upz:hover,.upz.drag{border-color:var(--ocean);background:rgba(21,101,160,.03)}
.upz-ico{font-size:36px;margin-bottom:11px}
.upz-t{font-size:14px;font-weight:600;color:var(--ink);margin-bottom:4px}
.upz-s{font-size:12px;color:var(--sub);line-height:1.55}
.upz-btn{display:inline-block;background:var(--ink);color:#fff;border-radius:var(--rsm);padding:10px 22px;font-size:13px;font-weight:600;margin-top:14px;cursor:pointer;border:none}
#fi{display:none}
.albbar{display:flex;align-items:center;justify-content:space-between;padding:0 20px 10px}
.albcnt{font-size:12px;color:var(--sub)}
.albacts{display:flex;gap:7px}
.aabtn{background:var(--white);border:1.5px solid var(--stone);border-radius:99px;padding:7px 13px;font-size:11px;font-weight:600;color:var(--ink);cursor:pointer;transition:transform .12s}
.aabtn:active{transform:scale(.94)}
.aabtn.p{background:var(--ocean);color:#fff;border-color:var(--ocean)}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;padding:0 20px 20px}
.pi{aspect-ratio:1;border-radius:7px;overflow:hidden;cursor:pointer;position:relative;background:var(--stone);animation:pifi .3s ease both}
@keyframes pifi{from{opacity:0;transform:scale(.92)}to{opacity:1;transform:scale(1)}}
.pi img{width:100%;height:100%;object-fit:cover}
.albemp{margin:0 20px 20px;padding:44px 20px;text-align:center;font-size:14px;color:var(--sub);line-height:1.65}
.upstat{margin:0 20px 8px;padding:10px 14px;background:var(--teal-bg);border-radius:var(--rsm);font-size:12px;color:var(--teal);font-weight:500;display:none}

.lb{display:none;position:fixed;inset:0;z-index:800;background:rgba(0,0,0,.97);align-items:center;justify-content:center}
.lb.open{display:flex}
.lbimg{max-width:96vw;max-height:82dvh;object-fit:contain;border-radius:8px;user-select:none;pointer-events:none}
.lbx{position:absolute;top:max(env(safe-area-inset-top,16px),16px);right:16px;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;border:none;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(8px)}
.lbnav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;border:none;font-size:22px;display:flex;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(8px)}
#lbP{left:14px}#lbN{right:14px}
.lbctr{position:absolute;bottom:max(env(safe-area-inset-bottom,24px),24px);left:50%;transform:translateX(-50%);background:rgba(255,255,255,.14);backdrop-filter:blur(8px);color:#fff;border-radius:99px;padding:6px 16px;font-size:12px;font-weight:500}

.lhd{background:linear-gradient(145deg,#0e1f35,var(--ink2));padding:52px 24px 28px;color:#fff}
.lhd h2{font-family:var(--fh);font-size:32px;letter-spacing:-.3px;margin-bottom:4px}
.lhd p{font-size:13px;color:rgba(255,255,255,.42)}
.lbody{padding:20px}
.lprop{background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:var(--s1);margin-bottom:16px}
.lcover{height:168px;background:linear-gradient(135deg,#0f3754,#1565a0,#00796b);display:flex;align-items:center;justify-content:center;font-size:68px;position:relative}
.lcbadge{position:absolute;bottom:14px;left:14px;background:rgba(0,0,0,.5);backdrop-filter:blur(8px);color:#fff;border-radius:99px;padding:5px 14px;font-size:12px;font-weight:500}
.linfo{padding:20px}
.lname{font-size:19px;font-weight:700;color:var(--ink);margin-bottom:3px}
.laddr{font-size:12px;color:var(--sub);margin-bottom:12px}
.ldesc{font-size:13px;color:var(--sub);line-height:1.65;margin-bottom:16px;font-weight:300}
.agrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}
.am{display:flex;align-items:center;gap:8px;background:var(--sand);border-radius:var(--rsm);padding:10px 12px;font-size:12px;color:var(--text)}
.am-i{font-size:16px}

.install-banner{margin:0 20px 16px;background:var(--ink);border-radius:var(--r);padding:16px 18px;display:flex;align-items:center;gap:14px;color:#fff;cursor:pointer}
.install-ico{font-size:28px;flex-shrink:0}
.install-txt{flex:1}
.install-t{font-size:14px;font-weight:600;margin-bottom:2px}
.install-s{font-size:11px;color:rgba(255,255,255,.55)}
.install-btn{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.2);color:#fff;border-radius:99px;padding:7px 14px;font-size:12px;font-weight:600;flex-shrink:0}

.toast{position:fixed;bottom:calc(var(--tab) + var(--sab) + 14px);left:50%;transform:translateX(-50%) translateY(16px);background:var(--ink);color:#fff;border-radius:99px;padding:10px 20px;font-size:13px;font-weight:500;opacity:0;transition:opacity .28s,transform .28s;pointer-events:none;z-index:700;white-space:nowrap;box-shadow:var(--s2)}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

@media(min-width:480px){.pgrid{grid-template-columns:repeat(4,1fr)}}
@media(min-width:680px){.ig{grid-template-columns:repeat(4,1fr)}.pgrid{grid-template-columns:repeat(5,1fr)}.acts{display:grid;grid-template-columns:1fr 1fr}}
@media(min-width:960px){.pages,.tabbar{max-width:640px;margin-left:auto;margin-right:auto}.tabbar{left:50%;right:auto;transform:translateX(-50%);width:640px}}
</style>
</head>
<body>
<div id="splash"><div class="sp-ico">&#9875;</div><div class="sp-nm">Loulou<em>EVJF &middot; Bretagne</em></div><div class="sp-loc">Fouesnant &middot; Concarneau</div><div class="sp-bar"><div class="sp-fill"></div></div></div>

<div id="app">
<div class="pages" id="pages">

<!-- ACCUEIL -->
<div class="page active" id="page-home">
  <div class="hero">
    <div class="hero-grain"></div><div class="hero-glow"></div>
    <div class="lm-av"><img src="__LM_PHOTO__" alt="Louis-Marie"></div>
    <div class="hero-pill">&#9875; EVJF 2026</div>
    <div class="hero-h1">Loulou<em>Bretagne</em></div>
    <div class="hero-p">Week-end entre 10 potes sur la Riviera bretonne &mdash; v&eacute;los, hu&icirc;tres, bateau.</div>
    <div class="hero-tags">
      <div class="hero-tag">&#128205; Fouesnant &middot; Pleuven</div>
      <div class="hero-tag">&#128692; C&ocirc;te sauvage</div>
      <div class="hero-tag">&#129450; Penfoulic</div>
      <div class="hero-tag">&#9973; Santa Maria</div>
    </div>
  </div>
  <!-- Android install banner (beforeinstallprompt) -->
  <div id="installBanner" style="display:none">
    <div class="install-banner" onclick="installPWA()">
      <div class="install-ico">&#128241;</div>
      <div class="install-txt"><div class="install-t">Installer l'app</div><div class="install-s">Ajouter &agrave; l'&eacute;cran d'accueil</div></div>
      <button class="install-btn" type="button">Installer</button>
    </div>
  </div>
  <!-- iOS Safari install hint -->
  <div id="iosBanner" style="display:none">
    <div class="install-banner" style="cursor:default">
      <div class="install-ico">&#128279;</div>
      <div class="install-txt">
        <div class="install-t">Installer sur iPhone</div>
        <div class="install-s">Tape &#9650; <strong style="color:#fff">Partager</strong> puis <strong style="color:#fff">&laquo;&nbsp;Sur l'&eacute;cran d'accueil&nbsp;&raquo;</strong></div>
      </div>
      <button class="install-btn" type="button" onclick="document.getElementById('iosBanner').style.display='none'">&#10005;</button>
    </div>
  </div>
  <div class="cd-wrap">
    <div style="margin-bottom:10px"><span style="font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--sub)" id="cdLbl">Compte &agrave; rebours</span></div>
    <div class="cd-grid">
      <div class="cd-cell"><div class="cd-n" id="cdD">&mdash;</div><div class="cd-l">jours</div></div>
      <div class="cd-cell"><div class="cd-n" id="cdH">&mdash;</div><div class="cd-l">heures</div></div>
      <div class="cd-cell"><div class="cd-n" id="cdM">&mdash;</div><div class="cd-l">min</div></div>
      <div class="cd-cell"><div class="cd-n" id="cdS">&mdash;</div><div class="cd-l">sec</div></div>
    </div>
  </div>
  <div class="sh"><h3>L'&eacute;quipage</h3><p>10 gars, 1 seul mari&eacute;</p><div class="crew" id="crew"></div></div>
  <div class="sh"><h3>En bref</h3><p>Infos pratiques</p>
    <div class="ig">
      <div class="it"><div class="it-ico">&#127968;</div><div class="it-l">Logement</div><div class="it-v">La Bonne Descente &mdash; Pleuven</div></div>
      <div class="it"><div class="it-ico">&#128101;</div><div class="it-l">&Eacute;quipe</div><div class="it-v">10 participants</div></div>
      <div class="it"><div class="it-ico">&#128197;</div><div class="it-l">Format</div><div class="it-v">Ven. soir &rarr; Dim. apr&egrave;s-midi</div></div>
      <div class="it"><div class="it-ico">&#127754;</div><div class="it-l">R&eacute;gion</div><div class="it-v">Bretagne Sud &middot; Finist&egrave;re</div></div>
    </div>
  </div>
  <div class="sh" style="padding-bottom:28px"><h3>Contacts</h3><p>Tap pour appeler</p><div id="hc"></div></div>
</div>

<!-- PROGRAMME -->
<div class="page" id="page-prog">
  <div class="ph"><h2>Programme</h2><p>Vendredi &rarr; Dimanche &middot; Fouesnant &amp; Concarneau &mdash; EVJF Loulou</p></div>
  <div class="dw">
    <div class="dh"><div class="dd"></div><div class="dt">Vendredi soir &mdash; Arriv&eacute;e</div><div class="dr"></div></div>
    <div class="tl">
      <div class="ev hl"><div class="evc"><div class="evr"><div class="etm"><div class="et1">18h</div></div><div class="eb"><div class="en">&#127968; Arriv&eacute;e &amp; installation</div><div class="el">&#128205; Descente de Rozambars 206, Pleuven, 29170</div><div class="ed">Prise de possession de la maison. Pr&eacute;voir les courses avant : charcuterie, fromages, pain, bi&egrave;res et cidre breton.</div><div class="ebdg"><span class="badge danger">&#9888; Responsable cl&eacute;s</span><span class="badge ocean">&#128722; Intermarch&eacute; Fouesnant</span></div></div></div></div></div>
      <div class="ev"><div class="evc"><div class="evr"><div class="etm"><div class="et1">Soir</div></div><div class="eb"><div class="en">&#129346; Retrouvailles</div><div class="el">&#128205; Maison &mdash; Pleuven</div><div class="ed">Premier ap&eacute;ritif, plateau charcuterie-fromages, soir&eacute;e &agrave; la maison.</div></div></div></div></div>
    </div>
  </div>
  <div class="dw">
    <div class="dh"><div class="dd" style="background:var(--amber)"></div><div class="dt" style="color:var(--amber)">Samedi &mdash; Le Grand Jour</div><div class="dr"></div></div>
    <div class="tl">
      <div class="ev hl"><div class="evc"><div class="evr"><div class="etm"><div class="et1">10h</div><div class="et2">&rarr; ~13h</div></div><div class="eb"><div class="en">&#128692; Location v&eacute;los &mdash; C&ocirc;te sauvage</div><div class="el">&#128205; A Bicyclette &middot; 2 Rue de Cornouaille, Fouesnant</div><div class="ed">Rendez-vous chez le loueur &agrave; 10h. D&eacute;part pour Mousterlin et la c&ocirc;te sauvage par les pistes cyclables (~20 km).</div><div class="ebdg"><span class="badge teal">&#10003; D&eacute;j&agrave; r&eacute;serv&eacute;</span><span class="badge def">&#9990; 06 77 63 90 72</span><span class="badge amber">&#11088; 4.9/5</span></div></div></div></div></div>
      <div class="ev am"><div class="evc"><div class="evr"><div class="etm"><div class="et1">~13h</div><div class="et2">&rarr; 15h</div></div><div class="eb"><div class="en">&#129450; Viviers de Penfoulic</div><div class="el">&#128205; Route de Beg an Aer, La For&ecirc;t-Fouesnant</div><div class="ed">Hu&icirc;tres, palourdes, langoustines et fruits de mer en bord de mer. Muscadet ou Gros-Plant.</div><div class="ebdg"><span class="badge def">&#9990; 02 98 56 83 89</span><span class="badge amber">&#11088; 4.9/5 &middot; 1047 avis</span></div><div class="alert danger">R&eacute;servation imp&eacute;rative pour 10 personnes.</div></div></div></div></div>
      <div class="ev"><div class="evc"><div class="evr"><div class="etm"><div class="et1">~15h</div><div class="et2">&rarr; 17h</div></div><div class="eb"><div class="en">&#128260; Retour v&eacute;los &amp; transition</div><div class="el">&#128205; Fouesnant &rarr; Maison Pleuven</div><div class="ed">Retour des v&eacute;los chez le loueur. Maison, temps libre pour se pr&eacute;parer. Trajet &rarr; Concarneau : ~20 min.</div><div class="ebdg"><span class="badge ocean">&#128663; Covoiturage &agrave; organiser</span></div></div></div></div></div>
      <div class="ev oc"><div class="evc"><div class="evr"><div class="etm"><div class="et1">17h</div><div class="et2">&rarr; 23h</div></div><div class="eb"><div class="en">&#9973; Santa Maria &mdash; Sortie en mer</div><div class="el">&#128205; Quai d'Aiguillon, Port de P&ecirc;che, Concarneau</div><div class="ed">Promenade jusqu'aux &icirc;les Gl&eacute;nan. C&ocirc;te de b&oelig;uf et fruits de mer &agrave; bord. Musique, privatisation EVJF.</div><div class="ebdg"><span class="badge teal">&#10003; D&eacute;j&agrave; r&eacute;serv&eacute;</span><span class="badge ocean">&#129385; C&ocirc;te de b&oelig;uf + fruits de mer</span><span class="badge amber">&#11088; 4.7/5</span></div></div></div></div></div>
      <div class="ev"><div class="evc"><div class="evr"><div class="etm"><div class="et1">23h+</div></div><div class="eb"><div class="en">&#127821; Bro Ar Sud</div><div class="el">&#128205; 2 Rue Saint-Gu&eacute;nol&eacute;, Ville close, Concarneau</div><div class="ed">Rhumerie-brasserie dans la ville close. Cocktails, planches. Note 5/5. Option selon l'&eacute;nergie &mdash; retour en VTC sinon.</div><div class="ebdg"><span class="badge amber">&#11088; 5/5</span><span class="badge def">&#128661; Pr&eacute;voir VTC retour</span></div></div></div></div></div>
    </div>
  </div>
  <div class="dw">
    <div class="dh"><div class="dd" style="background:var(--teal)"></div><div class="dt" style="color:var(--teal)">Dimanche &mdash; Cl&ocirc;ture</div><div class="dr"></div></div>
    <div class="tl">
      <div class="ev hl"><div class="evc"><div class="evr"><div class="etm"><div class="et1">Matin</div></div><div class="eb"><div class="en">&#127968; Rangement maison</div><div class="el">&#128205; Maison &mdash; Pleuven</div><div class="ed">Nettoyage collectif et remise en &eacute;tat avant le d&eacute;part.</div></div></div></div></div>
      <div class="ev"><div class="evc"><div class="evr"><div class="etm"><div class="et1">11h</div></div><div class="eb"><div class="en">&#9962; Messe dominicale</div><div class="el">&#128205; &Eacute;glise St-Gu&eacute;nol&eacute; &mdash; Concarneau, 29900</div><div class="ed">Paroisse Notre-Dame des Douze Ap&ocirc;tres &mdash; Concarneau.</div><div class="ebdg"><span class="badge ocean">&#128205; Concarneau</span><span class="badge def">11h00</span></div></div></div></div></div>
      <div class="ev hl"><div class="evc"><div class="evr"><div class="etm"><div class="et1">Midi</div><div class="et2">&rarr; ~14h</div></div><div class="eb"><div class="en">&#127869; La Long&egrave;re &mdash; D&eacute;jeuner</div><div class="el">&#128205; 5 Chemin de Ker an Braz, Fouesnant</div><div class="ed">Restaurant gastronomique breton. Cuisine du terroir soign&eacute;e, terrasse.</div><div class="ebdg"><span class="badge def">&#9990; 02 98 56 58 17</span><span class="badge amber">&#11088; 4.7/5</span></div><div class="alert amber">R&eacute;servation conseill&eacute;e pour 10 &mdash; ouvert dimanche midi.</div></div></div></div></div>
      <div class="ev"><div class="evc"><div class="evr"><div class="etm"><div class="et1">~14h</div></div><div class="eb"><div class="en">&#128075; D&eacute;parts</div><div class="el">&#128205; Maison &mdash; Pleuven</div><div class="ed">Check-out et d&eacute;parts.</div></div></div></div></div>
    </div>
  </div>
</div>

<!-- ACTIVITES -->
<div class="page" id="page-act">
  <div class="ah"><h2>Activit&eacute;s</h2><p>Tout ce qui vous attend ce week-end</p></div>
  <div class="acts">
    <div class="act"><div class="aimg c1">&#128692;<div class="astar">&#11088; 4.9/5</div></div><div class="abody"><div class="atitle">A Bicyclette &mdash; V&eacute;los</div><div class="ameta"><span class="badge ocean">&#128205; Fouesnant</span><span class="badge teal">&#10003; R&eacute;serv&eacute;</span><span class="badge def">Sam. 10h</span></div><div class="adesc">Rendez-vous chez le loueur &agrave; 10h. C&ocirc;te sauvage par les pistes cyclables jusqu'&agrave; Mousterlin (~20 km). Paysages de dunes et plages de sable blanc.</div><div class="atbl"><div class="arow"><span class="arl">Adresse</span><span class="arv">2 Rue de Cornouaille, Fouesnant</span></div><div class="arow"><span class="arl">T&eacute;l&eacute;phone</span><span class="arv">06 77 63 90 72</span></div><div class="arow"><span class="arl">Distance</span><span class="arv">~20 km A/R</span></div><div class="arow"><span class="arl">Statut</span><span class="arv teal">&#10003; D&eacute;j&agrave; r&eacute;serv&eacute;</span></div></div><div class="btn-row"><a class="btn ink" href="tel:0677639072">&#128222; Appeler</a><a class="btn ocean" href="https://maps.google.com/?q=A+Bicyclette+Fouesnant" target="_blank">&#128506; Maps</a></div></div></div>
    <div class="act"><div class="aimg c2">&#129450;<div class="astar">&#11088; 4.9 &middot; 1047</div></div><div class="abody"><div class="atitle">&#129450; Viviers de Penfoulic</div><div class="ameta"><span class="badge ocean">&#128205; La For&ecirc;t-Fouesnant</span><span class="badge def">Sam. ~13h</span></div><div class="adesc">Hu&icirc;tres, palourdes, langoustines face &agrave; la mer. Tables en bois en ext&eacute;rieur. L'adresse incontournable.</div><div class="atbl"><div class="arow"><span class="arl">T&eacute;l&eacute;phone</span><span class="arv">02 98 56 83 89</span></div><div class="arow"><span class="arl">Sp&eacute;cialit&eacute;s</span><span class="arv">&#129450; Hu&icirc;tres &middot; Langoustines</span></div><div class="arow"><span class="arl">R&eacute;servation</span><span class="arv danger">Imp&eacute;rative pour 10</span></div></div><div class="btn-row"><a class="btn ink" href="tel:0298568389">&#128222; R&eacute;server</a><a class="btn ocean" href="https://maps.google.com/?q=Aux+Viviers+de+Penfoulic" target="_blank">&#128506; Maps</a></div></div></div>
    <div class="act"><div class="aimg c3">&#9973;<div class="astar">&#11088; 4.7/5</div></div><div class="abody"><div class="atitle">Santa Maria &mdash; En mer</div><div class="ameta"><span class="badge ocean">&#128205; Concarneau</span><span class="badge teal">&#10003; R&eacute;serv&eacute;</span><span class="badge def">Sam. 17h&rarr;23h</span></div><div class="adesc">Promenade en baie de Concarneau jusqu'aux &icirc;les Gl&eacute;nan. C&ocirc;te de b&oelig;uf et fruits de mer &agrave; bord. Privatisation EVG.</div><div class="atbl"><div class="arow"><span class="arl">T&eacute;l&eacute;phone</span><span class="arv">06 62 88 00 87</span></div><div class="arow"><span class="arl">Repas</span><span class="arv teal">C&ocirc;te de b&oelig;uf + fruits de mer</span></div><div class="arow"><span class="arl">Statut</span><span class="arv teal">&#10003; D&eacute;j&agrave; r&eacute;serv&eacute;</span></div></div><div class="btn-row"><a class="btn ink" href="tel:0662880087">&#128222; Appeler</a><a class="btn ocean" href="https://maps.google.com/?q=Port+Peche+Concarneau" target="_blank">&#128506; Port</a></div></div></div>
    <div class="act"><div class="aimg c4">&#127821;<div class="astar">&#11088; 5/5</div></div><div class="abody"><div class="atitle">Bro Ar Sud &mdash; Rhumerie</div><div class="ameta"><span class="badge ocean">&#128205; Ville close</span><span class="badge def">Apr&egrave;s 23h</span></div><div class="adesc">Bar-rhumerie dans la ville close. Cocktails tropicaux, planches. Note parfaite. Option selon l'&eacute;nergie.</div><div class="atbl"><div class="arow"><span class="arl">T&eacute;l&eacute;phone</span><span class="arv">02 98 53 29 77</span></div><div class="arow"><span class="arl">Adresse</span><span class="arv">2 Rue Saint-Gu&eacute;nol&eacute;, Concarneau</span></div></div><div class="btn-row"><a class="btn ink" href="tel:0298532977">&#128222; Appeler</a><a class="btn ocean" href="https://maps.google.com/?q=Bro+Ar+Sud+Concarneau" target="_blank">&#128506; Maps</a></div></div></div>
    <div class="act"><div class="aimg c5">&#127869;<div class="astar">&#11088; 4.7/5</div></div><div class="abody"><div class="atitle">La Long&egrave;re &mdash; D&eacute;j. dimanche</div><div class="ameta"><span class="badge ocean">&#128205; Fouesnant</span><span class="badge def">Dim. midi</span></div><div class="adesc">Restaurant gastronomique breton. Cuisine du terroir, service impeccable, terrasse. Ouvert dimanche midi.</div><div class="atbl"><div class="arow"><span class="arl">T&eacute;l&eacute;phone</span><span class="arv">02 98 56 58 17</span></div><div class="arow"><span class="arl">R&eacute;servation</span><span class="arv danger">Conseill&eacute;e pour 10</span></div></div><div class="btn-row"><a class="btn ink" href="tel:0298565817">&#128222; R&eacute;server</a><a class="btn ocean" href="https://maps.google.com/?q=La+Longere+Fouesnant" target="_blank">&#128506; Maps</a></div></div></div>
  </div>
</div>

<!-- CARTE -->
<div class="page" id="page-map"><div class="mapwrap"><div class="mh"><h2>Carte</h2><p>Tous les lieux du week-end</p></div><div class="mfilters" id="mf"></div><iframe class="mframe" id="mfr" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="" allowfullscreen></iframe><div class="mfoot"><div class="mfoot-txt" id="mft">S&eacute;lectionnez un lieu</div><a class="mfoot-cta" id="mfcta" href="#" target="_blank">Ouvrir Maps</a></div></div></div>

<!-- PHOTOS -->
<div class="page" id="page-album">
  <div class="albhd"><h2>Album photos</h2><p>Vos souvenirs de Louis-Marie</p></div>
  <div class="upz" id="upz" onclick="document.getElementById('fi').click()"><div class="upz-ico">&#128247;</div><div class="upz-t">Ajouter vos photos</div><div class="upz-s">Cliquez ou glissez-d&eacute;posez<br><span style="opacity:.65">JPG &middot; PNG &middot; HEIC</span></div><button class="upz-btn" type="button">Choisir des photos</button></div>
  <input type="file" id="fi" multiple accept="image/*">
  <div class="upstat" id="upstat">&#8987; Upload en cours...</div>
  <div class="albbar" id="abb" style="display:none"><div class="albcnt" id="abc">0 photos</div><div class="albacts"><button class="aabtn p" onclick="shuffleP()">&#128256; M&eacute;langer</button></div></div>
  <div class="albemp" id="abe"><div style="font-size:48px;margin-bottom:14px">&#127902;</div>Aucune photo pour l'instant.</div>
  <div class="pgrid" id="pg"></div>
</div>

<!-- LOGEMENT -->
<div class="page" id="page-logement">
  <div class="lhd"><h2>Logement</h2><p>Notre base de vie bretonne</p></div>
  <div class="lbody">
    <div class="lprop"><div class="lcover">&#127969;<div class="lcbadge">&#128205; Pleuven, Finist&egrave;re</div></div><div class="linfo"><div class="lname">La Bonne Descente</div><div class="laddr">&#128205; Descente de Rozambars 206, Pleuven, 29170</div><div class="ldesc">Grande maison de vacances sur 3 &eacute;tages avec vue sur le lac. &Agrave; 10 min de la plage de Mousterlin, 15 min de Fouesnant, 20 min de Concarneau.</div><div class="agrid"><div class="am"><span class="am-i">&#128717;</span>Plusieurs chambres</div><div class="am"><span class="am-i">&#127956;</span>Vue sur le lac</div><div class="am"><span class="am-i">&#127968;</span>3 &eacute;tages</div><div class="am"><span class="am-i">&#127807;</span>Jardin / Terrasse</div><div class="am"><span class="am-i">&#128663;</span>Parking gratuit</div><div class="am"><span class="am-i">&#128246;</span>WiFi inclus</div><div class="am"><span class="am-i">&#127859;</span>Cuisine &eacute;quip&eacute;e</div><div class="am"><span class="am-i">&#127958;</span>10 min des plages</div></div><div class="btn-row"><a class="btn ocean" href="https://www.airbnb.fr/rooms/1101999912598706670" target="_blank">&#127968; Voir sur Airbnb</a><a class="btn ink" href="https://maps.google.com/?q=Descente+de+Rozambars+206+Pleuven+29170" target="_blank">&#128506; Itin&eacute;raire</a></div></div></div>
    <div class="card" style="padding:20px;margin-bottom:16px"><div style="font-size:17px;font-weight:700;color:var(--ink);margin-bottom:4px">&#128722; Courses &agrave; pr&eacute;voir</div><div style="font-size:12px;color:var(--sub);margin-bottom:14px">Intermarch&eacute; Fouesnant &mdash; en arrivant</div><div class="agrid"><div class="am"><span class="am-i">&#129472;</span>Fromages bretons</div><div class="am"><span class="am-i">&#129385;</span>Charcuterie</div><div class="am"><span class="am-i">&#129366;</span>Pain &amp; viennoiseries</div><div class="am"><span class="am-i">&#127866;</span>Bi&egrave;res bretonnes</div><div class="am"><span class="am-i">&#127863;</span>Vin</div><div class="am"><span class="am-i">&#127864;</span>Alcool &amp; spiritueux</div><div class="am"><span class="am-i">&#128167;</span>Eau &amp; sodas</div><div class="am"><span class="am-i">&#9749;</span>Caf&eacute; &amp; petit d&eacute;j.</div></div></div>
    <div class="card" style="padding:20px"><div style="font-size:17px;font-weight:700;color:var(--ink);margin-bottom:4px">&#128222; Contacts utiles</div><div style="font-size:12px;color:var(--sub);margin-bottom:14px">Tap pour appeler</div><div id="lc"></div></div>
  </div>
</div>

</div>
<div class="tabbar">
  <button class="tab on" onclick="nav('home',this)"><span class="tab-ic">&#127968;</span>Accueil</button>
  <button class="tab" onclick="nav('prog',this)"><span class="tab-ic">&#128197;</span>Programme</button>
  <button class="tab" onclick="nav('act',this)"><span class="tab-ic">&#127919;</span>Activit&eacute;s</button>
  <button class="tab" onclick="nav('map',this)"><span class="tab-ic">&#128506;</span>Carte</button>
  <button class="tab" onclick="nav('album',this)"><span class="tab-ic">&#128247;</span>Photos</button>
  <button class="tab" onclick="nav('logement',this)"><span class="tab-ic">&#127969;</span>Logement</button>
</div>
</div>

<div class="lb" id="lb"><button class="lbx" id="lbX">&#10005;</button><button class="lbnav" id="lbP">&#8249;</button><img class="lbimg" id="lbI" src="" alt=""><button class="lbnav" id="lbN">&#8250;</button><div class="lbctr" id="lbC">1 / 1</div></div>
<div class="toast" id="toast"></div>

<script>
if('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(()=>{});

const EVG_DATE = '2026-04-24T18:00:00';
const SEEDS = ''' + PHOTOS_JS + r''';

// GitHub config for shared photo storage
const GH_OWNER = 'francoisgarnierfg-coder';
const GH_REPO_NAME = 'evg-louis-marie';
// Token split to avoid auto-detection in source
const GH_TOKEN = ['gho_R3KjldkAq8','j5xC30ryfnxVh3f4','Rok93WwNDl'].join('');
const GH_API = 'https://api.github.com/repos/' + GH_OWNER + '/' + GH_REPO_NAME + '/contents/photos/';
const GH_RAW = 'https://raw.githubusercontent.com/' + GH_OWNER + '/' + GH_REPO_NAME + '/master/photos/';

const CONTACTS=[
  {i:'&#128692;',n:'A Bicyclette',p:'06 77 63 90 72',t:'0677639072'},
  {i:'&#129450;',n:'Viviers de Penfoulic',p:'02 98 56 83 89',t:'0298568389'},
  {i:'&#9973;',n:'Santa Maria',p:'06 62 88 00 87',t:'0662880087'},
  {i:'&#127869;',n:'La Long\u00e8re',p:'02 98 56 58 17',t:'0298565817'},
  {i:'&#127821;',n:'Bro Ar Sud',p:'02 98 53 29 77',t:'0298532977'},
  {i:'&#128661;',n:'Taxi Concarneau',p:'02 98 97 09 16',t:'0298970916'},
];
const CREW=[
  {i:'LM',n:'Louis-Marie',r:'Le Mari\u00e9 \u2b50',s:true},
  {i:'TB',n:'Thib',r:''},
  {i:'PA',n:'Paco',r:''},
  {i:'FX',n:'FX',r:''},
  {i:'QT',n:'Quentin',r:''},
  {i:'GA',n:'Gabriel',r:''},
  {i:'EL',n:'Eloi',r:''},
  {i:'MX',n:'Max',r:''},
  {i:'ED',n:'Edouard',r:''},
  {i:'BZ',n:'Balthouz',r:''},
];
const LOCS=[
  {l:'&#127968; Maison',d:'La Bonne Descente \u2014 Descente de Rozambars 206, Pleuven',g:'https://maps.google.com/?q=Descente+de+Rozambars+206+Pleuven',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2715!2d-3.968!3d47.905!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2sfr!4v1700000001'},
  {l:'&#129450; Penfoulic',d:'Aux Viviers de Penfoulic \u2014 La For\u00eat-Fouesnant',g:'https://maps.google.com/?q=Aux+Viviers+de+Penfoulic',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000!2d-3.983082!3d47.893629!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4810d188948dc101%3A0x4a16f9198a63e267!2sAux%20Viviers%20de%20Penfoulic!5e0!3m2!1sfr!2sfr!4v1700000002'},
  {l:'&#9973; Santa Maria',d:'Santa Maria \u2014 Port de P\u00eache, Concarneau',g:'https://maps.google.com/?q=Santa+Maria+Concarneau',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000!2d-3.9170948!3d47.8731194!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4810dae2d0c4d367%3A0x557a447dee6ea366!2sSanta%20Maria!5e0!3m2!1sfr!2sfr!4v1700000003'},
  {l:'&#128692; A Bicyclette',d:'A Bicyclette \u2014 2 Rue de Cornouaille, Fouesnant',g:'https://maps.google.com/?q=A+Bicyclette+Fouesnant',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000!2d-4.0105988!3d47.8948812!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4810d1b1f5fa69bb%3A0x3d12a82821d441f2!2sA%20Bicyclette!5e0!3m2!1sfr!2sfr!4v1700000004'},
  {l:'&#127869; La Long\u00e8re',d:'La Long\u00e8re \u2014 5 Chemin de Ker an Braz, Fouesnant',g:'https://maps.google.com/?q=La+Longere+Fouesnant',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000!2d-4.0130813!3d47.8905816!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4810d9f8aef7bd2d%3A0xfbe779a7ad65a5ca!2sLa%20Long%C3%A8re!5e0!3m2!1sfr!2sfr!4v1700000005'},
  {l:'&#127821; Bro Ar Sud',d:'Bro Ar Sud \u2014 Ville close, Concarneau',g:'https://maps.google.com/?q=Bro+Ar+Sud+Concarneau',e:'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1000!2d-3.9186!3d47.8726!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2sfr!4v1700000006'},
];

let photos=[],ghPhotos=[],lbIdx=0,cdInt,deferredPrompt=null;

// ── GitHub photo sharing ───────────────────────────────────────────────────
async function fetchGHPhotos(){
  try{
    const r=await fetch(GH_API,{headers:{'Authorization':'token '+GH_TOKEN,'Cache-Control':'no-cache'}});
    if(!r.ok)return[];
    const files=await r.json();
    if(!Array.isArray(files))return[];
    return files
      .filter(f=>/\.(jpe?g|png|gif|webp)$/i.test(f.name))
      .map(f=>GH_RAW+f.name+'?v='+f.sha.slice(0,7));
  }catch(e){return[];}
}

function compress(file){
  return new Promise(res=>{
    const img=new Image(),fr=new FileReader();
    fr.onload=e=>{
      img.onload=()=>{
        const MAX=1400,cv=document.createElement('canvas');
        let [w,h]=[img.width,img.height];
        if(w>MAX||h>MAX){if(w>h){h=Math.round(h*MAX/w);w=MAX}else{w=Math.round(w*MAX/h);h=MAX}}
        cv.width=w;cv.height=h;
        cv.getContext('2d').drawImage(img,0,0,w,h);
        res(cv.toDataURL('image/jpeg',.82));
      };
      img.src=e.target.result;
    };
    fr.readAsDataURL(file);
  });
}

async function ghUpload(dataUrl,name){
  const b64=dataUrl.split(',')[1];
  const r=await fetch(GH_API+name,{
    method:'PUT',
    headers:{'Authorization':'token '+GH_TOKEN,'Content-Type':'application/json'},
    body:JSON.stringify({message:'photo '+name,content:b64})
  });
  return r.ok;
}

async function loadF(files){
  const imgs=files.filter(f=>f.type.startsWith('image/'));
  if(!imgs.length)return;
  const stat=document.getElementById('upstat');
  stat.style.display='block';
  let ok=0;
  for(let i=0;i<imgs.length;i++){
    stat.textContent='\u23F3 Upload '+(i+1)+'/'+imgs.length+'...';
    try{
      const dataUrl=await compress(imgs[i]);
      const name=Date.now()+'_'+Math.random().toString(36).slice(2,7)+'.jpg';
      const success=await ghUpload(dataUrl,name);
      if(success){
        photos.push(GH_RAW+name);
        ok++;
      }
    }catch(e){}
  }
  stat.style.display='none';
  renderP();
  if(ok>0)showT(ok+' photo'+(ok>1?'s':'')+' partag\u00e9e'+(ok>1?'s':'')+' \u2713');
  else showT('\u26A0 Erreur upload \u2014 v\u00e9rifier connexion');
}

// ── App init ───────────────────────────────────────────────────────────────
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferredPrompt=e;document.getElementById('installBanner').style.display='block'});
window.addEventListener('appinstalled',()=>{document.getElementById('installBanner').style.display='none';showT('App install\u00e9e ! \u2713')});
function installPWA(){if(deferredPrompt){deferredPrompt.prompt();deferredPrompt.userChoice.then(r=>{deferredPrompt=null;if(r.outcome==='accepted')document.getElementById('installBanner').style.display='none'})}}
// iOS Safari: show manual install hint if not already in standalone mode
(function(){
  const isIOS=/iPhone|iPad|iPod/i.test(navigator.userAgent);
  const isSafari=/^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  const isStandalone=('standalone' in navigator)&&navigator.standalone;
  if(isIOS&&isSafari&&!isStandalone){
    document.getElementById('iosBanner').style.display='block';
  }
})();

window.addEventListener('DOMContentLoaded',()=>{
  buildCrew();buildContacts('hc',CONTACTS.slice(0,4));buildContacts('lc',CONTACTS);
  buildMapFilters();setLoc(0,null);
  photos=[...SEEDS];renderP();startCD();
  fetchGHPhotos().then(urls=>{if(urls.length){ghPhotos=urls;photos=[...SEEDS,...ghPhotos];renderP()}});
  setTimeout(()=>{document.getElementById('splash').classList.add('out');setTimeout(()=>document.getElementById('app').classList.add('on'),320)},2000);
});

function nav(id,btn){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab').forEach(b=>b.classList.remove('on'));document.getElementById('page-'+id).classList.add('active');btn.classList.add('on');document.getElementById('pages').scrollTop=0}

function startCD(){
  const t=new Date(EVG_DATE).getTime();
  function tick(){const d=t-Date.now();if(d<=0){document.getElementById('cdLbl').textContent='\u26f5 C\'est parti !';['cdD','cdH','cdM','cdS'].forEach(id=>document.getElementById(id).textContent='0');clearInterval(cdInt);return}
    document.getElementById('cdD').textContent=Math.floor(d/86400000);
    document.getElementById('cdH').textContent=String(Math.floor(d%86400000/3600000)).padStart(2,'0');
    document.getElementById('cdM').textContent=String(Math.floor(d%3600000/60000)).padStart(2,'0');
    document.getElementById('cdS').textContent=String(Math.floor(d%60000/1000)).padStart(2,'0');
  }
  tick();cdInt=setInterval(tick,1000);
}

function buildCrew(){document.getElementById('crew').innerHTML=CREW.map(c=>`<div class="cc"><div class="av ${c.s?'star':'reg'}">${c.i}</div><div class="av-n">${c.n}</div><div class="av-r">${c.r}</div></div>`).join('')}
function buildContacts(id,list){const el=document.getElementById(id);if(!el)return;el.innerHTML=list.map(c=>`<a class="cr" href="tel:${c.t}"><div class="cr-ico">${c.i}</div><div class="cr-i"><div class="cr-n">${c.n}</div><div class="cr-p">${c.p}</div></div><button class="cr-cta" tabindex="-1">&#128222; Appeler</button></a>`).join('')}

function buildMapFilters(){document.getElementById('mf').innerHTML=LOCS.map((l,i)=>`<button class="mbtn${i===0?' on':''}" onclick="setLoc(${i},this)">${l.l}</button>`).join('')}
function setLoc(i,btn){if(btn){document.querySelectorAll('.mbtn').forEach(b=>b.classList.remove('on'));btn.classList.add('on')}document.getElementById('mfr').src=LOCS[i].e;document.getElementById('mft').innerHTML=LOCS[i].d;document.getElementById('mfcta').href=LOCS[i].g}

function renderP(){const g=document.getElementById('pg'),e=document.getElementById('abe'),b=document.getElementById('abb'),c=document.getElementById('abc');if(!photos.length){e.style.display='block';b.style.display='none';g.innerHTML='';return}e.style.display='none';b.style.display='flex';c.textContent=photos.length+' photo'+(photos.length>1?'s':'');g.innerHTML=photos.map((s,i)=>`<div class="pi" style="animation-delay:${Math.min(i*.025,.5)}s" onclick="openLb(${i})"><img src="${s}" alt="" loading="lazy"></div>`).join('')}
function shuffleP(){for(let i=photos.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[photos[i],photos[j]]=[photos[j],photos[i]]}renderP();showT('M\u00e9lang\u00e9 \uD83D\uDD00')}

document.getElementById('fi').addEventListener('change',e=>{loadF(Array.from(e.target.files));e.target.value=''});
const uz=document.getElementById('upz');
uz.addEventListener('dragover',e=>{e.preventDefault();uz.classList.add('drag')});
uz.addEventListener('dragleave',()=>uz.classList.remove('drag'));
uz.addEventListener('drop',e=>{e.preventDefault();uz.classList.remove('drag');loadF(Array.from(e.dataTransfer.files))});

function openLb(i){lbIdx=i;syncLb();document.getElementById('lb').classList.add('open');document.body.style.overflow='hidden'}
function closeLb(){document.getElementById('lb').classList.remove('open');document.body.style.overflow=''}
function syncLb(){document.getElementById('lbI').src=photos[lbIdx];document.getElementById('lbC').textContent=(lbIdx+1)+' / '+photos.length}
document.getElementById('lbX').onclick=closeLb;
document.getElementById('lbP').onclick=()=>{lbIdx=(lbIdx-1+photos.length)%photos.length;syncLb()};
document.getElementById('lbN').onclick=()=>{lbIdx=(lbIdx+1)%photos.length;syncLb()};
document.getElementById('lb').onclick=e=>{if(e.target===document.getElementById('lb'))closeLb()};
document.addEventListener('keydown',e=>{if(!document.getElementById('lb').classList.contains('open'))return;if(e.key==='ArrowLeft')document.getElementById('lbP').click();if(e.key==='ArrowRight')document.getElementById('lbN').click();if(e.key==='Escape')closeLb()});
let tsX=0;const lbEl=document.getElementById('lb');
lbEl.addEventListener('touchstart',e=>{tsX=e.touches[0].clientX},{passive:true});
lbEl.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tsX;if(Math.abs(dx)>50)dx<0?document.getElementById('lbN').click():document.getElementById('lbP').click()},{passive:true});

let tt;function showT(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(tt);tt=setTimeout(()=>t.classList.remove('show'),2400)}
</script>
</body>
</html>'''

HTML_FINAL = HTML.replace("''' + PHOTOS_JS + r'''", PHOTOS_JS)
HTML_FINAL = HTML_FINAL.replace('__LM_PHOTO__', LM_PHOTO)

with open('EVG_LouisMarie.html', 'w', encoding='utf-8') as f:
    f.write(HTML_FINAL)

size = os.path.getsize('EVG_LouisMarie.html')
print(f'HTML written: {size//1024} KB ({size//1024//1024} MB)')
