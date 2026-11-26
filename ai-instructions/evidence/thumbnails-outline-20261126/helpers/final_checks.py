import hashlib,json,struct,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
from PySide6 import QtGui
repo=Path('C:/Users/dgium/Documents/__Apps/FreeCAD/FreeCAD-Plus')
root=Path('C:/Users/dgium/Documents/__Apps/_temp builds/FreeCAD-Plus')
out=root/'validation/thumbnails-outline-20261126'
approved=Path('C:/Users/dgium/Documents/__Apps/_temp builds/app-render-companion/sessions/2e9aa4de838c/candidate/icon.svg')
svg=repo/'src/Gui/Icons/freecad-plus.svg'
assert svg.read_bytes()==approved.read_bytes()
original=ET.fromstring((repo.parent/'icon-outline-preview/review-source/original.svg').read_bytes())
candidate=ET.fromstring(svg.read_bytes())
for identity in ('g1','freecad-plus-overlay'):
    find=lambda tree:next(e for e in tree.iter() if e.get('id')==identity)
    assert ET.tostring(find(original))==ET.tostring(find(candidate))
ico=(repo/'src/Main/icon.ico').read_bytes()
assert struct.unpack_from('<HHH',ico)==(0,1,10)
sizes=[]
for i in range(10):
    width,height,_,_,_,_,length,offset=struct.unpack_from('<BBBBHHII',ico,6+16*i)
    width=width or 256;height=height or 256
    image=QtGui.QImage.fromData(ico[offset:offset+length])
    assert not image.isNull() and image.width()==width and image.height()==height
    assert image.hasAlphaChannel() and image.pixelColor(0,0).alpha()==0
    sizes.append(width)
manifest=json.loads((out/'install-manifest.json').read_text())
for item in manifest:
    assert hashlib.sha256((root/'app'/item['file']).read_bytes()).hexdigest()==item['sha256']
# Inspect, without changing, the owner's one visually blank saved PNG.
paths=[Path(n.text) for n in ET.parse(root/'profiles/owner-test/user.cfg').findall(".//FCParamGroup[@Name='RecentFiles']/FCText")]
blank_count=0
for path in paths:
    with zipfile.ZipFile(path) as z:image=QtGui.QImage.fromData(z.read('thumbnails/Thumbnail.png'))
    colors={image.pixelColor(x,y).rgba() for y in range(image.height()) for x in range(image.width())}
    if len(colors)==1:blank_count+=1
result=dict(approved_svg_exact=True,original_artwork_and_plus_unchanged=True,
            transparent_ico_sizes=sizes,installed_hashes_match=len(manifest),uniform_saved_owner_previews=blank_count)
(out/'final-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
