# GitHub 프로필 적용 안내

이 ZIP 안의 `README.md` 및 `assets/` 폴더를 프로필 저장소의 루트에 복사하세요.

Dark #8BC34A / Light #33691E는 방문자의 GitHub 테마에 맞춰 자동 변경됩니다.
`cat tech-stack.md` 뒤 커서가 깜빡이는 2프레임 Animated WebP입니다.
전체 항목: Skills 13, Databases 5, Tools 9 — 총 27개.

이미지의 모든 항목은 이미지 안에 렌더링되어 있습니다. 수정할 때는 `render_terminal.py`를 편집한 뒤 실행해서 다시 생성하세요.

## 재생성 방법

```bash
python -m pip install Pillow
python render_terminal.py
```

픽셀 단위로 동일한 결과를 만들려면 Inter와 DejaVu Sans Mono 폰트를 사용하세요. 폰트 파일은 동봉하지 않습니다.
Windows / macOS에서 시스템 대체 폰트를 사용할 수 있지만 자간과 태그 너비에 차이가 생길 수 있습니다. 환경변수 `TERMINAL_MONO_FONT`, `TERMINAL_MONO_BOLD_FONT`, `TERMINAL_SANS_FONT`, `TERMINAL_BOLD_FONT`, `TERMINAL_MEDIUM_FONT`으로 설치된 폰트 경로를 지정할 수 있습니다.

생성 결과는 `assets/terminal-dark.webp`, `assets/terminal-light.webp`와 ZIP 패키지입니다.
