
import json, os, importlib.util
from collections import defaultdict

STORE = "/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps"
OUTDIR = "/workspace/competitor-scan-2026-11-21"
spec = importlib.util.spec_from_file_location("fin", os.path.join(OUTDIR, "finalize.py"))
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

fin.ALIASES.update({
    "jingle-bell-rock-mean-girls": "jingle-bell-rock",
    "mean-girls-jingle-bell-rock": "jingle-bell-rock",
    "give-it-all-to-me": "give-it-all",
    "rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "put-the-rollie-on-my-wrist": "shoulder-carry-im-the-one",
    "im-the-one": "shoulder-carry-im-the-one",
    "im-the-one-shoulder-carry": "shoulder-carry-im-the-one",
    "cause-im-the-one": "shoulder-carry-im-the-one",
    "shoulder-carry": "shoulder-carry-im-the-one",
    "feel-the-pressure": "mourinho-pressure",
    "mourinho-pressure-original-audio": "mourinho-pressure",
    "quiet-on-the-creek-dance": "quiet-on-the-creek",
    "jingle-bell-brazil-dance": "jingle-bell-brazil",
    "la-tormenta-de-arena": "te-he-perdido",
    "catch-santa-on-camera": "santa-caught-on-camera",
    "youre-under-arrest": "under-arrest-dance",
    "youre-under-arrest-dance": "under-arrest-dance",
    "tidal-wave-video": "tidal-wave",
    "su-gibi-git-su-gibi-gel": "tidal-wave",
    "christmas-pajama-dance": "christmas-dance",
    "smalltown-boy-ai-dance": "smalltown-boy-cat",
    "smalltown-boy": "smalltown-boy-cat",
    "ai-cafe": "first-time-in-a-fancy-cafe",
    "mini-tricycle-crash": "tricycle-crash",
    "trouble-maker-dance": "trouble-maker",
    "gta-5-goodbye": "gta-farewell",
    "gta-6-farewell": "gta-farewell",
    "goodbye-gta-5": "gta-farewell",
    "pterodactyl-juarez": "mexico-pterodactyl",
    "kung-fu-goalkeeper": "funny-goalkeeper",
    "oh-my-carne-asada-singing-dog": "oh-my-carne-asada",
    "carne-asada-singing-dog": "oh-my-carne-asada",
    "dip-on-em-dance": "dip-on-em",
    "gta-wasted-meme": "gta-wasted",
    "jatayu-indian-mythology": "jatayu",
    "wassup-in-a-minute-dance": "wassup-in-a-minute",
    "wassup-dance": "wassup-in-a-minute",
    "in-a-minute-wassup": "wassup-in-a-minute",
    "wassup-in-a-minute-wassup": "wassup-in-a-minute",
    "ai-fashion-video-edit": "fashion-video-edit",
    "boom-clap-confetti-cannon": "boom-clap-confetti",
    "boom-clap-trend": "boom-clap-confetti",
    "gta-6-girlfriend-lucia": "gta-6-lucia",
    "i-am-a-celebrity": "im-a-celebrity-jungle-filter",
    "im-a-celebrity": "im-a-celebrity-jungle-filter",
    "im-a-celebrity-jungle-filter": "im-a-celebrity-jungle-filter",
    "hanuman-ji": "hanuman",
    "here-we-go-again-gta-meme": "here-we-go-again-gta",
    "here-we-go-again-gta": "here-we-go-again-gta",
    "the-box-podium-meme": "the-box-podium",
    "the-box-podium-ai-meme": "the-box-podium",
    "water-flyboard": "flyboard",
    "mr-tumble-filter": "mr-tumble",
    "london-mews-house": "mews-house-london",
    "i-just-wanted-to-take-another-look-at-you": "take-another-look-at-you",
    "thats-my-opinion": "thats-my-opinion",
    "gta-ai-filter": "gta-6-loading-screen",
    "gta-6-loading-screen": "gta-6-loading-screen",
    "hotel-lobby-dance": "hotel-lobby",
    "kiss-cam": "kiss-cam",
    "coldplay-kiss-cam": "kiss-cam",
})

def core_of(slug, title=""):
    # try fin helpers
    if hasattr(fin, "canonical_core"):
        return fin.canonical_core(slug, title)
    if hasattr(fin, "core_key"):
        return fin.core_key(slug, title)
    if hasattr(fin, "normalize_core"):
        return fin.normalize_core(slug)
    # fallback inspect
    return None

# print helper names
print("fin helpers:", [n for n in dir(fin) if "core" in n.lower() or "alias" in n.lower() or "norm" in n.lower() or "overlap" in n.lower() or "canon" in n.lower() or "slug" in n.lower()])
