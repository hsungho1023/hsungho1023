"""
Run: python render_terminal.py
Requires Pillow; font files are loaded from your installed system fonts, not packaged.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import zipfile
import os

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)
W, H, SCALE = 1200, 1100, 2
SKILLS = ['C#', '.NET', 'Java', 'Spring', 'Spring Boot', 'Thymeleaf', 'JavaScript',
          'jQuery', 'React', 'Vue.js', 'HTML5', 'CSS', 'Bootstrap']
DB = ['Oracle', 'MySQL', 'MariaDB', 'Microsoft SQL Server', 'PostgreSQL']
TOOLS = ['Eclipse', 'IntelliJ IDEA', 'Visual Studio Code', 'Notion', 'Adobe Photoshop',
         'Postman', 'DBeaver', 'ChatGPT Codex', 'GitHub Copilot']
assert (len(SKILLS), len(DB), len(TOOLS)) == (13, 5, 9)
# For pixel-identical regeneration use Inter and DejaVu Sans Mono. No fonts are bundled.
# Override individual paths through env vars on Windows/macOS if necessary.
def pick_font(env_var, *candidates):
    override = os.environ.get(env_var)
    if override:
        if Path(override).is_file():
            return Path(override)
        raise FileNotFoundError(f"{env_var} points to missing file: {override}")
    for candidate in candidates:
        if Path(candidate).is_file():
            return Path(candidate)
    raise FileNotFoundError(
        f"Required font not found. Set {env_var} to an installed font file."
    )

FONT_FILES = {
    'mono': pick_font('TERMINAL_MONO_FONT',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        'C:/Windows/Fonts/consola.ttf',
        '/System/Library/Fonts/Menlo.ttc'),
    'monobold': pick_font('TERMINAL_MONO_BOLD_FONT',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        'C:/Windows/Fonts/consolab.ttf',
        '/System/Library/Fonts/Menlo.ttc'),
    'sans': pick_font('TERMINAL_SANS_FONT',
        '/usr/share/fonts/opentype/inter/Inter-Regular.otf',
        'C:/Windows/Fonts/segoeui.ttf',
        '/System/Library/Fonts/Helvetica.ttc'),
    'bold': pick_font('TERMINAL_BOLD_FONT',
        '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf',
        'C:/Windows/Fonts/segoeuib.ttf',
        '/System/Library/Fonts/Helvetica.ttc'),
    'medium': pick_font('TERMINAL_MEDIUM_FONT',
        '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
        'C:/Windows/Fonts/segoeui.ttf',
        '/System/Library/Fonts/Helvetica.ttc'),
}

def font(sz, kind='mono'):
    return ImageFont.truetype(str(FONT_FILES[kind]), round(sz * SCALE))

def palette(mode):
    return ({'bg':'#171B16','head':'#222A20','surface':'#222A20', 'fg':'#E8EDE4',
             'muted':'#A7B0A2','line':'#364031','accent':'#8BC34A'} if mode=='dark' else
            {'bg':'#FAFBF7','head':'#F0F4EB','surface':'#F0F4EB', 'fg':'#252B22',
             'muted':'#687364','line':'#D8E0D2','accent':'#33691E'})

class P:
    def __init__(self,mode):
        self.c = palette(mode)
        self.im = Image.new('RGB',(W*SCALE,H*SCALE),self.c['bg'])
        self.d = ImageDraw.Draw(self.im)

    def box(self,x0,y0,x1,y1,fill,outline=None,width=1,r=0):
        xy=[round(v*SCALE) for v in (x0,y0,x1,y1)]
        self.d.rounded_rectangle(xy,radius=r*SCALE,fill=fill,outline=outline,width=width*SCALE)

    def line(self,x0,y0,x1,y1,color,width=1):
        self.d.line([(round(x0*SCALE),round(y0*SCALE)),(round(x1*SCALE),round(y1*SCALE))],fill=color,width=width*SCALE)

    def circle(self,x,y,r,color):
        self.d.ellipse([(x-r)*SCALE,(y-r)*SCALE,(x+r)*SCALE,(y+r)*SCALE],fill=color)

    def width(self,text,size=20,kind='mono'):
        return self.d.textlength(text,font=font(size,kind))/SCALE

    def ink_bbox(self,text,size=20,kind='mono'):
        f = font(size,kind)
        return self.d.textbbox((0,0),text,font=f,anchor='lt')

    def text(self,x,y,text,size=20,kind='mono',color=None):
        # x,y are coordinates of visible ink upper-left; avoids font-top-offset errors.
        f = font(size,kind)
        l,t,r,b = self.ink_bbox(text,size,kind)
        self.d.text((int(round(x*SCALE))-l,int(round(y*SCALE))-t),text,font=f,fill=color or self.c['fg'],anchor='lt')

    def center_text(self,cx,cy,text,size=20,kind='mono',color=None):
        # Optical center of visible glyph extents: every tag label is centered in its cell.
        f=font(size,kind)
        l,t,r,b=self.ink_bbox(text,size,kind)
        self.d.text((round(cx*SCALE-(l+r)/2),round(cy*SCALE-(t+b)/2)),text,
                    font=f,fill=color or self.c['fg'],anchor='lt')

    def final(self):
        return self.im.resize((W,H),Image.Resampling.LANCZOS)

def render(mode, cursor_on):
    p=P(mode); c=p.c
    # Entire terminal window, matching the approved A안 v1 mockup.
    p.box(2,2,W-3,H-3,c['bg'],c['line'],2,18)
    p.box(4,4,W-5,71,c['head'],r=15)
    p.box(4,52,W-5,72,c['head'])
    p.line(5,72,W-5,72,c['line'])
    for i,x in enumerate((40,61,82)):
        p.circle(x,36,6,c['accent'] if i==0 else c['line'])
    header='hsungho1023@github ~ / profile'
    p.center_text(W/2,36,header,18,'mono',c['muted'])
    p.box(1126,22,1159,49,None,c['muted'],1,5)
    p.line(1134,28,1140,35,c['muted'],2)
    p.line(1140,35,1134,42,c['muted'],2)
    p.line(1144,43,1151,43,c['muted'],2)

    # Hero / prompt. Separate rendering keeps all prompt symbols and command labels aligned.
    p.center_text(83,121,'~ $',26,'mono',c['accent'])
    # Align visible ink center of command text to the prompt (~ $), instead of its top.
    # Original: p.text(118,107,...), ink-center y=117.25 vs prompt y=121.
    p.center_text(118+p.width('whoami',26)/2,121,'whoami',26,'mono',c['fg'])
    p.text(48,161,'Web Developer',58,'bold',c['fg'])
    p.text(49,238,'Backend · Frontend · Databases',23,'sans',c['muted'])
    p.center_text(82,316,'~ $',24,'mono',c['accent'])
    cmd='cat tech-stack.md'
    # Original: p.text(117,301,...), ink-center y=310.25 vs prompt y=316.
    p.center_text(117+p.width(cmd,24)/2,316,cmd,24,'mono',c['fg'])
    if cursor_on:
        cx=117+p.width(cmd,24)+11
        # Keep cursor on the command line's ink area; old y=304..329 appeared low.
        # New y=305..325: shorter and shifted up optically relative to raised command.
        p.box(cx,305,cx+12,325,c['accent'],r=1)
    p.line(48,365,1152,365,c['line'],2)

    for idx,(command,items,y_head,divider) in enumerate([
        ('skills --all', SKILLS,399,614),
        ('databases --all', DB,645,771),
        ('tools --all', TOOLS,802,1007),
    ]):
        # All section prompt rows are exactly 2px higher than the previous release.
        # Move the prompt, command and right-hand counter together to preserve baselines.
        p.center_text(80,y_head+10,'~ $',22,'mono',c['accent'])
        p.center_text(112+p.width(command,22)/2,y_head+10,command,22,'mono',c['fg'])
        count=f'{len(items):02d} items'
        p.center_text(1152-p.width(count,16)/2,y_head+11,count,16,'mono',c['muted'])
        x=48
        y=y_head+54
        for name in items:
            # Text and > marker as a unified centered group, identical cell heights.
            inner_text_w=p.width(name,20)
            chip_w=round(inner_text_w+65)
            if x+chip_w>1153:
                x=48
                y+=60
            chip_h=48
            p.box(x,y,x+chip_w,y+chip_h,c['surface'],c['line'],1,5)
            group_w=12+12+inner_text_w
            group_x=x+(chip_w-group_w)/2
            center_y=y+chip_h/2
            # Geometric > sign: same centerline and size in all 27 chips.
            chevron_x=group_x+5
            p.line(chevron_x-3,center_y-5,chevron_x+2,center_y,c['accent'],2)
            p.line(chevron_x+2,center_y,chevron_x-3,center_y+5,c['accent'],2)
            p.center_text(group_x+24+inner_text_w/2,center_y,name,20,'mono',c['fg'])
            x+=chip_w+11
        assert y+48 < divider, (command,y,divider)
        p.line(48,divider,1152,divider,c['line'],2)

    p.circle(55,1042,5,c['accent'])
    p.center_text(73+p.width('27 entries loaded',17)/2,1042,'27 entries loaded',17,'mono',c['muted'])
    p.center_text(1152-p.width('[EOF]',18)/2,1042,'[EOF]',18,'mono',c['accent'])
    return p.final()


def main():
    for mode in ('dark','light'):
        on=render(mode,True)
        off=render(mode,False)
        dest=ASSETS/f'terminal-{mode}.webp'
        on.save(dest,format='WEBP',save_all=True,append_images=[off],duration=[600,550],
                loop=0,quality=91,method=6)
        anim=Image.open(dest)
        assert anim.format=='WEBP' and anim.n_frames==2 and anim.size==(W,H)
        frames=[]
        for index in range(2):
            anim.seek(index)
            frames.append(anim.convert('RGB').copy())
        diff=ImageChops.difference(frames[0],frames[1])
        bbox=diff.getbbox()
        assert bbox and 300 <= bbox[1] <= 307, ('Cursor upper edge is not where expected',bbox)
        assert 323 <= bbox[3] <= 330, ('Unexpected non-cursor animation',bbox)
        expected_x = 117 + P(mode).width('cat tech-stack.md',24) + 11
        assert expected_x-6 <= bbox[0] <= expected_x+3, ('Cursor X differs from expected', bbox)
        assert expected_x+8 <= bbox[2] <= expected_x+18, ('Animation changed outside cursor',bbox)
        print(mode,dest.stat().st_size,'bytes, 2 frames, change-bbox',bbox)
    # Readme includes only two WebP images: GitHub changes them with theme.
    (HERE/'README.md').write_text('''<!-- GitHub Profile: A안 Terminal 정밀 목업 v1 / vertical alignment corrected -->\n<!-- Dark #8BC34A / Light #33691E; both images are animated WebP. -->\n\n<p align="center">\n  <picture>\n    <source media="(prefers-color-scheme: dark)" srcset="./assets/terminal-dark.webp" />\n    <source media="(prefers-color-scheme: light)" srcset="./assets/terminal-light.webp" />\n    <img src="./assets/terminal-light.webp" width="1200" alt="hsungho1023 Web Developer: 13 Skills, 5 Databases, 9 Tools in a terminal interface." />\n  </picture>\n</p>\n''', encoding='utf-8')
    (HERE/'USAGE.md').write_text('''# GitHub 프로필 적용 안내\n\n이 ZIP 안의 `README.md` 및 `assets/` 폴더를 프로필 저장소의 루트에 복사하세요.\n\nDark #8BC34A / Light #33691E는 방문자의 GitHub 테마에 맞춰 자동 변경됩니다.\n`cat tech-stack.md` 뒤 커서가 깜빡이는 2프레임 Animated WebP입니다.\n전체 항목: Skills 13, Databases 5, Tools 9 — 총 27개.\n\n이미지의 모든 항목은 이미지 안에 렌더링되어 있습니다. 수정할 때는 `render_terminal.py`를 편집한 뒤 실행해서 다시 생성하세요.

## 재생성 방법

```bash
python -m pip install Pillow
python render_terminal.py
```

픽셀 단위로 동일한 결과를 만들려면 Inter와 DejaVu Sans Mono 폰트를 사용하세요. 폰트 파일은 동봉하지 않습니다.
Windows / macOS에서 시스템 대체 폰트를 사용할 수 있지만 자간과 태그 너비에 차이가 생길 수 있습니다. 환경변수 `TERMINAL_MONO_FONT`, `TERMINAL_MONO_BOLD_FONT`, `TERMINAL_SANS_FONT`, `TERMINAL_BOLD_FONT`, `TERMINAL_MEDIUM_FONT`으로 설치된 폰트 경로를 지정할 수 있습니다.

생성 결과는 `assets/terminal-dark.webp`, `assets/terminal-light.webp`와 ZIP 패키지입니다.\n''', encoding='utf-8')
    zip_path=HERE.with_suffix('.zip')
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        package_files = [HERE/'README.md', HERE/'USAGE.md', HERE/'render_terminal.py',
                         ASSETS/'terminal-dark.webp', ASSETS/'terminal-light.webp']
        for file in package_files:
            archive.write(file,file.relative_to(HERE))
    with zipfile.ZipFile(zip_path) as archive:
        names=archive.namelist()
        assert all(not name.lower().endswith(('.png','.jpg','.jpeg','.svg','.gif')) for name in names)
        assert set(names) == {'README.md','USAGE.md','render_terminal.py',
                              'assets/terminal-dark.webp','assets/terminal-light.webp'}
        print(zip_path,zip_path.stat().st_size,'bytes; entries:',names)

if __name__ == '__main__':
    main()
