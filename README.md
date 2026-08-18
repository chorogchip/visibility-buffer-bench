# Visibility Buffer Bench

Forward, Deferred, Triangle Visibility Buffer(TVB)의 비용 구조를 동일한 Direct3D 12 환경에서 비교하는 재현 가능한 렌더링 연구 프로젝트다. 단순히 평균 프레임 시간을 나열하지 않고 overdraw, geometry density, material class, cache locality, resolution을 독립적으로 바꾸면서 어떤 비용이 승패를 만드는지 pass 단위로 추적한다.

## 대표 결과

현재 구현과 RTX 5060 Ti 16GB에서 수행한 1,301-run 후속 캠페인에서는 Deferred + depth pre-pass가 전체 카메라 경로의 세 장면에서 모두 더 빨랐다.

| Scene | DeferredPrepass | VisBuf | VisBuf overhead |
|---|---:|---:|---:|
| Sponza | 1.172 ms | 1.761 ms | +50.2% |
| Sponza + Ivy | 1.688 ms | 2.077 ms | +23.1% |
| Bistro | 0.539 ms | 0.663 ms | +22.9% |

VisBuf의 compute G-buffer가 geometry 비용을 줄이는 구간은 있었지만, 현재 구현에서는 visibility pass와 material binning, attribute reconstruction 비용이 그 이득을 상쇄했다. Material record 수 자체보다 active material class 수가 더 큰 영향을 주었고, 255 materials 고정 조건에서 class 수가 1→255로 늘 때 VisBuf는 0.344→0.562 ms로 증가했다.

정확성은 성능과 분리해 검증했다. Sponza, Sponza + Ivy, Bistro의 raster-reference/VisBuf 910쌍에서 interior channel 98.3831%가 bit-exact였고 평균 오차는 8-bit 기준 0.018412 LSB, 평균 coverage mismatch는 0%였다.

이 수치는 특정 구현·GPU·driver·scene·camera 조건의 결과이며 TVB 일반의 우열을 뜻하지 않는다. 근거, 해석과 한계는 [결과 문서](docs/results.md)에 정리했다.

## 직접 설계·구현한 범위

- Forward, ForwardPrepass, Deferred, DeferredPrepass, VisBuf, VisBuf+G-buffer의 비교 가능한 D3D12 pipeline
- draw/geometry instance ID와 triangle ID를 사용하는 visibility 및 fullscreen reconstruction 경로
- material class histogram, prefix, flatten, bin dispatch로 이어지는 Material Binning
- barycentric, derivative, UV LOD reconstruction의 raster reference 비교와 debug capture
- synthetic scene parameterization과 Sponza/Bistro/San Miguel 계열 실제 장면 비교
- GPU timestamp, camera playback, raster workload proxy, CSV sidecar 수집
- build → run → normalize → plot → dashboard bundle을 한 번에 수행하는 Python 자동화

NVIDIA Donut 유래 셰이더와 외부 라이브러리·장면은 직접 기여와 분리해 고지한다. 자세한 범위는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)와 [SCENE_ASSET_NOTICES.md](SCENE_ASSET_NOTICES.md)를 본다.

## 5분 안에 실행하기

요구 사항:

- Windows 10/11, Direct3D 12 GPU
- Visual Studio C++ toolchain
- CMake 3.20 이상과 Ninja
- Python 3.11 이상

PowerShell에서 저장소 루트를 기준으로 실행한다.

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/reproduce.py --suite smoke --build --overwrite
```

두 번째 명령은 clean Release build를 만들고 synthetic smoke 6개를 실행한다. 결과는 Git에 저장하지 않고 `results/` 아래에 생성한다.

```text
results/
├─ environment.json
├─ dashboard_bundle.json
└─ synthetic/followup_01_synth_decoupling_smoke/
   ├─ raw.csv
   ├─ runs.csv
   ├─ passes.csv
   ├─ frames.csv
   ├─ run_report.json
   └─ plots/
      ├─ total_time.png
      ├─ pass_breakdown.png
      └─ manifest.json
```

`dashboard_bundle.json` 하나에는 정규화된 run, 환경 정보와 PNG 그래프가 들어간다. 형제 프로젝트 [TVB Performance Atlas](../visibility-buffer-bench-dasboard)의 `npm run data:import -- <bundle>`에 파일 하나만 전달하면 웹에서 볼 수 있다.

## 실제 장면 실행

장면 파일은 라이선스와 용량 때문에 저장소에 포함하지 않는다. `experiments/local.example.json`을 `experiments/local.json`으로 복사하고 필요한 scene alias만 로컬 경로로 지정한다.

```json
{
  "scenes": {
    "sponza": "D:/scenes/Sponza/glTF/Sponza.gltf",
    "bistro": "D:/scenes/Bistro/BistroExterior.fbx"
  }
}
```

그다음 대표 포트폴리오 묶음을 실행한다.

```powershell
python scripts/reproduce.py --suite portfolio --build --overwrite --keep-going
```

설정하지 않은 장면은 renderer 실패로 위장하지 않고 `skipped_missing_asset`으로 기록한다. 반복 측정은 spec에 명시된 fixed camera playback, warm-up, measurement frame, VSync, VFC, texture 조건을 그대로 사용한다.

## 실험 재현 계약

과거 결과 파일 대신 결과를 만드는 정의를 버전 관리한다.

- `experiments/specs/`: 66개 canonical experiment JSON
- `experiments/suites/`: `smoke`, `portfolio`, `all` 실행 묶음
- `experiments/camera_paths/`: 고정 camera playback
- `experiments/plot_theme.json`: renderer/pass 색상과 순서
- `scripts/reproduce.py`: build, 실행, 정규화, 그래프, bundle의 단일 진입점
- `results/`: 매번 생성되는 로컬 산출물, Git ignore

현재 inventory는 총 4,280 runs이며 57개 spec은 이전 실행 의미를 그대로 옮긴 `exact`, 9개는 제거된 인자나 현재 계약에 맞춰 조정한 `adapted`로 표시된다.

```powershell
python scripts/reproduce.py --verify
python scripts/reproduce.py --suite all --dry-run
```

세부 형식과 이관 기준은 [실험 카탈로그](experiments/README.md), clean-machine 절차는 [재현성 문서](docs/reproducibility.md)를 본다.

## 시각 언어

그래프는 JSON의 `analysis.plots` 선언으로 생성한다. renderer family는 Forward=파랑, Deferred=주황, VisBuf=초록으로 고정하고, pre-pass/visibility는 밝게, geometry는 중간, lighting/resolve는 진하게 표현한다. Material binning 같은 utility pass는 노랑, shared pass는 보라, 계측되지 않은 나머지는 회색이다. 같은 의미의 pass는 모든 실험에서 같은 색과 순서를 사용한다.

## 저장소 구조

```text
include/, src/          C++20 Direct3D 12 benchmark
assets/shaders/        HLSL runtime shaders
experiments/           experiment specs, suites, camera paths, plot theme
scripts/               Python runner, normalization, plotting, export
docs/                  methodology, results, reproducibility
tests/                 automation contract tests
```

웹/TypeScript 시각화와 생성 데이터는 이 저장소에서 제거했다. 이 저장소에는 renderer 소스, HLSL, Python 도구와 선언형 JSON만 남는다.

## 문서

- [연구 방법과 실험 구조](docs/methodology.md)
- [대표 결과와 한계](docs/results.md)
- [실험 이관 상태](docs/experiments.md)
- [Clean build와 데이터 provenance](docs/reproducibility.md)
- [라이선스](LICENSE), [외부 코드 고지](THIRD_PARTY_NOTICES.md), [장면 자산 고지](SCENE_ASSET_NOTICES.md)

## Related project

[fast-jungle-renderer](https://github.com/chorogchip/fast-jungle-renderer)는 약 900만 인스턴스 장면을 GPU-driven 방식으로 다루는 별도 프로젝트다.
