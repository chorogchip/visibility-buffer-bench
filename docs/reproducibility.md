# 재현성

## Clean environment 절차

지원 기준은 Windows, Direct3D 12, MSVC, CMake 3.20+, Ninja, Python 3.11+다. 저장소 clone 후 scene이 필요 없는 smoke는 다음 두 명령으로 확인한다.

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/reproduce.py --suite smoke --build --overwrite
```

`--build`는 `out/build/reproduce-Release`를 configure/build한다. Visual Studio developer shell이 아니어도 설치된 `vcvars64.bat`을 찾아 같은 명령 안에서 MSVC 환경을 구성한다.

그래프의 직접 의존성은 `scripts/requirements.txt`에 검증한 버전으로 고정한다. C++ dependency revision과 외부 코드 라이선스는 `CMakeLists.txt`, `THIRD_PARTY_NOTICES.md`가 기준이다.

## Machine-local 입력

실험 spec에는 개인 PC의 절대 경로를 넣지 않는다. executable, camera와 scene은 다음 alias를 사용한다.

- `@executable/release`, `@executable/debug`
- `@camera/<name>`
- `@scene/sponza`, `@scene/bistro` 등

`experiments/local.example.json`을 `experiments/local.json`으로 복사해 scene 경로 또는 비표준 executable을 지정한다. 이 파일은 Git ignore다. alias가 없는 scene sample은 `skipped_missing_asset`이 되고 같은 JSON의 나머지 sample은 계속된다.

## 실행 전에 확인할 것

```powershell
python scripts/reproduce.py --verify
python scripts/reproduce.py --suite all --dry-run
```

검증기는 canonical top-level key, 현재 `ProgramArgument`, renderer variant 1–15, 절대 scene/camera 경로, sweep/sample 충돌, reproduction fidelity를 확인한다.

## 생성되는 증거

`results/environment.json`에는 OS, Python, processor, GPU/driver/VRAM, Git commit/dirty state, executable path와 SHA-256이 기록된다. 각 experiment 폴더에는 입력 spec과 alias가 풀린 spec을 모두 복사한다.

- `raw.csv`: C++ ProgramResult와 runner context
- `runs.csv`: run 단위 정규화 표
- `passes.csv`: pass 단위 long-form 표
- `frames.csv`: playback/result sidecar의 frame 단위 표
- `run_report.json`: success/salvaged/failed/skipped와 진단
- `artifacts.json`: row 수와 plot 결과
- `plots/manifest.json`: 생성된 PNG/SVG 목록

그래프와 CSV는 source가 아니라 생성물이다. `results/`는 Git에 포함하지 않는다.

## Dashboard 전달

재현 명령이 끝나면 `results/dashboard_bundle.json`이 자동 생성된다. 이 파일 하나에 environment, experiment summary, normalized runs와 base64 PNG가 포함된다.

```powershell
python scripts/export_dashboard.py
cd ..\visibility-buffer-bench-dasboard
npm run data:import -- ..\visibility-buffer-bench\results\dashboard_bundle.json
```

따라서 dashboard와 benchmark 사이에 CSV/PNG 폴더 구조를 공유하거나 대량 파일을 복사할 필요가 없다.

## 현재 검증 기준선

2026-08-19에 clean `out/build/reproduce-Release` configure/build를 완료했고 synthetic smoke 6/6이 success, salvaged/failed/skipped 0이었다. 정규화 결과는 runs 6, passes 39, frames 0이었으며 total과 pass-breakdown PNG/SVG, 단일 dashboard bundle이 생성됐다.

같은 날 Sponza, Sponza + Ivy, Bistro Exterior/Interior 경로를 구성해 portfolio suite를 검증했다. 15 specs의 786 runs 중 783이 success였고 failed/salvaged는 0이었다. 나머지 3개는 검증 머신에 San Miguel, Sun Temple, Zero Day가 없어 `skipped_missing_asset`으로 기록됐다.

Sponza와 Bistro barycentric validation은 raster reference와 VisBuf reconstruction을 합쳐 28/28 runs가 전체 camera playback을 완료했다. Sponza run마다 2,500 measured frames와 42 captures, Bistro run마다 5,500 measured frames와 46 captures 및 sidecar CSV가 생성됐다. 장면 없이 생기는 skip과 renderer crash는 `run_report.json`에서 계속 구분한다.
